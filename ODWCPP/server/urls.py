
from django.urls import path
from . import views

app_name = 'server'

urlpatterns = [
    # path('', views.index, name='index'),
    path(r'^startprocessing/', views.start_processing, name='start_processing'),
    path(r'^showprogress', views.show_progress, name='show_progress'),
    path(r'^download/', views.file_download, name='file_download'),
    path('encode/result/', views.encoderesult_index, name = 'encoderesult_index'),
    path('encode/', views.encodeindex, name='encodeindex'),
    path('decode/result/', views.decoderesult_index, name='decoderesult_index'),
    path('decode/', views.decodeindex, name='decodeindex'),
    path('team/', views.teamindex, name='teamindex'),
    path('error/', views.errorindex, name='errorindex'),
]