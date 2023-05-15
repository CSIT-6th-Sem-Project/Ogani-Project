
from .models import *
from django.shortcuts import render ,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.
from django.views.generic.base import View
from django.views.generic.list import ListView

def convert_to_twodarray(item):
    gap = 3
    return [item[i:i + gap] for i in range(0, len(item), gap)]

class BaseView(View):
    view = dict()
    view['Departments'] = Department.objects.all()
    view['Categories'] = Category.objects.all()


    latest = Product.objects.filter(labels ='new')
    view['hot']= Product.objects.filter(labels='hot')
    # filter products with rating greater than or equal to 4
    top_rated = Product.objects.filter(rating__gte=4)
    # filter products with discount greater than 20%
    discounted = Product.objects.filter(discount__gte=20.0)

    view['Discounted_Products'] = convert_to_twodarray(discounted)
    view['Latest_Products'] = convert_to_twodarray(latest)
    view['Top_Rated_Products'] = convert_to_twodarray(top_rated)


    view['Featured_Categories'] = Category.objects.filter(labels = 'hot')
    view['Featured_Products'] = { cat.cname:Product.objects.filter(category = cat) for cat in view['Featured_Categories']}


    view['Title'] = None

class HomeView(BaseView):
    def get(self,request):
        self.view

        #if(request.user.is_authenticated):
            #self.view['Wishlist'] = [ wishlist.items.slug for wishlist in Wishlist.objects.filter(user=request.user)]
        return render(request,'index.html',self.view)

class ContactView(BaseView):

    def get(self,request):
        self.view
        return render(request,'contact.html',self.view)

class CartView(BaseView,ListView):
    model = Cart
    template_name = "shopping-cart.html"
    context_object_name = 'cart_items'


    def get_queryset(self):
        user_cart_items = Cart.objects.filter(user=self.request.user)
        return user_cart_items


def add_to_cart(request,slug):
    product = get_object_or_404(Product,slug = slug)
    if(not Cart.objects.filter(user = request.user,product=product).exists()):
        cart_obj = Cart.objects.create(user=request.user,product=product,total=product.discounted_price)
        cart_obj.save()
        messages.success(request,message=f"{product.name} added to your cart")
    else:
        cart = get_object_or_404(Cart,user=request.user,product=product)
        cart.quantity += 1
        cart.save()
        messages.info(request,message=f"{product.name} already added to cart increased quantity by one")

    return redirect(request.META['HTTP_REFERER'])

def add_to_wishlist(request,slug):
    product = get_object_or_404(Product, slug=slug)
    if (not Wishlist.objects.filter(user=request.user, items=product).exists()):
        wish_obj = Wishlist.objects.create(user=request.user, items=product,total=product.discounted_price)
        wish_obj.save()
        messages.success(request, message=f"{product.name} added to your wishlist")
    else:
        cart = get_object_or_404(Cart, user=request.user, items=product)
        cart.delete()
        messages.info(request, message=f"{product.name} removed from the wishlist")

    return redirect(request.META['HTTP_REFERER'])

def update_cart(request):
    if (request.method == "POST"):
        user_cart = Cart.objects.filter(user = request.user)

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
                messages.error(request,"Please enter a valid quantity")
                return redirect("cart")

        messages.success(request,"Cart updated Successfully")
        return redirect("cart")

def remove_from_cart(request,slug):
    cart = get_object_or_404(Cart,slug=slug,user=request.user)
    cart.delete()
    messages.success(request,message=f"{cart.product.name} removed from the cart")
    return redirect("cart")

class WishListView(BaseView,ListView):
    model = Wishlist
    template_name = "shopping-wishlist.html"
    context_object_name = 'wishlist_items'

    def get_queryset(self):
        users_wishlist = Wishlist.objects.filter(user =self.request.user)
        return users_wishlist

def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        if password == cpassword:
            if User.objects.filter(username = username).exists():
                messages.error(request,'The username is already taken')
                return redirect('/signup')
            elif User.objects.filter(email = email).exists():
                messages.error(request,'The email already exists')
                return redirect('/signup')
            else:
                data = User.objects.create_user(
                    first_name = first_name,
                    last_name = last_name,
                    username = username,
                    email = email,
                    password = password
                )
                data.save()
                messages.success(request,"Registered Successfully !!")
                return redirect('/login')
        else:
            messages.error(request,'The password does not match')
            return redirect('/signup')

    view = BaseView.view
    view['Title'] = 'Signup'
    return render(request,'signup.html',view)

def search(request):
    query = request.GET['query']
    query = query.split('')
    search_result = Product.objects.filter(name__in=query) and Product.objects.filter(description__in=query)
    return redirect('/')