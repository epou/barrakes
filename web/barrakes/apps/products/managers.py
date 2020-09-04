from django.db import models


class ProductManager(models.Manager):

    def active(self):
        return self.get_queryset().filter(active=True)
