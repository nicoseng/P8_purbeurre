from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.fields.CharField(max_length=100, null=True)
    category = models.ManyToManyField(Category)
    nutriscore = models.fields.CharField(max_length=100)

    def __str__(self):
        return self.name



