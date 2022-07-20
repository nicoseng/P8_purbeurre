from django.contrib import admin
from .models import Category, Product


# Register your models here.
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('user_id',
#                     'username',
#                     )


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_id',
                    'category_name',
                    'category_url')


# class FavouriteAdmin(admin.ModelAdmin):
#     list_display = ('user_id',
#                     'product_id'
#                     )


class ProductAdmin(admin.ModelAdmin):
    list_display = ('category_id',
                    'product_id',
                    'product_name',
                    'product_nutriscore',
                    'product_image',
                    'product_ingredients',
                    'product_url')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
# admin.site.register(Favourite, FavouriteAdmin)
# admin.site.register(User, UserAdmin)
