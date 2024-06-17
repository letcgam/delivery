from django.contrib.auth.models import User
from ..exceptions.exceptions import FieldError
from django.shortcuts import redirect, render
from ..models import BillingAdress, Document,Order, OrderItem, OrderStatus, Category, Adress, Driver, DriversLicense, User as UserInfo
from ..signals import order_signals


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
            for field in model.fields_values():
                if field in ["", None]:
                    return 0
    
    if context["type"] == "seller applicant":
        user_info.type = "seller"
    elif context["type"] == "deliveryman applicant":
        user_info.type = "deliveryman"
    user_info.save()
    
    return 1


def add_adress(request):
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


def update_order_status(request, status_id, order_id):
    user = request.user
    context = get_layout_context(request)
    order = Order.objects.get(pk = order_id)
    status = OrderStatus.objects.get(pk = status_id)
    
    old_status = OrderStatus.objects.get(pk = order.status.id)    
    order.status = status
    order.save()
    
    order_signals.order_edited.send(
        sender = user,
        order = order,
        old_status = old_status,
        new_status = order.status
    )

    order_items = OrderItem.objects.filter(order=order)
    items = [item for item in order_items if item.product.owner == user]

    context.update({"order": order, "items": items})
        
    return render(request, "seller/sale.html", context)