from django.urls import path

from orders import views

app_name = "orders"

urlpatterns = [
    path('create', views.create_order, name='create_order'),
    path('list', views.user_orders, name='user_orders'),
    path('checkout/<int:order_id>', views.checkout, name='checkout'),
    path('fake-payment/<int:order_id>', views.fake_payment, name='pay_order')
]