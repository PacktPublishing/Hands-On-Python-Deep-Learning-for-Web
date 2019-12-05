from django.forms import ModelForm
from django import forms
from .models import Order

class OrderForm(ModelForm):
    OPTIONS = (
        ('Confirmed', 'Confirmed'),
        ('Shipping', 'Shipping'),
        ('Delivered', 'Delivered'),
    )
    order_status = forms.TypedChoiceField(required=False, choices=OPTIONS, widget=forms.RadioSelect)

    class Meta:
        model = Order
        fields = ['name','phone','address','product_id','amount','order_status']