from django.urls import path

from .views import *
urlpatterns = [
    path('',HomeView.as_view(),name = 'home'),
    path('contact-us',ContactView.as_view(),name='contact'),
    path('cart',CartView.as_view(),name='cart'),
    path('wishlist',WishListView.as_view(),name='wishlist'),
    path('signup', signup, name='signup'),
    path('search',search,name='search'),
    path('add-to-cart/<slug>',add_to_cart,name='add_to_cart'),
    path('remove-from-cart/<slug>',remove_from_cart,name='remove_from_cart'),
    path('update_cart',update_cart,name='update_cart')
]