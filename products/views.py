from django.shortcuts import render,redirect
from django.shortcuts import get_list_or_404, get_object_or_404
from .models import Products,Cart,Ratings,My_order,Shipping_adress,Order,billing_adress,Dispute
from .forms import Shipping_address_form,billing_address_form
from django.contrib import messages
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
import stripe
from django.contrib.auth.models import User
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import authenticate, login, logout
import json
from django.contrib.auth.decorators import login_required

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
def home(request):
    products=Products.objects.all()
    return render(request,'products/home.html',{'products':products})

def register_user(request):
    user_form = UserCreationForm()
    if request.method == "POST":
        user_form = UserCreationForm(request.POST,None)
        if user_form.is_valid():
            user_form.save()
            return redirect('products:home')

    return render(request,'products/register.html',{"user_form":user_form})


def login_user(request):
    user_form = AuthenticationForm()
    if request.method == "POST":
        user_form = AuthenticationForm(request=request, data=request.POST)
        print(user_form)
        
        if user_form.is_valid():
            print("wwwwwwwwwwwwwwwwwwwww")
            username = user_form.cleaned_data.get('username')
            password = user_form.cleaned_data.get('password')
            user= authenticate(request, username=username,password=password)
            if user is not None:
                login(request,user,)
                return redirect("products:home")

    return render(request,'products/login.html',{"user_form":user_form})

def logout_view(request):
    logout(request)
    return redirect('products:home')

def detail(request,product_id):
    product = get_object_or_404(Products, pk=product_id)
    products=Products.objects.all()
    rating = Ratings.objects.filter(product=product)
    average = 0
    ave_round = 0
    
    
    if rating.exists():
        average= sum(rate.rate for rate in rating)/len(rating)
        ave_round = round(average,1)
        page = request.GET.get('page', 1)

        paginator = Paginator(rating, 5)
        try:
            the_ratings = paginator.page(page)
        except PageNotAnInteger:
            the_ratings = paginator.page(1)
        except EmptyPage:
            the_ratings = paginator.page(paginator.num_pages)

    ranges= [1,2,3,4,5]
    return render(request,'products/details.html',{'product':product,"products":products,"average":round(average),"rating":rating,"ranges":ranges,"ave_round":ave_round,"the_ratings":the_ratings})
@login_required
def add_to_cart(request):
    if request.method == "POST":
        item = request.POST.get('item')
        quantity =request.POST.get("quantity")
        product = get_object_or_404(Products, pk=item)
        item_to_order,created = My_order.objects.get_or_create(user=request.user,purchased=False,product=product)
        order = Order.objects.filter(user=request.user,purchased=False)
        if order.exists():
            
            my_order = order[0]
            if my_order.items.filter(product=product).exists():
                item_to_order.quantity += 1
                item_to_order.save()
                messages.success(request,'item has been added to your cart')
            else:
                my_order_ = my_order.items.add(item_to_order)
                messages.success(request,'item has been added to your cart')
        else:
            my_order = Order.objects.create(user=request.user)
            my_order.items.add(item_to_order)
            messages.success(request,'item has been added to your cart')
            
    return redirect('products:detail',product_id=product.id)

@login_required
def delete_from_cart(request,product_id):
    product = get_object_or_404(Products, pk=product_id)
    order = Order.objects.filter(user=request.user,purchased=False)
    if order.exists():
        
        my_order = order[0]
        if my_order.items.filter(product=product).exists():
            order_ = My_order.objects.get(user=request.user,purchased=False,product=product)
            my_order.items.remove(order_)
            order_.delete()
        else:
            pass
            #message item was not found in the cart
    else:
        pass
        # your cart is empty      
    return redirect('products:cart')

@login_required
def cart(request):
    my_carts=Order.objects.filter(user=request.user,purchased=False)
    if my_carts.exists():
        print("exist")
        return render(request,'products/cart.html',{'cart':my_carts[0]})
    else:
        return redirect('products:home')

@login_required
def my_orders(request):
    if request.method == "POST":
        for key in request.POST:
            value = request.POST[key]
            
            try:
                value_int = int(value)
                print(value_int)
                the_product = Cart.objects.get(id=value_int)
                print(value_int)
                if the_product.product.quantity >0:
                    my_order=My_order(product=the_product.product,user=request.user)
                    my_order.save()
                    quantity=the_product.product
                    quantity.quantity -=1
                    quantity.save()  
                    cart_item = Cart.objects.get(user=request.user,id=value_int)
                    cart_item.delete()
            except:
                pass
    #   my_carts=Cart.objects.filter(user=request.user)
    
    return redirect('products:cart')

@login_required
def shipping_address(request):
    my_address= Shipping_adress.objects.filter(user=request.user)
    shipping_address_found = False
    if my_address.exists():
        shipping_address_found = True
    context = {
        'address': my_address,
        'is_address': shipping_address_found
    }
    return render(request,'products/my_shipping_address.html',context)


@login_required
def create_shipping_address(request):
    form = Shipping_address_form(request.POST,None)
    context = {
        'form': form,
        }
    if request.method == 'POST':
        form = Shipping_address_form(request.POST)
        if form.is_valid():
            
            my_default = form.cleaned_data['default']
            my_city = form.cleaned_data['city']
            my_apt_suit = form.cleaned_data['apt_suit']
            my_zipcode = form.cleaned_data['zipcode']
            my_nationality = form.cleaned_data['nationality']
            my_address = Shipping_adress.objects.filter(user=request.user,default=True)
            
            if my_address.exists():
                if my_default:
                    for adrs in my_address:
                        adrs.default = False
                        adrs.save()

                    save_shipping_address=Shipping_adress(user=request.user,city=my_city,apt_suit=my_apt_suit,zipcode=my_zipcode,nationality=my_nationality,default=my_default)
                    save_shipping_address.save()
                    messages.success(request,'shipping address created successfully')
                    return redirect('products:shipping_address')
                else:
                    save_shipping_address=Shipping_adress(user=request.user,city=my_city,apt_suit=my_apt_suit,zipcode=my_zipcode,nationality=my_nationality,default=my_default)
                    save_shipping_address.save()
                    messages.success(request,'shipping address created successfully')
                    return redirect('products:shipping_address')

            else:                
                
                save_shipping_address=Shipping_adress(user=request.user,city=my_city,apt_suit=my_apt_suit,zipcode=my_zipcode,nationality=my_nationality,default=my_default)
                save_shipping_address.save()
                messages.success(request,'shipping address created successfully')
                return redirect('products:shipping_address')

    return render(request,'products/create_shipping_address.html',context)

@login_required
def update_shipping_address(request,address_id):
    address = Shipping_adress.objects.get(user=request.user,id=address_id)
    form = Shipping_address_form(request.POST or None, instance=address)
    context = {
        'form': form,
        }
    
    if form.is_valid():
        
        my_default = form.cleaned_data['default']
        my_city = form.cleaned_data['city']
        my_apt_suit = form.cleaned_data['apt_suit']
        my_zipcode = form.cleaned_data['zipcode']
        my_nationality = form.cleaned_data['nationality']
        my_address = Shipping_adress.objects.filter(user=request.user,default=True)
        
        if my_address.exists():
            if my_default:
                for adrs in my_address:
                    adrs.default = False
                    adrs.save()

                address.city=my_city
                address.apt_suit=my_apt_suit
                address.zipcode=my_zipcode
                address.nationality=my_nationality
                address.default=my_default
                address.save()

            else:
                address.city=my_city
                address.apt_suit=my_apt_suit
                address.zipcode=my_zipcode
                address.nationality=my_nationality
                address.default=my_default
                address.save()

        else:                
            
            address.city=my_city
            address.apt_suit=my_apt_suit
            address.zipcode=my_zipcode
            address.nationality=my_nationality
            address.default=my_default
            address.save()

    return render(request,'products/update_shipping_address.html',context)


@login_required
def add_item(request,product_id):
    item = My_order.objects.get(user=request.user,pk=product_id)
    product_quantity = item.product.quantity
    if product_quantity > item.quantity:
        item.quantity +=1
        item.save()
    else:
        messages.warning(request,'have exceeded item quantity')
        return redirect('products:cart')
    return redirect('products:cart')

@login_required
def sub_item(request,product_id):
    item = get_object_or_404(My_order,user=request.user,pk=product_id,purchased=False)
    order = Order.objects.filter(user=request.user,purchased=False)
    if order.exists():
        if item.quantity <= 1:
            get_order = order[0]
            get_order.items.remove(item)
            item.delete()
        else:
            item.quantity -=1
            item.save()
    return redirect('products:cart')

@login_required
def checkout(request):
    get_orders = Order.objects.filter(user=request.user,purchased=False)

    if get_orders.exists():

        is_outofstock = []
        for order_item in get_orders[0].items.all():
            if order_item.quantity > order_item.product.quantity:
                is_outofstock.append(order_item.product.name)

        if len(is_outofstock) == 0:
            payment_address = billing_adress.objects.filter(user=request.user)
            shipping_address = Shipping_adress.objects.filter(user=request.user,default=True)
            is_shipping_address = False
            if shipping_address.exists():
                is_shipping_address=True

            if payment_address.exists():
                form = billing_address_form(request.POST or None, instance=payment_address[0])
                context = {
                    'form':form,
                    'shipping_address':shipping_address,
                    'is_shipping_address':is_shipping_address,
                    'get_orders':get_orders[0]
                }
            
                if form.is_valid():
                    print("order exixts")
                    my_city = form.cleaned_data['city']
                    my_apt_suit = form.cleaned_data['apt_suit']
                    my_zipcode = form.cleaned_data['zipcode']
                    my_nationality = form.cleaned_data['nationality']
                    payment_types = form.cleaned_data['payment_types']
                    company = form.cleaned_data['company']
                    email = form.cleaned_data['email']
                    first_name = form.cleaned_data['first_name']
                    last_name = form.cleaned_data['last_name']
                    if is_shipping_address:
                        payment_address_ = payment_address[0]
                        payment_address_.city = my_city
                        payment_address_.apt_suit = my_apt_suit
                        payment_address_.zipcode = my_zipcode
                        payment_address_.nationality = my_nationality
                        payment_address_.payment_types = payment_types
                        payment_address_.company = company
                        payment_address_.email = email
                        payment_address_.first_name = first_name
                        payment_address_.last_name = last_name
                        
                        payment_address_.save()
                        orders= Order.objects.filter(user=request.user,purchased=False)
                        if orders.exists():
                            orders = orders[0]
                            orders.shipping_address = shipping_address[0]
                            orders.billing_address = payment_address_
                            orders.save()
                            print("order exixts")
                            # go to payment option
                            if payment_types == "stripe":
                                messages.success(request,'pay with stripe')
                                return redirect('products:stripe_payment')
                            else:
                                # paypal payment
                                messages.success(request,'pay with paypal')
                                return render(request,'products/checkout_utro.html', context)
                        
                        else:
                            
                            # return to cart
                            # no item found in your cart
                            messages.success(request,'no item found in your cart')
                            return redirect('products:cart')


                    else:
                        #message please create or set a default shipping address
                        messages.success(request,'please create or set a default shipping address')
                        return render(request,'products/checkout_utro.html', context)
                return render(request,'products/checkout_utro.html', context)
                
            else:
                form = billing_address_form()
                context = {
                    'form':form,
                    'shipping_address':shipping_address,
                    'is_shipping_address':is_shipping_address,
                    'get_orders':get_orders[0],
                }
                if request.method == "POST":
                    my_form = billing_address_form(request.POST)
                    if my_form.is_valid():
                        my_city = my_form.cleaned_data['city']
                        my_apt_suit = my_form.cleaned_data['apt_suit']
                        my_zipcode = my_form.cleaned_data['zipcode']
                        my_nationality = my_form.cleaned_data['nationality']
                        payment_types = my_form.cleaned_data['payment_types']
                        billing_adds = billing_adress(user=request.user,city=my_city,apt_suit=my_apt_suit,zipcode=my_zipcode,nationality=my_nationality,payment_types=payment_types)
                        if is_shipping_address:
                            billing_adds.save()
                            orders= Order.objects.filter(user=request.user,purchased=False)
                            if orders.exists():
                                orders = orders[0]
                                orders.shipping_address = shipping_address[0]
                                orders.billing_address = billing_adds
                                orders.save()
                                # go to payment option
                                if payment_types == "stripe":
                                    messages.success(request,'pay with stripe')
                                    return redirect('products:stripe_payment')
                                else:
                                    # paypal payment
                                    messages.success(request,'pay with paypal')
                                    return render(request,'products/checkout_utro.html', context)
                        
                            else:
                                
                                # return to cart
                                # no item found in your cart
                                messages.success(request,'no item found in your cart')
                                return redirect('products:cart')
                        else:
                            #message please create or set a default shipping address
                            messages.error(request,'please create or set a default shipping address')
                            return render(request,'products/checkout_utro.html', context)
                return render(request,'products/checkout_utro.html', context)
        else:
            messages.warning(request, str(is_outofstock) + " is out of stock")
            return redirect('products:cart')


    else:
        return redirect('products:home')

@login_required
def stripe_payment(request):
    order = Order.objects.filter(user=request.user,purchased=False)
    if order.exists():
        """if request.method == "POST":
            order = Order.objects.filter(user=request.user,purchased=False)
            order_= order[0]
            order_.purchased = True
            for item in order_.items.all():
                item.purchased = True
                item.order_state = "processesing"  
                item.save()
            order_.save()
            messages.success(request,'purchased was successful!')
            return redirect('products:cart')"""

        return render(request,'products/stripe.html',{'get_orders':order[0],'stripe_public_key':settings.STRIPE_PUBLIC_KEY})
    else:
         messages.warning(request,'no item found in your cart')
         return redirect('products:cart')

@login_required
def purchased_items(request):
    purchased_item = My_order.objects.filter(user=request.user,purchased=True)
    if purchased_item.exists():
        purchased_item_ = purchased_item
        if request.method == "POST":
            order_id = request.POST.get("order_id")
            item = My_order.objects.get(user=request.user,id=order_id)
            item.order_state = "received"
            item.save()
        return render(request,'products/list_order.html',{'purchased_item':purchased_item_})
    else:
        return redirect('products:home')

@login_required
def dispute(request,order_id):
    order = get_object_or_404(My_order,id=order_id,user=request.user,purchased=True)
    if request.method == "POST":
        reason = request.POST.get("reason")
        dispute=Dispute(user=request.user,order=order,reason=reason)
        dispute.save()
        order.disput_state = "yes"
        order.save()
        messages.success(request,"your dispute message has been sent we will reply to you shortly")
        return redirect('products:purchased_items')
    return render(request,'products/dispute.html')

@login_required
def order_state_json(request):
    data=request.POST
    data_ = dict(data.lists())
    data_.pop('csrfmiddlewaretoken')
    item = My_order.objects.get(user=request.user,id=int(data_['id'][0]))
    item.order_state = "received"
    item.save()
    
    return JsonResponse({"results":True})

@login_required
def rating(request):
    data=request.POST
    data_ = dict(data.lists())
    data_.pop('csrfmiddlewaretoken')
    print(data)
    order =get_object_or_404(My_order,user=request.user,id=int(data_['id'][0]),purchased=True) 
    my_rate = Ratings(author=request.user,product=order.product,rate=int(data_['rate'][0]),comments= data_['coment'][0])
    my_rate.save()
    return JsonResponse({"results":True})

@login_required
def charge_customer(customer_id):
    # Lookup the payment methods available for the customer
    payment_methods = stripe.PaymentMethod.list(
        customer=customer_id,
        type='card'
    )
    # Charge the customer and payment method immediately
    try:
        stripe.PaymentIntent.create(
            amount=1099,
            currency='usd',
            customer=customer_id,
            payment_method=payment_methods.data[0].id,
            off_session=True,
            confirm=True
            
        )
    except stripe.error.CardError as e:
        err = e.error
        # Error code will be authentication_required if authentication is needed
        print('Code is: %s' % err.code)
        payment_intent_id = err.payment_intent['id']
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)


@login_required
def create_payment(request):
    
    # Alternatively, set up a webhook to listen for the payment_intent.succeeded event
    # and attach the PaymentMethod to a new Customer
    customer = stripe.Customer.create()
    

    try:
        data = Order.objects.filter(user = request.user,purchased=False)
        total_amount = data[0].get_total_amount()
        total_amount = int(total_amount) * 100

        

        # Create a PaymentIntent with the order amount and currency
        intent = stripe.PaymentIntent.create(
            customer=customer['id'],
            setup_future_usage='off_session',
            amount= total_amount,
            currency='usd',
            metadata = {
                "user" : request.user
            },
            automatic_payment_methods={
                'enabled': True,
            },
        )
        print( intent['client_secret'])
        return JsonResponse({
            'clientSecret': intent['client_secret']
        })
    except Exception as e:
        print(e)
        return JsonResponse({'error':str(e)})


@csrf_exempt
def my_webhook_view(request):

    payload = request.body
    
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
        payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
        
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)
    if event["type"] == "payment_intent.succeeded":
        intent = event['data']['object']
        user = intent["metadata"]["user"]
       
        get_user = User.objects.get(username=user)
       
        order = Order.objects.filter(user=get_user,purchased=False)
        order_= order[0]
        order_.purchased = True
        print("wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww")
        for item in order_.items.all():
            item.purchased = True
            item.order_state = "processesing"  
            print("wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww")
            
            
            product_item = item.product.id
            
            get_p = Products.objects.get(id=product_item)
            get_p.quantity -= item.quantity
            print("substracted")
            item.save()
            get_p.save()
        order_.save()
    #    
    # Passed signature verification
    return HttpResponse(status=200)

@login_required
def payment_succeded(request):
    return render(request,'products/succeded.html')

