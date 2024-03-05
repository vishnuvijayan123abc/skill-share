from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


# Create your models here.
class Userprofile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    profile_pic=models.ImageField(upload_to="profile_pics",default='default.webp',null=True)
    bio=models.CharField(max_length=200)
    option=(
        ("drawing","drawing"),
        ("communication","communication"),
        ("crafting","crafting"),
        ("coding","coding")
    )
    skills=models.CharField(max_length=200,choices=option)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    media=models.FileField(upload_to="product_media")
    description=models.CharField(max_length=200)
    price=models.PositiveIntegerField()
    created_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Cart(models.Model):
    
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="cart")
    created_at=models.DateTimeField(auto_now_add=True)
    

    @property
    def cartitems(self):
        qs=self.cartitems.all()
        return qs
    @property
    def cartitem_total(self):
        cartitem=self.cartitems
        if cartitem:
            total=sum([items.total for items in cartitem])
        else:
            return 0    



class CartItem(models.Model):
    cart=models.ForeignKey(Cart, on_delete=models.CASCADE,related_name="cartitems")
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    qty=models.PositiveIntegerField(default=1)
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    @property
    def total(self):
        return self.qty*self.product.price

class Comment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="comment")
    text=models.CharField(max_length=200)
    created_date=models.DateTimeField(auto_now_add=True)
    product=models.ForeignKey(Product,related_name="post_comments",on_delete=models.CASCADE)

    def _str_(self):
        return self.text

class Bids(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_bids")
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    amount=models.PositiveIntegerField()
    bids_options=(
        ("Pending","pending"),
        ("Accept","accept"),
        ("Reject","reject"),
    )
    status=models.CharField(max_length=200,choices=bids_options,default="Pending")

    def _str_(self):
        return self.amount


def create_profile(sender,created,instance,**kwargs):
    if created:
        Userprofile.objects.create(user=instance)    

post_save.connect(create_profile,sender=User)    

def create_cart(sender,created,instance,**kwargs):
    if created:
        Cart.objects.create(user=instance)    

post_save.connect(create_cart,sender=User)   








