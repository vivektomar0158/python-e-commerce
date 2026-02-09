from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
import stripe

from .models import Category, Product, Cart, CartItem, Order, OrderItem

stripe.api_key = settings.STRIPE_SECRET_KEY


def home(request):
    """Homepage view"""
    categories = Category.objects.filter(is_active=True)
    featured_products = Product.objects.filter(is_active=True)[:8]
    
    context = {
        'categories': categories,
        'featured_products': featured_products,
    }
    return render(request, 'shop/home.html', context)


class CategoryProductListView(ListView):
    """Product listing by category"""
    model = Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'
    paginate_by = 20

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Product.objects.filter(category=self.category, is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['categories'] = Category.objects.filter(is_active=True)
        return context


class ProductDetailView(DetailView):
    """Product detail view"""
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True)
        # Get related products from same category
        context['related_products'] = Product.objects.filter(
            category=self.object.category,
            is_active=True
        ).exclude(id=self.object.id)[:4]
        return context


def search_products(request):
    """Search products"""
    query = request.GET.get('q', '')
    products = []
    
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query),
            is_active=True
        )
    
    context = {
        'products': products,
        'query': query,
        'categories': Category.objects.filter(is_active=True),
    }
    return render(request, 'shop/search_results.html', context)


@login_required
def cart_view(request):
    """Shopping cart view"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'categories': Category.objects.filter(is_active=True),
    }
    return render(request, 'shop/cart.html', context)


@login_required
def add_to_cart(request, product_id):
    """Add product to cart"""
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    
    if not product.in_stock or quantity > product.stock_quantity:
        messages.error(request, 'Product is out of stock or insufficient quantity.')
        return redirect('shop:product_detail', slug=product.slug)
    
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    
    cart_item.save()
    messages.success(request, f'{product.name} added to cart!')
    return redirect('shop:cart')


@login_required
def update_cart(request, item_id):
    """Update cart item quantity"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > 0 and quantity <= cart_item.product.stock_quantity:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, 'Cart updated successfully!')
    else:
        messages.error(request, 'Invalid quantity.')
    
    return redirect('shop:cart')


@login_required
def remove_from_cart(request, item_id):
    """Remove item from cart"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f'{product_name} removed from cart.')
    return redirect('shop:cart')


@login_required
def checkout(request):
    """Checkout view"""
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.all()
    
    if not cart_items:
        messages.error(request, 'Your cart is empty.')
        return redirect('shop:cart')
    
    if request.method == 'POST':
        try:
            # Get form data
            delivery_name = request.POST.get('delivery_name')
            delivery_phone = request.POST.get('delivery_phone')
            delivery_address = request.POST.get('delivery_address')
            delivery_city = request.POST.get('delivery_city')
            delivery_state = request.POST.get('delivery_state')
            delivery_postal_code = request.POST.get('delivery_postal_code')
            stripe_token = request.POST.get('stripeToken')
            
            # Calculate total
            subtotal = cart.subtotal
            shipping = 0 if subtotal >= 999 else 50
            total = subtotal + shipping
            
            # Create Stripe charge (in test mode)
            try:
                charge = stripe.Charge.create(
                    amount=int(total * 100),  # Amount in paise
                    currency='inr',
                    source=stripe_token,
                    description=f'Order for {request.user.username}'
                )
                stripe_payment_id = charge.id
            except stripe.error.CardError as e:
                messages.error(request, 'Payment failed. Please try again.')
                return redirect('shop:checkout')
            
            # Create order
            order = Order.objects.create(
                user=request.user,
                total_amount=total,
                delivery_name=delivery_name,
                delivery_phone=delivery_phone,
                delivery_address=delivery_address,
                delivery_city=delivery_city,
                delivery_state=delivery_state,
                delivery_postal_code=delivery_postal_code,
                stripe_payment_id=stripe_payment_id,
                payment_status='completed',
                status='processing'
            )
            
            # Create order items
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price_snapshot=item.product.price
                )
                # Update stock
                item.product.stock_quantity -= item.quantity
                item.product.save()
            
            # Clear cart
            cart_items.delete()
            
            # Send confirmation email (console backend)
            send_mail(
                subject=f'Order Confirmation - {order.order_number}',
                message=f'Thank you for your order! Your order number is {order.order_number}. Total amount: ₹{order.total_amount}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[request.user.email],
                fail_silently=True,
            )
            
            messages.success(request, 'Order placed successfully!')
            return redirect('shop:order_confirmation', order_id=order.id)
            
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return redirect('shop:checkout')
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'categories': Category.objects.filter(is_active=True),
    }
    return render(request, 'shop/checkout.html', context)


@login_required
def order_confirmation(request, order_id):
    """Order confirmation view"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    context = {
        'order': order,
        'categories': Category.objects.filter(is_active=True),
    }
    return render(request, 'shop/order_confirmation.html', context)


@login_required
def order_history(request):
    """Order history view"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'orders': orders,
        'categories': Category.objects.filter(is_active=True),
    }
    return render(request, 'shop/order_history.html', context)


@login_required
def order_detail(request, order_id):
    """Order detail view"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    context = {
        'order': order,
        'categories': Category.objects.filter(is_active=True),
    }
    return render(request, 'shop/order_confirmation.html', context)
