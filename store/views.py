from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from django.db.models import Q

def convert_to_twodarray(item):
    gap = 3
    return [item[i:i + gap] for i in range(0, len(item), gap)]


class BaseView(View):
    view = dict()

    view['Departments'] = Department.objects.all()
    view['Categories'] = Category.objects.all()
    latest = Product.objects.filter(labels='new')
    view['hot'] = Product.objects.filter(labels='hot')
    # filter products with rating greater than or equal to 4
    top_rated = Product.objects.filter(rating__gte=4)
    # filter products with discount greater than 20%
    discounted = Product.objects.filter(discount__gte=20.0)

    view['Discounted_Products'] = convert_to_twodarray(discounted)
    view['Latest_Products'] = convert_to_twodarray(latest)
    view['Top_Rated_Products'] = convert_to_twodarray(top_rated)
    view['Featured_Categories'] = Category.objects.filter(labels='hot')
    view['Featured_Products'] = {cat.cname: Product.objects.filter(category=cat) for cat in view['Featured_Categories']}





class HomeView(BaseView):
    def get(self, request):
        self.view

        return render(request, 'index.html', self.view)


class ContactView(BaseView):

    def get(self, request):
        self.view
        return render(request, 'contact.html', self.view)


class ProductDetailView(BaseView, DetailView):
    model = Product
    template_name = "shop-details.html"
    context_object_name = "product"

    def calc_average_rating(self,context):
        if context['Reviews'].count() > 0:
            five_star = context['Reviews'].filter(rating=5).count()
            four_star = context['Reviews'].filter(rating=4).count()
            three_star = context['Reviews'].filter(rating=3).count()
            two_star = context['Reviews'].filter(rating=2).count()
            one_star = context['Reviews'].filter(rating=1).count()
            average_rating = int(
                (one_star + 2 * two_star + 3 * three_star + 4 * four_star + 5 * five_star) / context[
                    'Reviews'].count())
        else:
            average_rating = 0

        return average_rating

    def get_context_data(self, *args, **kwargs):
        self.view
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        context.update(self.view)
        obj = kwargs['object']
        context['Related_Products'] = Product.objects.filter(category = obj.category)
        context['Reviews'] = ProductReview.objects.filter(product__slug = obj.slug)
        context['Avg_Review'] = self.calc_average_rating(context)
        return context

def add_product_review(request,slug):
    if(request.method == "POST"):
        rating = int(request.POST['rating'])
        product = get_object_or_404(Product,slug = slug)
        review = request.POST["review"]
        if(rating >= 1 and len(review) > 10):
            review_obj = ProductReview.objects.create(user = request.user , product = product,review= review,rating =rating)
            review_obj.save()
            messages.success(request,"Review Posted Successfully")
        else:
            messages.error(request,"Please Enter a valid Review length must be greater than 10")

    return redirect(request.META['HTTP_REFERER'])

def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'The username is already taken')
                return redirect('/signup')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'The email already exists')
                return redirect('/signup')
            else:
                data = User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=email,
                    password=password
                )
                data.save()
                messages.success(request, "Registered Successfully !!")
                return redirect('/login')
        else:
            messages.error(request, 'The password does not match')
            return redirect('/signup')

    view = BaseView.view
    return render(request, 'signup.html', view)


# Cart Based Views
class CartView(BaseView, ListView):
    model = Cart
    template_name = "shopping-cart.html"
    context_object_name = 'cart_items'

    def get_queryset(self):
        user_cart_items = Cart.objects.filter(user=self.request.user)
        return user_cart_items



def add_to_cart(request, slug):
    if request.method == "POST":
        product = get_object_or_404(Product, slug=slug)
        try:
            quantity = int(request.POST["quantity"])
            if (not Cart.objects.filter(user=request.user, product=product).exists()):
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
        user_cart = Cart.objects.filter(user=request.user)

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
    cart = get_object_or_404(Cart, slug=slug, user=request.user)
    cart.delete()
    messages.success(request, message=f"{cart.product.name} removed from the cart")
    return redirect("cart")


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

def search(request):
    query = request.GET['query']
    query = query.split('')
    search_result = Product.objects.filter(name__in=query) and Product.objects.filter(description__in=query)
    return redirect('/')
