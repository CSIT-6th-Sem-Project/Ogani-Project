from django.urls import path

from .views import HomeView,ContactView,CartView,WishListView
urlpatterns = [
    path('',HomeView.as_view(),name = 'home'),
    path('contact-us',ContactView.as_view(),name='contact'),
    path('cart',CartView.as_view(),name='cart'),
    path('wishlist',WishListView.as_view(),name='wishlist')
    path('signup', signup, name='signup')
]