from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model
User = get_user_model()
from django.core.validators import MinValueValidator,MaxValueValidator

# models.Modelを継承した汎用クラス
class ExtendedModel(models.Model):
    deleted_at = models.DateTimeField(verbose_name='論理削除日', auto_now=True, blank=True, null=True)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True, blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)

# カテゴリー
class Category(ExtendedModel):
    name = models.CharField(verbose_name='カテゴリ名', max_length=15)

    def __str__(self):
        return self.name

# 曜日
class Day(models.Model):
    name = models.CharField(verbose_name='曜日', max_length=10)

    def __str__(self):
        return self.name
    

# 店舗
class Restaurant(ExtendedModel):
    name = models.CharField(verbose_name='店舗名', max_length=30)
    category_id = models.ForeignKey(Category, verbose_name='カテゴリー', on_delete=models.PROTECT)
    description = models.CharField(verbose_name='店舗説明', max_length=500)
    floor_price = models.PositiveIntegerField(verbose_name='下限価格')
    maximum_price = models.PositiveIntegerField(verbose_name='上限価格')
    opening_time = models.TimeField(verbose_name='開店時刻')
    closing_time = models.TimeField(verbose_name='閉店時刻')
    postal_code = models.CharField(verbose_name='郵便番号', max_length=8)
    city = models.CharField(verbose_name='市区町村', max_length=50)
    street_address = models.CharField(verbose_name='番地以降住所', max_length=50)
    phone_number = models.CharField(verbose_name='電話番号', max_length=11)
    regular_closing_day = models.ManyToManyField(Day, verbose_name='定休日')

    def __str__(self):
        return self.name
    
    def get_regular_closing_day(self):
        return "\n".join([day.name for day in self.regular_closing_day.all()])


# レビュー
MAX_STAR = 5
class Review(ExtendedModel):
    restaurant_id = models.ForeignKey(Restaurant, verbose_name='店舗', on_delete=models.CASCADE)
    #user_id = models.ForeignKey(User, verbose_name='投稿者', on_delete=models.CASCADE)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="ユーザー", on_delete=models.CASCADE)
    number_of_stars = models.PositiveIntegerField(verbose_name='星の数', validators=[MinValueValidator(1),MaxValueValidator(MAX_STAR)],default=1)
    comment = models.CharField(verbose_name='コメント', max_length=800)
    visited_date = models.DateField(verbose_name='利用日')

