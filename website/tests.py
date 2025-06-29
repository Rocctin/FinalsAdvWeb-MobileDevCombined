from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import datetime, date
from .models import Title
from .serializers import TitleSerializer, TitleCreateSerializer

class TitleModelTest(TestCase):
    "Test the Title model"
    # Use for testingplaceholder data
    def setUp(self):
        self.title_data = {
            'show_id': 'test123',
            'type': 'Movie',
            'title': 'Test Movie',
            'director': 'Test Director',
            'cast': 'Actor 1, Actor 2',
            'country': 'United States',
            'date_added': date(2024, 1, 15),
            'release_year': 2023,
            'rating': 'PG-13',
            'duration': '120 min',
            'listed_in': 'Action, Drama',
            'description': 'A test movie for unit testing'
        }
    
# Testin for every single query
    def test_title_creation(self):
        # Being the admin means that we should be able to add new movies
        "Test creating a new title"
        title = Title.objects.create(**self.title_data)
        self.assertEqual(title.title, 'Test Movie')
        self.assertEqual(title.type, 'Movie')
        self.assertEqual(title.release_year, 2023)
        self.assertEqual(str(title), 'Test Movie')
    
    def test_title_unique_show_id(self):
        # In databases primary key cannot be duplicated, else db will crash
        "Test that show_id must be unique"
        Title.objects.create(**self.title_data)
        
        # Try to create another title with same show_id
        duplicate_data = self.title_data.copy()
        duplicate_data['title'] = 'Different Title'
        
        with self.assertRaises(Exception):
            Title.objects.create(**duplicate_data)

class TitleSerializerTest(TestCase):
    # Convert Python datatypes that can then be easily rendered into JSON, XML
    "Test Title serializers"
    def setUp(self):
        self.valid_data = {
            'show_id': 'movie1',
            'type': 'TV Show',
            'title': 'Test TV Show',
            'director': 'irector',
            'cast': 'Actor 1, Actor 2, Actor 3',
            'country': 'Canada',
            'date_added': '2024-01-15',
            'release_year': 2022,
            'rating': 'TV-MA',
            'duration': '3 Seasons',
            'listed_in': 'Comedy, Drama',
            'description': 'A test TV show for serializer testing'
        }
    
    def test_title_serializer_valid_data(self):
        # Convert Python datatypes that can then be easily rendered into JSON, XML
        """Test serializer with valid data"""
        serializer = TitleCreateSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
    
    def test_title_serializer_invalid_type(self):
        """Test serializer with invalid type"""
        invalid_data = self.valid_data.copy()
        invalid_data['type'] = 'Invalid Type'
        
        serializer = TitleCreateSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('type', serializer.errors)
    
    def test_title_serializer_invalid_year(self):
        """Test serializer with invalid release year"""
        invalid_data = self.valid_data.copy()
        invalid_data['release_year'] = 1850  # Too old
        
        serializer = TitleCreateSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('release_year', serializer.errors)
        
#Testing the APIs
class TitleAPITest(APITestCase):
    """Test the Title API endpoints"""
    def setUp(self):
        # Create test titles
        self.movie1 = Title.objects.create(
            show_id='movie1',
            type='Movie',
            title='Action Movie',
            director='Director A',
            cast='Actor 1, Actor 2',
            country='USA',
            date_added=date(2024, 1, 1),
            release_year=2023,
            rating='PG-13',
            duration='120 min',
            listed_in='Action, Adventure',
            description='An action-packed movie'
        )
        
        self.tv_show1 = Title.objects.create(
            show_id='tv1',
            type='TV Show',
            title='Comedy Series',
            director='Director B',
            cast='Actor 3, Actor 4',
            country='UK',
            date_added=date(2024, 2, 1),
            release_year=2022,
            rating='TV-14',
            duration='2 Seasons',
            listed_in='Comedy, Drama',
            description='A hilarious TV series'
        )
    
    def test_get_title_list(self):
        """Test GET /api/titles/ - List all titles"""
        url = reverse('title-list-create')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_create_title(self):
        """Test POST /api/titles/ - Create new title"""
        url = reverse('title-list-create')
        new_title_data = {
            'show_id': 'new123',
            'type': 'Movie',
            'title': 'New Test Movie',
            'director': 'New Director',
            'cast': 'New Actor 1, New Actor 2',
            'country': 'France',
            'date_added': '2024-03-01',
            'release_year': 2024,
            'rating': 'R',
            'duration': '95 min',
            'listed_in': 'Horror, Thriller',
            'description': 'A new horror movie'
        }
        
        response = self.client.post(url, new_title_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Title.objects.count(), 3)
        self.assertEqual(response.data['title'], 'New Test Movie')
    
    def test_get_title_detail(self):
        """Test GET /api/titles/{id}/ - Get specific title"""
        url = reverse('title-detail', kwargs={'pk': self.movie1.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Action Movie')
        self.assertIn('cast_count', response.data)
        self.assertIn('genres_list', response.data)
    
    def test_update_title(self):
        """Test PUT /api/titles/{id}/ - Update title"""
        url = reverse('title-detail', kwargs={'pk': self.movie1.pk})
        updated_data = {
            'show_id': 'movie1',
            'type': 'Movie',
            'title': 'Updated Action Movie',
            'director': 'Updated Director',
            'cast': 'Updated Actor 1, Updated Actor 2',
            'country': 'USA',
            'date_added': '2024-01-01',
            'release_year': 2023,
            'rating': 'R',
            'duration': '125 min',
            'listed_in': 'Action, Adventure, Thriller',
            'description': 'An updated action-packed movie'
        }
        
        response = self.client.put(url, updated_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Action Movie')
        self.assertEqual(response.data['rating'], 'R')
    
    def test_delete_title(self):
        """Test DELETE /api/titles/{id}/ - Delete title"""
        url = reverse('title-detail', kwargs={'pk': self.movie1.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Title.objects.count(), 1)
    
    def test_get_movies_only(self):
        """Test GET /api/titles/movies/ - List movies only"""
        url = reverse('movie-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['type'], 'Movie')
    
    def test_get_tv_shows_only(self):
        """Test GET /api/titles/tv-shows/ - List TV shows only"""
        url = reverse('tv-show-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['type'], 'TV Show')
    
    def test_get_titles_by_year(self):
        """Test GET /api/titles/by-year/{year}/ - Get titles by year"""
        url = reverse('titles-by-year', kwargs={'year': 2023})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['release_year'], 2023)
    
    def test_get_titles_by_genre(self):
        """Test GET /api/titles/by-genre/{genre}/ - Get titles by genre"""
        url = reverse('titles-by-genre', kwargs={'genre': 'Action'})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertIn('Action', response.data['results'][0]['listed_in'])
    
    def test_get_recent_titles(self):
        """Test GET /api/titles/recent/ - Get recently added titles"""
        url = reverse('recent-titles')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should return titles added in last 30 days
        self.assertIsInstance(response.data, list)
    
    def test_get_title_statistics(self):
        """Test GET /api/titles/stats/ - Get dataset statistics"""
        url = reverse('title-stats')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_titles', response.data)
        self.assertIn('movies_count', response.data)
        self.assertIn('tv_shows_count', response.data)
        self.assertIn('top_genres', response.data)
        self.assertEqual(response.data['total_titles'], 2)
        self.assertEqual(response.data['movies_count'], 1)
        self.assertEqual(response.data['tv_shows_count'], 1)
    
    def test_create_title_with_invalid_data(self):
        """Test creating title with invalid data"""
        url = reverse('title-list-create')
        invalid_data = {
            'show_id': 'invalid',
            'type': 'Invalid Type',  # Invalid type
            'title': '',  # Empty title
            'release_year': 1800,  # Invalid year
            'listed_in': 'Comedy',
            'description': 'Test'
        }
        
        response = self.client.post(url, invalid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('type', response.data)
    
    def test_create_duplicate_show_id(self):
        """Test creating title with duplicate show_id"""
        url = reverse('title-list-create')
        duplicate_data = {
            'show_id': 'movie1',  # Already exists
            'type': 'Movie',
            'title': 'Duplicate Movie',
            'release_year': 2024,
            'listed_in': 'Drama',
            'description': 'A duplicate movie'
        }
        
        response = self.client.post(url, duplicate_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('show_id', response.data)

class TitleModelMethodsTest(TestCase):
    """Test custom methods and properties of Title model"""
    
    def setUp(self):
        self.title = Title.objects.create(
            show_id='test789',
            type='Movie',
            title='Test Methods Movie',
            director='Director A, Director B',
            cast='Actor 1, Actor 2, Actor 3, Actor 4',
            country='USA, Canada',
            date_added=date(2024, 1, 15),
            release_year=2023,
            rating='PG-13',
            duration='110 min',
            listed_in='Action, Adventure, Comedy',
            description='A test movie for testing methods'
        )
    
    def test_title_string_representation(self):
        """Test __str__ method"""
        self.assertEqual(str(self.title), 'Test Methods Movie')
    
    def test_title_ordering(self):
        """Test model ordering"""
        # Create another title that should come first alphabetically
        Title.objects.create(
            show_id='abc123',
            type='Movie',
            title='ABC Movie',
            release_year=2023,
            listed_in='Drama',
            description='ABC description'
        )
        
        titles = Title.objects.all()
        self.assertEqual(titles[0].title, 'ABC Movie')
        self.assertEqual(titles[1].title, 'Test Methods Movie')
