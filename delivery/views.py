from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User
from .signals import user_signals
from .models import Document, User as UserInfo
from .models import BillingAdress, Card, Order, OrderItem, OrderStatus, Payment, PaymentType, Recipient, Product, Category, WishList, Cart, CartItem, Adress, Driver, DriversLicense
from .exceptions.exceptions import FieldError
from .logs.logger import productEditLog,  userEditLog


def index(request):
    products = Product.objects.all()

    context = get_layout_context(request)
    context.update({"products": products})
    user = request.user
    if user.is_authenticated:
        print(productEditLog.objects.all())

    return render(request, "index.html", context)


def get_layout_context(request):
    # get user type
    try:
        type = UserInfo.objects.get(user_id=request.user.id).type
    except:
        type = None

    # get all categories
    categories = Category.objects.all().order_by('name')

    context = {'type': type, 'categories': categories}

    return context


def update_type(request):
    context = get_layout_context(request)
    if context["type"] == "seller applicant":
        type_request="seller"
    elif context["type"] == "deliveryman applicant":
        type_request="deliveryman"
    else:
        return None

    user = request.user

    models = []

    user_info = UserInfo.objects.filter(user_id = user.id).first()
    document = Document.objects.get(pk = user_info.document.id) if user_info.document else None
    billing_adress = BillingAdress.objects.filter(user_id = user.id).first()
    adress = Adress.objects.get(pk = billing_adress.adress.id) if billing_adress else None
    try:
        driver = Driver.objects.filter(user_id = user.id).first() if "deliveryman" in context["type"] else None
        license = DriversLicense.objects.get(pk = driver.license.id) if "deliveryman" in context["type"] else None
        models += [user_info, document, adress, license]
    except:
        pass
    
    models += [user_info, document, adress]
    
    for model in models:
        if model == None:
            return 0
        else:
            for field in model.get_fields_values():
                if field in ["", None]:
                    return 0
    
    if context["type"] == "seller applicant":
        user_info.type = "seller"
    elif context["type"] == "deliveryman applicant":
        user_info.type = "deliveryman"
    user_info.save()
    
    return 1


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
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken."
            })
        
        fields = user_info.get_fields_values
        user_signals.user_created.send(
            sender = request.user,
            user = user_info,
            altered_fields = fields,
        )
        
        login(request, user)
        context = get_layout_context(request)
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
                old_user_info = user_info.get_fields_values
                new_user_info = user_info.get_fields_values

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
                        user = user_info,
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


@login_required
def add_adress(request, is_billing=0):
    context = get_layout_context(request)
    user = User.objects.get(pk = request.user.id)

    message = {"text": "", "class": ""}
    try:
        error_message = []
        fields = ['adress', 'postal-code', 'city', 'state', 'country']
        for field in fields:
            if request.POST[field] == "":
                error_message.append(field)
                
        if error_message != []:
            raise FieldError(error_message)
        else:
            adress, created_adress = Adress.objects.get_or_create(
                street = request.POST["adress"],
                postal_code = request.POST["postal-code"],
                city = request.POST["city"],
                state = request.POST["state"],
                country = request.POST["country"]
            )
            adress.save()

            if is_billing:
                billing_adress = BillingAdress.objects.filter(user_id = user.id).first()
                if billing_adress == None:
                    billing_adress = BillingAdress.objects.create(
                        user_id = user.id,
                        adress_id = adress.id
                    )
                else:
                    billing_adress.adress_id = adress.id
                billing_adress.save()

    except FieldError as e:
        message['text'] = "Provide valid data for required fields: " + e.error_message + "."
        message['class'] = "text-danger"
    else:
        message['class'] = "text-success"
        message['text'] = "Successfully altered billing adress."

    try:
        billing_adress = BillingAdress.objects.filter(user_id = user.id).first()
        adress = Adress.objects.get(pk = billing_adress.adress_id)
        context.update({'adress': adress})
    except:
        pass

    if "applicant" in context["type"]:
        update_type(request)

    context.update({"adress_message": message})
    return render(request, "account/account.html", context)


@login_required
def add_drivers_license(request):
    context = get_layout_context(request)
    user = User.objects.get(pk = request.user.id)
    message = {}
    try:
        license = DriversLicense.objects.create(
            number = request.POST["license-number"],
            type = request.POST["license-type"],
            issue_date = request.POST["license-issue-date"],
            expiration_date = request.POST["license-expiration-date"]
        )
        
        driver = Driver.objects.filter(user_id = user.id).first()
        if driver == None:
            driver = Driver.objects.create(
                user_id = user.id,
                license_id = license.id
            )
        else:
            driver.license_id = license.id
        license.save()
        driver.save()
        
        message['class'] = "text-success"
        message['text'] = "Successfully altered license."
    except:
        message['class'] = "text-danger"
        message['text'] = "Error saving license."

    if "applicant" in context["type"]:
        update_type(request)

    context.update({
        "license_message": message,
        "license": license
        })
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
    try:
        item = Product.objects.get(pk = product_id)
        item.name = request.POST["name"]
        item.price = request.POST["price"]
        item.description = request.POST["description"]
        item.category = Category.objects.get(pk = request.POST["category"])
        item.stock = request.POST["stock"]
        item.save()
        message = "Successfully edited product."
    except:
        message = "Failed to edit product."
    return product(request, product_id, message=message)


@login_required
def my_products(request):
    products = Product.objects.filter(owner=request.user.id)
    context = get_layout_context(request)
    context.update({"products": products})
    return render(request, "seller/my-products.html", context)


@login_required
def my_sales(request):
    context = get_layout_context(request)
    orders = Order.objects.all().order_by("creation_date")
    order_items = OrderItem.objects.all()

    # sale["order_id"] = {"order": order,
    #                     "items": [order_items]
    #                     }
    sales = {}
    reverse_sales = {}

    for order in orders:
        sales.update({str(order.id): {"order": order, "items": []}})

        for item in order_items:
            if item.order == order and item.product.owner == request.user:
                sales[str(order.id)]["items"].append({
                    "product": item.product,
                    "quant": item.quant
                })
    
    for order in orders.reverse():
        reverse_sales.update({str(order.id): {"order": order, "items": []}})

        for item in order_items:
            if item.order == order and item.product.owner == request.user:
                reverse_sales[str(order.id)]["items"].append({
                    "product": item.product,
                    "quant": item.quant
                })

    sales = {key: value for key, value in sales.items() if value["items"] != []}
    reverse_sales = {key: value for key, value in reverse_sales.items() if value["items"] != []}
    
    context.update({
        "sales": sales,
        "reverse_sales": reverse_sales
    })
    return render(request, "seller/my-sales.html", context)


@login_required
def sale(request, order_id):
    user = request.user
    order = Order.objects.get(pk = order_id)
    order_items = OrderItem.objects.filter(order=order)
    items = [item for item in order_items if item.product.owner == user]
    context = get_layout_context(request)

    context.update({"order": order, "items": items})
    return render(request, "seller/sale.html", context)


def product(request, product_id, success=False, message=""):
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
        "success": success,
        "message": message
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
                    item.product.stock -= 1
                    item.product.save()
                    item.delete()
                    message.append(order_item)

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

    if order.user_id == user.id:
        order_items = OrderItem.objects.filter(order_id = order.id)
        context.update({
            "order": order,
            "order_items": order_items,
            "new_order": new_order
        })
        return render(request, "shopping/order.html", context)


@login_required
def my_orders(request):
    user = request.user
    context = get_layout_context(request)
    orders = Order.objects.filter(user_id = user.id).order_by("-creation_date")
    for order in orders:
        items = OrderItem.objects.filter(order_id = order.id)
        order.quant = 0
        for item in items:
            order.quant += item.quant

    context.update({"orders": orders})

    return render(request, "shopping/my-orders.html", context)


@login_required
def update_order_status(request, status_id, order_id):
    user = request.user
    context = get_layout_context(request)
    order = Order.objects.get(pk = order_id)
    status = OrderStatus.objects.get(pk = status_id)
    order.status = status
    order.save()

    order_items = OrderItem.objects.filter(order=order)
    items = [item for item in order_items if item.product.owner == user]

    context.update({"order": order, "items": items})
    if context['type'] == 'seller':
        return render(request, "seller/sale.html", context)