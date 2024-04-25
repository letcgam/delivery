from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("seller", views.seller, name="seller"),
    path("new-product", views.add_product, name="add_product"),
    path("my-products", views.my_products, name="my_products"),
    path("product/<int:product_id>/", views.product, name="product"),
    path("my-cart", views.my_cart, name="my-cart"),
    path("my-wishlist", views.my_wishlist, name="my-wishlist"),
    path("add-to-cart", views.add_to_cart, name="add_to_cart"),
    path("remove-from-cart/<int:product_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("add_to_wishlist/<int:product_id>/", views.add_to_wishlist, name="add_to_wishlist"),
    path("move_to_wishlist/<int:product_id>/", views.move_to_wishlist, name="move_to_wishlist"),
]
