from django.urls import path
from . import views


urlpatterns = [
    path("",views.Home, name= "home"),
    path('add-movie', views.AddMovie, name='add_movie'),
    path('review/<str:slug>/<str:_id>/', views.ReviewPage, name='moviereview'),
    path('update-movie/<str:movie_slug>/<str:movie_id>/', views.UpdateMovie, name='update_movie'),
    path('delete-movie/<str:movie_slug>/<str:movie_id>/', views.DeleteMovie, name='delete_movie'),
    path('update-comment/<int:comment_id>/', views.UpdateComment, name='update_comment'),
    path('delete-comment/<int:comment_id>/', views.DeleteComment, name='delete_comment'),
]
