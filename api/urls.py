from django.urls import path

from . import views

urlpatterns = [
    path("genres/", views.getGenres, name="genres"),
    path("movies/", views.getMovies, name="movies"),
    path("movies/search/", views.searchMovies, name="search-movies"),
    path("movies/<int:id>/", views.getMovie, name="movie"),
    path("movies/add/", views.addMovie, name="add-movie"),
    path("movies/recommendations/", views.getRecommendations, name="recommendations"),
]
