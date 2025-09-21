from django.urls import path, re_path

from shop import views

app_name = "shop"

urlpatterns = [
	path('', views.home_page, name='home_page'),
	re_path(r'^product/(?P<slug>[-\w]+)/$', views.product_detail, name='product_detail'),
	path('add/favorites/<int:product_id>/', views.add_to_favorites, name='add_to_favorites'),
	path('remove/favorites/<int:product_id>/', views.remove_from_favorites, name='remove_from_favorites'),
	path('favorites/', views.favorites, name='favorites'),
	path('search/', views.search, name='search'),
	re_path(r'^filter/(?P<slug>[-\w]+)/$', views.filter_by_category, name='filter_by_category'),
	path('search-suggestions/', views.search_suggestions, name='search_suggestions'),
    
	re_path(r'^car-article/(?P<slug>[-\w]+)/$', views.car_article_detail, name='car_article_detail'),
	path('brand/<str:brand_slug>/articles/', views.car_brand_articles, name='car_brand_articles')
	]