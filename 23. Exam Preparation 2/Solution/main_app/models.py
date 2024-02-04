from django.db import models
from django.core.validators import MinValueValidator, MinLengthValidator, MaxLengthValidator

from main_app.custom_manager import CustomProfileManager
from main_app.model_mixins import TimeStampMixin

# Create your models here.


class Profile(TimeStampMixin, models.Model):
    full_name = models.CharField(max_length=100,
                                 validators=[MinLengthValidator(2), ])
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    is_active = models.BooleanField(default=True)

    objects = CustomProfileManager()

    def __str__(self):
        return self.full_name


class Product(TimeStampMixin, models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10,
                                decimal_places=2,
                                validators=[MinValueValidator(0.01)])
    in_stock = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)


class Order(TimeStampMixin, models.Model):
    profile = models.ForeignKey(Profile,
                                on_delete=models.CASCADE,
                                related_name='orders')
    products = models.ManyToManyField(Product, related_name='orders')
    total_price = models.DecimalField(max_digits=10,
                                      decimal_places=2,
                                      validators=[MinValueValidator(0.01)])
    is_completed = models.BooleanField(default=False)

