from django.urls import path
from . import views


urlpatterns = [
    path('', views.main_page, name='main'),

    path('products/', views.ProductsList.as_view(), name='products'),

    path('create-product/', views.CreateProduct.as_view(), name='create_product'),

    path('update-product/', views.redirect_to_update, name='redirect_to_update'),
    path('update-product/<int:pk>', views.UpdateProduct.as_view(), name='update_product'),

    path('delete-product/', views.redirect_to_delete, name='redirect_to_delete'),
    path('delete-product/<int:pk>', views.DeleteProduct.as_view(), name='delete_product')
]
