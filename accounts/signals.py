from allauth.account.signals import user_logged_in
from django.dispatch import receiver
from cart.utils import merge_session_cart_to_db

@receiver(user_logged_in)
def merge_cart_on_login(request, user, **kwargs):
    merge_session_cart_to_db(request, user)
