from django.contrib import admin
from .models import Product, Bid, Comments
# Register your models here.

admin.site.register(Product)
admin.site.register(Bid)
admin.site.register(Comments)
