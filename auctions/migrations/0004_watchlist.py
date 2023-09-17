# Generated by Django 4.2.5 on 2023-09-17 09:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_delete_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='WatchList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('listings', models.ManyToManyField(blank=True, related_name='listings', to='auctions.product')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watchlist', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
