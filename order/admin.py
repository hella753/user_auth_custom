from django.contrib import admin
from order.models import Checkout, Cart, CartItems


@admin.register(CartItems)
class CartItemsAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'product_quantity', 'cart' )
    list_prefetch_related = ('product', 'cart')
    search_fields = ('id', 'cart__user__username', 'product__product_name')
    list_per_page = 10


@admin.register(Checkout)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'country', 'order_date', 'product_cart' )
    list_filter = ('order_date',)
    list_prefetch_related = ('product_cart',)
    search_fields = ('id', 'country')
    list_per_page = 10


@admin.register(Cart)
class UserCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'flat_rate')
    list_select_related = ('user',)
    search_fields = ('user__username',)
    list_per_page = 10