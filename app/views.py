from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from django.db.models import Count

from app.forms import CustomerProfileForm, CustomerRegistrationForm
from app.models import Cart, Customer, Product
from django.contrib import messages
from django.db.models import Q

# Create your views here.
def home(request):
    return render(request,"myapp/home.html")



def about(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request,"myapp/about.html",locals())



def contact(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request,"myapp/contact.html",locals())



class Categoryview(View):
    def get(self,request,val):
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title').annotate(total=Count('title'))
        return render(request,"myapp/category.html",locals())
    


class CategoryTitle(View):
    def get(self,request,val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        return render(request,"myapp/category.html",locals())
    


class ProductDetail(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        return render(request,"myapp/productdetail.html",locals())
    


class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request,'myapp/customerregistration.html',locals())
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congratulations! User Register Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request,'myapp/customerregistration.html',locals())



class ProfileView(View):
    def get(self,request,):
        form = CustomerProfileForm()
        return render(request,'myapp/profile.html',locals())
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            
            reg = Customer(user=user,name=name,locality=locality,mobile=mobile,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,"Congratulations! profile save Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request,'myapp/profile.html',locals())



def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request,'myapp/address.html',locals())



class updateAddress(View):
    def get(self,request,pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request,'myapp/updateAddress.html',locals())
    def post(self,request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request,"Congratulations! PProfile Update Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return redirect("address")
    


def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect("/cart")



def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 40
    return render(request,'myapp/addtocart.html',locals())

class checkout(View):
    def get(self,request):
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount = famount + value
        totalamount = famount + 40
        return render(request,'myapp/checkout.html',locals())


def plus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user =request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
            
        }
        return JsonResponse(data)
    

def minus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    

def remove_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data={
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)