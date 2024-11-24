from django.shortcuts import get_object_or_404, render, redirect
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth .models import User
from django.contrib.auth.decorators import login_required
from Accounts.models import UserProfile
from Movies.models import *
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from Movies.forms import AddMovieForm, ProfileEditForm , BioUpdateForm

def LoginPage(request):
    #redirect
    if request.user.is_authenticated:
        return redirect('home')
    #login
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me') == 'on'
        # Validate 
        if not username or not password:
            messages.error(request, "Please provide both !.")
            return render(request, 'login.html')
        # Authenticate 
        user = authenticate(request, username=username, password=password)
        # Login
        if user is not None:
            login(request, user)
            if not remember_me:
                request.session.set_expiry(0)  
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'login.html')
    return render(request, 'login.html', )

#logout
def LogoutPage(request):
    logout(request)
    return redirect('login')

#register
def RegisterPage(request):
    if request.method == 'POST':
        # Get form data
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()
        # Check
        if not all([first_name, last_name, username, email, password, confirm_password]):
            messages.error(request, "All fields are required.")
            return render(request, 'register.html')

        # match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'register.html')

        # Validate unique username and email
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'register.html')
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use.")
            return render(request, 'register.html')
        # Profile picture
        profile = request.FILES.get('profile', None)
        # Create user
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            # Create user profile
            user_profile = UserProfile(user=user, profile=profile)
            user_profile.save()
            # Log in user
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f"Welcome, {user.username}! Your account has been created successfully.")
                # Redirect to the next page or home page
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return render(request, 'register.html')
    return render(request, 'register.html')

@login_required(login_url='login')
def Profilepage(request):
    profile = UserProfile.objects.select_related('user').get(user=request.user)
    user_movies = Movie.objects.filter(posted_by=request.user).order_by('-created')
    user_reviews = Comment.objects.filter(user=profile).order_by('-created_at')
    watchlist = profile.watchlist.all()
    favorites = profile.favorites.all()
    # Pass 
    context = {
        'profile': profile,
        'user_movies': user_movies,
        'user_reviews': user_reviews,
        'watchlist': watchlist,
        'favorites': favorites
    }
    return render(request, 'profile.html', context)

@login_required
def ProfileEdit(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)  
    
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            if 'profile_picture' in request.FILES:
                user_profile.profile_picture = request.FILES['profile_picture']
            user_profile.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('profile') 
        else:
            messages.error(request, "There was an error updating your profile. Please try again.")
    else:
        form = ProfileEditForm(instance=user)
    return render(request, 'profile_edit.html', {'form': form, 'user_profile': user_profile})

def AdminLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_superuser:
                if request.user.is_authenticated:
                    logout(request)
                login(request, user)
                return redirect('admin_home')
            else:
                messages.error(request, "You are not authorized to access the admin area.")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'admin_login.html')

def AdminLogout(request):
    logout(request)
    return redirect('admin_login')

@staff_member_required(login_url='admin_login')
def AdminHome(request):
    user=request.user
    totalmovies = Movie.objects.all().count()
    totalcategories = Category.objects.all().count()
    totalusers = UserProfile.objects.all().count()
    totalcomments = Comment.objects.all().count()
    conext = {
        'user': user,
        'totalcategories': totalcategories,
        'totalmovies': totalmovies,
        'totalcomments': totalcomments,
        'totalusers': totalusers    
    }
    return render(request, 'admin/admin_home.html', conext)

@staff_member_required(login_url='admin_login')
def ChangePassword(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password =request.POST.get('confirm_password')
        if current_password == request.user.password:
            messages.error(request, 'Current password is incorrect')
            return redirect('changePassword')
        if new_password == confirm_password:
            user =User.objects.get(id=request.user.id)
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password updated successfully')
            return redirect('admin_home')
        else:    
            messages.error(request, 'Password does not match')
            return redirect('changePassword')
    return render(request, 'admin/changePassword.html')

@staff_member_required(login_url='admin_login')
def ManageCategories(request):
    categories = Category.objects.all()
    return render(request, 'admin/manage_categories.html', {'categories': categories})

@staff_member_required(login_url='admin_login')
def DeleteCategory(request, category_id):
    category = Category.objects.get(id=category_id)
    category.delete()
    return redirect('manage_categories')

@staff_member_required(login_url='admin_login')
def AddCategory(request):
    if request.method == 'POST':
        name = request.POST.get('newcategory').strip()
        if not name:
            messages.error(request, "Category name cannot be empty.")
            return redirect('manage_categories')
        #check exists
        if Category.objects.filter(name__iexact=name).exists():
            messages.error(request, "Category already exists.")
            return redirect('manage_categories')
        Category.objects.create(name=name)
        messages.success(request, f"Category '{name}' added successfully!")
        return redirect('manage_categories')
    return render(request, 'admin/manage_categories.html')

@staff_member_required(login_url='admin_login')
def UpdateCategory(request, category_id):
    category = Category.objects.get(id=category_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        category.name = name
        category.save()
        return redirect('manage_categories')
    return render(request, 'admin/update_category.html', {'category': category})

@staff_member_required(login_url='admin_login')
def RegisterUsers(request):
    data = UserProfile.objects.all()
    context = {
        'data': data}
    return render(request, 'admin/reg_user.html', locals())

@staff_member_required(login_url='admin_login')
def DeleteUser(request, user_id):
    user = UserProfile.objects.get(id=user_id)
    user.delete()
    return redirect('reg_user')

@staff_member_required(login_url='admin_login')
def ManageMovies(request):
    movies = Movie.objects.all()
    return render(request, 'admin/manage_movies.html', {'movies': movies})

@staff_member_required(login_url='admin_login')
def DeleteMovie(request, movie_id):
    movie = Movie.objects.get(id=movie_id )
    movie.delete()
    return redirect('manage_movies')

@staff_member_required(login_url='admin_login')
def MovieEdit(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == 'POST':
        form = AddMovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            messages.success(request, "Movie updated successfully!")
            return redirect('manage_movies')  
        else:
            messages.error(request, "Please correct the errors .")
    else:
        form = AddMovieForm(instance=movie)
    return render(request, 'admin/edit_movie.html', {
        'form': form,
        'movie': movie,
    })
    
@login_required
def UpdateBio(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = BioUpdateForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your bio has been updated successfully!")
            return redirect('profile')
        else:
            messages.error(request, "An error occurred.")
    else:
        form = BioUpdateForm(instance=user_profile)
    return render(request, 'update_bio.html', {'form': form})

def Addtowatchlist(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    user=UserProfile.objects.get(user=request.user)
    user.watchlist.add(movie)
    return redirect(request.META.get('HTTP_REFERER', 'watchlist'))

#sn