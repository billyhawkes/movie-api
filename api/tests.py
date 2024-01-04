from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from base.models import Genre, Movie


class MovieAPITests(APITestCase):
    def setUp(self):
        """
        Setup for tests
        1. Create a genre
        2. Create a movie with the genre
        """
        self.genre = Genre.objects.create(id=1, name="Action")
        self.movie = Movie.objects.create(
            id=1,
            title="Test Movie 1",
            budget=1000000,
            popularity=10,
            homepage="https://www.google.com/",
            overview="This is a test movie.",
        )
        self.movie.genres.add(self.genre)

    def test_create_movie(self):
        """
        Test that a movie can be created (/movies/add/)
        """
        url = reverse("add-movie")
        data = {
            "id": 2,
            "title": "Test Movie 2",
            "genres": [1],
            "budget": 1000000,
            "popularity": 10,
            "homepage": "https://www.google.com/",
            "overview": "This is a test movie.",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Movie.objects.count(), 2)
        self.assertEqual(Movie.objects.get(id=2).title, "Test Movie 2")

    def test_get_movies(self):
        """
        Test that movies can be retrieved (/movies/)
        """
        url = reverse("movies")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Test Movie 1")

    def test_get_movies_genre(self):
        """
        Test that movies can be filtered by genre (/movies/?genre=Action)
        """
        url = reverse("movies")
        response = self.client.get(url + "?genre=Action")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Test Movie 1")

    def test_search_movies(self):
        """
        Test that movies can be searched by title (/movies/search/?query=Test)
        """
        url = reverse("search-movies")
        response = self.client.get(url + "?query=Test")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Test Movie 1")
        # Test with query that doesn't match any movies
        response = self.client.get(url + "?query=Test2")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_movie(self):
        """
        Test that a movie can be retrieved by id (/movies/1/)
        """
        url = reverse("movie", args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Movie 1")

    def test_get_recommendations(self):
        """
        Test that recommendations can be retrieved (/movies/recommendations)
        """
        url = reverse("recommendations")
        response = self.client.get(url + "?genres=Action,Adventure")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Test Movie 1")
