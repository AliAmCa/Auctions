# Generated by Django 4.2.5 on 2023-09-23 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_category_alter_comments_date_alter_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.URLField(blank=True, default='', null=True),
        ),
    ]