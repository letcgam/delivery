from django.contrib import admin
from .models import (
    User,
    Driver,
    Category,
    Product,
    Vehicle,
    CartItem,
    Cart,
    PaymentType,
    Payment,
    Order,
    OrderItem,
    DeliveryRecord,
)

admin.site.register(User)
admin.site.register(Driver)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Vehicle)
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(PaymentType)
admin.site.register(Payment)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(DeliveryRecord)