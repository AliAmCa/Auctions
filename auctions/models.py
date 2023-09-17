from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass




class Product(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=200, null = True)
    price = models.FloatField()
    date = models.DateField()
    image = models.CharField(max_length=64, default="")
    category = models.CharField(max_length=30, null = True)
    seller = models.ForeignKey(User, on_delete= models.CASCADE, related_name="productos" )
    def __str__(self) -> str:
        return f"{self.name} - Price: ${self.price}"


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE, related_name="bids" )
    product = models.ForeignKey(Product, on_delete= models.CASCADE, related_name="bids")
    bid = models.FloatField()
    date = models.DateField(null=True)
    def __str__(self) -> str:
        return f"{self.user.username} - Product: ${self.product.name} - Bid: ${self.bid}"


class Comments(models.Model):
    author = models.ForeignKey(User, on_delete= models.CASCADE, related_name="comments" )
    product = models.ForeignKey(Product, on_delete= models.CASCADE, related_name="comments")
    comment = models.TextField(max_length=200)

class WatchList(models.Model):
    owner = models.ForeignKey(User, on_delete= models.CASCADE, related_name="watchlist" )
    listings = models.ManyToManyField(Product, blank=True, related_name="listings")