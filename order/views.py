from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.db.models.functions import Round
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView
from order.forms import CartItemForm
from order.models import CartItem


class CartView(LoginRequiredMixin, ListView):
    model = CartItem
    template_name = "cart/cart.html"
    context_object_name = "cart_items"

    def get(self, *args, **kwargs):
        if self.request.GET.get('q'):
            return redirect(f'/category/?q={self.request.GET.get('q')}')
        return super().get(*args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(
            total_price=Round(
                F("product_quantity")*F("product__product_price")
            )
        ).filter(cart__user_id=self.request.user.id)
        return queryset.select_related("product")


class CheckoutView(LoginRequiredMixin, ListView):
    model = CartItem
    template_name = "checkout/chackout.html"
    context_object_name = "cart_items"

    def get(self, *args, **kwargs):
        if self.request.GET.get('q'):
            return redirect(f'/category/?q={self.request.GET.get('q')}')
        return super().get(*args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(
            total_price=Round(
                F("product_quantity")*F("product__product_price")
            )
        ).filter(cart__user_id=self.request.user.id)
        return queryset.select_related("product")


class AddToCartView(LoginRequiredMixin, CreateView):
    model = CartItem
    form_class = CartItemForm

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER', '')

    def form_valid(self, form):
        new_item = form.save(commit=False)
        new_item.cart_id = self.request.user.id
        new_item.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors.as_json())
        return redirect(self.request.META.get('HTTP_REFERER', ''))


class AddToCartDeleteView(LoginRequiredMixin, DeleteView):
    model = CartItem

    def get_success_url(self):
        return reverse_lazy("order:cart")
