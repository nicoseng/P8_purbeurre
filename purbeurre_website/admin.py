from django.contrib import admin
from .models import Substitute, Basket, Product, Category


# Register your models here.
# class CustomerAdmin(admin.ModelAdmin):
#     list_display = ('customer_id',
#                     'name',
#                     'user')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_id',
                    'category_name',
                    'category_url')


class BasketAdmin(admin.ModelAdmin):
    list_display = ('category_key',
                    'substitute_id',
                    'substitute_name',
                    'substitute_nutriscore',
                    'substitute_image',
                    'substitute_ingredients',
                    'substitute_url'
                    )


class SubstituteAdmin(admin.ModelAdmin):
    list_display = ('category_key',
                    'substitute_id',
                    'substitute_name',
                    'substitute_nutriscore',
                    'substitute_image',
                    'substitute_ingredients',
                    'substitute_url')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('category_key',
                    'product_id',
                    'product_name',
                    'product_nutriscore',
                    'product_image',
                    'product_ingredients',
                    'product_url')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Substitute, SubstituteAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Basket, BasketAdmin)
# admin.site.register(Customer, CustomerAdmin)
