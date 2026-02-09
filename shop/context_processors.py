"""Context processor for cart count"""
from .models import Cart


def cart_count(request):
    """Add cart item count to all templates"""
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            count = cart.total_items
        except Cart.DoesNotExist:
            count = 0
    else:
        count = 0
    
    return {'cart_count': count}
