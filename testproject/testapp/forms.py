from django import forms


class ProductForm(forms.Form):
    image_url = forms.CharField(max_length=100000, label='Enter URL to image')
    name = forms.CharField(max_length=100, label='Enter product name')
    price = forms.FloatField(label='Enter price')
    creator = forms.CharField(max_length=100, label='Enter your username')
    create_date = forms.DateTimeField(label='Enter product creation date and time')
