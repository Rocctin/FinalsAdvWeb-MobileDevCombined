"""
URL configuration for website app.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""

from django.urls import path
from . import views

urlpatterns = [
    # Home page with API documentation
    path('', views.home, name='home'),
    
    # RESTful API endpoints
    #Main REStful API, retrieves the title and uses <int:pk> to show  the db id as a number
    path('api/titles/', views.TitleListCreateView.as_view(), name='title-list-create'),
    path('api/titles/<int:pk>/', views.TitleDetailView.as_view(), name='title-detail'),
    
    path('api/titles/movies/', views.MovieListView.as_view(), name='movie-list'), # Filter by movies
    path('api/titles/tv-shows/', views.TVShowListView.as_view(), name='tv-show-list'),# Filter by TV Shows
    path('api/titles/by-year/<int:year>/', views.TitlesByYearView.as_view(), name='titles-by-year'), # Titles from what year depending on <int:year>
    path('api/titles/by-genre/<str:genre>/', views.TitlesByGenreView.as_view(), name='titles-by-genre'), # Titles configured by what genre
    
    # Additional useful endpoints
    path('api/titles/recent/', views.recent_titles, name='recent-titles'), # Display any titles added
    path('api/titles/stats/', views.title_statistics, name='title-stats'), # Stats of the whole DB
]