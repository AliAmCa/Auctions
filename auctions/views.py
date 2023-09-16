from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Product
from .forms  import NewProductForm

from .models import User


def index(request):
    return render(request, "auctions/index.html", {
        "products": Product.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    
@login_required
def newProduct(request):
    if request.method == 'POST':
        newProductForm = NewProductForm()

        try:
            title = request.POST['title']
            description = request.POST['description']
            startBid = float(request.POST['initialPrice'])
            image = request.POST['image']
            category = request.POST['category']
            seller = User.objects.get(username= request.user)
            today = datetime.now()
            product = Product(name= title, description= description, 
                    price= startBid, image = image, category= category,
                    seller = seller, date = today)
            product.save()
            return HttpResponseRedirect(reverse("index"))
        except Exception as e:
            print(e)
            return render(request, "auctions/createListing.html",{
            'new_product_form': newProductForm
        })
    else:
        newProductForm = NewProductForm()
        return render(request, "auctions/createListing.html",{
            'new_product_form': newProductForm
        })
    
def showListing(request, listing_id):
    listing = Product.objects.get(pk= listing_id)
    
    return render(request,"auctions/listingPage.html",{
        "listing": listing
    } )
    

