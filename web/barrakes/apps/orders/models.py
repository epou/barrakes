from django.db import models
from django.utils.translation import ugettext as _
from django.db.models import Sum
from django.urls import reverse

from decimal import Decimal
import uuid

from model_utils.models import StatusModel
from model_utils import Choices

from ..products.models import Product

class OrderManager(models.Manager):

    def pending(self):
        return self.get_queryset().filter(status__in=(Order.RECEIVED, Order.PREPARING, Order.ON_DELIVERY))

    def finished(self):
        return self.get_queryset().filter(status=Order.PAID)

# Create your models here.
class Order(StatusModel):

    MAX_STEPS = 4

    RECEIVED = "received"
    FORMAT_RECEIVED = "Rebut"

    PREPARING = 'preparing'
    FORMAT_PREPARING = 'En procés'

    ON_DELIVERY = "on_delivery"
    FORMAT_ON_DELIVERY = "En camí"

    PAID = 'paid'
    FORMAT_PAID = 'Pagat'

    CANCELLED = 'cancelled'
    FORMAT_CANCELLED = 'Cancel·lat'

    @classmethod
    def get_status_step(cls, status):
        result = 1
        if status == cls.PREPARING:
            result = 2
        elif status == cls.ON_DELIVERY:
            result = 3
        elif status == cls.PAID:
            result = 4
        elif status == cls.CANCELLED:
            result = 5
        return result

    STATUS = Choices(
        RECEIVED,
        PREPARING,
        ON_DELIVERY,
        PAID,
        CANCELLED
    )

    PAYMENT_CARD = 'card'
    PAYMENT_CASH = 'cash'

    PAYMENT_OPTIONS = Choices('card', 'cash')

    # Relations
    # Attributes - Mandatory
    slug = models.SlugField(default=uuid.uuid4, editable=False)
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Hora')
    seat_number = models.PositiveSmallIntegerField(verbose_name='Cadira')
    total_price = models.DecimalField(default=0.00, decimal_places=2, max_digits=20, verbose_name='Preu')
    status = models.CharField(max_length=32, choices=STATUS, default='received', verbose_name='estat')
    payment_method = models.CharField(max_length=16, choices=PAYMENT_OPTIONS, default=PAYMENT_CARD, verbose_name='Pagament')
    # Attributes - Optional
    payment_amount = models.DecimalField(decimal_places=2, max_digits=20, null=True, default=None)
    # Object Manager
    objects = OrderManager()

    # Custom Properties
    @property
    def status_steps(self):
        return self.get_status_step(status=self.status)

    @property
    def payment_change(self):
        return self.total_price - self.payment_amount if self.payment_method == self.PAYMENT_CASH else None

    # Methods
    def save(self, *args, **kwargs):
        items = self.items.all()
        self.total_price = items.aggregate(Sum('total_price'))['total_price__sum'] if items.exists() else 0.00
        if self.payment_method != self.PAYMENT_CASH:
            self.payment_amount = None
        super().save(*args, **kwargs)

    def get_edit_url(self):
        return reverse('update_order', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('delete_order', kwargs={'pk': self.id})

    # Meta and String
    class Meta:
        ordering = ['timestamp']
        verbose_name = _('order')
        verbose_name_plural = _('orders')

    def __str__(self):
        return str(self.seat_number)

class OrderItem(models.Model):

    # Relations
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='Producte')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    # Attributes - Mandatory
    price = models.DecimalField(default=0.00, decimal_places=2, max_digits=10, verbose_name='Preu')
    quantity = models.PositiveSmallIntegerField(default=1, verbose_name='Quantitat')
    total_price = models.DecimalField(default=0.00, decimal_places=2, max_digits=20, verbose_name='Preu')

    # Attributes - Optional
    # Object Manager
    # Custom Properties
    # Methods
    def save(self, *args, **kwargs):
        self.price = self.product.price
        self.total_price = Decimal(self.quantity) * Decimal(self.price)
        super().save(*args, **kwargs)
        self.order.save()

    # Meta and String
    class Meta:
        verbose_name = _('order item')
        verbose_name_plural = _('order items')

    def __str__(self):
        return str(self.product)
