from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from . import models, forms
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib import messages

# index
class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'nagoyameshi/index.html')

index = IndexView.as_view()

# top
class TopView(LoginRequiredMixin, View):
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
        if selected_category:
            query &= Q(category_id=selected_category)

        # 条件に合致する店舗を検索
        restaurants = models.Restaurant.objects.filter(query)
        
        context = {'restaurants': restaurants}
        return render(request, 'nagoyameshi/top.html', context)
    
top = TopView.as_view()

# 店舗詳細
class RestaurantDetailView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        restaurant = models.Restaurant.objects.get(pk=pk)
        favorite = models.Favorite.objects.filter(user_id=request.user, restaurant_id=restaurant).exists()
        context = {'restaurant': restaurant, 'favorite':favorite}

        return render(request, 'nagoyameshi/restaurant_detail.html', context)
    
    def post(self, request, pk, *args, **kwargs):
        '''
        お気に入り登録の処理
        '''
        restaurant = models.Restaurant.objects.get(pk=pk)
        query = Q()
        query &= Q(user_id = request.user)
        query &= Q(restaurant_id = models.Restaurant.objects.get(pk=pk))
        favorite = models.Favorite.objects.filter(query)

        if favorite:
            # 登録されていれば削除し、お気に入り登録を解除
            favorite.delete()
            messages.info(request, 'お気に入り登録を解除しました')
        else:
            # 登録されていなければ、お気に入り登録する
            new_favorite = models.Favorite()
            new_favorite.restaurant_id = models.Restaurant.objects.get(pk=pk)
            new_favorite.user_id = request.user
            new_favorite.save()
            messages.info(request, 'お気に入りに登録しました')

        favorite = models.Favorite.objects.filter(user_id=request.user, restaurant_id=restaurant).exists()
        context = {'restaurant': restaurant, 'favorite':favorite}
        
        return render(request, 'nagoyameshi/restaurant_detail.html', context)

restaurant_detail = RestaurantDetailView.as_view()

# 店舗ごとのレビュー一覧
class ReviewListView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        restaurant = models.Restaurant.objects.get(pk=pk)
        review_list = models.Review.objects.filter(restaurant_id=pk)
        context = {'restaurant':restaurant, 'review_list': review_list}
        return render(request, 'nagoyameshi/review_list.html', context)

review_list = ReviewListView.as_view()


# レビューフォーム
class ReviewFormView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        form = forms.ReviewForm()
        restaurant = models.Restaurant.objects.get(pk=pk)
        context = {'restaurant':restaurant, 'form': form}
        return render(request, 'nagoyameshi/review_form.html', context)
    
    def post(self, request, pk, *args, **kwargs):
        '''
        レビューの投稿処理
        '''
        copied = request.POST.copy()
        copied['restaurant_id'] = models.Restaurant.objects.get(pk=pk)
        copied['user_id'] = request.user

        form = forms.ReviewForm(copied)

        print('======form======')
        print(form)

        if form.is_valid():
            print('投稿完了')
            form.save()
            messages.success(request, 'レビューを投稿しました')
            return redirect('nagoyameshi:review_list', pk=pk)
        else:
            print(form.errors)
            restaurant = models.Restaurant.objects.get(pk=pk)
            context = {'restaurant':restaurant, 'form': form}
            messages.warning(request, '投稿に失敗しました')
            return render(request, 'nagoyameshi/review_form.html', context)

review_form = ReviewFormView.as_view()


# マイページ
class MypageView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        favorites = models.Favorite.objects.filter(user_id=request.user)
        context = {'favorites': favorites}
        return render(request, 'nagoyameshi/mypage.html', context)

mypage = MypageView.as_view()