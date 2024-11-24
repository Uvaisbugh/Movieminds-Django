from django.urls import path
from . import views
from .views import *


urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('register/', views.RegisterPage, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/',views.profile, name='profile'),
    path('bio/', views.update_bio_view, name='bio_update'),
    path('add_to_watchlist/<int:movie_id>', views.add_to_watchlist, name='add_to_watchlist'),
    #admin
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_logout', views.admin_logout, name='admin_logout'),
    path('admin_home/', views.admin_home, name='admin_home'),
    path('manage_categories/', manage_categories, name='manage_categories'),
    path('add_category/', add_category, name='add_category'),
    path('delete_category/<int:category_id>/', delete_category, name='delete_category'),
    path('update_category/<int:category_id>/', update_category, name='update_category'),
    path('changePassword', ChangePassword, name='changePassword'),
    path('reg_user/', reg_user, name="reg_user"),
    path('delete_user/<int:user_id>', delete_user, name="delete_user"),
    path('manage_movies', manage_movies, name="manage_movies"),
    path('edit_movie/<int:movie_id>', edit_movie, name="edit_movie"),
    path('movie_delete/<int:movie_id>', movie_delete, name="movie_delete"),
    path('profile/edit/', profile_edit, name='profile_edit'),
]

