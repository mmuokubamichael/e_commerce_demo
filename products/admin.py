from django.contrib import admin
from .models import Products,Ratings,Cart,My_order,Shipping_adress,Order,billing_adress,Dispute

# Register your models here.

admin.site.register(Products)
admin.site.register(Ratings)
admin.site.register(Cart)
admin.site.register(My_order)
admin.site.register(Shipping_adress)
admin.site.register(Order)
admin.site.register(billing_adress)
admin.site.register(Dispute)
