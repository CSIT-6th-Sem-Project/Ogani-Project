from django.urls import path
from .views import *
from store.views import BaseView
urlpatterns = [

    path("", WishListView.as_view(extra_context=BaseView.view), name='wishlist'),
    path("add-to-wishlist/<slug>", add_to_wishlist, name='add_to_wishlist'),
    path("update-wishlist", update_wishlist, name='update_wishlist'),
    path("move-single-cart/<slug>", move_single_to_cart, name='move_single_cart'),
    path("move-all-cart", move_all_to_cart, name='move_all_cart'),
    path("remove-wishlist/<slug>", remove_wishlist, name='remove_wishlist'),

]