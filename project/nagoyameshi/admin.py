from django.contrib import admin
from .models import ExtendedModel, Category, Day, Restaurant

admin.site.register(ExtendedModel)
admin.site.register(Day)

# カテゴリー
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'deleted_at', 'updated_at', 'created_at')

admin.site.register(Category, CategoryAdmin)

# 店舗
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_id', 'description', 'floor_price', 'maximum_price', 'opening_time',
                    'closing_time', 'postal_code', 'city', 'street_address', 'phone_number', 'get_regular_closing_day')
    search_fields = ('name', )
    list_filter = ('category_id', )

    def get_regular_closing_day(self, obj):
        return "\n".join([day.name for day in obj.regular_closing_day.all()])

admin.site.register(Restaurant, RestaurantAdmin)