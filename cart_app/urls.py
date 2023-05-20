
from django.urls import path
from .views import *


urlpatterns = [
    path('', CartView.as_view(extra_context=BaseView.view), name='cart'),
    path('add-to-cart/<slug>', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<slug>', remove_from_cart, name='remove_from_cart'),
    path('update_cart', update_cart, name='update_cart'),
]