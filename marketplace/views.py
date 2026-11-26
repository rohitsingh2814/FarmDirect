from decimal import Decimal, InvalidOperation
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from django.contrib.auth.models import User
from .forms import SignUpForm, ProductForm, CheckoutForm, ResetPasswordDirectForm
from .models import FarmerProfile, Product, Order, OrderItem


def home(request):
    available_products = Product.objects.filter(
        is_available=True, quantity_kg__gt=0
    ).select_related("farmer", "farmer__user")

    trending_qs = available_products.filter(
        Q(discount_percent__gt=0) | Q(is_trending=True)
    ).order_by("-discount_percent", "-is_trending", "-created_at")
    trending_products = list(trending_qs[:12])
    if not trending_products:
        trending_products = list(available_products[:6])
    trending_slides = [trending_products[i : i + 3] for i in range(0, len(trending_products), 3)]

    products = available_products
    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "")
    if query:
        products = products.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(farmer__farm_name__icontains=query)
        )
    if category:
        products = products.filter(category=category)
    page_obj = Paginator(products, 9).get_page(request.GET.get("page"))

    return render(
        request,
        "marketplace/home.html",
        {
            "page_obj": page_obj,
            "query": query,
            "category": category,
            "trending_products": trending_products,
            "trending_slides": trending_slides,
            "categories": Product.CATEGORY_CHOICES,
            "total_farms": FarmerProfile.objects.count(),
        },
    )


def signup(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Your account has been created.")
        return redirect("farmer_dashboard" if hasattr(user, "farmer_profile") else "home")
    return render(request, "marketplace/signup.html", {"form": form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("farmer_dashboard" if hasattr(user, "farmer_profile") else "home")
        messages.error(request, "Invalid username or password.")
    return render(request, "marketplace/login.html")


@login_required
def user_logout(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, "You have been logged out.")
    return redirect("home")


def password_reset_direct(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = ResetPasswordDirectForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        email = form.cleaned_data["email"].strip().lower()
        new_password = form.cleaned_data["new_password"]
        users = User.objects.filter(email__iexact=email)
        if users.exists():
            for user in users:
                user.set_password(new_password)
                user.save()
            messages.success(request, "Your password has been reset successfully. Please login with your new password.")
            return redirect("login")
        else:
            messages.error(request, "No account found with this email address.")
    return render(request, "marketplace/password_reset.html", {"form": form})


def product_detail(request, pk):
    product = get_object_or_404(Product.objects.select_related("farmer"), pk=pk, is_available=True)
    return render(request, "marketplace/product_detail.html", {"product": product})


@login_required
def farmer_dashboard(request):
    if not hasattr(request.user, "farmer_profile"):
        messages.error(request, "Only farmer accounts can access the farmer dashboard.")
        return redirect("home")
    farmer = request.user.farmer_profile
    products = farmer.products.all()
    order_items = (
        OrderItem.objects.filter(farmer=farmer)
        .select_related("order", "product", "order__customer")
        .order_by("-order__created_at", "-id")
    )
    total_revenue = sum(
        (item.subtotal for item in order_items if item.order.status != "cancelled"),
        Decimal("0.00"),
    )
    return render(
        request,
        "marketplace/farmer_dashboard.html",
        {
            "farmer": farmer,
            "products": products,
            "order_items": order_items,
            "total_revenue": total_revenue,
            "status_choices": Order.STATUS_CHOICES,
        },
    )


@login_required
@require_POST
def farmer_order_status(request, pk):
    if not hasattr(request.user, "farmer_profile"):
        return redirect("home")
    farmer = request.user.farmer_profile
    order = get_object_or_404(
        Order.objects.filter(items__farmer=farmer).distinct(), pk=pk
    )
    new_status = request.POST.get("status", "")
    valid_statuses = {code for code, _ in Order.STATUS_CHOICES}
    if new_status in valid_statuses:
        order.status = new_status
        order.save(update_fields=["status"])
        messages.success(request, f"Order #{order.pk} marked as {order.get_status_display()}.")
    else:
        messages.error(request, "Invalid order status.")
    return redirect("farmer_dashboard")


@login_required
def product_add(request):
    if not hasattr(request.user, "farmer_profile"):
        return redirect("home")
    form = ProductForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        product = form.save(commit=False)
        product.farmer = request.user.farmer_profile
        product.save()
        messages.success(request, "Product added successfully.")
        return redirect("farmer_dashboard")
    return render(request, "marketplace/product_form.html", {"form": form, "heading": "Add product"})


@login_required
def product_edit(request, pk):
    if not hasattr(request.user, "farmer_profile"):
        return redirect("home")
    product = get_object_or_404(Product, pk=pk, farmer=request.user.farmer_profile)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Product updated.")
        return redirect("farmer_dashboard")
    return render(request, "marketplace/product_form.html", {"form": form, "heading": "Edit product"})


@login_required
@require_POST
def product_delete(request, pk):
    if not hasattr(request.user, "farmer_profile"):
        return redirect("home")
    product = get_object_or_404(Product, pk=pk, farmer=request.user.farmer_profile)
    product.delete()
    messages.success(request, "Product deleted.")
    return redirect("farmer_dashboard")


def _get_cart(request):
    return request.session.setdefault("cart", {})


def cart_view(request):
    cart = request.session.get("cart", {})
    cleaned_cart = {}
    items, total, total_savings = [], Decimal("0.00"), Decimal("0.00")
    removed_unavailable = False

    for product_id, quantity in cart.items():
        product = Product.objects.filter(pk=product_id, is_available=True).first()
        try:
            qty = Decimal(str(quantity))
        except InvalidOperation:
            qty = Decimal("0")
        if product and qty > 0:
            cleaned_cart[product_id] = str(qty)
            unit_price = product.discounted_price
            subtotal = (unit_price * qty).quantize(Decimal("0.01"))
            savings = (product.savings_per_kg * qty).quantize(Decimal("0.01"))
            items.append({
                "product": product,
                "quantity": qty,
                "unit_price": unit_price,
                "subtotal": subtotal,
                "savings": savings,
            })
            total += subtotal
            total_savings += savings
        else:
            removed_unavailable = True

    if cleaned_cart != cart:
        request.session["cart"] = cleaned_cart
        if removed_unavailable:
            messages.info(request, "Unavailable or deleted items were removed from your cart.")

    return render(
        request,
        "marketplace/cart.html",
        {"items": items, "total": total, "total_savings": total_savings},
    )


@require_POST
def cart_add(request, pk):
    product = get_object_or_404(Product, pk=pk, is_available=True)
    try:
        qty = Decimal(request.POST.get("quantity", "1"))
    except InvalidOperation:
        qty = Decimal("1")
    if qty <= 0 or qty > product.quantity_kg:
        messages.error(request, "Enter a valid quantity within available stock.")
        return redirect("product_detail", pk=pk)
    cart = request.session.get("cart", {})
    new_qty = Decimal(str(cart.get(str(pk), "0"))) + qty
    if new_qty > product.quantity_kg:
        messages.error(request, "Requested quantity exceeds available stock.")
        return redirect("product_detail", pk=pk)
    cart[str(pk)] = str(new_qty)
    request.session["cart"] = cart
    messages.success(request, "Added to cart.")
    return redirect("cart")


@require_POST
def cart_update(request, pk):
    cart = request.session.get("cart", {})
    if str(pk) in cart:
        try:
            qty = Decimal(request.POST.get("quantity", "1"))
        except InvalidOperation:
            qty = Decimal("0")
        product = Product.objects.filter(pk=pk, is_available=True).first()
        if qty <= 0:
            cart.pop(str(pk), None)
        elif product and qty <= product.quantity_kg:
            cart[str(pk)] = str(qty)
        else:
            messages.error(request, "Quantity exceeds available stock.")
    request.session["cart"] = cart
    return redirect("cart")


@require_POST
def cart_remove(request, pk):
    cart = request.session.get("cart", {})
    cart.pop(str(pk), None)
    request.session["cart"] = cart
    return redirect("cart")


@login_required
def checkout(request):
    cart = request.session.get("cart", {})
    if not cart:
        messages.info(request, "Your cart is empty.")
        return redirect("home")
    form = CheckoutForm(request.POST or None, initial={
        "full_name": request.user.get_full_name() or request.user.username,
        "phone": getattr(getattr(request.user, "customer_profile", None), "phone", ""),
        "delivery_address": getattr(getattr(request.user, "customer_profile", None), "address", ""),
    })
    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            # Validate every cart line before creating the order so an invalid cart
            # cannot leave behind an empty/partial order.
            locked_products = {}
            for product_id, quantity in list(cart.items()):
                product = Product.objects.select_for_update().filter(
                    pk=product_id, is_available=True
                ).first()
                try:
                    qty = Decimal(str(quantity))
                except InvalidOperation:
                    qty = Decimal("0")
                if product is None:
                    cart.pop(product_id, None)
                    request.session["cart"] = cart
                    messages.warning(request, "An unavailable product was removed from your cart. Please review your cart.")
                    return redirect("cart")
                if qty <= 0 or qty > product.quantity_kg:
                    messages.error(request, f"Not enough stock for {product.name} ({product.quantity_kg} kg left). Please update your cart.")
                    return redirect("cart")
                locked_products[product_id] = (product, qty)

            order = Order.objects.create(
                customer=request.user,
                full_name=form.cleaned_data["full_name"],
                phone=form.cleaned_data["phone"],
                delivery_address=form.cleaned_data["delivery_address"],
            )
            total = Decimal("0.00")
            for product, qty in locked_products.values():
                unit_price = product.discounted_price
                OrderItem.objects.create(
                    order=order, product=product, farmer=product.farmer,
                    quantity_kg=qty, price_per_kg=unit_price
                )
                product.quantity_kg -= qty
                if product.quantity_kg == 0:
                    product.is_available = False
                product.save(update_fields=["quantity_kg", "is_available"])
                total += unit_price * qty
            order.total_amount = total
            order.save(update_fields=["total_amount"])
        request.session["cart"] = {}
        messages.success(request, f"Order #{order.pk} placed successfully.")
        return redirect("my_orders")
    return render(request, "marketplace/checkout.html", {"form": form})


@login_required
def my_orders(request):
    orders = Order.objects.filter(customer=request.user).prefetch_related("items", "items__product")
    return render(request, "marketplace/my_orders.html", {"orders": orders})
