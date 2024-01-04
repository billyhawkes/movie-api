import json
import os

import django
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")
django.setup()

from base.models import Genre, Movie  # noqa: E402


def populate_genres(genre_df):
    # Get unique genres
    unique_genres = []
    for genre_list in genre_df:
        for genre in genre_list:
            # Create genre dict
            genre_dict = {"id": genre["id"], "name": genre["name"]}

            # Add genre dict to unique genres if not already in it
            if genre_dict not in unique_genres:
                unique_genres.append(genre_dict)

    # Create dataframe from unique genres
    unique_genres_df = pd.DataFrame(list(unique_genres))

    # Populate genres table
    for index, row in unique_genres_df.iterrows():
        # Create genre from row
        genre = Genre(id=row["id"], name=row["name"])
        genre.save()

    print("Genres table populated.")


def populate_movies(movie_df):
    # Iterate through movies and populate movies table
    for index, row in movie_df.iterrows():
        # Create movie from row
        movie = Movie(
            id=row["id"],
            budget=row["budget"],
            homepage=row["homepage"],
            title=row["title"],
            overview=row["overview"],
            popularity=row["popularity"],
        )

        # Save movie
        movie.save()

        # Add genres relationship to movie
        for genre in row["genres"]:
            movie.genres.add(Genre.objects.get(id=genre["id"]))

    print("Movies table populated.")


def load_csv(filename):
    # Load csv
    df = pd.read_csv(filename)

    # Parse genres column from json to list
    df["genres"] = df["genres"].apply(json.loads)

    # Populate genres and movies tables
    populate_genres(df["genres"])
    populate_movies(df)


# Run script
load_csv("tmdb_5000_movies.csv")
