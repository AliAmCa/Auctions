from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=64)

class Product(models.Model):
    name = models.CharField(max_length=64)
    price = models.FloatField()
    date = models.DateField()
    image = models.CharField(max_length=64, default="")
    category = models.ForeignKey(Category, on_delete= models.CASCADE, related_name="productos", null=True)
    seller = models.ForeignKey(User, on_delete= models.CASCADE, related_name="productos" )
    def __str__(self) -> str:
        return f"{self.name} - Price: ${self.price}"


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE, related_name="bids" )
    product = models.ForeignKey(Product, on_delete= models.CASCADE, related_name="bids")
    bid = models.FloatField()
    def __str__(self) -> str:
        return f"{self.user.username} - Product: ${self.product.name} - Bid: ${self.bid}"


class Comments(models.Model):
    author = models.ForeignKey(User, on_delete= models.CASCADE, related_name="comments" )
    product = models.ForeignKey(Product, on_delete= models.CASCADE, related_name="comments")
    comment = models.TextField(max_length=200)