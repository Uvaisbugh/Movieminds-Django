from django.shortcuts import redirect, render
from Moviesapp.models import *
from accounts.models import UserProfile
from django.db.models import Avg
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from .forms import  AddMovieForm , CommentForm
from django.utils.datastructures import MultiValueDictKeyError
from django.urls import reverse
from django.shortcuts import get_object_or_404


def home(request):
    query = request.GET.get('q', '').strip()
    sort = request.GET.get('sort', 'latest')
    category = request.GET.get('category', '').strip()
    # Filter by title
    movies = Movie.objects.filter(title__icontains=query)
    # Filter by category
    if category:
        movies = movies.filter(category__name=category)
    #sorting
    valid_sort_options = ['popular', 'latest']
    if sort == 'popular':
        movies = movies.annotate(avg_rating=Avg('ratings__rating')).order_by('-avg_rating')
    elif sort == 'latest':
        movies = movies.order_by('-created')
    elif sort not in valid_sort_options:
        sort = 'latest'  
    # Prefetch related data
    movies = movies.select_related('category').prefetch_related('ratings')
    # Pagination
    paginator = Paginator(movies, 9) 
    page_number = request.GET.get('page')
    movies = paginator.get_page(page_number)
    # Fetch user profile if authenticated
    profile = None
    if request.user.is_authenticated:
        profile = UserProfile.objects.filter(user=request.user).first()
    Cat= Category.objects.all()
    context = {
        'Category': Cat,
        'movies': movies,
        'profile': profile,
        'query': query,
        'sort': sort,
        'category': category,
    }
    return render(request, 'index.html',context )

@login_required(login_url='login')
def add_movie(request):
    profile = UserProfile.objects.filter(user=request.user).first()
    if request.method == 'POST':
        form = AddMovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.posted_by = request.user
            movie.save()
            form.save_m2m() 
            
            messages.success(request, "Movie added successfully!")
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = AddMovieForm()

    return render(request, 'add-movie.html', {'profile': profile, 'form': form})

@login_required(login_url='login')
def movie_review_page(request, slug, _id):
    movie = get_object_or_404(Movie, slug=slug, id=_id)
    profile = UserProfile.objects.filter(user=request.user).first()
    comments = Comment.objects.filter(movie=movie)
    similar_movies = Movie.objects.filter(category=movie.category).exclude(id=movie.id)[:5]
    avg_rating = Rating.objects.filter(movie=movie).aggregate(Avg('rating'))['rating__avg']
    
    if request.method == 'POST':
        rate = request.POST.get('rating')
        comment = request.POST.get('comment')
        if not rate:
            messages.error(request, "Please provide a rating.")
        elif not comment:
            messages.error(request, "Please provide a comment.")
        else:
            existing_rating = Rating.objects.filter(user=request.user, movie=movie).first()
            if not existing_rating:
                Rating.objects.create(user=request.user, movie=movie, rating=rate)
            else:
                existing_rating.rating = rate
                existing_rating.save()
                messages.warning(request, "Rate updated.")
        
            Comment.objects.create(user=profile, movie=movie, content=comment)
            messages.success(request, "Review added successfully!")
            return redirect('movie_review_page', slug=movie.slug, _id=movie.id)
        
    actors = movie.actors.all()
    rate = Rating.objects.filter(user=request.user, movie=movie).first()
    return render(
        request, 
        'review.html', 
        {
            'movie': movie,
            'actors': actors,
            'comments': comments,
            'profile': profile,
            'similar_movies': similar_movies,
            'avg_rating': avg_rating,
            'rate': rate
            
        }
    )

@login_required(login_url='login')
def update_movie(request, movie_slug, movie_id):
    movie = get_object_or_404(Movie, slug=movie_slug, id=movie_id)
    profile = UserProfile.objects.filter(user=request.user).first()
    
    if movie.posted_by != request.user:
        return redirect('home')
    
    if request.method == 'POST':
        form = AddMovieForm(request.POST,request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movie_review_page', slug=movie.slug, _id=movie.id)
    else:
        form = AddMovieForm(instance=movie)
    return render(request, 'update_movie.html', {
        'movie': movie, 
        'profile': profile, 
        'form': form
        })

@login_required(login_url='login')
def update_comment(request, comment_id):
    
    comment = get_object_or_404(Comment, id=comment_id)

    if request.user != comment.user.user:
        messages.error(request, "You are not authorized to edit this comment.")
        return redirect(reverse('review', args=(comment.movie.slug, comment.movie.id)))

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, "Comment updated successfully!")
            return redirect('movie_review_page', comment.movie.slug, comment.movie.id)
        else:
            messages.error(request, "There was an error updating your comment. Please try again.")
    else:
        form = CommentForm(instance=comment)
    
    return render(request, "update_comment.html", {
        'form': form
    })

@login_required(login_url='login')
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.method == "POST":
        comment.delete()
        messages.success(request, "Comment deleted successfully!")
        return redirect('movie_review_page', comment.movie.slug, comment.movie.id)
    return render(request, 'delete_comment.html', {'comment_id': comment_id, 'comment': comment})

#sn