from django.contrib import admin
from .models import FarmerProfile, CustomerProfile, Product, Order, OrderItem

admin.site.register(FarmerProfile)
admin.site.register(CustomerProfile)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "farmer", "category", "price", "quantity_kg", "is_available")
    list_filter = ("category", "is_available")
    search_fields = ("name", "farmer__farm_name")

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "total_amount", "status", "created_at")
    list_filter = ("status", "created_at")
    inlines = [OrderItemInline]
