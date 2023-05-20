from django.db import models
import os
from binascii import hexlify
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from django.template.loader import get_template
from xhtml2pdf import pisa


# Create your models here.
from store.models import *

class Order(BaseModel):
    CASH_ON_DELIVERY = 'cash-on-delivery'
    EPAYMENT = 'e-payment'

    SHIPPING = 99

    SHIPPED = "shipped"
    ORDERED = "ordered"
    PENDING = "pending"

    ORDER_STATUS = (
        (SHIPPED,'Shipped'),
        (ORDERED,'Ordered'),
        (PENDING,'Pending')
    )
    PAYMENT_CHOICES = (
        (CASH_ON_DELIVERY, 'Cash on Delivery'),
        (EPAYMENT,"E-payment")
    )

    user = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='billing_user')
    first_name = models.CharField(max_length=500)
    last_name = models.CharField(max_length = 600)
    email = models.EmailField(max_length=200)
    phone = models.BigIntegerField()
    address = models.TextField()
    city = models.CharField(max_length=400)
    shipping_address = models.TextField(blank=True)
    payment_type = models.CharField(choices=PAYMENT_CHOICES,max_length=100,default=PAYMENT_CHOICES[1][0])
    order_notes = models.TextField(blank=True)

    paid = models.BooleanField(default=False)
    status = models.CharField(max_length=100,choices=ORDER_STATUS,default=ORDERED)


    def save(self, *args, **kwargs):
        if not self.slug:
            rand = os.urandom(32)
            rand = hexlify(rand)
            self.slug = slugify(f"order {self.user.username} {rand.decode()}")

        return super(Order,self).save(*args, **kwargs)

    @property
    def total_payment(self):
        total = 0
        order_items = OrderItem.objects.filter(order = self)
        for item in order_items:
            total += item.price
        return total

class OrderItem(BaseModel):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name="order_items_order")
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.FloatField(default=0.0)

    def save(self, *args, **kwargs):
        if not self.slug:
            rand = os.urandom(32)
            rand = hexlify(rand)
            self.slug = slugify(f"order item {self.product.name} {rand.decode()}")


        self.price = self.product.discounted_price * self.quantity

        return super(OrderItem,self).save(*args, **kwargs)

class KhaltiTransactionRecord(BaseModel):
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name="khalti_tran_user")
    transaction = models.TextField()
    def save(self,*args,**kwargs):
        def save(self, *args, **kwargs):  # new
            if not self.slug:
                rand = os.urandom(32)
                rand = hexlify(rand)
                self.slug = slugify(f"khalti transaction {self.user.username} {rand.decode()}")
            return super(KhaltiTransactionRecord, self).save(*args, **kwargs)


