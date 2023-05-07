from django.shortcuts import render ,redirect
from django.contrib.auth.models import User
from django.contrib import messages
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



def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        username = request.POST['username'],
        phone = request.POST['phone'],
        email = request.POST['email'],
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        if password == cpassword:
            if User.objects.filter(username = username).exists():
                messages.error(request,'The username is already taken')
                return redirect('/signup')
            elif User.objects.filter(phone = phone).exists():
                messages.error(request,'The phone number already exists')
                return redirect('/signup')
            elif User.objects.filter(email = email).exists():
                messages.error(request,'The email already exists')
                return redirect('/signup')

            else:
                data = User.objects.create(
                    first_name = first_name,
                    last_name = last_name,
                    username = username,
                    phone  = phone,
                    email = email,
                    password = password
                )
                data.save()
        else:
            messages.error(request,'The password does not match')
            return redirect('/signup')

    return render(request,'signup.html')

