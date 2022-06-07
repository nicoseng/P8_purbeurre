from django.db import models


# Create your models here.

class Substitute(models.Model):
    class Meta:
        ordering = ['substitute_id']

    substitute_id = models.IntegerField(primary_key=True)
    substitute_name = models.fields.CharField(max_length=100, null=True)
    substitute_image = models.fields.CharField(max_length=100, null=True)
    substitute_url = models.fields.CharField(max_length=100, null=True)
    substitute_nutriscore = models.fields.CharField(max_length=100)


class Basket(models.Model):
    class Meta:
        ordering = ['substitute_id']

    substitute_id = models.IntegerField(primary_key=True)
    substitute_name = models.fields.CharField(max_length=100, null=True)
    substitute_image = models.fields.CharField(max_length=100, null=True)
    substitute_url = models.fields.CharField(max_length=100, null=True)
    substitute_nutriscore = models.fields.CharField(max_length=100)
