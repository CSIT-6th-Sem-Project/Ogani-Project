from django.utils.deprecation import MiddlewareMixin
from wishlist_app.models import Wishlist
from cart_app.models import Cart

# custom middle ware for updating users session information
class UpdateUserSessionMiddleWare(MiddlewareMixin):
    def process_request(self, request):
        if (request.user.is_authenticated):
            request.session['wishlist'] = {wlist.slug: wlist.items.slug for wlist in
                                           Wishlist.objects.filter(user=request.user)}

            request.session['wishlist_count'] = Wishlist.objects.filter(user=request.user).count()
            request.session['cart_count'] = Cart.objects.filter(user=request.user,checkout=False).count()

            cart_items = Cart.objects.filter(user=request.user,checkout = False).values_list('total')
            total = 0
            for item in cart_items:
                total += item[0]
            request.session['total_cart_price'] = total
