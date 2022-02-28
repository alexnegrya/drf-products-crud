from django import forms
from .models import Products, JSON
from .serializers import Base64ImageField
from .widgets import DateTimePickerInput
from prettyjson import PrettyJSONWidget


class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['name', 'price', 'image', 'creator', 'create_date']


class JSONForm(forms.ModelForm):
    class Meta:
        model = JSON
        fields = ['content']
        widgets = {
            'content': PrettyJSONWidget()
        }


def _get_products_choices():
    queryset = Products.objects.all()
    choices = []
    for product in queryset:
        choices.append(
            (product.pk, f'{product.pk} | {product.name}')
        )
    return choices

class HiddenProductForm(forms.Form):
    pk = forms.CharField(
        max_length=10000000,
        label='Select product:',
        widget=forms.Select(choices=_get_products_choices())
    )
