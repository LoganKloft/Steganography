from django.urls import path
from . import views

app_name = 'app'
urlpatterns = [
    path('', views.index, name='index'),
    path('log', views.log, name='log'),
    path('encode', views.encode, name='encode')
]