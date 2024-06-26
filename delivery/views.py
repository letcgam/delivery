import decimal
import secrets
import string
from math import ceil
from delivery.logs.logger import orderUpdateLog
from .exceptions.exceptions import FieldError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User
from .signals import user_signals, product_signals, order_signals
from .utilities.functions import get_layout_context, update_type
from .models import BankAccount, Comment, DeliveryRecord, Document, Rating, User as UserInfo, Wallet, Withdraw
from .models import BillingAdress, Card, Order, OrderItem, OrderStatus, Payment, PaymentType, Recipient, Product, Category, WishList, Cart, CartItem, Adress, Driver, DriversLicense, ClientCode, SellerCode


def index(request):
    products = (Product.objects.order_by('?'))

    context = get_layout_context(request)
    context.update({"products": products})

    return render(request, "index.html", context)


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
            user_info = UserInfo.objects.create(
                user=user,
                type=request.POST["user-type"]
            )
            user.save()
            user_info.save()

            Cart.objects.create(user_id = user.id).save()

            fields = ""
            for key, value in user_info.fields_values.items():
                fields += f""" | {key}={value}"""
            user_signals.user_created.send(
                sender = user,
                user = user,
                fields = fields,
            )
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken."
            })


        login(request, user)
        context = get_layout_context(request)

        if "deliveryman" in context["type"] or "seller" in context["type"]:
            Wallet.objects.create(user = user)

        if context["type"] == "deliveryman applicant":
            return render(request, "account/account.html", context)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")


@login_required
def my_account(request):
    user = User.objects.get(pk = request.user.id)
    user_info = UserInfo.objects.get(user = user)
    user_info.birth = str(user_info.birth)
    context = get_layout_context(request)

    context.update({
        'user': user,
        'user_info': user_info,
    })

    try:
        document = user_info.document
        if document != None:
            document.issue_date = str(document.issue_date)
            document.expiration_date = str(document.expiration_date)
            context.update({'document': document})

        billing_adress = BillingAdress.objects.get(user_id = user.id)
        if billing_adress != None:
            adress = Adress.objects.get(pk = billing_adress.adress_id)
            context.update({'adress': adress})

        driver = Driver.objects.get(user_id = user.id)
        if driver != None:
            license = DriversLicense.objects.get(pk = driver.license_id)
            license.issue_date = str(license.issue_date)
            license.expiration_date = str(license.expiration_date)
            context.update({'license': license})
    except:
        pass

    if request.method == 'GET':
        return render(request, "account/account.html", context)
    else:
        try:
            fields = ['username', 'email', 'first-name', 'last-name', 'phone-number', 'birth']
            if "seller" in context["type"] or "deliveryman" in context["type"]:
                fields += ['doc-number', 'doc-issue-date', 'doc-expiration-date', 'document-type']
            error = []

            for field in fields:
                if request.POST[field] == "":
                    error.append(field)

            if len(error) >= 1:
                raise FieldError(error)
            else:
                old_user_info = user_info.fields_values
                new_user_info = user_info.fields_values

                user.first_name = new_user_info["first_name"] = request.POST['first-name']
                user.last_name = new_user_info["last_name"] = request.POST['last-name']
                user.username = new_user_info["username"] = request.POST['username']
                user.email = new_user_info["email"] = request.POST['email']
                user_info.phone = new_user_info["phone"] = request.POST['phone-number']
                user_info.birth = new_user_info["birth"] = request.POST['birth'] if request.POST['birth'] != "" else None

                if "seller" in context["type"] or "deliveryman" in context["type"]:
                    document, created = Document.objects.get_or_create(
                        number = request.POST['doc-number']
                    )
                    document.type = request.POST['document-type'],
                    document.issue_date = request.POST['doc-issue-date'],
                    document.expiration_date = request.POST['doc-expiration-date']
                    if document != user_info.document:
                        document.save()
                        if created:
                            user_info.document = document
                        context.update({"document": document})

                user_info.save()
                user.save()

                altered_fields = ""
                for key in new_user_info.keys():
                    if old_user_info[key] != new_user_info[key]:
                        altered_fields += f""" | {key} > old: {old_user_info[key]} > new: {new_user_info[key]}"""

                if altered_fields != "":
                    user_signals.user_edited.send(
                        sender = request.user,
                        user = user,
                        action="Edited",
                        altered_fields = altered_fields,
                    )

                if "applicant" in user_info.type:
                    update_type(request)

                context.update({
                    'user': user,
                    'user_info': user_info,
                })
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


def categories_filter(request, category_id):
    if category_id != 0:
        chosen_category = Category.objects.get(pk=category_id)
        products = Product.objects.filter(category_id=chosen_category.id)
    else:
        chosen_category = {'name': "All categories"}
        products = Product.objects.all()

    context = get_layout_context(request)
    context.update({"products": products, "chosen_category": chosen_category, 'products_len': len(products)})

    return render(request, "filter.html", context)


@login_required
def seller(request):
    context = get_layout_context(request)

    sales = Order.objects.filter(seller = request.user)

    sold_categories = {}
    for sale in sales:
        for item in OrderItem.objects.filter(order = sale):
            if item.product.category not in sold_categories.keys():
                sold_categories.update({(item.product.category): 0})
            sold_categories[item.product.category] += item.quant

    sold_categories = sorted(sold_categories.items(), key=lambda x: -x[1])

    context.update({"sold_categories": sold_categories})
    for cat in sold_categories:
        print(cat[0].name, cat[1])

    return render(request, "seller/seller.html", context)


@login_required
def add_product(request):
    message = None
    if request.method == "POST":
        try:
            product = Product.objects.create(
                name = request.POST["name"],
                description = request.POST["description"],
                image_url = request.POST["image-url"],
                category = Category.objects.get(pk = request.POST["category"]),
                stock = request.POST["stock"],
                price = request.POST["price"],
                owner_id = request.user.id
            )
            product.save()

            user = User.objects.get(pk = request.user.id)
            fields = ""
            for key, value in product.fields_values:
                fields += f""" | {key}={value}"""
            product_signals.product_created.send(
                sender = user,
                product = product,
                fields = fields,
            )
        except:
            message = {
                "class": "text-danger",
                "text": "Failed to register product. Make sure to fill in every field."
            }
        else:
            message = {
                "class": "text-success",
                "text": "Successfully registered product!"
            }

    context = get_layout_context(request)
    context.update({"message": message})

    return render(request, "seller/add-product.html", context)


@login_required
def edit_product(request, product_id):
    # try:
    item = Product.objects.get(pk = product_id)
    old_att = item.fields_values
    new_att = item.fields_values

    item.name = new_att["name"] = request.POST["name"]
    item.price = new_att["price"] = request.POST["price"]
    item.description = new_att["description"] = request.POST["description"]
    item.category = new_att["category"] = Category.objects.get(pk = request.POST["category"])
    item.stock = new_att["stock"] = request.POST["stock"]
    item.image_url = new_att["image_url"] = request.POST["image_url"] if request.POST["image_url"] != "" else item.image_url
    item.save()

    new_att["price"] = decimal.Decimal(new_att["price"])
    new_att["stock"] = int(new_att["stock"])

    user = User.objects.get(pk = request.user.id)
    fields = ""
    for key in old_att.keys():
        if old_att[key] != new_att[key]:
                fields += f""" | {key} > old: {old_att[key]} > new: {new_att[key]}"""
    if fields != "":
        product_signals.product_edited.send(
            sender = user,
            product = item,
            altered_fields = fields,
        )

    message = "Successfully edited product."
    # except:
    #     message = "Failed to edit product."
    return product(request, product_id, message=message)


@login_required
def my_products(request):
    products = Product.objects.filter(owner=request.user.id)
    context = get_layout_context(request)
    context.update({"products": products})
    return render(request, "seller/my-products.html", context)


@login_required
def my_sales(request):
    seller = request.user
    context = get_layout_context(request)
    orders = Order.objects.all().order_by("creation_date")
    order_items = OrderItem.objects.all()

    for order in orders:
        order.items = []
        for item in order_items:
            if item.order == order and item.product.owner == seller:
                order.items.append(item)

    orders = [order for order in orders if order.items != []]

    context.update({"orders": orders})

    return render(request, "seller/my-sales.html", context)


@login_required
def sale(request, order_id):
    user = request.user
    order = Order.objects.get(pk = order_id)
    order_items = OrderItem.objects.filter(order=order)
    order.seller_code = SellerCode.objects.get(order = order) if SellerCode.objects.filter(order = order) else None
    items = [item for item in order_items if item.product.owner == user]
    context = get_layout_context(request)

    context.update({
        "order": order,
        "items": items,
        "seller_code": order.seller_code
    })
    return render(request, "seller/sale.html", context)


def product(request, product_id, success=False, message=""):
    context = get_layout_context(request)
    product = Product.objects.get(pk=product_id)
    wishlist = WishList.objects.filter(
        product_id = product_id,
        user_id = request.user.id
    )

    same_seller = Product.objects.filter(owner = product.owner).exclude(pk = product.id)
    same_seller.len = len(same_seller)
    same_seller.range = {"3": range(1, ceil(len(same_seller)/3+1)), "5": range(1, ceil(len(same_seller)/5+1))}

    same_category = Product.objects.filter(category = product.category).exclude(pk = product.id)
    same_category.len = len(same_category)
    same_category.range = {"3": range(1, ceil(len(same_category)/3+1)), "5": range(1, ceil(len(same_category)/5+1))}

    if request.user.is_authenticated:
        complete_orders = Order.objects.filter(user = request.user).filter(status = OrderStatus.objects.get(description = "Deliver"))
        bought_items = []
        for order in complete_orders:
            for item in OrderItem.objects.filter(order = order):
                bought_items.append(item.product)

        already_bought = (product in bought_items)
        already_made_review = len(Rating.objects.filter(user = request.user, product = product)) != 0

        context.update({"accept_review": already_bought and not already_made_review})

    ratings = Rating.objects.filter(product = product)
    ratings.average = sum([rating.rating for rating in ratings]) / len(ratings) if len(ratings) > 0 else 0

    comments = Comment.objects.filter(product = product)

    context.update({
        "main_product": product,
        "wishlist": wishlist,
        "success": success,
        "message": message,
        "same_category": same_category,
        "same_seller": same_seller,
        "ratings": ratings,
        "comments": comments
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

        seller_products = {}
        for item in items:
            seller = item.product.owner
            if seller not in seller_products.keys():
                seller_products.update({seller: []})
            seller_products[seller].append(item)

        if len(seller_products) == 0:
            seller_products = None

        context.update({"seller_products": seller_products})

        return render(request, "shopping/my-cart.html", context)
    else:
        seller = User.objects.get(pk = request.POST['seller-radio'])
        cart = Cart.objects.get(user_id = user.id)
        items = [item for item in CartItem.objects.filter(cart_id = cart.id) if item.product.owner == seller]
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
            'seller': seller,
            'total': total,
            'products': products
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
                seller = User.objects.get(pk = request.POST["seller-id"])

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
                    seller = seller,
                    payment_id = payment.id,
                    recipient_id = recipient.id,
                    delivery_adress_id = adress.id,
                    shipping = decimal.Decimal(request.POST["shipping-price"])
                )
                new_order.save()

                cart = Cart.objects.get(user_id = user.id)
                cart_items = [item for item in CartItem.objects.filter(cart_id = cart.id) if item.product.owner == seller]

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

                    seller_wallet = Wallet.objects.get(user = seller)
                    seller_wallet.balance += decimal.Decimal(new_order.total_price)
                    seller_wallet.save()

                    item.product.stock -= 1
                    item.product.save()
                    item.delete()
                    message.append(order_item)

                order_signals.order_created.send(
                    sender = user,
                    order = new_order
                )

        except FieldError as e:
            message = "Provide valid data for required fields: " + e.error_message + "."
        except:
            message = "An error ocured trying to checkout. Try again later."

        context.update({"message": message})
        return order(request, new_order.id, new_order=True)


@login_required
def order(request, order_id, new_order=False):
    user = request.user
    order = Order.objects.get(pk = order_id)
    context = get_layout_context(request)

    order.client_code = ClientCode.objects.get(order = order) if ClientCode.objects.filter(order = order) else None
    order.updates = [update.timestamp for update in orderUpdateLog.objects.filter(order = order)]
    order.total_price += decimal.Decimal(order.shipping)

    if order.user_id == user.id:
        order_items = OrderItem.objects.filter(order_id = order.id)
        context.update({
            "order": order,
            "order_items": order_items,
            "new_order": new_order,
        })
        return render(request, "shopping/order.html", context)


@login_required
def my_orders(request):
    user = request.user
    context = get_layout_context(request)
    orders = Order.objects.filter(user_id = user.id).order_by("-creation_date")
    for order in orders:
        order.items = OrderItem.objects.filter(order_id = order.id)
        order.quant = 0
        for item in order.items:
            order.quant += item.quant

    context.update({"orders": orders})

    return render(request, "shopping/my-orders.html", context)


@login_required
def deliveryman_menu(request, message=""):
    deliveryman = request.user
    driver = Driver.objects.get(deliveryman = deliveryman)
    context = get_layout_context(request)

    record = DeliveryRecord.objects.filter(driver = driver).last()
    if record:
        order_in_progress = record.order if record.order.status.description != "Deliver" else None

        if order_in_progress:
            order_in_progress.quant = 0
            for item in OrderItem.objects.filter(order = order_in_progress):
                order_in_progress.quant += item.quant

            order_in_progress.seller_adress = BillingAdress.objects.filter(user = order_in_progress.seller).first()
            order_in_progress.seller_code = SellerCode.objects.get(order = order_in_progress) if SellerCode.objects.filter(order = order_in_progress) else None
            order_in_progress.client_code = ClientCode.objects.get(order = order_in_progress) if ClientCode.objects.filter(order = order_in_progress) else None

            context.update({"order_in_progress": order_in_progress})

    history = [record.order for record in DeliveryRecord.objects.filter(driver = driver)]
    for order in history:
        order.pickup = orderUpdateLog.objects.get(
            order = order,
            new_status = OrderStatus.objects.get(description="On route")
        )
        order.delivery = orderUpdateLog.objects.get(
            order = order,
            new_status = OrderStatus.objects.get(description="Deliver")
        )

    orders = Order.objects.all()
    orders_awaiting = [order for order in orders if order.status.description.lower() == "ready for pick up" and not SellerCode.objects.filter(order = order)]
    for order in orders_awaiting:
        quant = 0
        for item in OrderItem.objects.filter(order = order):
            quant += item.quant
        order.quant = quant
        order.seller_adress = BillingAdress.objects.filter(user = order.seller).first()

    context.update({
        "orders_awaiting": orders_awaiting,
        "history": history,
        "message": message
    })

    return render(request, "delivery/deliveryman-menu.html", context)


@login_required
def take_delivery_order(request, order_id):
    deliveryman = Driver.objects.get(deliveryman = request.user)
    order = Order.objects.get(pk = order_id)

    try:
        old_status = OrderStatus.objects.get(pk = order.status.id)
        order.status = OrderStatus.objects.get(description = "Awaiting withdraw")
        order.save()

        order_signals.order_edited.send(
            sender = request.user,
            order = order,
            old_status = old_status,
            new_status = order.status
        )

        record = DeliveryRecord.objects.create(
            driver = deliveryman,
            order = order
        )
        record.save()

        if not SellerCode.objects.filter(order = order):
            seller_code = SellerCode.objects.create(
                order = order,
                code = "".join(secrets.choice(string.digits) for _ in range(6))
            )
            seller_code.save()

        message = "Order registered"
    except:
        message = "Error registering order"

    return deliveryman_menu(request, message)


def pick_order_up(request):
    if request.method == 'POST':
        order = Order.objects.get(pk = request.POST['order-id-input'])
        code = request.POST['seller-code-input']

        if SellerCode.objects.get(order = order).code == code:
            try:
                old_status = OrderStatus.objects.get(pk = order.status.id)
                order.status = OrderStatus.objects.get(description = "On route")
                order.save()

                order_signals.order_edited.send(
                    sender = request.user,
                    order = order,
                    old_status = old_status,
                    new_status = order.status
                )

                if not ClientCode.objects.filter(order = order):
                    client_code = ClientCode.objects.create(
                        order = order,
                        code = "".join(secrets.choice(string.digits) for _ in range(6))
                    )
                    client_code.save()
                message = "Seller code ok"
            except:
                message = "Error verifying code"
        else:
            message = "Wrong seller code"

        return deliveryman_menu(request, message)


def confirm_delivery(request):
    if request.method == 'POST':
        order = Order.objects.get(pk = request.POST['order-id-input'])
        code = request.POST['client-code-input']

        if ClientCode.objects.filter(order = order):
            if ClientCode.objects.get(order = order).code == code:
                try:
                    old_status = OrderStatus.objects.get(pk = order.status.id)
                    order.status = OrderStatus.objects.get(description = "Deliver")
                    order.save()

                    order_signals.order_edited.send(
                        sender = request.user,
                        order = order,
                        old_status = old_status,
                        new_status = order.status
                    )

                    wallet = Wallet.objects.get(user = request.user)
                    wallet.balance += decimal.Decimal(new_order.shipping)
                    wallet.save()

                    message = "Client code ok"
                except:
                    message = "Error verifying code"
            else:
                message = "Wrong client code"

        return deliveryman_menu(request, message)


def rate_product(request, product_id):
    if request.method == 'POST':
        rating_value = request.POST["rating-input"]
        rating = Rating.objects.create(
            user = request.user,
            product = Product.objects.get(pk = product_id),
            rating = rating_value
        )
        rating.save()

    return product(request, product_id)


def add_comment(request, product_id):
    if request.method == 'POST':
        text = request.POST["comment-input"]
        comment = Comment.objects.create(
            user = request.user,
            product = Product.objects.get(pk = product_id),
            content = text
        )
        comment.save()

    return product(request, product_id)


@login_required
def my_wallet(request):
    context = get_layout_context(request)

    user = User.objects.get(pk = request.user.id)
    wallet = Wallet.objects.get(user = user)
    withdraws_made = Withdraw.objects.filter(user = user)

    if request.method == "POST":
        try:
            amount = request.POST["amount"]
            bank = request.POST["bank"]
            agency = request.POST["agency"]
            account = request.POST["account"]

            account, created_account = BankAccount.objects.get_or_create(
                bank = bank,
                agency = agency,
                account = account
            )
            if created_account:
                account.save()

            withdraw = Withdraw.objects.create(
                user = user,
                bank_account = account,
                wallet = wallet,
                amount = amount
            )
            withdraw.save()

            wallet.balance -= decimal.Decimal(amount)
            wallet.save()

            context.update({"message": 1})
        except:
            pass

    context.update({
        "wallet": wallet,
        "withdraws_made": withdraws_made
    })

    return render(request, "account/wallet.html", context)