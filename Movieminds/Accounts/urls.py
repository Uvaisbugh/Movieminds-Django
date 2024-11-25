from django.urls import path
from . import views
from .views import *


urlpatterns = [
    path('login/', views.LoginPage, name='login'),
    path('logout/', views.LogoutPage, name='logout'),
    path('register/', views.RegisterPage, name='register'),
    path('profile/', views.Profilepage, name='profile'),
    path('bio/', views.UpdateBio, name='bio_update'),
    path('add_to_watchlist/<int:movie_id>', views.Addtowatchlist, name='add_to_watchlist'),
    path('remove_from_watchlist/<int:movie_id>', views.Removefromwatchlist, name='remove_from_watchlist'),
    #admin
    path('admin_login/', views.AdminLogin, name='admin_login'),
    path('admin_logout', views.AdminLogout, name='admin_logout'),
    path('admin_home/', views.AdminHome, name='admin_home'),
    path('manage_categories/', ManageCategories, name='manage_categories'),
    path('add_category/', AddCategory, name='add_category'),
    path('delete_category/<int:category_id>/', DeleteCategory, name='delete_category'),
    path('update_category/<int:category_id>/', UpdateCategory, name='update_category'),
    path('changePassword', ChangePassword, name='changePassword'),
    path('register_user/', RegisterUsers, name="reg_user"),
    path('delete_user/<int:user_id>', DeleteUser, name="delete_user"),
    path('manage_movies', ManageMovies, name="manage_movies"),
    path('edit_movie/<int:movie_id>', MovieEdit, name="edit_movie"),
    path('delete_movie/<int:movie_id>', DeleteMovie, name="movie_delete"),
    path('profile/edit/', ProfileEdit, name='profile_edit'),
]

