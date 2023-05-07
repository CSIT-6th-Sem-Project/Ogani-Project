from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Product)

admin.site.register(Department)

admin.site.register(Category)

admin.site.register(Cart)

admin.site.register(Wishlist)

admin.site.register(Billing)

admin.site.register(Blog)
