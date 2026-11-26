from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("password-reset/", views.password_reset_direct, name="password_reset"),
    path("product/<int:pk>/", views.product_detail, name="product_detail"),
    path("farmer/dashboard/", views.farmer_dashboard, name="farmer_dashboard"),
    path("farmer/order/<int:pk>/status/", views.farmer_order_status, name="farmer_order_status"),
    path("farmer/product/add/", views.product_add, name="product_add"),
    path("farmer/product/<int:pk>/edit/", views.product_edit, name="product_edit"),
    path("farmer/product/<int:pk>/delete/", views.product_delete, name="product_delete"),
    path("cart/", views.cart_view, name="cart"),
    path("cart/add/<int:pk>/", views.cart_add, name="cart_add"),
    path("cart/update/<int:pk>/", views.cart_update, name="cart_update"),
    path("cart/remove/<int:pk>/", views.cart_remove, name="cart_remove"),
    path("checkout/", views.checkout, name="checkout"),
    path("orders/", views.my_orders, name="my_orders"),
]
