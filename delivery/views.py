from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from django.contrib.auth.models import User
from .models import User as UserInfo, Product, Category, WishList


def index(request):
    products = Product.objects.all()
    context = {"products": products}

    if request.user is not None:
        try:
            user_type = UserInfo.objects.get(user_id=request.user.id).user_type
            context = {
                "user_type": user_type,
                "products": products
            }
        except:
            pass

    return render(request, "index.html", context)


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
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    return render(request, "login.html")


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
            return render(request, "register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            UserInfo.objects.create(
                user=user,
                user_type=request.POST["user-type"]
            )
            user.save()
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")


def seller(request):
    return render(request, "seller/seller.html")


def add_product(request):
    message = None
    if request.method == "POST":
        try:
            product = Product.objects.create(
                name = request.POST["name"],
                description = request.POST["description"],
                category = Category.objects.get(pk = request.POST["category"]),
                stock = request.POST["stock"],
                price = request.POST["price"],
                owner_id = request.user.id
            )
            product.save()
        except:
            message = {
                'class': 'text-danger',
                'text': 'Failed to register product. Make sure to fill in every field.'
            }
        else:
            message = {
                'class': 'text-success',
                'text': 'Successfully registered product!'
            }
    categories = Category.objects.all().order_by("name")
    return render(request, "seller/add-product.html", {
        "categories": categories,
        'message': message
    })


def my_products(request):
    products = Product.objects.filter(owner=request.user.id)
    return render(request, "seller/my-products.html", {
        'products': products,
    })


def add_to_wishlist(request, product_id):
    wishlist_item = WishList.objects.create(
        product = request.GET["product_id"],
        user = request.user
    )
    wishlist_item.save()
    return HttpResponseRedirect(reverse("index"))