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
        "products": Product.objects.filter(active = True)
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
        is_owner = False
        # Is user the seller?
        if user.pk == listing.seller.pk:
            is_owner = True

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
    
    bids = Bid.objects.filter(product= listing).order_by('-bid')
    mayor_bid = listing.price
    if bids:
        mayor_bid = bids[0].bid

    if request.method == 'GET':
        
        return render(request,"auctions/listingPage.html",{
            "listing": listing,
            "item_in_watchlist": item_in_watchlist,
            "mayor_bid": mayor_bid+0.1, 
            "item_bids": bids,
            "is_owner": is_owner,
            "message": message

        } )
    else:
        if 'addToWatchlist' in request.POST:
            if watchlist:
                watchlist.listings.add(listing) 
            else:
                watchlist = WatchList(owner= user)
                watchlist.save()
                watchlist.listings.add(listing)
                watchlist.save()
            return HttpResponseRedirect(reverse("listing", args=[listing_id]))
            
        if 'removeFWatchlist' in request.POST:
            watchlist.listings.remove(listing)
            return HttpResponseRedirect(reverse("listing", args=[listing_id]))
        
        if 'closeAuction' in request.POST:
            # Closing auction
            # make the highest bidder the winner of the auction 
            # makes the listing no longer active
            listing.closeAuction()
            return HttpResponseRedirect(reverse("index"))

            
        
def newBid (request, listing_id):
    if request.method == 'POST':
        try:
            user =  User.objects.get(username= request.user)
            # Taking listing info
            listing = Product.objects.get(pk= listing_id)
        
            bidAmount = float(request.POST["bidAmount"])
            isvalid = False
            mayor_bid = listing.mayorBid()
            if mayor_bid and bidAmount > mayor_bid or bidAmount > listing.price:
                isvalid= True
            if isvalid:
                # Create nuevo bid
                newBid = Bid(user= user, product = listing, bid = bidAmount, date= datetime.now())
                newBid.save()
                return HttpResponseRedirect(reverse("listing", args=listing_id))
            
            
        except Exception as e:
            return HttpResponseRedirect(reverse("listing", args=[listing_id]))

