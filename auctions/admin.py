from django.contrib import admin
from .models import Product, Bid, Comments, WatchList, User
# Register your models here.

admin.site.register(User)
admin.site.register(Product)
admin.site.register(Bid)
admin.site.register(Comments)
admin.site.register(WatchList)
