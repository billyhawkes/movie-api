from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response

from base.models import Genre, Movie

from .serializers import GenreSerializer, MovieSerializer


@extend_schema(responses={200: GenreSerializer(many=True)}, description="Get genres")
@api_view(["GET"])
def getGenres(request):
    # Get all genres
    genres = Genre.objects.all()

    # Return serialized genres
    serializer = GenreSerializer(genres, many=True)
    return Response(serializer.data)


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="genre", description="Genre name", required=False, type=str
        ),
        OpenApiParameter(
            name="sort", description="Sort parameter", required=False, type=str
        ),
    ],
    examples=[
        OpenApiExample(
            "Top rated action movies",
            value={
                "genre": "Action",
                "sort": "-popularity",
            },
        ),
    ],
    responses={200: MovieSerializer(many=True)},
    description="Get movies",
)
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


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="query", description="Search query", required=True, type=str
        )
    ],
    examples=[
        OpenApiExample(
            "Search for Titanic",
            value={
                "query": "Titanic",
            },
        ),
    ],
    responses={200: MovieSerializer(many=True)},
    description="Search movies",
)
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


@extend_schema(
    parameters=[
        OpenApiParameter(name="id", description="Movie ID", required=True, type=str)
    ],
    examples=[
        OpenApiExample(
            "Get Titanic",
            value={
                "id": "597",
            },
        ),
    ],
    responses={200: MovieSerializer()},
    description="Get movie by ID",
)
@api_view(["GET"])
def getMovie(request, id):
    # Get movie by id
    movie = Movie.objects.get(id=id)

    # Return serialized movie
    serializer = MovieSerializer(movie)
    return Response(serializer.data)


@extend_schema(
    parameters=[
        OpenApiParameter(name="genres", description="Genres", required=True, type=str)
    ],
    examples=[
        OpenApiExample(
            "Get recommendations for action and adventure movies",
            value={
                "genres": "Action,Adventure",
            },
        ),
    ],
    responses={200: MovieSerializer(many=True)},
    description="Get recommendations",
)
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


@extend_schema(
    request=MovieSerializer,
    responses={201: MovieSerializer()},
    description="Add movie",
    examples=[
        OpenApiExample(
            "Add Titanic",
            value={
                "budget": 200000000,
                "genres": [
                    {
                        "id": 18,
                        "name": "Drama",
                    },
                    {
                        "id": 10749,
                        "name": "Romance",
                    },
                ],
                "homepage": "http://www.titanicmovie.com/",
                "id": 597,
                "overview": "101-year-old Rose DeWitt Bukater tells the story of her life aboard the Titanic, 84 years later. A young Rose boards the ship with her mother and fiancé. Meanwhile, Jack Dawson and Fabrizio De Rossi win third-class tickets aboard the ship. Rose tells the whole story from Titanic's departure through to its death—on its first and last voyage—on April 15, 1912.",
                "popularity": 38.116,
                "title": "Titanic",
            },
        ),
    ],
)
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
