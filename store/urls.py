from django.urls import path

from .views import *

view = BaseView.view

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contact-us', ContactView.as_view(), name='contact'),

    path('product-detail/<slug>',ProductDetailView.as_view(),name='product_detail'),

    path('cart', CartView.as_view(extra_context=view), name='cart'),
    path('cart/add-to-cart/<slug>', add_to_cart, name='add_to_cart'),
    path('cart/remove-from-cart/<slug>', remove_from_cart, name='remove_from_cart'),
    path('cart/update_cart', update_cart, name='update_cart'),

    path("wishlist", WishListView.as_view(extra_context=view), name='wishlist'),
    path("wishlist/add-to-wishlist.<slug>",add_to_wishlist,name='add_to_wishlist'),
    path("wishlist/update-wishlist",update_wishlist,name='update_wishlist'),
    path("wishlist/move-single-cart/<slug>",move_single_to_cart,name='move_single_cart'),
    path("wishlist/move-all-cart",move_all_to_cart,name='move_all_cart'),
    path("wishlist/remove-wishlist/<slug>",remove_wishlist,name='remove_wishlist'),

    path("add-product-review/<slug>",add_product_review,name="add_product_review"),

    path('signup', signup, name='signup'),
    path('search', search, name='search'),



    path('add-to-wishlist/<slug>', add_to_wishlist, name="add_to_wishlist"),

]
