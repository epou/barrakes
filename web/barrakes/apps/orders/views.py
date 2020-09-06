from django.views.generic import ListView, CreateView, UpdateView, DetailView, RedirectView
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, reverse
from django.urls import reverse_lazy
from django.contrib import messages
from django.template.loader import render_to_string
from django.conf import settings
from django.http import JsonResponse
from django.db.models import Sum
from django_tables2 import RequestConfig
from .models import Order, OrderItem
from .forms import OrderCreateForm, OrderEditForm
from ..products.models import Product, Category
from .tables import ProductTable, OrderItemTable, OrderTable
from django.http import HttpResponse
from django.forms.models import model_to_dict
import datetime
from django.core import serializers
import json

from django.views.decorators.csrf import csrf_exempt

@method_decorator(staff_member_required, name='dispatch')
class HomepageView(ListView):
    template_name = 'index.html'
    model = Order
    queryset = Order.objects.all()[:10]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        orders = Order.objects.pending()
        num_finished_orders = Order.objects.finished().count()
        num_pending_orders = orders.count()

        orders = OrderTable(orders)
        order_items = OrderItemTable(OrderItem.objects.none())

        RequestConfig(self.request).configure(orders)
        RequestConfig(self.request).configure(order_items)
        context.update(locals())
        return context


@method_decorator(staff_member_required, name='dispatch')
class OrderListView(ListView):
    template_name = 'order_list.html'
    model = Order
    paginate_by = 50
    queryset = Order.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = OrderTable(self.object_list)
        order_items = OrderItemTable(OrderItem.objects.none())

        RequestConfig(self.request).configure(orders)
        RequestConfig(self.request).configure(order_items)
        context.update(locals())
        return context

class OrderStatusView(DetailView):
    template_name = 'order_status.html'
    model = Order
    query_pk_and_slug=True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_unactive_progress'] = Order.MAX_STEPS - self.object.status_steps
        context.update(locals())
        return context

@method_decorator(staff_member_required, name='dispatch')
class OrderStatusRedirectView(RedirectView):
    def get_redirect_url(self, pk):
        order = Order.objects.get(pk=pk)
        return reverse('order_status', args=[order.slug])

class CreateOrderView(CreateView):
    template_name = 'order_form.html'
    form_class = OrderCreateForm
    model = Order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.active()

        context.update(locals())
        return context

    def get_success_url(self):
        self.new_object.refresh_from_db()
        return reverse('update_order', kwargs={'pk': self.new_object.id})

    def form_valid(self, form):
        object = form.save()
        object.refresh_from_db()
        self.new_object = object
        return super().form_valid(form)

@method_decorator(staff_member_required, name='dispatch')
class ProductListView(ListView):
    template_name = 'product_list.html'
    model = Product
    paginate_by = 50
    queryset = Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = ProductTable(self.object_list)

        RequestConfig(self.request).configure(products)
        context.update(locals())
        return context

@csrf_exempt
def create_new_order(request):
    if request.method == "POST":
        order = request.POST.get("order")
        order_json = json.loads(order)
        order = Order.objects.create(
            seat_number=order_json['seat_number'],
            payment_method=order_json['payment_method'],
            payment_amount=order_json['payment_amount'],
        )
        for item in order_json['items']:
            OrderItem.objects.create(
                product_id=item['product_id'],
                quantity=item['quantity'],
                order=order
            )
        data = {}
        if request.user.is_anonymous:
            data['href'] = reverse('order_status', kwargs={'slug': order.slug})
        else:
            data['href'] = reverse('order_list')
        return JsonResponse(data)
    else:
        return HttpResponse(status=404)

@staff_member_required
def change_order_status(request):
    if request.method == "POST":
        data = request.POST.get("data")

        data_json = json.loads(data)

        instance = get_object_or_404(Order, id=data_json['order_id'])
        instance.status = data_json['status']
        instance.save()

        if data_json['return_only_pending']:
            orders = Order.objects.pending()
        else:
            orders = Order.objects.all()

        if data_json['return_inverse_order']:
            orders = orders.order_by(['-timestamp'])

        num_pending_orders = Order.objects.pending().count()
        num_finished_orders = Order.objects.finished().count()

        orders = OrderTable(orders)

        RequestConfig(request).configure(orders)
        data = dict()
        data['orders'] = render_to_string(
            template_name='include/order_table.html',
            request=request,
            context={
                'orders': orders,
            }
        )
        data['num_finished_orders'] = num_finished_orders
        data['num_pending_orders'] = num_pending_orders
        return JsonResponse(data)

    else:
        return HttpResponse(status=404)

@staff_member_required
def order_list(request):
    if request.method == "GET":
        return_only_pending = request.GET.get("return_only_pending")
        return_inverse_order = request.GET.get("return_inverse_order")
        if return_only_pending == 'true':
            orders = Order.objects.pending()
        else:
            orders = Order.objects.all()

        if return_inverse_order == 'true':
            orders = orders.order_by('-timestamp')

        num_pending_orders = Order.objects.pending().count()
        num_finished_orders = Order.objects.finished().count()

        orders = OrderTable(orders)

        RequestConfig(request).configure(orders)
        data = dict()
        data['orders'] = render_to_string(
            template_name='include/order_table.html',
            request=request,
            context={
                'orders': orders,
            }
        )
        data['num_finished_orders'] = num_finished_orders
        data['num_pending_orders'] = num_pending_orders
        return JsonResponse(data)

    else:
        return HttpResponse(status=404)

@staff_member_required
def order_items_list(request):
    if request.method == "GET":
        order_id = request.GET.get("order_id")

        order = get_object_or_404(Order, id=order_id)

        order_items = OrderItemTable(order.items.all())

        RequestConfig(request).configure(order_items)
        data = dict()
        data['modal'] = render_to_string(
            template_name='include/order_item_modal.html',
            request=request,
            context={
                'order_items': order_items,
                'order': order
            }
        )
        return JsonResponse(data)

    else:
        return HttpResponse(status=404)

def order_status(request):
    if request.method == "GET":

        slug = request.GET.get("slug")
        if not slug:
            return HttpResponse(status=404)

        object = OrderStatusView(kwargs={"slug": slug}).get_object()

        data = dict()
        data['object'] = render_to_string(
            template_name="./include/order_status_container.html",
            request=request,
            context={
                'object': object,
                'num_unactive_progress': Order.MAX_STEPS - object.status_steps
            }
        )
        return JsonResponse(data)

    else:
        return HttpResponse(status=404)

@staff_member_required
def change_product_status(request):
    if request.method == "POST":
        data = request.POST.get("data")

        data_json = json.loads(data)

        instance = get_object_or_404(Product, id=data_json['product_id'])
        instance.active = data_json['status']
        instance.save()

        products = ProductTable(Product.objects.all())

        RequestConfig(request).configure(products)
        data = dict()
        data['products'] = render_to_string(
            template_name='include/product_container.html',
            request=request,
            context={
                'products': products,
            }
        )
        return JsonResponse(data)

    else:
        return HttpResponse(status=404)
