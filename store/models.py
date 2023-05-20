from binascii import hexlify

from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from django.core.validators import MaxValueValidator, MinValueValidator

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
    price = models.FloatField(validators=[MinValueValidator(0.0)])
    picture = models.ImageField(upload_to='products')
    description = models.TextField(blank=True)
    information = models.TextField(blank=True)
    weight = models.FloatField()
    labels = models.CharField(choices=LABELS,max_length=100)
    department = models.ForeignKey(Department,on_delete=models.DO_NOTHING)
    category = models.ForeignKey(Category,on_delete=models.DO_NOTHING)
    discount = models.FloatField(default=0.0,validators=[
        MaxValueValidator(100.0),MinValueValidator(0.0)])
    rating = models.IntegerField(default=0,validators=[
        MinValueValidator(0),MaxValueValidator(100)])
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


class Product_Images(BaseModel):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='product_images')
    image = models.ImageField(upload_to='products/details')
    thumb = models.ImageField(upload_to='products/details/thumbnail')

    def __str__(self):
        return f"{self.product.name} {self.created_at}"






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

class ProductReview(BaseModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MaxValueValidator(5),MinValueValidator(1)])
    review = models.TextField()

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            rand = os.urandom(32)
            rand = hexlify(rand)
            self.slug = slugify(self.user.username + " "+self.product.name+" "+ rand.decode())

        return super(ProductReview,self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} - {self.created_at}"



