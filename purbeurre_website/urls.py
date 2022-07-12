from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create_account/', views.create_account, name='create_account'),
    path('access_login/', views.access_login, name='login'),
    path('check_my_account/', views.check_my_account, name='check_my_account'),
    path('logout/', views.logout_user, name='logout'),
    path('check_product/', views.check_product, name='check_product'),
    path('display_my_basket/', views.display_my_basket, name='display_my_basket'),
    path('check_substitute/', views.check_substitute, name='check_substitute'),
    path('display_results/', views.display_results, name='display_results'),
    path('display_substitute/', views.display_substitute, name='display_substitute'),
    # path('add_product/', views.add_product, name='add_product'),
    path('admin/', admin.site.urls),
]
