from django.urls import path
from .views import (home,detail,add_to_cart,cart,my_orders,
shipping_address,create_shipping_address,update_shipping_address,add_item,sub_item,delete_from_cart,
checkout,stripe_payment,purchased_items,dispute,order_state_json,rating,create_payment,my_webhook_view,payment_succeded,register_user,login_user,logout_view)

app_name = "products"


urlpatterns = [
    path('',home,name='home'),
    path('item/<int:product_id>',detail,name='detail'),
    path('cart/',add_to_cart,name='add_to_cart'),
    path('my_carts/',cart,name='cart'),
    path('my_orders/',my_orders,name='my_orders'),
    path('my_address/',shipping_address,name='shipping_address'),
    path('create_address/',create_shipping_address,name='create_shipping_address'),
    path('update_address/<int:address_id>/',update_shipping_address,name='update_shipping_address'),
    path('add_quantity/<int:product_id>/',add_item,name='add_item'),
    path('sub_quantity/<int:product_id>/',sub_item,name='sub_item'),
    path('delete_cart_item/<int:product_id>/',delete_from_cart,name='delete_from_cart'),
    path('checkout/',checkout,name='checkout'),
    path('stripe_payment/',stripe_payment,name='stripe_payment'),
    path('orders/',purchased_items,name='purchased_items'),
    path('dispute/<int:order_id>',dispute,name='dispute'),
    path('order_state_json/',order_state_json,name='order_state_json'),
    path('rating/',rating,name='rating'),
    path('create_payment_intent/',create_payment,name='create_payment'),
    path('my_webhook/stripe/',my_webhook_view,name='my_webhook'),
    path('stripe/succeded/',payment_succeded,name='payment_succeded'),
    path('register/user/',register_user,name='register_user'),
    path('login/user/',login_user,name='login_user'),
    path('logout/', logout_view, name='logout'),

    

    
]
