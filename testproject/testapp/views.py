from django.shortcuts import render, redirect
from django.contrib.auth import models
from rest_framework import viewsets, permissions, views
from .serializers import UserSerializer, GroupSerializer, ProductsSerializer
from .models import Products
from .forms import ProductForm, HiddenProductForm
from rest_framework.response import Response
from django.template.defaulttags import register
from django.utils import timezone
from rest_framework.renderers import TemplateHTMLRenderer
from django.core import serializers
from django.db import DatabaseError
from datetime import datetime
from dateutil import parser as datetime_parser


# Template filters

@register.filter
def get_dict_key_by_index(d: dict, i: int) -> str:
    return list(d.keys())[i]

@register.filter
def get_dict_value(key, d: dict):
    return d[key]

# Default views

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = models.User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = models.Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

# User defined functions and views

def create_test_products():
    Products.objects.create(
        name='Smartphone Samsung A035',
        price=3299,
        image='Samsung_A035.webp',
        creator='Admin'
    )
    Products.objects.create(
        name='Smartphone Xiaomi Mi 11T',
        price=8699,
        image='Xiaomi_Mi_11T.webp',
        creator='Admin'
    )
    Products.objects.create(
        name='Smartphone Apple iPhone 13',
        price=17900,
        image='Apple_iPhone_13.webp',
        creator='Admin'
    )
    Products.objects.create(
        name='Laptop Acer TMP215-53',
        price=10000,
        image='Acer_TMP215-53.webp',
        creator='Admin'
    )
    Products.objects.create(
        name='Laptop Asus VivoBook K513EA-L11950',
        price=17000,
        image='Asus_VivoBook_K513EA-L11950.webp',
        creator='Admin'
    )
    Products.objects.create(
        name='TV LG 60UP77506LA',
        price=12800,
        image='LG_60UP77506LA.jpg',
        creator='Admin'
    )
    Products.objects.create(
        name='TV Sony XR65A80JAEP',
        price=46000,
        image='Sony_XR65A80JAEP.webp',
        creator='Admin'
    )
    Products.objects.create(
        name='Headphones Hoco ES280SAPGD',
        price=900,
        image='Hoco_ES280SAPGD.webp',
        creator='Admin'
    )
    Products.objects.create(
        name='Headphones JBL Tune 215 TWS',
        price=1800,
        image='JBL_Tune_215_TWS.webp',
        creator='Admin'
    )
    Products.objects.create(
        name='Microphone Marvo MIC-01',
        price=350,
        image='Marvo_MIC-01.webp',
        creator='Admin'
    )

if len(Products.objects.all()) <= 0:
    create_test_products()


def main_page(request):
    try:
        if request.session['msg_show_count'] >= 1:
            request.session['msg'] = None
            request.session['msg_show_count'] = None
        else:
            request.session['msg_show_count'] += 1
    except:
        pass

    return render(request, 'index.html', {
        'path': {'': 'Main page'},
        'form': HiddenProductForm
    })


class ProductsAPIView:
    permission_classes = [permissions.AllowAny]
    renderer_classes = [TemplateHTMLRenderer]


class ProductsList(ProductsAPIView, views.APIView):
    template_name = 'products.html'

    def get(self, request):
        queryset = Products.objects.all()
        json_data = serializers.serialize('json', queryset)
        return Response({
            'path': {'/': 'Main page', '/products/': 'Products'},
            'json_data': json_data
        })


class CreateProduct(ProductsAPIView, views.APIView):
    template_name = 'create_product.html'
    form = ProductForm
    path = {'/': 'Main page', '/create-product/': 'Create product'}

    def get(self, request):
        return Response({
            'path': self.path,
            'form': self.form,
            'created': False,
            'include_product_form_styles': True
        })
    
    def post(self, request):
        try:
            create_dt = datetime_parser.parse(request.POST['create_date'])

            product = Products.objects.create(
                name=request.POST['name'],
                price=request.POST['price'],
                image=request.POST['image'],
                creator=request.POST['creator'],
                create_date=create_dt
            )
            
            json_data = serializers.serialize('json', [product])
            product.save()

            return Response({
                'path': self.path,
                'form': self.form,
                'created': True,
                'json_data': json_data,
                'include_product_form_styles': True
            })
        except DatabaseError as error:
            return Response({
                'path': self.path,
                'form': self.form,
                'created': False,
                'error': error,
                'error_name': error.__class__.__name__,
                'include_product_form_styles': True
            })


def redirect_to_update(request):
    return redirect('update_product', pk=request.GET['pk'])

class UpdateProduct(ProductsAPIView, views.APIView):
    template_name = 'update_product.html'
    form = ProductForm

    def __get_path(self, pk: int) -> dict[str, str]:
        return {'/': 'Main page', f'/update-product/{pk}/': 'Update product'}
    
    def get(self, request, pk):
        path = self.__get_path(pk)

        try:
            product = Products.objects.get(pk=pk)
            
            form = ProductForm(initial={
                'name': product.name,
                'price': product.price,
                'image': product.image,
                'creator': product.creator,
                'create_date': product.create_date
            })

            return Response({
                'path': path,
                'product': product,
                'updated': False,
                'form': form,
                'product_pk': pk,
                'include_product_form_styles': True
            })
        except DatabaseError as error:
            return Response({
                'path': path,
                'error': error,
                'error_name': error.__class__.__name__,
                'updated': False,
                'form': self.form,
                'product_pk': pk,
                'include_product_form_styles': True
            })
    
    def post(self, request, pk):
        path = self.__get_path(pk)

        try:
            product = Products.objects.get(pk=pk)

            for field in request.POST:
                if not field.startswith('csrf') and field != 'create_date':
                    setattr(product, field, request.POST[field])
                elif field == 'create_date':
                    setattr(product, field, datetime_parser.parse(request.POST['create_date']))

            json_data = serializers.serialize('json', [product])
            product.save()

            return Response({
                'path': path,
                'updated': True,
                'json_data': json_data,
                'form': self.form,
                'product_pk': pk
            })
        except DatabaseError as error:
            return Response({
                'path': path,
                'error': error,
                'error_name': error.__class__.__name__,
                'updated': False,
                'form': self.form,
                'product_pk': pk
            })


def redirect_to_delete(request):
    return redirect('delete_product', pk=request.GET['pk'])

class DeleteProduct(ProductsAPIView, views.APIView):
    def get(self, request, pk):
        Products.objects.get(pk=pk).delete()
        request.session['msg'] = f'Product with PK {pk} was deleted successfully!'
        request.session['msg_show_count'] = 0
        
        return redirect('main')
