from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render, redirect

urlpatterns = [
    path('', views.tshirts_view, name='home'),
    path('product/<str:name>/', views.product_detail_view, name='product_detail'),
    path('product/<str:name>/delete/', views.delete_product_view, name='delete_product'),
    path('add-product/', views.add_product, name='add_product'),
   
   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


