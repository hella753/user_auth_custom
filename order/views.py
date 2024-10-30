from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F
from django.db.models.functions import Round
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, ListView
from order.forms import CartItemForm
from order.models import Cart, CartItems
from utils.utils import set_activity_expiry


@method_decorator(login_required, name='dispatch')
class CartView(ListView):
    model = CartItems
    template_name = "cart/cart.html"
    context_object_name = "cartitems"

    def get(self, *args, **kwargs):
        if self.request.GET.get('q'):
            set_activity_expiry(self.request)
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


@method_decorator(login_required, name='dispatch')
class CheckoutView(ListView):
    model = CartItems
    template_name = "checkout/chackout.html"
    context_object_name = "cartitems"

    def get(self, *args, **kwargs):
        if self.request.GET.get('q'):
            set_activity_expiry(self.request)
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


@method_decorator(login_required, name='dispatch')
class AddToCartView(CreateView):
    model = CartItems
    form_class = CartItemForm

    def get_success_url(self):
        set_activity_expiry(self.request)
        return self.request.META.get('HTTP_REFERER', '')

    def form_valid(self, form):
        new_item = form.save(commit=False)
        new_item.cart_id = self.request.user.id
        new_item.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors.as_json())
        return redirect(self.request.META.get('HTTP_REFERER', ''))


@method_decorator(login_required, name='dispatch')
class AddToCartDeleteView(DeleteView):
    model = CartItems

    def get_success_url(self):
        set_activity_expiry(self.request)
        return reverse_lazy("order:cart")

