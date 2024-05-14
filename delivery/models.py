from ast import Delete
from django.db import models
from django.contrib.auth.models import User as AuthUser


class Document(models.Model):
    type = models.CharField(max_length=30, choices=[
        ('SSN', 'Social Security Number'),
        ('EIN', 'Employer Identification Number')
    ])
    number = models.CharField(max_length=50, unique=True)
    issue_date = models.DateField()
    expiration_date = models.DateField()

    def __str__(self):
        return f"{self.get_document_type_display()} - {self.number}"

    class Meta:
        db_table = "document"
    

class User(models.Model):
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE, primary_key=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    birth = models.DateField(blank=True, null=True)
    document = models.ForeignKey(Document, blank=True, null=True, on_delete=models.SET_NULL)
    user_type = models.CharField(max_length=30, choices=[
        ('admin', 'Admin'),
        ('client', 'Client'),
        ('seller applicant', 'Seller applicant'),
        ('seller', 'Seller'),
        ('deliveryman applicant', 'Deliveryman applicant'),
        ('deliveryman', 'Deliveryman')
    ])
    exclude_fields = [id]

    class Meta:
        db_table = "user_info"
    
    def get_fields_values(self):
        fields = [field.name for field in self._meta.get_fields()]
        values = []
        for field in fields:
            try:
                values.append([field, getattr(self, field)])
            except:
                pass
        return values


class DriversLicense(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.CharField(max_length=20)
    issue_date = models.DateField()
    expiration_date = models.DateField()
    type = models.CharField(max_length=20, choices=[
        ('DL', 'DL'),
        ('CDL', 'CDL'),
        ('M', 'M'),
        ('EDL', 'EDL')
    ])

    def __str__(self):
        return self.number
    
    class Meta:
        db_table = "license"
    
    def get_fields_values(self):
        fields = [field.name for field in self._meta.get_fields()]
        values = []
        for field in fields:
            try:
                values.append([field, getattr(self, field)])
            except:
                pass
        return values


class Driver(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    license = models.ForeignKey(DriversLicense, on_delete=models.CASCADE)

    class Meta:
        db_table = "driver"
    
    def get_fields_values(self):
        fields = [field.name for field in self._meta.get_fields()]
        values = []
        for field in fields:
            try:
                values.append([field, getattr(self, field)])
            except:
                pass
        return values


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
    category = models.ForeignKey(Category, default=24, on_delete=models.SET_DEFAULT)
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
    
    def get_fields_values(self):
        fields = [field.name for field in self._meta.get_fields()]
        values = []
        for field in fields:
            try:
                values.append([field, getattr(self, field)])
            except:
                pass
        return values


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
    user = models.ForeignKey(AuthUser, on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now_add=True)
    card = models.ForeignKey(Card, on_delete=models.PROTECT)

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
        ("CANCELED", "Canceled")
    ])

    class Meta:
        db_table = "order_status"


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.ForeignKey(OrderStatus, on_delete=models.PROTECT, default=1)
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
    driver = models.ForeignKey(Driver, on_delete=models.DO_NOTHING)
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