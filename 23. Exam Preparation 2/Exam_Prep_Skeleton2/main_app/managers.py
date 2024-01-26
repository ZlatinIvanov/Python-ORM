from django.db import models
from django.db.models import Count


class ProfileManager(models.Manager):

    def get_regular_customers(self):
        return (self.annotate(
            regular_customers=Count('profile_order'))
                .filter(regular_customers__gt=2).order_by('-regular_customers'))

