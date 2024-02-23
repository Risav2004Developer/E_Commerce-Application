from django.shortcuts import render, redirect
from store_app.models import Product,Categories,Color,Brand,Order,OrderItem,Banner
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.contrib import messages
from django.http import HttpResponse


def BASE(request):
    banner= Banner.objects.all()[0]
    file={
        'banner': banner,
    }
    return render(request, 'main/base.html',file)


def HOME(request):
    product= Product.objects.filter(status='Publish')
    banner = Banner.objects.all()[0]

    def Merge(context, file):
        res = context | file
        return res
    context= {
        'product': product,
    }
    file = {
        'banner': banner,

    }
    total=Merge(context,file)

    return render(request, 'main/index.html',total)


def PRODUCT(request):
    product = Product.objects.filter(status='Publish')
    banner = Banner.objects.all()[0]
    categories=Categories.objects.all()
    color=Color.objects.all()
    brand=Brand.objects.all()
    CATID = request.GET.get('categories')
    COLORID = request.GET.get('color')
    BRANDID = request.GET.get('brand')
    if CATID:
        product = Product.objects.filter(Categories=CATID)
    elif COLORID:
        product = Product.objects.filter(Color=COLORID,status='Publish')
    elif BRANDID:
        product = Product.objects.filter(Brand=BRANDID, status='Publish')
    else:
        product = Product.objects.filter(status='Publish')
    context = {
        'product': product,
        'categories':categories,
        'color':color,
        'brand':brand,
    }
    def Merge(context, file):
        res = context | file
        return res
    file = {
        'banner': banner,
    }

    total=Merge(context,file)
    return render(request,'main/product.html',total)


def SEARCH(request):
    query=request.GET.get('query')
    banner = Banner.objects.all()[0]
    product=Product.objects.filter(name__icontains= query)

    context= {
        'product': product,
    }
    def Merge(context, file):
        res = context | file
        return res
    file = {
        'banner': banner,
    }

    total=Merge(context,file)
    return render(request,'main/search.html',total)


def AUTH(request):
    return render(request, 'Registration/auth.html')


def HANDLEREGISTER(request):
    banner = Banner.objects.all()[0]
    if request.method=="POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        pass1= request.POST.get('pass1')
        pass2= request.POST.get('pass2')
        customer= User.objects.create_user(username,email,pass1)
        customer.first_name = first_name
        customer.last_name = last_name
        customer.save()
        return redirect('home')
    file = {
        'banner': banner,
    }

    return render(request, 'Registration/auth.html',file)


def HANDLELOGIN(request):
    banner = Banner.objects.all()[0]
    if request.method == "POST":
        username = request.POST.get('username')
        password= request.POST.get('password')
        user = authenticate(username= username, password= password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, "Error: This is the sample error Flash message.")
            return redirect('login')
    file = {
        'banner': banner,
    }
    return render(request, 'Registration/auth.html',file)


def HANDLELOGOUT(request):
    banner = Banner.objects.all()[0]
    logout(request)
    redirect('home')
    file = {
        'banner': banner,
    }
    return render(request, 'Registration/auth.html',file)




def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("home")


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



def cart_detail(request):
    banner = Banner.objects.all()[0]
    file = {
        'banner': banner,
    }
    return render(request, 'cart/cart_details.html',file)

@login_required(login_url="/login/")
def checkout(request):
    banner = Banner.objects.all()[0]
    file = {
        'banner': banner,
    }
    return render(request,'cart/checkout.html',file)


def PLACE_ORDER(request):
    banner = Banner.objects.all()[0]
    if request.method == "POST" :
        uid= request.session.get('_auth_user_id')
        user= User.objects.get(id=uid)
        cart=request.session.get('cart')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        country = request.POST.get('country')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postcode = request.POST.get('postcode')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        amount = request.POST.get('amount')
        order_id = request.POST.get('order_id')
        payment = request.POST.get('payment')
        order = Order(
             user= user,
             firstname= firstname,
             lastname = lastname,
             country= country,
             city= city,
             address= address,
             state= state,
             postcode= postcode,
             phone= phone,
             email= email,
             amount = amount
         )
        order.save()
        for i in cart:
            a=(int(cart[i]['price']))
            b=cart[i]['quantity']
            total=a*b
            item=OrderItem(
                order = order,
                product = cart[i]['name'],
                image = cart[i]['image'],
                quantity = cart[i]['quantity'],
                price = cart[i]['price'],
                total = total
            )
            item.save()
    file = {
        'banner': banner,
    }
    return render(request, 'cart/placeorder.html',file)


def SUCCESS(request):
    banner = Banner.objects.all()[0]
    file = {
        'banner': banner,
    }

    return render(request,'cart/thankyou.html',file)