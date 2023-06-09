"""
URL configuration for Organi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views
from store.forms import UserAuthForm
from store.views import BaseView

view = BaseView.view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('store.urls')),
    path('login', views.LoginView.as_view(
        template_name="registration/login.html",
        authentication_form=UserAuthForm,
        extra_context = view
    ), name="login"),
    path('logout',views.LogoutView.as_view()),

    path('payment/',include('payment_app.urls')),

    path('cart/',include('cart_app.urls')),
    path('wishlist/',include(('wishlist_app.urls')))
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
