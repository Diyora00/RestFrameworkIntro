# Generated by Django 5.0.7 on 2024-08-03 16:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AttributeKey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key_name', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AttributeValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value_name', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('slug', models.SlugField(blank=True, max_length=250, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('slug', models.SlugField(blank=True, max_length=250, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groups', to='e_store.category')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('slug', models.SlugField(blank=True, max_length=250, unique=True)),
                ('price', models.FloatField()),
                ('description', models.TextField()),
                ('discount', models.PositiveIntegerField(default=0)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='e_store.group')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('is_primary', models.BooleanField(default=False)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='e_store.product')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveIntegerField(blank=True, choices=[(0, 'Zero'), (1, 'One'), (2, 'Two'), (3, 'Three'), (4, 'Four'), (5, 'Five')], default=0, null=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='')),
                ('message', models.TextField(blank=True, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='e_store.product')),
            ],
        ),
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='e_store.attributekey')),
                ('value', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='e_store.attributevalue')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='e_store.product')),
            ],
        ),
    ]
