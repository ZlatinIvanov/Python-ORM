import os
import django
from django.db.models import Q, Count, Avg, F, Max

from main_app import models
from main_app.models import Director, Actor, Movie

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()


def get_directors(search_name=None, search_nationality=None):
    if search_name is None and search_nationality is None:
        return ''

    query = Q()
    query_name = Q(full_name__icontains=search_name)
    query_nationality = Q(nationality__icontains=search_nationality)
    if search_name is not None and search_nationality is None:
        query |= query_name
    elif search_name is None and search_nationality is not None:
        query |= query_nationality
    else:
        query |= query_name & query_nationality
    directors = Director.objects.filter(query).order_by('full_name')
    result = []
    for director in directors:
        if not director:
            return ""
        result.append(
            f"Director: {director.full_name}, nationality: {director.nationality}, experience: {director.years_of_experience}")
    return '\n'.join(result)


# def get_top_director():
#     director = Director.objects.get_directors_by_movies_count().first()
#     if not director:
#         return ""
#     return f"Top Director: {director.full_name}, movies: {director.num_of_movies}."

def get_top_director():
    # Use the existing custom manager method to get directors ordered by movie count
    top_director = Director.objects.get_directors_by_movies_count().first()

    if top_director:
        # Get the number of movies directed by the top director
        num_of_movies = top_director.director_movies.count()

        return f"Top Director: {top_director.full_name}, movies: {num_of_movies}."

    return ""

# def get_top_actor():
#     actor = Actor.objects.prefetch_related(
#         'starring_movies').annotate(num_of_movies=Count(
#         'starring_movies'), movies_avg_rating=Avg('starring_movies__rating')).order_by(
#         '-num_of_movies', 'full_name').first()
#     movies = ", ".join(movie.title for movie in actor.starring_movies.all() if movie)
#     if not actor or not actor.num_of_movies:
#         return ''
#
#     return f"Top Actor: {actor.full_name}, starring in movies: {movies}, " \
#            f"movies average rating: {actor.movies_avg_rating:.1f}"


def get_top_actor():
    # Get the starring actor with the greatest number of movies
    top_actor = Actor.objects.annotate(movie_count=Count('starring_movies')).order_by('-movie_count', 'full_name').first()

    if top_actor:
        # Get the movies in which the actor stars
        movies_starring_top_actor = top_actor.starring_movies.all()

        if movies_starring_top_actor:
            # Calculate the average rating of the movies
            avg_rating = movies_starring_top_actor.aggregate(avg_rating=Avg('rating'))['avg_rating']
            avg_rating_formatted = f'{avg_rating:.1f}' if avg_rating is not None else 'N/A'

            # Get the titles of the movies
            movie_titles = ', '.join(movie.title for movie in movies_starring_top_actor)

            return f"Top Actor: {top_actor.full_name}, starring in movies: {movie_titles}, movies average rating: {avg_rating_formatted}"

    return ""


def get_actors_by_movies_count():
    # Use the existing custom manager method to get actors ordered by movie count
    top_actors = Actor.objects.annotate(num_movies=Count('actor_movies')).order_by('-num_movies', 'full_name')[:3]

    if top_actors:
        # Create a formatted string for each actor
        actor_info_list = [f"{actor.full_name}, participated in {actor.num_movies} movies" for actor in top_actors]

        # Join the formatted strings with newlines
        result = "\n".join(actor_info_list)

        return result

    return ""

# def get_actors_by_movies_count():
#     actors = Actor.objects.annotate(num_movies=Count('actor__movies')) \
#                  .order_by('-num_movies', 'full_name')[:3]
#
#     if not actors or not actors[0].num_movies:
#         return ""
#
#     result = []
#     for actor in actors:
#         result.append(f"{actor.full_name}, participated in {actor.num_movies} movies")
#
#     return '\n'.join(result)


def get_top_rated_awarded_movie():
    # Get the highest rating among awarded movies
    max_awarded_rating = Movie.objects.filter(is_awarded=True).aggregate(max_rating=Max('rating'))['max_rating']

    if max_awarded_rating is not None:
        # Get the awarded movie with the highest rating
        top_rated_awarded_movie = Movie.objects.filter(is_awarded=True, rating=max_awarded_rating).order_by('title').first()

        # Get the starring actor's full name or 'N/A' if None
        starring_actor_full_name = top_rated_awarded_movie.starring_actor.full_name if top_rated_awarded_movie.starring_actor else 'N/A'

        # Get the list of participating actors' full names, ordered by full name
        participating_actors = Actor.objects.filter(actor_movies=top_rated_awarded_movie).order_by('full_name')
        participating_actors_list = ', '.join(actor.full_name for actor in participating_actors)

        return f"Top rated awarded movie: {top_rated_awarded_movie.title}, rating: {top_rated_awarded_movie.rating:.1f}. Starring actor: {starring_actor_full_name}. Cast: {participating_actors_list}."

    return ""


# def get_top_rated_awarded_movie():
#     top_movie = Movie.objects\
#         .select_related('starring_actor')\
#         .prefetch_related('actors') \
#         .filter(is_awarded=True) \
#         .order_by('-rating', 'title') \
#         .first()
#
#     if top_movie is None:
#         return ""
#
#     starring_actor = top_movie.starring_actor.full_name if top_movie.starring_actor else "N/A"
#
#     participating_actors = top_movie.actors.order_by('full_name').values_list('full_name', flat=True)
#     cast = ", ".join(participating_actors)
#
#     return f"Top rated awarded movie: {top_movie.title}, rating: {top_movie.rating:.1f}. " \
#            f"Starring actor: {starring_actor}. Cast: {cast}."


def increase_rating():
    # Increase the rating for classic movies by 0.1, but not exceeding the maximum value of 10.0
    num_of_updated_movies = Movie.objects.filter(is_classic=True, rating__lt=10.0).update(rating=F('rating') + 0.1)

    if num_of_updated_movies > 0:
        return f"Rating increased for {num_of_updated_movies} movies."
    else:
        return "No ratings increased."


# def increase_rating():
#     updated_movies = Movie.objects.filter(is_classic=True, rating__lt=10.0)
#
#     if not updated_movies:
#         return "No ratings increased."
#
#     num_of_updated_movies = updated_movies.update(rating=F('rating') + 0.1)
#
#     return f"Rating increased for {num_of_updated_movies} movies."