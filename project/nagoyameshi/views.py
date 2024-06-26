from django.shortcuts import render
from django.views import View
from . import models

# index
class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'nagoyameshi/index.html')

index = IndexView.as_view()

# top
class TopView(View):
    def get(self, request, *args, **kwargs):

        keyword = request.GET.get('keyword')
        if keyword:
            # 検索キーワードがある場合、店名にキーワードが含まれる店舗を抽出して返却する
            restaurants = models.Restaurant.objects.filter(name__icontains=keyword)
        else:
            # 検索キーワードがない場合、全件を返却する
            restaurants = models.Restaurant.objects.all()

        categories = models.Category.objects.all()
        
        context = {'restaurants': restaurants, 'categories':categories}
        return render(request, 'nagoyameshi/top.html', context)
    
top = TopView.as_view()

# 店舗詳細
class RestaurantDetailView(View):
    def get(self, request, pk, *args, **kwargs):
        restaurant = models.Restaurant.objects.get(pk=pk)
        context = {'restaurant': restaurant}
        return render(request, 'nagoyameshi/restaurant_detail.html', context)

restaurant_detail = RestaurantDetailView.as_view()
