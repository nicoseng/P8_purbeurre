# Generated by Django 3.2.12 on 2022-06-30 21:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('purbeurre_website', '0033_alter_product_category_key'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='substitute',
            name='reference_product_key',
        ),
    ]
