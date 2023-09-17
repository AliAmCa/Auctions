from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Product, User, WatchList, Bid, Comments
from .forms  import NewProductForm



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
    message = ''
    try:
        user =  User.objects.get(username= request.user)
        # Taking listing info
        listing = Product.objects.get(pk= listing_id)

        # Is the listing included in user's watchlist?
        try:
            watchlist = WatchList.objects.get(owner = user)
            item_in_watchlist = watchlist.listings.filter(pk= listing.pk)
        except:
            watchlist = None
            item_in_watchlist= None
    except Exception as e:
        message = e
        return render(request,"auctions/listingPage.html",{
                "message": message
            })

    # Taking bids info
    bids = Bid.objects.filter(product= listing)

    if request.method == 'GET':
        
        return render(request,"auctions/listingPage.html",{
            "listing": listing,
            "item_in_watchlist": item_in_watchlist,
            "item_bids": bids,
            "message": message

        } )
    else:
        if request.POST['addToWatchlist']:
            if watchlist:
                watchlist.listings.add(listing) 
            else:
                watchlist = WatchList(owner= user)
                watchlist.save()
                watchlist.listings.add(listing)
                watchlist.save()

            return render(request,"auctions/listingPage.html",{
                "listing": listing,
                "item_in_watchlist": True,
                "item_bids": bids,
                "message": message

                } )
        if request.POST['removeFWatchlist']:
            watchlist.listings.remove(listing)
            return render(request,"auctions/listingPage.html",{
                "listing": listing,
                "item_in_watchlist": False,
                "item_bids": bids,
                "message": message

                } )


