from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from accounts import views


app_name = 'accounts'

urlpatterns = [
    path('register/', views.user_register, name='user_register'),
    path('login/', views.user_login, name='user_login'),
    path('login/manager/', views.manager_login, name='manager_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('profile/edit', views.edit_profile, name='edit_profile'),
    path('signup/', views.signup, name='signup'),
    path('verify-code/', views.verify_code, name='verify_code'),
    path('set_password/', views.set_password, name='set_password'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('verify_reset_code/', views.verify_reset_code, name='verify_reset_code'),
    path('set_new_password/', views.set_new_password, name='set_new_password'),

]

