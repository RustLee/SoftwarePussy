from django.urls import path, include
from . import views

app_name = 'login'
urlpatterns = [
    path('', views.index),
    path('index/', views.index, name='index'),
    path('login/', views.login),
    path('register/', views.register),
    path('logout/', views.logout),
    path('confirm/', views.user_confirm),
    #path('captcha/', include('captcha.urls')),
]