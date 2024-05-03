from django.db import models
from django.contrib.auth.models import User as AuthUser


class User(models.Model):
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE, primary_key=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    adress = models.CharField(max_length=255, blank=True, null=True)
    birth = models.DateField(blank=True, null=True)
    user_type = models.CharField(max_length=20)
    exclude_fields = [id]

    class Meta:
        db_table = "user_info"


class Driver(models.Model):
    id = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=20, blank=True)
    adress = models.CharField(max_length=255, blank=True)
    birth = models.DateField(blank=True)

    class Meta:
        db_table = "driver"


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "category"
        verbose_name_plural = "categories"


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    owner = models.ForeignKey(AuthUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "product"


class Vehicle(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=255)
    plate = models.CharField(max_length=7)
    city_state = models.CharField(max_length=200)
    model = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)

    class Meta:
        db_table = "vehicle"


class Adress(models.Model):
    id = models.AutoField(primary_key=True)
    street = models.CharField(max_length=200, blank=False)
    city = models.CharField(max_length=200, blank=False)
    state = models.CharField(max_length=200, blank=False)
    postal_code = models.CharField(max_length=20, blank=False)
    country = models.CharField(max_length=200, blank=False)

    class Meta:
        db_table = "adress"


class BillingAdress(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    adress = models.ForeignKey(Adress, on_delete=models.CASCADE)

    class Meta:
        db_table = "billing_adress"


class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "cart"


class CartItem(models.Model):
    id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quant = models.PositiveIntegerField()

    class Meta:
        db_table = "cart_item"


class PaymentType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(choices=[("CREDIT", "Credit card"), ("DEBIT", "Debit card")], max_length=20)

    class Meta:
        db_table = "payment_type"


class Card(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    number = models.CharField(max_length=19)
    cvv = models.IntegerField()
    expiration = models.CharField(max_length=5)
    type = models.ForeignKey(PaymentType, on_delete=models.CASCADE)
    add_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "card"


class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)

    class Meta:
        db_table = "payment"


class Recipient(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = "recipient"


class OrderStatus(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=25, choices=[
        ("PROCESSING", "Processing"),
        ("IN PREPARATION", "In preparation"),
        ("AWAITING WITHDRAW", "Awaiting withdrawal"),
        ("EN ROUTE", "En route"),
        ("DELIVER", "Deliver"),
    ])

    class Meta:
        db_table = "order_status"


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE, default=1)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE)
    delivery_adress = models.ForeignKey(Adress, on_delete=models.CASCADE)

    class Meta:
        db_table = "order"


class OrderItem(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quant = models.PositiveIntegerField()

    class Meta:
        db_table = "order_item"


class DeliveryRecord(models.Model):
    id = models.AutoField(primary_key=True)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    class Meta:
        db_table = "delivery_record"


class WishList(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = "wishlist"


class Rating(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    rating = models.FloatField()

    class Meta:
        db_table = "rating"


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    content = models.TextField(max_length=255)

    class Meta:
        db_table = "comment"