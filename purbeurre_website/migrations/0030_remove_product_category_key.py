# Generated by Django 3.2.12 on 2022-06-21 16:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('purbeurre_website', '0029_alter_product_category_key'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='category_key',
        ),
    ]
