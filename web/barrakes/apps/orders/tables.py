import django_tables2 as tables

from ..products.models import Product
from .models import OrderItem, Order


class OrderTable(tables.Table):
    total_price = tables.TemplateColumn(
        template_code='{{ record.total_price }} €',
        orderable=False
    )
    #action = tables.TemplateColumn(
    #    template_code='''
    #    <button type="button" class="btn btn-info btn-sm" title="Editar"><i class="fa fa-edit"></i></button>
    #    ''',
    #    orderable=False,
    #    verbose_name='Acció'
    #)
    status = tables.TemplateColumn(
        template_code='''
        <div class="jquery-btn-status btn-group" data-index='{{ record.id }}'>
            <button type="button" class="btn btn-rounded 
                {% if record.status == record.RECEIVED %}
                    btn-secundary
                {% elif record.status == record.PREPARING %}
                    btn-info
                {% elif record.status == record.ON_DELIVERY %}
                    btn-warning                    
                {% elif record.status == record.PAID %}
                    btn-success
                {% elif record.status == record.CANCELLED %}
                    btn-danger
                {% endif %}
                dropdown-toggle" data-toggle="dropdown">
                {% if record.status == record.RECEIVED %}
                    {{ record.FORMAT_RECEIVED }}
                {% elif record.status == record.PREPARING %}
                    {{ record.FORMAT_PREPARING }}
                {% elif record.status == record.ON_DELIVERY %}
                    {{ record.FORMAT_ON_DELIVERY }}
                {% elif record.status == record.PAID %}
                    {{ record.FORMAT_PAID }}
                {% elif record.status == record.CANCELLED %}
                    {{ record.FORMAT_CANCELLED }}
                {% endif %}
            </button>
            <div class="dropdown-menu">
                {% if record.status != record.RECEIVED %}
                    <a class="dropdown-item" data-value='{{ record.RECEIVED }}'>{{ record.FORMAT_RECEIVED }}</a>
                {% endif %}
                {% if record.status != record.PREPARING %}
                    <a class="dropdown-item" data-value='{{ record.PREPARING }}'>{{ record.FORMAT_PREPARING }}</a>
                {% endif %}
                {% if record.status != record.ON_DELIVERY %}
                    <a class="dropdown-item" data-value='{{ record.ON_DELIVERY }}'>{{ record.FORMAT_ON_DELIVERY }}</a>
                {% endif %}
                {% if record.status != record.PAID %}
                    <div class="dropdown-divider"></div>
                    <a class="dropdown-item" data-value='{{ record.PAID }}'>{{ record.FORMAT_PAID }}</a>
                {% endif %}
                {% if record.status != record.CANCELLED %}
                    <div class="dropdown-divider"></div>
                    <a class="dropdown-item text-danger" data-value='{{ record.CANCELLED }}'>{{ record.FORMAT_CANCELLED }}</a>
                {% endif %}
            </div>
        </div>
        '''
    )
    payment_method = tables.TemplateColumn(
        template_code='''
        {% if record.payment_method == record.PAYMENT_CASH %}
            <label class="mdi mdi-coin"></label> ({{ record.payment_amount }} €)
        {% elif record.payment_method == record.PAYMENT_CARD %}
            <label class="fa fa-credit-card"></label>
        {% endif %}
        ''',
    )

    payment_change = tables.TemplateColumn(
        template_code="{% if record.payment_change %}<a class='text-danger'> {{ record.payment_change }} €</a> {% endif%}",
        orderable=False,
        verbose_name='Canvi'
    )

    class Meta:
        model = Order
        template_name = './new_table.html'
        fields = ['id', 'timestamp', 'seat_number', 'status', 'payment_method', 'total_price', 'payment_change']
        attrs = {'class': 'table table-hover'}
        row_attrs = {'data-target': '#modal_aside_left', 'data-toggle': 'modal'}


class ProductTable(tables.Table):
    price = tables.TemplateColumn(
        template_code='{{ record.price }} €',
        orderable=False
    )

    status = tables.TemplateColumn(
        template_code='''
            <div class="jquery-btn-status btn-group" data-index='{{ record.id }}'>
                <button type="button" class="btn btn-rounded 
                    {% if record.active %}
                        btn-success
                    {% else %}
                        btn-danger
                    {% endif %}
                    dropdown-toggle" data-toggle="dropdown">
                    {% if record.active  %}
                        Disponible
                    {% else %}
                        Esgotat
                    {% endif %}
                </button>
                <div class="dropdown-menu">
                    {% if not record.active %}
                        <a class="dropdown-item" data-value='True'>Disponible</a>
                    {% else %}
                        <a class="dropdown-item" data-value='False'>Esgotat</a>
                    {% endif %}
                </div>
            </div>
            ''', verbose_name="Disponibilitat"
    )

    class Meta:
        model = Product
        template_name = 'django_tables2/bootstrap.html'
        fields = ['name', 'category', 'status', 'price']


class OrderItemTable(tables.Table):
    total_price = tables.TemplateColumn(
        template_code='{{ record.total_price }} €',
        orderable=False
    )

    class Meta:
        model = OrderItem
        template_name = 'django_tables2/bootstrap.html'
        fields = ['quantity', 'product', 'total_price']
        orderable = False
