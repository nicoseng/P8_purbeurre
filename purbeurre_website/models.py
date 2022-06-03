from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


class Substitute(models.Model):
    #id = models.IntegerField(primary_key=True)
    substitute_name = models.fields.CharField(max_length=100, null=True)
    #substitute_category = models.ManyToManyField(Category)
    substitute_nutriscore = models.fields.CharField(max_length=100)

    def __str__(self):
        return self.substitute_name
