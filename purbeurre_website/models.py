from django.db import models


# Create your models here.

class Category(models.Model):
    class Meta:
        ordering = ['category_id']

    category_id = models.IntegerField(primary_key=True)
    category_name = models.fields.CharField(max_length=100, null=True)
    category_url = models.fields.CharField(max_length=100, null=True)


class Product(models.Model):
    class Meta:
        ordering = ['product_id']

    #category_key = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_id = models.IntegerField(primary_key=True)
    product_name = models.fields.CharField(max_length=100, null=True)
    product_image = models.fields.CharField(max_length=100, null=True)
    product_url = models.fields.CharField(max_length=100, null=True)
    product_nutriscore = models.fields.CharField(max_length=100)


class Basket(models.Model):
    class Meta:
        ordering = ['substitute_id']

    # foreign_key = models.ForeignKey(Substitute, on_delete=models.CASCADE)
    substitute_id = models.IntegerField(primary_key=True)
    substitute_name = models.fields.CharField(max_length=100, null=True)
    substitute_image = models.fields.CharField(max_length=100, null=True)
    substitute_url = models.fields.CharField(max_length=100, null=True)
    substitute_nutriscore = models.fields.CharField(max_length=100)


class Substitute(models.Model):
    class Meta:
        ordering = ['substitute_id']

    reference_product_key = models.ForeignKey(Product, on_delete=models.CASCADE)
    substitute_id = models.IntegerField(primary_key=True)
    substitute_name = models.fields.CharField(max_length=100, null=True)
    substitute_image = models.fields.CharField(max_length=100, null=True)
    substitute_url = models.fields.CharField(max_length=100, null=True)
    substitute_nutriscore = models.fields.CharField(max_length=100)
