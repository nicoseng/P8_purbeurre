# Generated by Django 3.2.12 on 2022-07-11 14:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('purbeurre_website', '0037_auto_20220711_1434'),
    ]

    operations = [
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('substitute_id', models.IntegerField(primary_key=True, serialize=False)),
                ('substitute_name', models.CharField(max_length=100, null=True)),
                ('substitute_image', models.CharField(max_length=100, null=True)),
                ('substitute_url', models.CharField(max_length=100, null=True)),
                ('substitute_ingredients', models.CharField(max_length=500, null=True)),
                ('substitute_nutriscore', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['substitute_id'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('category_id', models.IntegerField(primary_key=True, serialize=False)),
                ('category_name', models.CharField(max_length=100, null=True)),
                ('category_url', models.CharField(max_length=100, null=True)),
            ],
            options={
                'ordering': ['category_id'],
            },
        ),
        migrations.CreateModel(
            name='Substitute',
            fields=[
                ('substitute_id', models.IntegerField(primary_key=True, serialize=False)),
                ('substitute_name', models.CharField(max_length=100, null=True)),
                ('substitute_image', models.CharField(max_length=100, null=True)),
                ('substitute_url', models.CharField(max_length=100, null=True)),
                ('substitute_ingredients', models.CharField(max_length=500, null=True)),
                ('substitute_nutriscore', models.CharField(max_length=100)),
                ('category_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purbeurre_website.category')),
            ],
            options={
                'ordering': ['substitute_id'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('product_id', models.IntegerField(primary_key=True, serialize=False)),
                ('product_name', models.CharField(max_length=100, null=True)),
                ('product_image', models.CharField(max_length=100, null=True)),
                ('product_url', models.CharField(max_length=100, null=True)),
                ('product_ingredients', models.CharField(max_length=500, null=True)),
                ('product_nutriscore', models.CharField(max_length=100)),
                ('category_key', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='purbeurre_website.category')),
            ],
            options={
                'ordering': ['product_id'],
            },
        ),
    ]
