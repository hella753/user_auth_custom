from django.db.models.signals import post_save
from django.dispatch import receiver
from user.models import User
from order.models import Cart


@receiver(post_save, sender=User)
def create_cart_for_user(sender, **kwargs):
    user_obj = kwargs.get("instance")
    if not user_obj.is_superuser:
        cart = Cart(user=user_obj, flat_rate=5)
        cart.save()
        print(f"cart has been created {user_obj}")