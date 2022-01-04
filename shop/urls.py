from django.urls import path

from shop import views

app_name = "shop"

urlpatterns = [
	path('', views.home_page, name='home_page')
]