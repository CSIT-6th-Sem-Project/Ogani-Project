from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View

class BaseView(View):
    view = dict()
    view['Departments'] = (
        'Fresh Meat',
        'Vegetables',
        'Fruit and Nut Gifts',
        'Fresh Berries',
        'Ocean Foods',
        'Butter and Eggs',
        'Fastfood',
        'Fresh Onion',
        'Papaya and Crisps',
        'Oat Meals',
        'Fresh Bananas'
    )

class HomeView(BaseView):
    def get(self,request):
        self.view
        self.view['Title'] = 'Home'
        return render(request,'index.html',self.view)


class ContactView(BaseView):

    def get(self,request):
        self.view
        return render(request,'contact.html',self.view)



