from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create_account/', views.create_account, name='create_account'),
    path('access_login/', views.access_login, name='login'),
    path('display_user_account/', views.display_user_account, name='display_user_account'),
    path('logout/', views.logout_user, name='logout'),
    path('display_product_data/', views.display_product_data, name='display_product_data'),
    path('display_favourite/', views.display_favourite, name='display_favourite'),
    path('display_substitute_data/', views.display_substitute_data, name='display_substitute_data'),
    path('display_searched_results/', views.display_searched_results, name='display_searched_results'),
    path('display_proposed_substitute/', views.display_proposed_substitute, name='display_proposed_substitute'),
    path('delete_product/', views.delete_product, name='delete_product'),
    path('admin/', admin.site.urls),
]
