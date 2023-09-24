from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Product, User, WatchList, Bid, Comments, Category
from .forms  import NewProductForm, categories



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
            category = Category.objects.get(pk= int(request.POST['category']))
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
    
def showListing(request, listing_id,  message ):
    if message== 'None':
        message= ""
    item_in_watchlist= None
    user_is_winner = False
    is_owner = False
    comments = []
    bids_number = 0
    current_bid = None

    try:
         # Taking listing info
        listing = Product.objects.get(pk= listing_id)
        comments = listing.getComments()

        try:
            user =  User.objects.get(username= request.user)
            
             # Is user the seller?
            if user.pk == listing.seller.pk:
                is_owner = True

            # Is the listing included in user's watchlist?
            try:
                watchlist = WatchList.objects.get(owner = user)
                item_in_watchlist = watchlist.listings.filter(pk= listing.pk)
            except:
                watchlist = None
        except:
            user = None
        
        # IF Listing is ACTIVE 
        if listing.active:
            # Taking bids info
            bids = Bid.objects.filter(product= listing).order_by('-bid')
            
            if bids:
                bids_number= len(bids)
                current_bid = bids[0]
        else:
            bids = []
            # user is winner?
            if user and listing.winner and user.id == listing.winner.id:
                user_is_winner= True

    except Exception as e:
        print(e)
        return render(request,"auctions/listingPage.html",{
                "message": "There is a problem with database, try again i a few minutes"
            })


    if request.method == 'GET':
        
        return render(request,"auctions/listingPage.html",{
            "listing": listing,
            "item_in_watchlist": item_in_watchlist,
            "bids_number": bids_number, 
            "current_bid": current_bid,
            "is_owner": is_owner,
            "user_winner": user_is_winner,
            "comments": comments,
            "message": message

        } )
    

def listingActions(request, listing_id):
    if request.method == 'POST':
        try:
            # User info
            user =  User.objects.get(username= request.user)
            # Taking listing info
            listing = Product.objects.get(pk= listing_id)
            try:
                watchlist = WatchList.objects.get(owner = user)
            except:
                watchlist = None
        except:
            message = 'Ups! Something happened. Try again in a few minutes!'

        if 'addToWatchlist' in request.POST: # Add the listing to user´s watchlist
            message = 'Listing added to Watchlist'

            if watchlist:
                watchlist.listings.add(listing) 
            else:
                watchlist = WatchList(owner= user)
                watchlist.save()
                watchlist.listings.add(listing)
                watchlist.save()
            
        if 'removeFWatchlist' in request.POST: # Remove listing from user´s watchlist
            message = 'Listing removed from Watchlist'
            watchlist.listings.remove(listing)
        
        if 'closeAuction' in request.POST:  # Closing auction
            message = "Auction closed"
            # make the highest bidder the winner of the auction 
            # makes the listing no longer active
            listing.closeAuction()
        return HttpResponseRedirect(reverse("listing", args=[listing_id, message]))

            
        
def newBid (request, listing_id):
    isvalid = False
    if request.method == 'POST':
        try:
            user =  User.objects.get(username= request.user)
            # Taking listing info
            listing = Product.objects.get(pk= listing_id)
            try:
                bidAmount = float(request.POST["bidAmount"])
                if bidAmount >  listing.price:
                    isvalid= True
            except:
                message = "You must make a valid bid"

            if isvalid:
                # Create nuevo bid
                newBid = Bid(user= user, product = listing, bid = bidAmount, date= datetime.now())
                newBid.save()
                listing.newBid(bidAmount)
                message = 'Bid done!'
            else:
                message = 'Sorry! You must make a better bid'    
        except Exception as e:
            print(e)
            message = 'Ups! Something happened. Try again in a few minutes!'
        return HttpResponseRedirect(reverse("listing", args=[listing_id, message]))

def newComment(request, listing_id):
    if request.method == 'POST':
        try:
            user =  User.objects.get(username= request.user)
            # Taking listing info
            listing = Product.objects.get(pk= listing_id)
            usercomment = request.POST["userComment"]
            if usercomment:
                newComment = Comments(author= user, product= listing, comment= usercomment, date = datetime.now())
                newComment.save()
                message= 'Comment saved'
            else:
                message = 'Comments should have some letters at least'
            
        except Exception as e:
            print(e)
            message = 'Ups! Something happened. Try again in a few minutes!'
        
        return HttpResponseRedirect(reverse("listing", args=[listing_id, message]))

@login_required
def watchlistView(request):
    message= ""
    watchlist= []
    try:
        user = User.objects.get(username= request.user)
        watchlist = user.getWatchlist()

    except:
        message = 'Ups! Something happened. Try again in a few minutes!'

    return render(request, "auctions/watchlist.html", {
        "products": watchlist,
        "message": message

    })

def categoriesView(request, category_id = 0):
    products = []
    if category_id != 0:
        # Search for the products with that category
        category = Category.objects.get(pk = category_id)
        products = category.getActiveListings()

        
    return render(request, "auctions/categories.html",{
        "categories": categories,
        "products": products,
        "category_id": category_id
    })
    