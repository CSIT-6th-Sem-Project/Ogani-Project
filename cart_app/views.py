from django.shortcuts import render
from django.views.generic import ListView
from .models import *
from store.views import BaseView
from django.shortcuts import get_object_or_404,redirect,render
from django.contrib import messages

# Create your views here.
class CartView(BaseView, ListView):
    model = Cart
    template_name = "shopping-cart.html"
    context_object_name = 'cart_items'

    def get_queryset(self):
        user_cart_items = Cart.objects.filter(user=self.request.user,checkout=False)
        return user_cart_items



def add_to_cart(request, slug):
    if request.method == "POST":
        product = get_object_or_404(Product, slug=slug)
        try:
            quantity = int(request.POST["quantity"])
            if (not Cart.objects.filter(user=request.user, product=product,checkout=False).exists()):
                cart_obj = Cart.objects.create(user=request.user, product=product, quantity = quantity,total=product.discounted_price*quantity)
                cart_obj.save()
                messages.success(request, message=f"{product.name} added to your cart")
            else:
                cart = get_object_or_404(Cart, user=request.user, product=product)
                cart.quantity += quantity
                cart.save()
                messages.info(request, message=f"{product.name} already added to cart increased quantity by one")
        except ValueError:
            messages.error(request, "Please enter a valid quantity")
        finally:
            return redirect(request.META['HTTP_REFERER'])

    return redirect(request.META['HTTP_REFERER'])

def update_cart(request):
    if (request.method == "POST"):
        user_cart = Cart.objects.filter(user=request.user,checkout=False)

        for cart in user_cart:
            try:
                new_quantity = int(request.POST[cart.slug])
                print(new_quantity)
                if new_quantity <= 0:
                    cart.delete()
                elif cart.quantity != new_quantity:
                    cart.quantity = new_quantity
                    cart.save()

            except ValueError:
                messages.error(request, "Please enter a valid quantity")
                return redirect("cart")

        messages.success(request, "Cart updated Successfully")


    return redirect("cart")

def remove_from_cart(request, slug):
    cart = get_object_or_404(Cart, slug=slug, user=request.user,checkout=False)
    cart.delete()
    messages.success(request, message=f"{cart.product.name} removed from the cart")
    return redirect("cart")