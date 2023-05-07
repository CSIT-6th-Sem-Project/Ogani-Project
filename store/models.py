from django.db import models
from django.contrib.auth.models import User

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
    slug = models.SlugField(max_length=200,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Department(BaseModel):
    dept_name = models.CharField(max_length=200,unique=True)
    image = models.ImageField(upload_to="department",null=True)

    def __str__(self):
        return f"<{self.dept_name}>"

    class Meta:
        ordering = ['dept_name']

class Category(BaseModel):
    cname = models.CharField(max_length=200)
    dept = models.ForeignKey(Department,on_delete=models.CASCADE)
    image = models.ImageField(null=True,upload_to="categories")

    def __str__(self):
        return f"<{self.cname}>"

class Product(BaseModel):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    picture = models.ImageField(upload_to='products')
    description = models.TextField()
    information = models.TextField()
    weight = models.FloatField()
    labels = models.CharField(choices=LABELS,max_length=100)
    department = models.ForeignKey(Department,on_delete=models.DO_NOTHING)
    category = models.ForeignKey(Category,on_delete=models.DO_NOTHING)
    discount = models.FloatField(default=0.0)
    rating = models.FloatField(default=0)



    def __str__(self):
        return f"<{self.name}>:<{id}>"


class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    total = models.FloatField()
    quantity = models.IntegerField()
    checkout = models.BooleanField(default=False)

    def __str__(self):
        return f"<{self.user.username} : {self.slug}>"



class Wishlist(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    items = models.ForeignKey(Product , on_delete = models.CASCADE)
    price = models.IntegerField()

    def __str__(self):
        return f"< {self.user.username}  : {self.items.pname} >"




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

class Blog(BaseModel):
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=600)
    description = models.TextField()
    content = models.TextField()
    image = models.ImageField(upload_to='blog')
    likes = models.IntegerField()





