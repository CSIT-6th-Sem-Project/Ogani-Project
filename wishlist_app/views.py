from django.shortcuts import render
from django.views.generic import ListView
from .models import *
from store.views import BaseView
from django.shortcuts import get_object_or_404,redirect,render
from django.contrib import messages

from cart_app.models import Cart

# Create your views here.
#

# Wishlist Based Views
class WishListView(BaseView, ListView):
    model = Wishlist
    template_name = "shopping-wishlist.html"
    context_object_name = 'wishlist_items'

    def get_queryset(self):
        users_wishlist = Wishlist.objects.filter(user=self.request.user)
        return users_wishlist

def add_to_wishlist(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if (not Wishlist.objects.filter(user=request.user, items=product).exists()):
        wish_obj = Wishlist.objects.create(user=request.user, items=product, total=product.discounted_price)
        wish_obj.save()
        messages.success(request, message=f"{product.name} added to your wishlist")
    else:
        cart = get_object_or_404(Cart, user=request.user, items=product)
        cart.delete()
        messages.info(request, message=f"{product.name} removed from the wishlist")

    return redirect(request.META['HTTP_REFERER'])

def update_wishlist(request):
    if (request.method == "POST"):
        user_wishlist = Wishlist.objects.filter(user=request.user)
        for wlist in user_wishlist:
            try:
                new_quantity = int(request.POST[wlist.slug])
                print(new_quantity)
                if new_quantity <= 0:
                    wlist.delete()
                elif wlist.quantity != new_quantity:
                    wlist.quantity = new_quantity
                    wlist.save()

            except ValueError:
                messages.error(request, "Please enter a valid quantity")
                return redirect("wishlist")

        messages.success(request, "Wishlist updated Successfully")
        return redirect("wishlist")

def remove_wishlist(request, slug):
    wlist = get_object_or_404(Wishlist, items__slug=slug, user=request.user)
    wlist.delete()
    messages.success(request, message=f"{wlist.items.name} removed from the wishlist")
    return redirect(request.META['HTTP_REFERER'])

def move_to_cart(request, wlist_single):
    if (not Cart.objects.filter(user=request.user, product__slug=wlist_single.items.slug).exists()):
        cart_obj = Cart.objects.create(
            user=request.user,
            product=wlist_single.items,
            quantity=wlist_single.quantity,
            total=wlist_single.items.discounted_price * wlist_single.quantity
        )
        cart_obj.save()
        wlist_single.delete()
        messages.success(request, f"{wlist_single.items.name} added to your cart")
    else:
        cart_obj = get_object_or_404(Cart, user=request.user, product__slug=wlist_single.items.slug)
        cart_obj.quantity += wlist_single.quantity
        wlist_single.delete()
        cart_obj.save()
        messages.info(request, f"{wlist_single.items.name} already on cart ... updating the quantity")

def move_single_to_cart(request, slug):
    wlist_single = get_object_or_404(Wishlist, user=request.user, slug=slug)
    move_to_cart(request, wlist_single)
    return redirect("wishlist")

def move_all_to_cart(request):
    wlist_items = Wishlist.objects.filter(user=request.user)
    for wlist_single in wlist_items:
        move_to_cart(request, wlist_single)

    return redirect("wishlist")


###