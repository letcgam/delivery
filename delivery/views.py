
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.contrib.auth.models import User
from .models import User as UserInfo, Product, Category, WishList, Cart, CartItem


def index(request):
    products = Product.objects.all()

    context = get_layout_context(request)
    context.update({"products": products})

    return render(request, "index.html", context)


def get_layout_context(request):
    # get user_type
    try:
        user_type = UserInfo.objects.get(user_id=request.user.id).user_type
    except:
        user_type = None

    # get all categories
    categories = Category.objects.all().order_by('name')

    context = {'user_type': user_type, 'categories': categories}

    return context


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication warningful
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

            Cart.objects.create(user_id = user.id).save()
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")


@login_required
def seller(request):    
    context = get_layout_context(request)
    return render(request, "seller/seller.html", context)


@login_required
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
                "class": "text-warning",
                "text": "Failed to register product. Make sure to fill in every field."
            }
        else:
            message = {
                "class": "text-warning",
                "text": "warningfully registered product!"
            }

    context = get_layout_context(request)
    context.update({"message": message})

    return render(request, "seller/add-product.html", context)


@login_required
def my_products(request):
    products = Product.objects.filter(owner=request.user.id)

    context = get_layout_context(request)
    context.update({"products": products})

    return render(request, "seller/my-products.html", context)


def product(request, product_id):
    product = Product.objects.get(pk=product_id)
    category = Category.objects.get(pk=product.category_id).name
    wishlist = WishList.objects.filter(
        product_id = product_id,
        user_id = request.user.id
    )

    context = get_layout_context(request)
    context.update({
        "product": product,
        "category": category,
        "wishlist": wishlist,
        "image_url": "../static/icon.png"
    })

    return render(request, "product.html", context)


@login_required
def add_to_wishlist(request, product_id):
    wishlist = WishList.objects.filter(
        product_id = product_id,
        user_id = request.user.id
    )
    if len(wishlist):
        wishlist.delete()
    else:
        wishlist_item = WishList.objects.create(
            product_id = product_id,
            user_id = request.user.id
        )
        wishlist_item.save()
    return product(request, product_id)


@login_required
def my_wishlist(request):
    user = request.user
    wishlist = WishList.objects.filter(user_id = user.id)
    products = []
    for item in wishlist:
        product = Product.objects.get(pk = item.product_id)
        products.append(product)

    if len(products) == 0:
        products = None
    
    context = get_layout_context(request)
    context.update({"products": product})

    return render(request, "shopping/my-wishlist.html", context)


@login_required
def add_to_cart(request):
    if request.method == "POST":
        user = request.user
        product_id = int(request.POST["product-id"])
        quantity = int(request.POST["quantity"])

        cart = Cart.objects.filter(user_id=user.id).first()

        old_cart_item = CartItem.objects.filter(
            cart_id = cart.id,
            product_id = product_id
        ).first()
        if old_cart_item:
            old_cart_item.quant += quantity
            old_cart_item.save()
        else:
            cart_item = CartItem.objects.create(
                cart_id = cart.id,
                product_id = product_id,
                quant = quantity
            )
            cart_item.save()

        return product(request, product_id)


@login_required
def remove_from_cart(request, product_id):
    user = request.user
    cart = Cart.objects.filter(user_id = user.id).first()
    product = CartItem.objects.filter(cart_id = cart.id, product_id = product_id)
    product.delete()

    return my_cart(request)


@login_required
def move_to_wishlist(request, product_id):
    wishlist = WishList.objects.filter(
        product_id = product_id,
        user_id = request.user.id
    )
    if len(wishlist):
        wishlist.delete()
    else:
        wishlist_item = WishList.objects.create(
            product_id = product_id,
            user_id = request.user.id
        )
        wishlist_item.save()
    
    return remove_from_cart(request, product_id)


@login_required
def my_cart(request):
    user = request.user
    cart = Cart.objects.filter(user_id = user.id).first()
    items = CartItem.objects.filter(cart_id = cart.id)
    products = []
    for item in items:
        product = {
            "product": Product.objects.get(pk = item.product_id),
            "quantity": item.quant
        }
        products.append(product)
    
    if len(products) == 0:
        products = None
    
    context = get_layout_context(request)
    context.update({"products": product})

    return render(request, "shopping/my-cart.html", context)