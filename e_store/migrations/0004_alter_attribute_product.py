# Generated by Django 5.0.7 on 2024-08-10 18:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_store', '0003_comment_user_product_is_liked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attribute',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attributes', to='e_store.product'),
        ),
    ]
