from django.urls import path

from .views import *

view = BaseView.view

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contact-us', ContactView.as_view(), name='contact'),

    path('product-detail/<slug>',ProductDetailView.as_view(),name='product_detail'),

    path("add-product-review/<slug>",add_product_review,name="add_product_review"),

    path('signup', signup, name='signup'),
    path('search', search, name='search'),




]


