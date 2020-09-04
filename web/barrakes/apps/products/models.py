from django.db import models
from django.utils.translation import ugettext as _

from .managers import ProductManager
# Create your models here.
class Category(models.Model):
    # Relations
    # Attributes - Mandatory
    name = models.CharField(max_length=32, unique=True, help_text="Name of the product category")

    # Attributes - Optional
    # Object Manager
    # Custom Properties
    # Methods

    # Meta and String
    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.name

class Product(models.Model):

    # Relations
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    # Attributes - Mandatory
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=150, unique=True, help_text="Name of the product")
    price = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)

    # Attributes - Optional
    # Object Manager
    objects = ProductManager()

    # Custom Properties
    # Methods

    # Meta and String
    class Meta:
        ordering = ['category', 'name']
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def __str__(self):
        return str(self.name)

