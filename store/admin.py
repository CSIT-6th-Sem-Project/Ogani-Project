from django.contrib import admin
from .models import *
from django.contrib import admin
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','price','category','department','labels']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['cname','dept','labels']

admin.site.register(Product,ProductAdmin)

admin.site.register(Department)

admin.site.register(Category,CategoryAdmin)


