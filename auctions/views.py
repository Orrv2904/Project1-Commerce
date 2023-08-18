from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .form import ListingForm
from django.contrib import messages
from .models import Listing, User, Category, Comment, Bid
from django.db.models import F
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def listing(request, id):
    listing_data = Listing.objects.get(pk=id)
    isListingInWatchlist = request.user in listing_data.watchlist.all()
    allComments = Comment.objects.filter(listing=listing_data)
    isOwner = request.user.username == listing_data.owner.username 
    return render(request, "auctions/listing.html", {
        "listing": listing_data,
        "isListingInWatchlist": isListingInWatchlist,
        "allComments": allComments,
        "isOwner": isOwner,
    })

def my_listings(request):
    user_winning_listings = Listing.objects.filter(price__user=request.user, price__bid=F('price__bid'))
    page_number = request.GET.get('page', 1)
    items_per_page = 5
    paginator = Paginator(user_winning_listings, items_per_page)
    page = paginator.get_page(page_number)
    
    return render(request, "auctions/my_listings.html", {
        "user_winning_listings": page,
    })

def closeAuction(request, id):
    listingData = Listing.objects.get(pk=id)
    listingData.isActive = False
    listingData.save()
    isOwner = request.user.username == listingData.owner.username 
    isListingInWatchlist = request.user in listingData.watchlist.all()
    allComments = Comment.objects.filter(listing=listingData)
    return render(request, "auctions/listing.html", {
        "listing": listingData,
        "isListingInWatchlist": isListingInWatchlist,
        "allComments": allComments,
        "isOwner": isOwner,
        "update": True,
        "message": "Congratulations! Your auction is closed."
    })


def addComment(request, id):
    currentUser = request.user
    listingData = Listing.objects.get(pk=id)
    message = request.POST['comment']

    newComment = Comment(
        author = currentUser,
        listing = listingData,
        message = message,
    )

    newComment.save()
    return HttpResponseRedirect(reverse("listing",args=(id, )))


def addBid(request, id):
    newBid = request.POST['newBid']
    listingData = Listing.objects.get(pk=id)
    isListingInWatchlist = request.user in listingData.watchlist.all()
    allComments = Comment.objects.filter(listing=listingData)
    isOwner = request.user.username == listingData.owner.username 
    if int(newBid) > listingData.price.bid:
        updateBid = Bid(user=request.user, bid=int(newBid))
        updateBid.save()
        listingData.price = updateBid
        listingData.save()
        success_message = "Bid was updated successfully"
        return render(request, "auctions/listing.html",{
            "listing": listingData,
            "success_message": success_message,
            "update": True,
            "isListingInWatchlist": isListingInWatchlist,
            "allComments": allComments,
            "isOwner": isOwner,
        })
    else:
        error_message = "Bid update failed. Your bid should be higher than the current highest bid."
        return render(request, "auctions/listing.html",{
            "listing": listingData,
            "error_message": error_message,
            "update": False,
            "isListingInWatchlist": isListingInWatchlist,
            "allComments": allComments,
            "isOwner": isOwner,
        })

    
def displayWatchlist(request):
    currentUser = request.user
    listings = currentUser.listingWatchlist.all()
    items_per_page = 5
    paginator = Paginator(listings, items_per_page)
    page_number = request.GET.get('page')
    page_listings = paginator.get_page(page_number)
    return render(request, "auctions/watchlist.html",{
        "listings": page_listings
    })

def removeWatchlist(request, id):
    listingData = Listing.objects.get(pk=id)
    currentUser = request.user
    listingData.watchlist.remove(currentUser)
    return HttpResponseRedirect(reverse("listing",args=(id, )))


def addWatchlist(request, id):
    listingData = Listing.objects.get(pk=id)
    currentUser = request.user
    listingData.watchlist.add(currentUser)
    return HttpResponseRedirect(reverse("listing",args=(id, )))


def index(request):
    listings = Listing.objects.filter(isActive=True)
    paginator = Paginator(listings, 5)
    page_number = request.GET.get('page')
    page_listings = paginator.get_page(page_number)

    allCategories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "listings": page_listings,
        "categories": allCategories,
    })

def displayCategory(request):
    if request.method == "POST":
        category_id = request.POST.get('category')
        try:
            category = get_object_or_404(Category, pk=category_id)
        except Category.DoesNotExist:
            return HttpResponse("Not Found")
        else:
            activeListings = Listing.objects.filter(isActive=True, category=category)
            paginator = Paginator(activeListings, 5)
            page_number = request.GET.get('page')
            page_listings = paginator.get_page(page_number)
            allCategories = Category.objects.all()
            return render(request, "auctions/index.html", {
                "listings": page_listings,
                "categories": allCategories,
            })
    else:
        return redirect('index')

def createListing(request):
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.save()

            custom_price = form.cleaned_data.get('custom_price')
            if custom_price is not None:
                existing_bid = Bid.objects.filter(bid=custom_price, user=request.user).first()
                if existing_bid:
                    listing.price = existing_bid
                else:
                    bid = Bid.objects.create(bid=custom_price, user=request.user)
                    bid.save()
                    listing.price = bid

                listing.save()

            messages.success(request, "New listing added successfully!")
            return redirect('index')
        else:
            messages.error(request, "Critical error")
    else:
        form = ListingForm()
        listings = Listing.objects.all()
        allCategories = Category.objects.all()
    context = {
        'form': form,
        'listings': listings,
        "allCategories": allCategories,
    }
    return render(request, "auctions/create.html", context)


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
