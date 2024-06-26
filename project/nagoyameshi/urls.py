from django.urls import path
from . import views

app_name = 'nagoyameshi'
urlpatterns = [
    path('', views.index, name='index'),
    path('top/', views.top, name='top'),
    path('restaurant/<int:pk>', views.restaurant_detail, name='restaurant_detail'),
]