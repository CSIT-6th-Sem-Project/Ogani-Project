from django.db import models

# Create your models here.
from store.models import *

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
