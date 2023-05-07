from django.shortcuts import render
from .models import *
# Create your views here.
from django.views.generic.base import View

class BaseView(View):
    view = dict()
    view['Departments'] = Department.objects.all()
    view['Categories'] = Category.objects.all()
    view['Title'] = None

class HomeView(BaseView):
    def get(self,request):
        self.view
        self.view['Title'] = 'Home'
        return render(request,'index.html',self.view)


class ContactView(BaseView):

    def get(self,request):
        self.view
        self.view['Title'] = 'Contact'
        return render(request,'contact.html',self.view)


class CartView(BaseView):

    def get(self,request):
        self.view
        self.view['Title'] = 'Cart'
        return render(request,'shopping-cart.html',self.view)


class WishListView(BaseView):
    def get(self,request):
        self.view
        self.view['Title'] = 'WishList'
        return render(request,'shopping-wishlist.html',self.view)


