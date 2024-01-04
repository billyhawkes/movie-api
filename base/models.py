from django.db import models


class Genre(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)


class Movie(models.Model):
    id = models.IntegerField(primary_key=True)
    budget = models.IntegerField()
    genres = models.ManyToManyField(Genre, related_name="movies")
    homepage = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    overview = models.TextField()
    popularity = models.FloatField()
