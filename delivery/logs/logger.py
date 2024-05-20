from itertools import product
from django.db import models
from django.contrib.auth.models import User as AuthUser
from ..models import Product


class userEditLog(models.Model):
    user = models.ForeignKey(AuthUser, on_delete=models.SET_NULL, null=True, related_name="target_user")
    altered_by = models.ForeignKey(AuthUser, on_delete=models.SET_NULL, null=True, default=user)
    timestamp = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=100)
    details = models.TextField()

    def __str__(self):
        user = AuthUser.objects.get(pk = self.user_id)
        return f"{self.timestamp} | : {self.action} {user.id} - {user}"

    class Meta:
        db_table = "user_edit_log"


class productEditLog(models.Model):
    user = models.ForeignKey(AuthUser, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=100)
    details = models.TextField()

    def __str__(self):
        product = Product.objects.get(pk = self.product_id)
        return f"{self.timestamp} | : {self.action} {product.id} - {product}"

    class Meta:
        db_table = "product_edit_log"

