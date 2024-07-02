from django.urls import path
from . import views

app_name = 'nagoyameshi'
urlpatterns = [
    path('', views.index, name='index'),
    path('top/', views.top, name='top'),
    path('restaurant/<int:pk>', views.restaurant_detail, name='restaurant_detail'),
    path('restaurant/review_list/<int:pk>', views.review_list, name='review_list'),
    path('restaurant/review_form/<int:pk>', views.review_form, name='review_form'),
    path('mypage/', views.mypage, name='mypage'),
]