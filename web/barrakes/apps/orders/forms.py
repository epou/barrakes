from django import forms

from .models import Order


class BaseForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class OrderCreateForm(BaseForm, forms.ModelForm):

    class Meta:
        model = Order
        fields = ['seat_number']


class OrderEditForm(BaseForm, forms.ModelForm):

    class Meta:
        model = Order
        fields = ['status']
