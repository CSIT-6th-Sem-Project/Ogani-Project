from django.urls import path
from .views import *

urlpatterns = [
    path('',HomeView.as_view(),name = 'home'),
    path('contact-us',ContactView.as_view(),name='contact'),
    path('signup', signup, name='signup'),
]