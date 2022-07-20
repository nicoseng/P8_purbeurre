from django.contrib.auth.models import User
from django.db import models


# Create your models here.

# class User(models.Model):
#     class Meta:
#         ordering = ['user_id']
#
#     user_id = models.IntegerField(primary_key=True)
#     username = models.CharField(max_length=100, default=None)


class Category(models.Model):
    class Meta:
        ordering = ['category_id']

    category_id = models.IntegerField(primary_key=True)
    category_name = models.fields.CharField(max_length=100, null=True)
    category_url = models.fields.CharField(max_length=100, null=True)


class Product(models.Model):
    class Meta:
        ordering = ['product_id']

    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    product_id = models.IntegerField(primary_key=True)
    product_name = models.fields.CharField(max_length=100, null=True)
    product_image = models.fields.CharField(max_length=100, null=True)
    product_url = models.fields.CharField(max_length=100, null=True)
    product_ingredients = models.fields.CharField(max_length=500, null=True)
    product_nutriscore = models.fields.CharField(max_length=100)


# class Favourite(models.Model):
#
#     class Meta:
#         ordering = ['product_id']
#
#     user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
#     product_id = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)





