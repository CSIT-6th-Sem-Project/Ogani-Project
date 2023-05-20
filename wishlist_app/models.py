from django.db import models
from store.models import *

# Create your models here.
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
            self.slug = slugify(f"wishlist {self.user.username} {rand.decode()}")

        if self.quantity > 1:
            self.total = self.items.discounted_price * self.quantity

        return super(Wishlist,self).save(*args, **kwargs)
