from django.db import models
from django.contrib.auth.models import User

#profile model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.TextField(blank=True, db_index=True)
    watchlist = models.ManyToManyField('Movies.Movie', blank=True, related_name="watchlisted_by")
    favorites = models.ManyToManyField('Movies.Movie', blank=True, related_name="favorited_by")

    def __str__(self):
        return self.user.username
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def save(self, *args, **kwargs):
        if self.profile and self.profile.size > 5 * 1024 * 1024:  
            raise ValueError("profile size should not exceed 5MB")
        super().save(*args, **kwargs)
