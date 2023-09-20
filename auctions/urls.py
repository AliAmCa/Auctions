from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newProduct", views.newProduct, name="new"),
    path("listing/<int:listing_id>/<str:message>", views.showListing, name="listing"),
    path("newBid/<int:listing_id>", views.newBid, name="newBid"),
    path("newComment/<int:listing_id>", views.newComment, name="newComment"),
    path("listingActions/<int:listing_id>", views.listingActions, name="listingActions"),
    path("watchlist", views.watchlistView, name="watchlist"),
    path("categories/", views.categoriesView, name="categories"),
    path("categories/<int:category_id>", views.categoriesView, name="categories_id")



]
