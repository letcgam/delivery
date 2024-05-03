from email import message
from multiprocessing import context
from operator import indexOf
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.contrib.auth.models import User

from .models import BillingAdress, Card, Order, OrderItem, Payment, PaymentType, Recipient, User as UserInfo, Product, Category, WishList, Cart, CartItem, Adress


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


class FieldError(Exception):
        def __init__(self, error_message) -> None:
            super().__init__()
            if len(error_message) > 1:
                for i in range(0, len(error_message) - 1):
                    error_message[i] += ", "
            self.error_message = "".join(error_message)

        def __str__(self) -> str:
            return self.error_message
        

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


def my_account(request):
    user = User.objects.get(pk = request.user.id)
    user_info = UserInfo.objects.get(user_id = user.id)
    user_info.birth = str(user_info.birth)
    context = get_layout_context(request)

    context.update({
        'user': user,
        'user_info': user_info,
    })

    try:
        billing_adress = BillingAdress.objects.get(user_id = user.id)
        adress = Adress.objects.get(pk = billing_adress.adress_id)
        context.update({'adress': adress})
    except:
        pass

    if request.method == 'GET':
        return render(request, "account/account.html", context)
    else:
        try:
            error = []
            if request.POST['username'] == "":
                error.append('Username')
            if request.POST['email'] == "":
                error.append('Email')
            if len(request.POST['phone-number']) != 19:
                error.append('Phone number')
            if len(error) >= 1:
                raise FieldError(error)
            else:
                user.first_name = request.POST['first-name']
                user.last_name = request.POST['last-name']
                user.username = request.POST['username']
                user.email = request.POST['email']
                user_info.phone = request.POST['phone-number']
                user_info.birth = request.POST['birth'] if request.POST['birth'] != "" else None

                user.save()
                user_info.save()
        except FieldError as e:
            message = {
                "text": "Provide valid data for required fields: " + e.error_message + ".",
                "class": "text-danger"
            }
        except:
            message = {
                "text": "Error during saving user information.",
                "class": "text-danger"
            }
        else:
            message = {
                "text": "Successfully saved profile.",
                "class": "text-success"
            }

        context.update({'message': message})
        return render(request, "account/account.html", context)
    

def add_adress(request):
    context = get_layout_context(request)
    user = User.objects.get(pk = request.user.id)

    message = {
        "text": "",
        "class": ""
    }
    try:
        error_message = []
        if request.POST['adress'] == "":
            error_message.append('Adress')
        if request.POST['postal-code'] == "":
            error_message.append('Postal code')
        if request.POST['city'] == "":
            error_message.append('City')
        if request.POST['state'] == "":
            error_message.append('State')
        if request.POST['country'] == "":
            error_message.append('Country')
        if error_message != []:
            raise FieldError(error_message)
        else:
            adress = Adress.objects.create(
                street = request.POST["adress"],
                postal_code = request.POST["postal-code"],
                city = request.POST["city"],
                state = request.POST["state"],
                country = request.POST["country"]
            )
            adress.save()
            billing_adress = BillingAdress.objects.create(
                user_id = request.user.id,
                adress_id = adress.id
            )
            billing_adress.save()
    except FieldError as e:
        message['text'] = "Provide valid data for required fields: " + e.error_message + "."
        message['class'] = "text-danger"
    else:
        message['text'] = "Successfully added billing adress."
        message['class'] = "text-success"
    
    try:
        billing_adress = BillingAdress.objects.filter(user_id = user.id).last()
        adress = Adress.objects.get(pk = billing_adress.adress_id)
        context.update({'adress': adress})
    except:
        pass

    context.update({"adress_message": message})
    return render(request, "account/account.html", context)


def categories_filter(request, category_id):
    if category_id != 0:
        chosen_category = Category.objects.get(pk=category_id)
        products = Product.objects.filter(category_id=chosen_category.id)
    else:
        chosen_category = {'name': "Alll categories"}
        products = Product.objects.all()

    context = get_layout_context(request)
    context.update({"products": products, "chosen_category": chosen_category, 'products_len': len(products)})

    return render(request, "categories-filter.html", context)


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


def product(request, product_id, success=False):
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
        "image_url": "../static/icon.png",
        "success": success
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
    context.update({"products": products})

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

        return product(request, product_id, success=True)


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
    user = User.objects.get(pk = request.user.id)
    user_info = UserInfo.objects.get(user_id = user.id)
    context = get_layout_context(request)

    if request.method == "GET":
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
        
        context.update({"products": products})
    
        return render(request, "shopping/my-cart.html", context)
    else:
        cart = Cart.objects.get(user_id = user.id)
        items = CartItem.objects.filter(cart_id = cart.id)
        products = []
        total = 0
        for item in items:
            product = Product.objects.get(pk = item.product_id)
            quantity = int(request.POST['quantity-input-' + str(product.id)])
            item.quant = quantity
            item.save()
            products.append({
                "product": Product.objects.get(pk = item.product_id),
                "quantity": item.quant
            })
            total += product.price * quantity
        
        try:
            billing_adress = BillingAdress.objects.get(user_id = user.id)
            adress = Adress.objects.get(pk = billing_adress.adress_id)
            context.update({'adress': adress})
        except:
            pass

        context.update({
            'user': user,
            'user_info': user_info,
            'total': total,
            'products': products,
            'products_len': len(products),
        })

        return render(request, "shopping/new-order.html", context)


@login_required
def new_order(request):
    user = request.user
    context = get_layout_context(request)

    if request.method == "POST":
        form = [ "first-name", "last-name", "email" , "phone-number", "street-input", "postal-code-input", "city-input", "state-input", "country-input", "paymentMethod" , "card-name", "card-cvv", "card-number", "card-expiration"]
        try:
            error = []
            for field in form:
                if request.POST[field] == "":
                    error.append(field)
            if len(error) > 0:
                raise FieldError(error)
            else:
                recipient, created_recipient = Recipient.objects.get_or_create(
                    first_name = request.POST["first-name"],
                    last_name = request.POST["last-name"],
                    email = request.POST["email"],
                    phone = request.POST["phone-number"]
                )
                recipient.save()

                adress, created_adress = Adress.objects.get_or_create(
                    street = request.POST["street-input"],
                    postal_code = request.POST["postal-code-input"],
                    city = request.POST["city-input"],
                    state = request.POST["state-input"],
                    country = request.POST["country-input"],
                )
                adress.save()

                card, created_card = Card.objects.get_or_create(
                    user_id = user.id,
                    name = request.POST["card-name"],
                    number = request.POST["card-number"],
                    cvv = request.POST["card-cvv"],
                    expiration = request.POST["card-expiration"],
                    type_id = PaymentType.objects.get(pk = request.POST["paymentMethod"]).id
                )
                card.save()

                payment, created_payment = Payment.objects.get_or_create(
                    user_id = user.id,
                    card_id = card.id
                )
                payment.save()

                new_order = Order.objects.create(
                    user_id = user.id,
                    payment_id = payment.id,
                    recipient_id = recipient.id,
                    delivery_adress_id = adress.id
                )
                new_order.save()

                cart = Cart.objects.get(user_id = user.id)
                cart_items = CartItem.objects.filter(cart_id = cart.id)

                message = []
                for item in cart_items:
                    order_item = OrderItem.objects.create(
                        order_id = new_order.id,
                        product_id = item.product.id,
                        quant = item.quant
                    )
                    order_item.save()
                    new_order.total_price += Product.objects.get(pk = order_item.product_id).price
                    new_order.save()
                    item.delete()
                    message.append(order_item)

        except FieldError as e:
            message = "Provide valid data for required fields: " + e.error_message + "."
        except:
            message = "An error ocured trying to checkout. Try again later."
    
        context.update({"message": message})
        return order(request, new_order.id)


@login_required
def order(request, order_id):
    user = request.user
    order = Order.objects.get(pk = order_id)
    context = get_layout_context(request)

    if order.user_id == user.id:
        order_items = OrderItem.objects.filter(order_id = order.id)
        context.update({"order": order, "order_items": order_items})
        return render(request, "shopping/order.html", context)
