from django.contrib import admin
from .models import Substitute, Basket

# Register your models here.


class BasketAdmin(admin.ModelAdmin):
    list_display = ('substitute_id', 'substitute_name', 'substitute_nutriscore', 'substitute_image', 'substitute_url')


class SubstituteAdmin(admin.ModelAdmin):
    list_display = ('substitute_id', 'substitute_name', 'substitute_nutriscore', 'substitute_image', 'substitute_url')


admin.site.register(Substitute, SubstituteAdmin)
admin.site.register(Basket, BasketAdmin)

