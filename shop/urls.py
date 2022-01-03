from django.urls import path

from shop import views

urlpatterns = [
	path('', views.home_page, name='home_page')
]