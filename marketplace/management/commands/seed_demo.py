from decimal import Decimal
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from marketplace.models import FarmerProfile, Product


DEMO_PRODUCTS = [
    {
        "name": "Organic Alphonso Mangoes",
        "category": "fruits",
        "description": "Sun-ripened Ratnagiri Alphonso mangoes harvested at peak sweetness with zero carbide.",
        "price": Decimal("240.00"),
        "discount_percent": 25,
        "quantity_kg": Decimal("45.00"),
        "is_trending": True,
    },
    {
        "name": "Heirloom Cherry Tomatoes",
        "category": "vegetables",
        "description": "Crisp, vine-ripened red & golden cherry tomatoes picked fresh every morning.",
        "price": Decimal("95.00"),
        "discount_percent": 20,
        "quantity_kg": Decimal("32.00"),
        "is_trending": True,
    },
    {
        "name": "A2 Gir Cow Desi Ghee",
        "category": "dairy",
        "description": "Slow-churned bilona method A2 ghee with rich nutty aroma and golden granules.",
        "price": Decimal("680.00"),
        "discount_percent": 15,
        "quantity_kg": Decimal("18.00"),
        "is_trending": True,
    },
    {
        "name": "Himalayan Red Rajma",
        "category": "grains",
        "description": "Unpolished, quick-cooking mountain kidney beans rich in protein and earthy flavor.",
        "price": Decimal("160.00"),
        "discount_percent": 30,
        "quantity_kg": Decimal("60.00"),
        "is_trending": True,
    },
    {
        "name": "Baby Spinach & Kale Mix",
        "category": "vegetables",
        "description": "Hydroponic pesticide-free tender leafy greens washed and packed in breathable crates.",
        "price": Decimal("110.00"),
        "discount_percent": 18,
        "quantity_kg": Decimal("24.00"),
        "is_trending": True,
    },
    {
        "name": "Wild Forest Raw Honey",
        "category": "other",
        "description": "Unfiltered single-origin multiflora honey cold-extracted straight from farm apiaries.",
        "price": Decimal("420.00"),
        "discount_percent": 22,
        "quantity_kg": Decimal("28.00"),
        "is_trending": True,
    },
]


class Command(BaseCommand):
    help = "Seed demo farmer and trending discounted produce items (idempotent)."

    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(
            username="greenvalley_farm",
            defaults={"email": "greenvalley@farmdirect.local"},
        )
        if created:
            user.set_unusable_password()
            user.save()

        farmer, _ = FarmerProfile.objects.get_or_create(
            user=user,
            defaults={
                "farm_name": "GreenValley Organic Farm",
                "phone": "9876543210",
                "location": "Nashik, Maharashtra",
                "is_verified": True,
            },
        )

        created_count = 0
        for item in DEMO_PRODUCTS:
            _, obj_created = Product.objects.get_or_create(
                farmer=farmer,
                name=item["name"],
                defaults=item,
            )
            if obj_created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f"Seeded {created_count} demo trending product(s)."))
