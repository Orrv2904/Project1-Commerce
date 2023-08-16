from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .form import ListingForm
from django.contrib import messages
from .models import Listing, User, Category
from django.core.paginator import Paginator


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
