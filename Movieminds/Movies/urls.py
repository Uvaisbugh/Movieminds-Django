from django.urls import path
from . import views


urlpatterns = [
    path("",views.home, name= "home"),
    path('add-movie', views.add_movie, name='add_movie'),
    path('review/<str:slug>/<str:_id>/', views.movie_review_page, name='movie_review_page'),
    path('update-movie/<str:movie_slug>/<str:movie_id>/', views.update_movie, name='update_movie'),
    path('update-comment/<int:comment_id>/', views.update_comment, name='update_comment'),
    path('delete-comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
]
