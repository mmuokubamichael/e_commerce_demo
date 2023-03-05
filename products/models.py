from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
# Create your models here.


TYPE_OF_PAYMENT = (
    ('stripe','stripe'),
    ('paypal','paypal')
)
ORDER_STATE = (
    ('not_ordered','not_ordered'),
    ('processesing','processesing'),
    ('shipped','shipped'),
    ('received','received')
)

DISPUTE_STATE = (
    ('no','no'),
    ('yes','yes'),
    ('resolved','resolved'),
)


class Products(models.Model):
    dealer = models.ForeignKey(User,on_delete=models.CASCADE,related_name="product")
    name = models.CharField(max_length=500)
    price = models.FloatField()
    discount = models.FloatField(blank=True,null=True)
    quantity = models.IntegerField()
    details = models.TextField()
    categories = models.CharField(max_length=500)
    pictures1 = models.ImageField(upload_to='product_photos',blank=True,null=True)
    pictures2 = models.ImageField(upload_to='product_photos',blank=True,null=True)
    pictures3 = models.ImageField(upload_to='product_photos',blank=True,null=True)
    pictures4 = models.ImageField(upload_to='product_photos',blank=True,null=True)
    pictures5 = models.ImageField(upload_to='product_photos',blank=True,null=True)
    pictures6 = models.ImageField(upload_to='product_photos',blank=True,null=True)

    def get_no_of_rating(self):
        return self.rating.all().count()
    def get_amount(self):
        if self.discount:
            return self.discount
        else:
            return self.price
    def get_discount_per(self):
        x = (self.discount * 100)/self.price
        return x

        


class Cart(models.Model):
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)


class My_order(models.Model):
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    purchased =  models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)
    order_state = models.CharField(max_length=15,choices=ORDER_STATE,default="not_ordered")
    disput_state = models.CharField(max_length=15,choices=DISPUTE_STATE,default="no")

    def get_item_amount(self):
        ammount= self.product.price * self.quantity
        return ammount
    def get_item_discount_amount(self):
        ammount= self.product.discount * self.quantity
        return ammount
    def get_quantity_amount(self):
        if self.product.discount:
            ammount= self.product.discount * self.quantity
            return ammount
        else:
            ammount= self.product.price * self.quantity
            return ammount
    def get_item_amount_saved(self):
        saved= self.get_item_amount() - self.get_item_discount_amount()
        return saved
    def get_item_main_amount(self):
        if self.product.discount:
            return self.get_item_discount_amount()
        else:
            return self.get_item_amount()

class Ratings(models.Model):
    product = models.ForeignKey(Products,on_delete=models.CASCADE,related_name="rating",blank=True,null=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    rate = models.IntegerField()
    comments = models.CharField(max_length=5000,blank=True)



class Dispute(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    order = models.ForeignKey(My_order,on_delete=models.CASCADE)
    reason = models.TextField()

class Shipping_adress(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    city = models.CharField(max_length=15)
    apt_suit = models.CharField(max_length=15)
    zipcode=models.CharField(max_length=10)
    nationality = CountryField(blank_label='(select country)')
    default = models.BooleanField(default=False)

class billing_adress(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30,blank=True)
    last_name = models.CharField(max_length=30,blank=True)
    company = models.CharField(max_length=100,blank=True)
    email = models.CharField(max_length=30,blank=True)
    city = models.CharField(max_length=15)
    apt_suit = models.CharField(max_length=15)
    zipcode=models.CharField(max_length=10)
    nationality = CountryField(blank_label='(select country)')
    payment_types = models.CharField(max_length=6,choices=TYPE_OF_PAYMENT,default="stripe")
    
    
    

class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    purchased =  models.BooleanField(default=False)
    items = models.ManyToManyField(My_order)
    shipping_address = models.ForeignKey(Shipping_adress,on_delete=models.SET_NULL,blank=True,null=True)
    billing_address = models.ForeignKey(billing_adress,on_delete=models.SET_NULL,blank=True,null=True)

    def get_total_amount(self):
        total = 0
        for item in self.items.all():
            print(item)
            total += item.get_item_main_amount()
        return int(total)

