from decimal import Decimal
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class FarmerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="farmer_profile")
    farm_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=160)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.farm_name


class CustomerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="customer_profile")
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.user.username


class Product(models.Model):
    CATEGORY_CHOICES = [
        ("vegetables", "Vegetables"),
        ("fruits", "Fruits"),
        ("grains", "Grains & Pulses"),
        ("dairy", "Dairy"),
        ("other", "Other"),
    ]
    farmer = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=120)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="vegetables")
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    discount_percent = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(90)],
        help_text="Discount percentage (0-90%)",
    )
    quantity_kg = models.DecimalField(max_digits=9, decimal_places=2, help_text="Available quantity in kg")
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    is_trending = models.BooleanField(default=False, help_text="Feature in the trending deals carousel")
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    @property
    def has_discount(self):
        return self.discount_percent > 0

    @property
    def discounted_price(self):
        if self.discount_percent <= 0:
            return self.price
        factor = (Decimal("100") - Decimal(self.discount_percent)) / Decimal("100")
        return (self.price * factor).quantize(Decimal("0.01"))

    @property
    def savings_per_kg(self):
        return (self.price - self.discounted_price).quantize(Decimal("0.01"))

    @property
    def category_emoji(self):
        return {
            "vegetables": "🥬",
            "fruits": "🍓",
            "grains": "🌾",
            "dairy": "🥛",
            "other": "🧺",
        }.get(self.category, "🌱")

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ("placed", "Placed"),
        ("confirmed", "Confirmed"),
        ("dispatched", "Dispatched"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="orders")
    full_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=20)
    delivery_address = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="placed")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.pk}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    farmer = models.ForeignKey(FarmerProfile, on_delete=models.PROTECT)
    quantity_kg = models.DecimalField(max_digits=9, decimal_places=2)
    price_per_kg = models.DecimalField(max_digits=9, decimal_places=2)

    @property
    def subtotal(self):
        return self.quantity_kg * self.price_per_kg

    def __str__(self):
        return f"{self.product.name} ({self.quantity_kg} kg)"
