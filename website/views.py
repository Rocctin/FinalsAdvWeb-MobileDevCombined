from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q, Count, Avg, Min, Max
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime
from .models import Title
from .serializers import TitleSerializer, TitleListSerializer, TitleCreateSerializer, TitleDetailSerializer

def home(request):
    # Simple HTML PAge to display everything
    """Home page with API information and links to all endpoints"""
    
    return HttpResponse("""
    <h1>Netflix Titles REST API</h1>
    <h2>Available Endpoints:</h2>
    <ul>
        <li><a href="/api/titles/">/api/titles/</a> - List all titles (GET) and create new title (POST)</li>
        <li><a href="/api/titles/1/">/api/titles/{id}/</a> - Get, update, or delete specific title</li>
        <li><a href="/api/titles/movies/">/api/titles/movies/</a> - List all movies only</li>
        <li><a href="/api/titles/tv-shows/">/api/titles/tv-shows/</a> - List all TV shows only</li>
        <li><a href="/api/titles/by-year/2020/">/api/titles/by-year/{year}/</a> - Titles by release year</li>
        <li><a href="/api/titles/by-genre/Drama/">/api/titles/by-genre/{genre}/</a> - Titles by genre</li>
        <li><a href="/api/titles/recent/">/api/titles/recent/</a> - Recently added titles</li>
        <li><a href="/api/titles/stats/">/api/titles/stats/</a> - Statistics about the dataset</li>
    </ul>
    <h3>Technical Information:</h3>
    <p><strong>Python Version:</strong> 3.13</p>
    <p><strong>Django Version:</strong> 5.2.3</p>
    <p><strong>Django REST Framework:</strong> 3.16.0</p>
    <p><strong>Django REST Framework:</strong> 3.16.0</p>
    <strong>List of Packages:</strong>
    <p>asgiref==3.8.1</p>
    <p>Django==5.2.3</p>
    <p>djangorestframework==3.16.0</p>
    <p>djangorestframework_simplejwt==5.5.0</p>
    <p>gunicorn==23.0.0</p>
    <p>numpy==2.3.1</p>
    <p>packaging==25.0</p>
    <p>pandas==2.3.0</p>
    <p>PyJWT==2.9.0</p>
    <p>python-dateutil==2.9.0.post0</p>
    <p>pytz==2025.2</p>
    <p>six==1.17.0</p>
    <p>sqlparse==0.5.3</p>
    <p>tzdata==2025.2</p>
    <p>whitenoise==6.9.2</p>
    <p><strong>Database:</strong> SQLite3</p>
    <p><strong>Admin Site:</strong> <a href="/admin/">/admin/</a> (username: admin, password: admin123)</p>
    """)

# API Views

class TitleListCreateView(generics.ListCreateAPIView):
    """API endpoint 1: List all titles (GET) and create new title (POST)"""
    queryset = Title.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TitleCreateSerializer
        return TitleListSerializer

class TitleDetailView(generics.RetrieveUpdateDestroyAPIView):
    """API endpoint 2: Get, update, or delete a specific title by ID"""

    queryset = Title.objects.all()
    serializer_class = TitleDetailSerializer

class MovieListView(generics.ListAPIView):
    """API endpoint 3: List all movies only"""
    
    serializer_class = TitleListSerializer
    
    def get_queryset(self):
        return Title.objects.filter(type='Movie')

class TVShowListView(generics.ListAPIView):
    """API endpoint 4: List all TV shows only"""
    serializer_class = TitleListSerializer
    
    def get_queryset(self):
        return Title.objects.filter(type='TV Show')

class TitlesByYearView(generics.ListAPIView):
    """API endpoint 5: Get titles by release year"""
    serializer_class = TitleListSerializer
    
    def get_queryset(self):
        year = self.kwargs.get('year')
        return Title.objects.filter(release_year=year)

class TitlesByGenreView(generics.ListAPIView):
    """API endpoint 6: Get titles by genre (case-insensitive search in listed_in field)"""
    serializer_class = TitleListSerializer
    
    def get_queryset(self):
        genre = self.kwargs.get('genre')
        return Title.objects.filter(listed_in__icontains=genre)

@api_view(['GET'])
def recent_titles(request):
    """Bonus endpoint: Get recently added titles (last 30 days from date_added)"""
    from datetime import datetime, timedelta
    thirty_days_ago = datetime.now().date() - timedelta(days=30)
    titles = Title.objects.filter(
        date_added__gte=thirty_days_ago
    ).order_by('-date_added')[:20]
    
    serializer = TitleListSerializer(titles, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def title_statistics(request):
    """Bonus endpoint: Get statistics about the dataset"""
    total_titles = Title.objects.count()
    movies_count = Title.objects.filter(type='Movie').count()
    tv_shows_count = Title.objects.filter(type='TV Show').count()
    
    # Get most common genres
    all_genres = []
    for title in Title.objects.exclude(listed_in__isnull=True):
        if title.listed_in:
            genres = [g.strip() for g in title.listed_in.split(',')]
            all_genres.extend(genres)
    
    genre_counts = {}
    for genre in all_genres:
        genre_counts[genre] = genre_counts.get(genre, 0) + 1
    
    top_genres = sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    
    # Get year range
    years = Title.objects.aggregate(
        min_year=Min('release_year'),
        max_year=Max('release_year')
    )
    
    # Display it in JSON like format
    stats = {
        'total_titles': total_titles,
        'movies_count': movies_count,
        'tv_shows_count': tv_shows_count,
        'year_range': f"{years['min_year']} - {years['max_year']}",
        'top_genres': dict(top_genres),
    }
    
    return Response(stats)
