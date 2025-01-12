from django.urls import path
from . import views

urlpatterns = [
    path('', views.fruits_view, name='fruits'),
    path('product/<str:name>/', views.product_detail_view, name='product_detail'),
    path('product/<str:name>/delete/', views.delete_product_view, name='delete_product'),
    path('add-product/', views.add_product, name='add_product'),
]


