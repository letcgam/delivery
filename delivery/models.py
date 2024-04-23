from django.db import models
from django.contrib.auth.models import User


class User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone = models.CharField(max_length=20, blank=True)
    adress = models.CharField(max_length=255, blank=True)
    birth = models.DateField(blank=True, null=True)
    user_type = models.CharField(max_length=20)
    exclude_fields = [id]


class Driver(models.Model):
    id = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=20, blank=True)
    adress = models.CharField(max_length=255, blank=True)
    birth = models.DateField(blank=True)


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    id = models.AutoField(primary_key=True)
    plate = models.CharField(max_length=7)
    city_state = models.CharField(max_length=200)
    model = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)


class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)


class CartItem(models.Model):
    id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quant = models.PositiveIntegerField()


class PaymentType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, choices=[('CARTAO_CREDITO', 'Cartão de Crédito'), ('CARTAO_DEBITO', 'Cartão de Débito'), ('BOLETO', 'Boleto')])


class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    type_name = models.ForeignKey(PaymentType, on_delete=models.CASCADE)
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('AGUARDANDO_PAGAMENTO', 'Aguardando Pagamento'),('PAGO', 'Pago'),('PROCESSANDO', 'Processando'),('ENVIADO', 'Enviado'),('CONCLUIDO', 'Concluído'),('CANCELADO', 'Cancelado')])
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, blank=True)
    delivery_postal_code = models.CharField(max_length=8)
    delivery_adress = models.CharField(max_length=255)


class OrderItem(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)


class DeliveryRecord(models.Model):
    id = models.AutoField(primary_key=True)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)


class WishList(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
