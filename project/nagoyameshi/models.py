from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model
User = get_user_model()
from django.core.validators import MinValueValidator,MaxValueValidator
from django.core.exceptions import ValidationError
from datetime import datetime

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

    postal_code_regex = RegexValidator(regex=r'^[0-9]{3}-[0-9]{4}$')
    postal_code = models.CharField(verbose_name='郵便番号', max_length=8, validators=[postal_code_regex])

    city = models.CharField(verbose_name='市区町村', max_length=50)
    street_address = models.CharField(verbose_name='番地以降住所', max_length=50)

    phone_number_regex = RegexValidator(regex=r'^[0-9]{10,11}$')
    phone_number = models.CharField(verbose_name='電話番号', max_length=11, validators=[phone_number_regex])

    regular_closing_day = models.ManyToManyField(Day, verbose_name='定休日')

    def __str__(self):
        return self.name
    
    def get_regular_closing_day(self):
        return "\n".join([day.name for day in self.regular_closing_day.all()])


# レビュー
MAX_STAR = 5
class Review(ExtendedModel):
    restaurant_id = models.ForeignKey(Restaurant, verbose_name='店舗', on_delete=models.CASCADE)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="ユーザー", on_delete=models.CASCADE)
    number_of_stars = models.PositiveIntegerField(verbose_name='星の数', validators=[MinValueValidator(1),MaxValueValidator(MAX_STAR)],default=1)
    comment = models.CharField(verbose_name='コメント', max_length=800)
    visited_date = models.DateField(verbose_name='利用日')

    def number_of_stars_str(self):
        '''
        星の数分の長さの文字列を返すメソッド
        '''
        true_star = self.number_of_stars * ' '
        false_star = (MAX_STAR - self.number_of_stars) * ' '
        return {'true_star': true_star, 'false_star': false_star}
    
    def clean(self):
        '''
        バリデーション
        '''
        super().clean()
        today = timezone.now().date()
        if self.visited_date > today:
            raise ValidationError("利用日には過去の日付を選択してください。")

# お気に入り
class Favorite(models.Model):
    class Meta:
        unique_together=("user_id","restaurant_id")

    restaurant_id = models.ForeignKey(Restaurant, verbose_name='店舗', on_delete=models.CASCADE)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="ユーザー", on_delete=models.CASCADE)


# 予約
class Reservation(ExtendedModel):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="ユーザー", on_delete=models.CASCADE)
    restaurant_id = models.ForeignKey(Restaurant, verbose_name='店舗', on_delete=models.CASCADE)
    reservation_datetime = models.DateTimeField(verbose_name='予約日時')
    number_of_persons = models.PositiveIntegerField(verbose_name='予約人数')
    comment = models.CharField(verbose_name='コメント', max_length=200, null=True, blank=True)

    def clean(self):
        '''
        バリデーション
        '''
        super().clean()

        restaurant = self.restaurant_id
        reservation_datetime = self.reservation_datetime.time()

        if self.reservation_datetime < timezone.now():
            raise ValidationError('予約日には未来の日付を選択してください。')

        if  not restaurant.opening_time <= reservation_datetime < restaurant.closing_time:
            raise ValidationError('予約時刻は営業時間内で指定してください。')



