from django.urls import path

from dashboard import views

app_name = 'dashboard'

urlpatterns = [
    path('products', views.products, name='products'),
    path('add-product/', views.add_product, name='add_product'),
]
