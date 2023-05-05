from django.db import models

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

class Department(models.Model):
    slug = models.CharField(max_length=200,unique=True)
    dept_name = models.CharField(max_length=200,unique=True)

    def __str__(self):
        return f"<{self.dept_name}>"

class Category(models.Model):
    slug = models.CharField(max_length=200,unique=True)
    cname = models.CharField(max_length=200)




class Products(models.Model):
    slug = models.CharField(unique=True,max_length=300)
    name = models.CharField(max_length=200)
    price = models.FloatField()
    picture = models.ImageField(upload_to='media')
    description = models.TextField()
    information = models.TextField()
    weight = models.FloatField()
    labels = models.CharField(choices=LABELS,max_length=100)
    department = models.ForeignKey(Department,on_delete=models.DO_NOTHING)
    category = models.ForeignKey(Category,on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"<{self.name}>:<{id}>"


