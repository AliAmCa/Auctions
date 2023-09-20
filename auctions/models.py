from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class User(AbstractUser):
    
    def getWatchlist(self):

        try:
            watchlist = self.watchlist.all().first()
            return watchlist.listings.all()
        except:
            return []

class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self) -> str:
        return f"{self.name}"


class Product(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=200, null = True)
    price = models.FloatField()
    date = models.DateField()
    image = models.CharField(max_length=64, default="", blank=True, null= True)
    category = models.ForeignKey(Category, on_delete= models.CASCADE, related_name="products", blank=True, null=True)
    seller = models.ForeignKey(User, on_delete= models.CASCADE, related_name="sales" )
    active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete= models.CASCADE, related_name="purchases", null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.name} - Price: ${self.price}"
    
    def mayorBid(self):
        
        bids = self.bids.all().order_by('-bid')
        if bids:
                return bids[0]
        else: return []
    
    def deactivate(self):
        self.active = False
        self.save()

    def closeAuction(self):
        mayor_bid = self.mayorBid()
        if mayor_bid:
            self.winner = mayor_bid.user
            self.save()
        self.deactivate()

    def getComments(self):
        return self.comments.all()


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE, related_name="bids" )
    product = models.ForeignKey(Product, on_delete= models.CASCADE, related_name="bids")
    bid = models.FloatField()
    date = models.DateField(null=True)
    def __str__(self) -> str:
        return f"{self.user.username} - Product: ${self.product.name} - Bid: ${self.bid}"
    
    def daysSinceBid(self):
        return datetime.today() - self.date



class Comments(models.Model):
    author = models.ForeignKey(User, on_delete= models.CASCADE, related_name="comments" )
    product = models.ForeignKey(Product, on_delete= models.CASCADE, related_name="comments")
    comment = models.TextField(max_length=200)
    date = models.DateField(blank= True)

class WatchList(models.Model):
    owner = models.ForeignKey(User, on_delete= models.CASCADE, related_name="watchlist" )
    listings = models.ManyToManyField(Product, blank=True, related_name="watchlist")
        
    def __str__(self) -> str:
        return f"{self.owner.username} - Products: {len(self.listings.all())}"
    
    
        
