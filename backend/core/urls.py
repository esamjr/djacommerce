from django.urls import path
from django.views.decorators.cache import cache_page
try:
    from core.views import (
                    Home,
                    OrderSummary,
                    ProductDetail,
                    CheckoutView
                    )
    from core.cart_views import (
                    add_to_cart,
                    remove_from_cart,
                    decrease_quantity,
                    increase_quantity
                    )

except ImportError:
    raise ImportError(
        "views doesn't contain some class or method"
    )

app_name = 'core'

urlpatterns = [
    # home
    path('', Home.as_view(), name='home'),
    # checkout
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    # user cart
    path('order-summary/', OrderSummary.as_view(), name='order-summary'),
    # detail of product
    path('product/<slug>', ProductDetail.as_view(), name='product'),
    # add product to cart
    path('add-to-cart/<slug>', add_to_cart, name='add-to-cart'),
    # remove product from cart
    path('remove-from-cart/<slug>', remove_from_cart, name='remove-from-cart'),
    # decrease quantity of an item in cart
    path('decrease-quantity/<slug>',
         decrease_quantity, name='decrease-quantity'),
    # increase quantity of an item in cart
    path('increase-quantity/<slug>',
         increase_quantity, name='increase-quantity'),
]
