from django.contrib import admin
from .models import Substitute, Basket, Product, Category


# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_id', 'category_name', 'category_url')


class BasketAdmin(admin.ModelAdmin):
    list_display = ('substitute_id', 'substitute_name', 'substitute_nutriscore', 'substitute_image', 'substitute_url')


class SubstituteAdmin(admin.ModelAdmin):
    list_display = ('substitute_id', 'substitute_name', 'substitute_nutriscore', 'substitute_image', 'substitute_url')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('category_key', 'product_id', 'product_name', 'product_nutriscore', 'product_image', 'product_url')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Substitute, SubstituteAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Basket, BasketAdmin)
