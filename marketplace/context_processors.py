from .models import Product


def cart_context(request):
    cart = request.session.get("cart", {})
    if not cart:
        return {"cart_count": 0}
    valid_ids = [pid for pid in cart.keys() if str(pid).isdigit()]
    count = Product.objects.filter(pk__in=valid_ids, is_available=True).count()
    return {"cart_count": count}
