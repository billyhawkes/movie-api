from rest_framework.decorators import api_view
from rest_framework.response import Response

from base.models import Genre, Movie

from .serializers import GenreSerializer, MovieSerializer


@api_view(["GET"])
def getGenres(request):
    # Get all genres
    genres = Genre.objects.all()

    # Return serialized genres
    serializer = GenreSerializer(genres, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getMovies(request):
    # Get genre and sort parameters from request
    genre = request.GET.get("genre")
    sort = request.GET.get("sort")

    # Filter movies by genre name (ex: ?genre=Action)
    if genre:
        # Check if genre exists and return error if not
        genre_exists = Genre.objects.filter(name=genre).exists()
        if genre_exists:
            movies = Movie.objects.filter(genres__name=genre)
        else:
            return Response(
                {"error": "Genre does not exist."},
                status=400,
            )
    else:
        movies = Movie.objects.all()

    # Sort movies by sort parameter (ex: ?sort=-budget)
    sort_options = ["budget", "popularity", "-budget", "-popularity"]
    if sort:
        # Sort or return error if invalid sort parameter
        if sort in sort_options:
            movies = movies.order_by(sort)
        else:
            return Response(
                {
                    "error": "Invalid sort parameter. Valid options are: "
                    + ", ".join(sort_options)
                    + "."
                },
                status=400,
            )

    # Return serialized movies
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def searchMovies(request):
    # Get query from request
    query = request.GET.get("query")

    # Return error if query parameter is missing
    if query is None:
        return Response(
            {"error": "Missing query parameter."},
            status=400,
        )

    # Search for movie titles that match query
    movies = Movie.objects.filter(title__icontains=query)

    # Return serialized movies
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getMovie(request, id):
    # Get movie by id
    movie = Movie.objects.get(id=id)

    # Return serialized movie
    serializer = MovieSerializer(movie)
    return Response(serializer.data)


@api_view(["GET"])
def getRecommendations(request):
    # Get genres parameter from request
    genresParam = request.GET.get("genres")

    # Return error if genres parameter is missing
    if genresParam is None:
        return Response(
            {"error": "Missing genres parameter."},
            status=400,
        )

    # Split genres parameter into list (ex: ?genres=Action,Adventure -> ["Action", "Adventure"])
    genres = genresParam.split(",")

    # Search for movies that match genres and sort by popularity
    movies = Movie.objects.filter(genres__name__in=genres).order_by("-popularity")

    # Return serialized movies
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def addMovie(request):
    # Create movie from request data
    serializer = MovieSerializer(data=request.data)

    # Validate serializer and return error and status 400 if invalid
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    else:
        return Response(serializer.errors, status=400)
