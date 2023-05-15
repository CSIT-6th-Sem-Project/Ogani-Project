from binascii import hexlify

from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
import os
# Create your models here.
LABELS = (
    ('hot','Hot'),
    ('new','New'),
    ('sale','Sale'),
    ('default','Default')
)


STOCK=(
    ('in_stock','In Stock'),
    ('out_stock','Out of stock')
)

class BaseModel(models.Model):
    slug = models.SlugField(max_length=200,unique=True,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Department(BaseModel):
    dept_name = models.CharField(max_length=200,unique=True)
    image = models.ImageField(upload_to="department",null=True)

    def __str__(self):
        return f"{self.dept_name}"

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.dept_name)
        return super(Department,self).save(*args, **kwargs)

    class Meta:
        ordering = ['dept_name']

class Category(BaseModel):
    cname = models.CharField(max_length=200)
    dept = models.ForeignKey(Department,on_delete=models.CASCADE)
    image = models.ImageField(null=True,upload_to="categories",blank=True)
    labels = models.CharField(choices=LABELS,max_length=100,default=LABELS[1][0])

    def __str__(self):
        return f"{self.cname}"

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.cname)
        return super(Category,self).save(*args, **kwargs)

class Product(BaseModel):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    picture = models.ImageField(upload_to='products')
    description = models.TextField(blank=True)
    information = models.TextField(blank=True)
    weight = models.FloatField()
    labels = models.CharField(choices=LABELS,max_length=100)
    department = models.ForeignKey(Department,on_delete=models.DO_NOTHING)
    category = models.ForeignKey(Category,on_delete=models.DO_NOTHING)
    discount = models.FloatField(default=0.0)
    rating = models.FloatField(default=0)
    stock = models.CharField(choices=STOCK,default=STOCK[0][0],max_length=100)

    @property
    def discounted_price(self):
        if(self.discount > 0.0):
            price = self.price - (self.discount/100) * self.price
            return price
        else:
            return self.price

    def save(self, *args, **kwargs):  # new
        rand = os.urandom(12)
        rand = hexlify(rand)
        if not self.slug:
            self.slug = slugify(self.name+" "+rand.decode())
        return super(Product,self).save(*args, **kwargs)


    def __str__(self):
        return f"{self.name}"



class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    total = models.FloatField()
    quantity = models.IntegerField(default=1)
    checkout = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} : {self.slug}"

    def save(self, *args, **kwargs):  # new

        if not self.slug:
            rand = os.urandom(32)
            rand = hexlify(rand)
            self.slug = slugify(self.user.username+" "+rand.decode())

        if self.quantity > 1:
            self.total = self.product.discounted_price * self.quantity


        return super(Cart,self).save(*args, **kwargs)


class Wishlist(BaseModel):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    items = models.ForeignKey(Product , on_delete = models.CASCADE)
    quantity = models.IntegerField(default=1)
    total = models.FloatField()

    def __str__(self):
        return f"< {self.user.username}  : {self.items.name} >"

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            rand = os.urandom(32)
            rand = hexlify(rand)
            self.slug = slugify(self.user.username + " " + rand.decode())

        if self.quantity > 1:
            self.total = self.items.discounted_price * self.quantity

        return super(Wishlist,self).save(*args, **kwargs)


class Billing(BaseModel):
    first_name = models.CharField(max_length=500)
    last_name = models.CharField(max_length = 600)
    email = models.EmailField(max_length=200)
    mobile_no = models.BigIntegerField()
    address = models.TextField()
    country = models.CharField(max_length=500)
    city = models.CharField(max_length=400)
    state = models.CharField(max_length=500,blank=True)
    zip_code = models.IntegerField()

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            rand = os.urandom(32)
            rand = hexlify(rand)
            self.slug = slugify(self.first_name + " " + rand.decode())
        return super(Billing,self).save(*args, **kwargs)

class Blog(BaseModel):
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=600)
    description = models.TextField()
    content = models.TextField()
    image = models.ImageField(upload_to='blog')
    likes = models.IntegerField()

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            rand = os.urandom(32)
            rand = hexlify(rand)
            self.slug = slugify("blog "+self.user.username + " "+ rand.decode()+f" {self.id}")
        return super(Blog,self).save(*args, **kwargs)




