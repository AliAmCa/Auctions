# Generated by Django 4.2.5 on 2023-09-20 16:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_category_alter_comments_date_alter_product_category_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='category2',
        ),
        migrations.AlterField(
            model_name='comments',
            name='date',
            field=models.DateField(default=datetime.datetime(2023, 9, 20, 16, 21, 23, 330579)),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
