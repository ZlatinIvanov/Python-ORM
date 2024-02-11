import os
import django
from django.db import models
from django.db.models import Q, Count, Avg

from main_app.models import Author, Article, Review

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

def get_authors(search_name=None, search_email=None):
    if search_name is None and search_email is None:
        return ''

    query = Q()
    query_name = Q(full_name__icontains=search_name)
    query_email = Q(email__icontains=search_email)
    if search_name is not None and search_email is None:
        query |= query_name
    elif search_name is None and search_email is not None:
        query |= query_email
    else:
        query |= query_name & query_email
    authors = Author.objects.filter(query).order_by('-full_name')
    if not authors:
        return ''
    result = []
    for author in authors:
        status = 'Banned' if author.is_banned else 'Not Banned'
        result.append(
            f"Author: {author.full_name}, email: {author.email}, status: {status}")
    return '\n'.join(result)


def get_top_publisher():

    authors_with_article_count = Author.objects.annotate(num_articles=models.Count('article'))

    authors_with_articles = authors_with_article_count.filter(num_articles__gt=0)

    top_publisher = authors_with_articles.order_by('-num_articles', 'email').first()

    if top_publisher:
        return f"Top Author: {top_publisher.full_name} with {top_publisher.num_articles} published articles."
    else:
        return ""

def get_top_reviewer():

    authors_with_review_count = Author.objects.annotate(num_reviews=models.Count('review'))

    authors_with_reviews = authors_with_review_count.filter(num_reviews__gt=0)

    top_reviewer = authors_with_reviews.order_by('-num_reviews', 'email').first()

    if top_reviewer:
        return f"Top Reviewer: {top_reviewer.full_name} with {top_reviewer.num_reviews} published reviews."
    else:
        return ""

def get_latest_article():
    latest_article = Article.objects.order_by('-published_on').first()

    if not latest_article:
        return ""

    authors = latest_article.authors.all().order_by('full_name')
    author_names = ", ".join([author.full_name for author in authors])

    num_reviews = Review.objects.filter(article=latest_article).count()
    avg_rating = Review.objects.filter(article=latest_article).aggregate(avg_rating=models.Avg('rating'))['avg_rating']

    formatted_avg_rating = "{:.2f}".format(avg_rating) if avg_rating is not None else "0.00"

    return f"The latest article is: {latest_article.title}. Authors: {author_names}. Reviewed: {num_reviews} times. Average Rating: {formatted_avg_rating}."


def get_top_rated_article():

    articles_with_ratings = Article.objects.annotate(
        avg_rating=models.Avg('review__rating'),
        num_reviews=models.Count('review')
    )

    articles_with_reviews = articles_with_ratings.filter(num_reviews__gt=0)

    top_rated_article = articles_with_reviews.order_by('-avg_rating', 'title').first()

    if top_rated_article:

        formatted_avg_rating = "{:.2f}".format(top_rated_article.avg_rating)
        return f"The top-rated article is: {top_rated_article.title}, with an average rating of {formatted_avg_rating}, reviewed {top_rated_article.num_reviews} times."
    else:
        return ""


def ban_author(email=None):
    if email is None:
        return "No authors banned."

    author_to_ban = Author.objects.filter(email=email).first()

    if author_to_ban is None:
        return "No authors banned."

    num_reviews = Review.objects.filter(author=author_to_ban).count()

    Review.objects.filter(author=author_to_ban).delete()

    author_to_ban.is_banned = True
    author_to_ban.save()

    return f"Author: {author_to_ban.full_name} is banned! {num_reviews} reviews deleted."

