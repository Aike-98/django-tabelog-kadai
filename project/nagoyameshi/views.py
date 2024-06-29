from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from . import models, forms
from django.contrib.auth import get_user_model
User = get_user_model()

# index
class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'nagoyameshi/index.html')

index = IndexView.as_view()

# top
class TopView(View):
    def get(self, request, *args, **kwargs):

        # クエリビルダを生成
        query = Q()

        # リクエストから検索条件を取得
        keyword = request.GET.get('keyword')
        selected_category = request.GET.get('category')

        # 検索キーワードがある場合、検索条件を追加
        if keyword:

            words = keyword.replace('　', ' ').split()

            for word in words:
                if word == '':
                    continue
                query &= Q(name__icontains=word)

        # カテゴリが指定されている場合、検索条件に追加
        if selected_category != '':
            query &= Q(category_id=selected_category)

        # 条件に合致する店舗を検索
        restaurants = models.Restaurant.objects.filter(query)
        
        context = {'restaurants': restaurants}
        return render(request, 'nagoyameshi/top.html', context)
    
top = TopView.as_view()

# 店舗詳細
class RestaurantDetailView(View):
    def get(self, request, pk, *args, **kwargs):
        restaurant = models.Restaurant.objects.get(pk=pk)
        context = {'restaurant': restaurant}
        return render(request, 'nagoyameshi/restaurant_detail.html', context)

restaurant_detail = RestaurantDetailView.as_view()

# 店舗ごとのレビュー一覧
class ReviewListView(View):
    def get(self, request, pk, *args, **kwargs):
        restaurant = models.Restaurant.objects.get(pk=pk)
        review_list = models.Review.objects.filter(restaurant_id=pk)
        context = {'restaurant':restaurant, 'review_list': review_list}
        return render(request, 'nagoyameshi/review_list.html', context)

review_list = ReviewListView.as_view()


# レビューフォーム
class ReviewFormView(View):
    def get(self, request, pk, *args, **kwargs):
        form = forms.ReviewForm()
        restaurant = models.Restaurant.objects.get(pk=pk)
        context = {'restaurant':restaurant, 'form': form}
        return render(request, 'nagoyameshi/review_form.html', context)
    
    def post(self, request, pk, *args, **kwargs):
        form = forms.ReviewForm(request.POST)
        if form.is_valid():
            review = models.Review()
            review.user_id = User.username
            review.restaurant_id = pk
            review.number_of_stars = form.cleaned_data['number_of_stars']
            review.comment = form.cleaned_data['comment']
            review.visited_date = form.cleaned_data['visited_date']
            review.save()
            return redirect('nagoyameshi:review_list', pk=pk)
        else:
            print('バリデーションエラー')
            restaurant = models.Restaurant.objects.get(pk=pk)
            context = {'restaurant':restaurant, 'form': form}
            return render(request, 'nagoyameshi/review_form.html', context)

review_form = ReviewFormView.as_view()
