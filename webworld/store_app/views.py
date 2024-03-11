from django.shortcuts import redirect, render
from django.conf import settings
from .models import Product,Categories,Filter_Price,Color,Brand,Contact_us,Order,OrderItem
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from cart.cart import Cart
import razorpay


client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))

def BaseFile(request):
    return render(request,'store_app/base.html')

def Home(request):
    product = Product.objects.filter(status = "Publish")

    context = {
        'product':product,
    }
    return render(request,'store_app/Home.html',context)

def Login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect("Home")
        else:
            return redirect("login")
    return render(request,'store_app/login.html')

def Logout(request):
    logout(request)
    return redirect('Home')

def Signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        customer =  User.objects.create_user(username, email, pass1)
        customer.first_name = first_name
        customer.last_name = last_name
        customer.save()
        return redirect("Home")

    return render(request,'store_app/signup.html')

def About(request):
    return render(request,'store_app/about.html')

def Address_detail(request):
    payment= client.order.create({
        "amount":500,
        "currency": "INR",
        'payment_capture':"1"    
    })
    order_id = payment['id']
    context = {
        'order_id':order_id,
        'payment':payment,
        # 'cart':cart,
        }
    if request.method == "POST":
        uid = request.session.get('_auth_user_id')
        user = User.objects.get(id = uid)
        cart = request.session.get('cart')
        first_name = request.POST.get('FirstName')
        last_name = request.POST.get('LastName')
        country = request.POST.get('country')
        address = request.POST.get('street_address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postcode = request.POST.get('postcode')
        phone = request.POST.get('phone')   
        email = request.POST.get('email')
        amount = request.POST.get('amount')
        order_id = request.POST.get('order_id')
        payment = request.POST.get('payment')

        order = Order(
            user = user,
            firstname = first_name,
            lastname = last_name,
            country = country,
            address = address,
            city = city,
            state = state,
            postcode = postcode,
            phone = phone,
            email = email,
            amount = amount,
            payment_id = order_id   
        )

        order.save()

        for i in cart:
            a = int(cart[i]['quantity'])
            b = int(cart[i]['price'])

            total = a * b
            print(total)

            item = OrderItem(
                order = order,
                product = cart[i]['name'], 
                image =  cart[i]['image'], 
                quantity = cart[i]['quantity'] ,
                price = cart[i]['price'], 
                total = total,
            )
            item.save()

        
    
    
    return render(request,'store_app/address.html',context)

def CartDetail(request):
    return render(request,'store_app/slide.html')

def ContactUs(request):
    if request.method == "POST":
        name = request.POST.get('Name')
        email = request.POST.get('Email')
        subject = request.POST.get('Subject')
        message = request.POST.get('Message')

        contact = Contact_us(
            name = name,
            email = email,
            subject = subject,
            message = message,
        )   
        
        subject = subject
        message = message
        email_form = settings.EMAIL_HOST_USER
        try:
            send_mail(subject, message, email_form, ['vaibhavgarg977@gmail.com'])
            contact.save()
            return redirect("Home")
        except:
             return redirect("Contact-Us")

    return render(request,'store_app/contact-us.html')

def ProductDetail(request,pk):
    product = Product.objects.get(pk=pk)
    categories = Categories.objects.all()

    CAT_ID = request.GET.get('categories')

    if CAT_ID:
        product = Product.objects.filter(categories = CAT_ID,status = "Publish")
    else:
        product = Product.objects.get(pk=pk)
    context = {
        'product':product,
        'categories': categories,
    }
    return render(request,'store_app/product-det.html',context)

def Store(request):
    product = Product.objects.filter(status = "Publish")
    categories = Categories.objects.all()
    price = Filter_Price.objects.all()
    color = Color.objects.all()
    brand = Brand.objects.all()
    query = request.GET.get('query')

    CAT_ID = request.GET.get('categories')
    COLOR_ID = request.GET.get('color')
    PRICE_ID = request.GET.get('filter_price')
    ATOZ_ID = request.GET.get('ATOZ')
    ZTOA_ID = request.GET.get('ZTOA')
    low_to_high_ID = request.GET.get('low_to_high')
    high_to_low_ID = request.GET.get('high_to_low')
    new_Id = request.GET.get('new')
    old_ID = request.GET.get('old')

    if CAT_ID:
        product = Product.objects.filter(categories = CAT_ID,status = "Publish")
    elif PRICE_ID:
        product = Product.objects.filter(filter_price = PRICE_ID,status = "Publish")
    elif COLOR_ID:
        product = Product.objects.filter(color = COLOR_ID,status = "Publish")
    elif ATOZ_ID:
        product = Product.objects.filter(status = "Publish").order_by('name')
    elif ZTOA_ID:
        product = Product.objects.filter(status = "Publish").order_by('-name')
    elif low_to_high_ID:
        product = Product.objects.filter(status = "Publish").order_by('price')
    elif high_to_low_ID:
        product = Product.objects.filter(status = "Publish").order_by('-price')
    elif new_Id:
        product = Product.objects.filter(status = "Publish",condition = "NEW").order_by('-id')
    elif old_ID:
        product = Product.objects.filter(status = "Publish",condition = "OLD").order_by('-id')
    elif query:
        product = Product.objects.filter(name__icontains = query)
    else:
        product = Product.objects.filter(status = "Publish")

    context = {
        'product':product,
        'categories': categories,
        'price':price,
        'color':color,
        'brand':brand,
    }
    return render(request,'store_app/store.html',context)

# cart

@login_required(login_url="/users/login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("Store")


@login_required(login_url="/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/login/")
def cart_detail(request):
    return render(request, 'store_app/cart-detail.html')

@csrf_exempt
def ThankYou(request):
    if request.method == 'POST':
        a = request.POST
        order_id = ""
        for key, val in a.items():
            if key == 'razorpay_order_id':
                order_id = val
                break
        
        user = Order.objects.filter(payment_id = order_id).first()
    return render(request,'store_app/thankyou.html')    