from django.urls import path
from . import views

urlpatterns = [
    path('menu/', views.menu, name='menu'),
    path('orders/', views.order_summary, name='orders'),
]
