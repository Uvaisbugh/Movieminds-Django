from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg
from Accounts.models import UserProfile
from django.utils.text import slugify

# 7. Required fields include movie title, poster, description, release date, actors,
# category and a YouTube trailer link.

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, db_index=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    #sn
class Actor(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    biography = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    avatar = models.ImageField(upload_to='actor_pics', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name
    #sn

class Movie(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(null=True,blank=True, unique=True)
    poster=models.ImageField(upload_to='movie_poster',default='images/fallback.jpg')
    description = models.TextField()
    release_date = models.DateField()
    actors = models.ManyToManyField(Actor, blank=True, related_name='movies')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,null=True, related_name='movies')
    youtube_link = models.URLField()
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='movies')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def average_rating(self):
        avg_rating = self.ratings.aggregate(Avg('rating'))['rating__avg']
        return round(avg_rating, 1) if avg_rating else 0.0
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Movie.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} by {self.posted_by.first_name} {self.posted_by.last_name}"
    #sn
class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    rating = models.DecimalField(
        max_digits=3, decimal_places=1, 
        default=1.0, 
        validators=[MinValueValidator(1.00), MaxValueValidator(10.00)]
        )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rating} by {self.user.username} for {self.movie.title}"
    
    class Meta:
        unique_together = ('movie', 'user')
    #sn
class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    rate = models.ForeignKey(Rating, on_delete=models.CASCADE, related_name='rate', blank=True, null=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.user.user} on {self.movie.title}."
    #sn