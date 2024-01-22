from django.core.validators import MinLengthValidator, MaxValueValidator, MinValueValidator
from django.db import models

from main_app.custom_model_manager import DirectorManager
from main_app.model_mixins import LastUpdatedMixin, IsAwardedMixin


# Create your models here.


class BasePerson(models.Model):
    full_name = models.CharField(
        max_length=120,
        validators=[MinLengthValidator(2)])
    birth_date = models.DateField(default='1900-01-01')
    nationality = models.CharField(
        max_length=50,
        default='Unknown')

    def __str__(self):
        return self.full_name

    class Meta:
        abstract = True


class Director(BasePerson):
    years_of_experience = models.SmallIntegerField(
        default=0,
        validators=[MinValueValidator(0)])

    objects = DirectorManager()


class Actor(LastUpdatedMixin, IsAwardedMixin, BasePerson):
    pass


class Movie(LastUpdatedMixin, IsAwardedMixin):
    GENRE_CHOICES = [
        ('Action', 'Action'),
        ('Comedy', 'Comedy'),
        ('Drama', 'Drama'),
        ('Other', 'Other'),
    ]

    title = models.CharField(
        max_length=150,
        validators=[MinLengthValidator(5)])

    release_date = models.DateField()

    storyline = models.TextField(null=True, blank=True)

    genre = models.CharField(
        max_length=6,
        choices=GENRE_CHOICES,
        default='Other')

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
        default=0.0)

    is_classic = models.BooleanField(default=False)

    director = models.ForeignKey(Director,
                                 on_delete=models.CASCADE,
                                 related_name='director_movies')
    starring_actor = models.ForeignKey(Actor,
                                       on_delete=models.SET_NULL,
                                       related_name='starring_movies',
                                       null=True, blank=True)
    actors = models.ManyToManyField(Actor,
                                    related_name='actor_movies')

    def __str__(self):
        return self.title
