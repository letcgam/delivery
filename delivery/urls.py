from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .utilities.functions import add_adress, add_drivers_license, update_order_status
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("my-account", views.my_account, name="my_account"),
    path("add-adress", add_adress, name="add_adress"),
    path("add-drivers-license", add_drivers_license, name="add_drivers_license"),
    path("seller", views.seller, name="seller"),
    path("new-product", views.add_product, name="add_product"),
    path("edit-product/<int:product_id>/", views.edit_product, name="edit_product"),
    path("my-products", views.my_products, name="my_products"),
    path("my-sales", views.my_sales, name="my_sales"),
    path("sale/<int:order_id>/", views.sale, name="sale"),
    path("update-order-status/<int:status_id>/<int:order_id>/", update_order_status, name="update_order_status"),
    path("product/<int:product_id>/", views.product, name="product"),
    path("my-cart", views.my_cart, name="my_cart"),
    path("my-wishlist", views.my_wishlist, name="my_wishlist"),
    path("add-to-cart", views.add_to_cart, name="add_to_cart"),
    path("remove-from-cart/<int:product_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("add-to-wishlist/<int:product_id>/", views.add_to_wishlist, name="add_to_wishlist"),
    path("move-to-wishlist/<int:product_id>/", views.move_to_wishlist, name="move_to_wishlist"),
    path("categories-filter/<int:category_id>/", views.categories_filter, name="categories_filter"),
    path("new-order", views.new_order, name="new_order"),
    path("my-orders", views.my_orders, name="my_orders"),
    path("order/<int:order_id>/", views.order, name="order"),
    path("deliveryman-menu", views.deliveryman_menu, name="deliveryman_menu"),
    path("take-delivery-order/<int:order_id>/", views.take_delivery_order, name="take_delivery_order"),
    path("pick-order-up", views.pick_order_up, name="pick_order_up"),
    path("confirm-delivery", views.confirm_delivery, name="confirm_delivery"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
