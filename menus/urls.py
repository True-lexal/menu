from django.urls import path
from .views import index

urlpatterns = [
    path('', index, name='index'),
    path('<slug:slug>', index, name='menu'),
]
