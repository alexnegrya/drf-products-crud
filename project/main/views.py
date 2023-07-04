from django.contrib.auth import models
from rest_framework import viewsets, permissions, views
from .serializers import UserSerializer, GroupSerializer
from .models import Products
from rest_framework.response import Response
from django.template.defaulttags import register
from rest_framework.renderers import TemplateHTMLRenderer
from datetime import datetime
from dateutil import parser as datetime_parser
import math
import uuid
from .forms import ProductForm
import pytz


# Template tags and filters

@register.simple_tag
def generate_uuid4():
    return uuid.uuid4()

@register.simple_tag
def get_product_form(pk):
    """
    Get Product form with initial model data.
    """
    try:
        pk = int(pk)
        product = Products.objects.get(pk=pk)

        return ProductForm(initial={
            'image_url': product.image_url,
            'name': product.name,
            'price': product.price,
            'creator': product.creator,
            'create_date': product.create_date
        })
    except Products.DoesNotExist:
        pass

@register.simple_tag
def get_now_datetime():
    """
    Get current datatime without timezone info.
    """
    dt_str = str(datetime_parser.isoparse(str(datetime.now())))
    dt_str = dt_str[:dt_str.find('.')]
    return datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')


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

class ProductsView(views.APIView):
    template_name = 'index.html'
    permission_classes = [permissions.AllowAny]
    renderer_classes = [TemplateHTMLRenderer]
    path = {'/': 'Main page'}
    data_title = 'Click to change...'
    product_form = ProductForm
    
    def separate_products(self, products, cols=4):
        """
        Separate list of Products into list of lists with length == specified columns (cols).
        """
        sep_prods = []
        prods = []
        start_index = 0

        for row in range(math.ceil(len(products) / cols)):
            for product in products[start_index:start_index+cols]:
                prods.append(product)
            sep_prods.append(prods.copy())
            prods.clear()
            start_index += cols
        
        return sep_prods

    def get_basic_context(self):
        return {
            'path': self.path,
            'products': self.separate_products(Products.objects.all()),
            'data_title': self.data_title,
            'product_form': self.product_form,
        }

    def get_parsed_datetime_string(self, string):
        return datetime_parser.parse(datetime.strptime(
            string, '%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.UTC).isoformat())

    # Getting all products
    def get(self, request):
        return Response(self.get_basic_context())

    # Create and update product
    def post(self, request):
        if 'pk' in request.POST:
            # Update product
            if request.POST['pk'] != 'create':
                try:
                    product = Products.objects.get(pk=request.POST['pk'])

                    product.image_url = request.POST['image_url']
                    product.name = request.POST['name']
                    product.price = request.POST['price']
                    product.creator = request.POST['creator']
                    product.create_date = self.get_parsed_datetime_string(request.POST['create_date'])

                    product.save()
                except Products.DoesNotExist:
                    pass
            # Create product
            else:
                Products.objects.create(
                    image_url=request.POST['image_url'],
                    name=request.POST['name'],
                    price=request.POST['price'],
                    creator=request.POST['creator'],
                    create_date=self.get_parsed_datetime_string(request.POST['create_date'])
                )
        
        return Response(self.get_basic_context())

    # Delete product
    def delete(self, request):
        try:
            Products.objects.get(pk=request.POST['pk']).delete()
        except Products.DoesNotExist:
            pass

        return Response(self.get_basic_context())
