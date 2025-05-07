from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from .forms import userregisterationform,loginform,product_form,contact,CustomerProfileForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import category_model,product_model,cart,CustomerProfile,orders_data,customer,User,product_rating
from django.contrib.auth.decorators import login_required
from django.views import View

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import productserializers
import datetime

from django.core.mail import send_mail
from django.conf import settings

# import razorpay
from myproject.settings import *
# Create your views here.


# Rest API-----------------------------
class crudapi_view(APIView):
    def get(self,request):
        id= request.data.get("id",None)
        if id:
            try:
                product_data=product_model.objects.get(id=id)
                serializer=productserializers(product_data)
                return Response (serializer.data,status=status.HTTP_200_OK)
            except:
                return Response({'error':'Data does not exist'},status=status.HTTP_400_BAD_REQUEST)
        product_data=product_model.objects.all()
        serializer=productserializers(product_data,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    






def show_all(request):
    category=category_model.objects.all()
    products=product_model.objects.filter()
    context={'category':category,'products':products}
    return render(request,'home.html',context)

# def get_all_products(request):
#     products=product_model.objects.all()
#     context={'all_prod':products}
#     return render(request,'show_product.html',context)

def about_us(request):
    return render(request,'about_us.html')

def show_product(request):
    if request.method=="POST":
        fm=product_form(request.POST)
        if fm.is_valid():
            fm.save()
    else:
        fm=product_form()
    prod=product_model.objects.all()
    return render(request,"update.html",{'form':fm,'prod':prod})


#-----------------update and delete-------------------

def show(request):
    category=category_model.objects.all()
    products=product_model.objects.all()
    context={'category':category,'product':products}
    return render(request,'home.html',context)



def updatedata(request,id):
    obj = product_model.objects.get(id=id)
    
    if request.method == "POST":
        fm = product_form(request.POST, instance=obj)
        if fm.is_valid():
            fm.save()
            messages.success(request, "Product updated successfully")
            # return redirect('update')  # Redirect to the update page or another appropriate page
        else:
            messages.warning(request, "Something went wrong")
    else:
        fm = product_form(instance=obj)

    prod = product_model.objects.all()
    context = {'prod': prod, 'form': fm}
    return render(request, "update.html", context)


def deleteview(request,id):
    if request.method=="POST":
        pi=product_model.objects.get(id=id)
        pi.delete()
    fm=product_form()    
    prod=product_model.objects.all()
    return render(request,"update.html",{'form':fm,'prod':prod})

def searchview_for_admin(request):
    if request.method=='POST':
        value=request.POST['search2']
        result=category_model.objects.filter(title__contains=value)
        return render(request,'search_update.html',{'result':result})
    



def cat_view_for_update(request,id):
    category=category_model.objects.all()

    context={'category5':category}
    return render(request,'update.html',context)


#-------------------------Add product-----------------------------
def productview(request):
    if request.method=='POST':
        fm=product_form(request.POST,request.FILES)
        print(fm)
        if fm.is_valid():
            task=fm.save(commit=False)
            task.upload_by=request.user
            task.save()
            messages.success(request,"Product Added Successfully")
           
            # return render(request,'product.html',context)
        else:
            messages.warning(request,"Something went wrong")
    else:
        fm=product_form()
    prod=product_model.objects.all()
    context={'prod':prod,'forms':fm}
    return render(request,'product.html',context)

 
#----------------------------------register-------------------------------
# def registerview(request):
#     if request.method=="POST":
#         fm=userregisterationform(request.POST)
#         if fm.is_valid():
#             fm.save()
#             messages.success(request,"Registration is successful")
#             return redirect('login')
#         else:
#             messages.warning(request,"Something went wrong")
#     else:
#         fm=userregisterationform()
#     return render(request,'register.html',{'forms':fm})


def registerview(request):
    if request.method == "POST":
        fm = userregisterationform(request.POST)
        if fm.is_valid():
            # Get password before saving (as it will be hashed after save)
            raw_password = fm.cleaned_data.get('password1')
            user = fm.save()
            
            # Send welcome email with credentials
            subject = 'Welcome to TECH-IL@ - Your Login Credentials'
            message = f'''Hi {user.username},

Thank you for registering with us! Your account has been successfully created.

Your login credentials:
Username: {user.username}
Password: {raw_password}

Please keep these credentials safe and change your password after first login.

Best regards,
Your Platform Team'''

            from_email = settings.EMAIL_HOST_USER
            recipient_list = [user.email]
            
            send_mail(
                subject,
                message,
                from_email,
                recipient_list,
                fail_silently=False,
            )
            
            messages.success(request, "Registration successful! Login credentials sent to your email.")
            return redirect('login')
        else:
            messages.warning(request, "Something went wrong")
    else:
        fm = userregisterationform()
    return render(request, 'register.html', {'forms': fm})


#----------------------Login and Logout
#class loginview(view)
def loginview(request):
    if request.method=="POST":
        uname=request.POST['username']
        upass=request.POST['password']
        user=authenticate(request,username=uname,password=upass)
        if user is not None:
            login(request,user)
            #request.session['username']
            messages.success(request,"Login successful")
            return redirect('home')
        else:
            messages.warning(request,"Something went wrong")
    
    fm=loginform()
    return render(request,'login.html',{"forms":fm})


# class loginview(View):
#     def get(self,request):
#         fm=loginform()
#         return render(request,'login.html',{"forms":fm})

#     def post(self,request):
#         uname=request.POST['username']
#         upass=request.POST['password']
#         user=authenticate(request,username=uname,password=upass)
#         if user is not None:
#             login(request,user)
#             # for session
#             request.session['username'] = uname
#             messages.success(request,f"Successfully {uname} Loggedin")
#             response=render(request,'home.html',{'username':uname})
#             response.set_cookie('username',datetime.datetime.now())
#             return response
#         else:
#             messages.warning(request,"Something went wrong")   


def my_order(request):
    return render(request,'my_orders.html')

def my_account(request):
    return render(request,'my_account.html')

def logoutview(request):
    logout(request)
    messages.success(request,"Logout Successfully")
    return redirect('home')


#-----------------category view------------------
def cat_view(request,id):
    category=category_model.objects.all()
    product=product_model.objects.filter(cat=id)

    context={'category':category,'products':product}
    return render(request,'home.html',context)

#------------------search product---------------
def searchview(request):
    if request.method == 'POST':
        value = request.POST.get('search1', '').strip()

        if not value:
            return redirect('home')

        result = product_model.objects.filter(title__contains=value)
        
        if not result:  # Check if the result queryset is empty
            messages.info(request, 'No matches found.')
            
        return render(request, 'search.html', {'result': result})
    
    return render(request, 'search.html')
    
    return render(request, 'search.html')
    
def addtocartview(request,id):
    product=product_model.objects.filter(id=id)
    context={'result':product}
    return render(request,'add_to_cart.html',context)





#----------------------store cart and show cart
   
@login_required
def store_cart(request,id):
    product=product_model.objects.get(id=id)
    cart_item, item_created = cart.objects.get_or_create(user=request.user, product=product)
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('home')

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        cart_info = cart.objects.filter(user=request.user)
        total = 0
        quantity = 0

        for item in cart_info:
            subtotal = item.quantity * item.product.price
            total += subtotal
            quantity += item.quantity

        return render(request, 'add_to_cart.html', {'cart_info': cart_info, 'total': total, 'cart_value': quantity})


@login_required
def show_cart(request):
    
    cart_info=cart.objects.filter(user=request.user)
    total=0+1
    quantity=0
    for i in cart_info:
        subtotal=i.quantity*i.product.price
        total=total+subtotal
        quantity=quantity+i.quantity
        





    return render(request,'add_to_cart.html',{'cart_info':cart_info,'total':total,'cart_value':quantity})




#-----------------increase decrease cart product

def increase_cart(request,id):
    product=product_model.objects.get(id=id)
    cart_item, item_created = cart.objects.get_or_create(user=request.user,product=product)

    if cart_item.quantity < 5:
        cart_item.quantity += 1
        cart_item.save()
    else:
        messages.warning(request, "reached max limit.")
    return redirect('add_to_cart2')

def decrease_cart(request, id):
    product = product_model.objects.get(id=id)
    cart_item, item_created = cart.objects.get_or_create(user=request.user, product=product)
    
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
        messages.info(request, "Item removed from the cart.")
    return redirect('add_to_cart2')

def delete_cart(request,id):
    cart_items=cart.objects.get(id=id)
    cart_items.delete()
    return redirect('show_cart')

#--------------Related products
def show_data(request,id):
    
    products=product_model.objects.get(id=id)
    products_all=product_model.objects.all()

    cat_info = products.cat
    productinfo=product_model.objects.filter(id=id)

    products_info=product_model.objects.filter(cat=cat_info)

    

    rate_list=[]
    rate1=product_rating.objects.all()



    review_list=[]
    reviews=product_rating.objects.all()

    for i in reviews:
        if i.product.id==id:
            review_list.append([i.user,i.rating,i.info])


    for i in rate1:
        if id == i.product.id:
            rate_list.append(i.rating)
            avrage=sum(rate_list)/len(rate_list)
    else:
        avrage=0


    
   

    context={'product':productinfo,"categories":products_info, "products_all":products_all,'rate':avrage,'products':productinfo,'review':review_list,}

    return render(request, "show_product.html",context)

@login_required
def rating(request,id):
  prod=product_model.objects.get(id=id)






  if request.method=="POST":
      rating=request.POST['stars']
      info=request.POST['info']

      obj=product_rating.objects.create(user=request.user,product=prod,info=info,rating=rating)
      obj.save()
      return redirect('home')
      
      
  return render(request,'show_product.html',)





#--------------contact us----------------------------------------
@login_required
def contact_view(request):
    if request.method == "POST":
        form = contact(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your request is submited")
            return redirect('home')
        else:
            messages.warning(request, "Something went wrong")

    else:
        form=contact()
        return render(request, "contact.html", {'form':form})

#------------------Profile----------------------

@login_required
def profile(request):
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = CustomerProfileForm(instance=request.user)

    return render(request, 'profile.html', {'form': form})                  

def checkout(request):
    cart_info = cart.objects.filter(user=request.user)
    
    # Check if cart is empty
    if not cart_info.exists():
        messages.warning(request, 'Your cart is empty. Add items to your cart before checking out.')
        return redirect('add_to_cart2')  # Redirect to your cart page

    total = 0+1
    quantity = 0
    # product_id = None

    for item in cart_info:
        subtotal = item.quantity * item.product.price
        total += subtotal
        quantity += item.quantity
        product_id = item.product  # Assuming product is a ForeignKey in the Cart model


    if request.method == 'POST':
        F_name = request.POST['name']
        m_number = request.POST['number']
        email_adress = request.POST['email']
        Address = request.POST['address']
        try:

            total2 = 0

            for i in cart_info:
                subtotal2 = i.quantity * i.product.price
                total2 = subtotal2
                product_id=i.product
                quantity2 = i.quantity
               


                orders_d = orders_data.objects.create(
                user=request.user,
                product=product_id,  # Assuming product is a ForeignKey in the OrdersData model
                quntity=quantity2,  # Corrected variable name from quntity to quantity
                Address=Address,
                total_amount=total2,
                fname=F_name,
                mobile_no=m_number,
                email=email_adress
                )   
                orders_d.save()
                messages.success(request, 'Your order has been placed successfully!')
            cart_info=cart.objects.filter(user=request.user)
            cart_info.delete()
        except Exception as e:
            print(e)
            messages.error(request, 'Something went wrong. Please try again.')
  

    context = { 'total': total}
    return render(request, 'checkout.html', context) 

@login_required
def checkout_direct(request, id):
    total = 0
    quantity = 0
    product_id = None

    prod = product_model.objects.filter(id=id)
    for i in prod:
        title = i.title
        quantity = 1
        subtotal = quantity * i.price
        total += subtotal

        # Assign the current product's ID to product_id
        product_id = i.id

        all_total = int(total * 100)

        if request.method == 'POST':
            F_name = request.POST['name']
            m_number = request.POST['number']
            email_adress = request.POST['email']
            Address = request.POST['address']
            try:
                orders_d = orders_data.objects.create(
                    user=request.user,
                    product_id=product_id,
                    quntity=quantity,
                    Address=Address,
                    total_amount=total,
                    fname=F_name,
                    mobile_no=m_number,
                    email=email_adress
                )
                orders_d.save()
                messages.success(request, 'Your order has been placed successfully!')
            except Exception as e:
                print(e)
                messages.error(request, 'Something went wrong. Please try again.')

        context = {'title': title, 'subtotal': subtotal, 'total': total, 'cart_value': total, 'all_total': all_total}

        return render(request, 'checkout.html', context)
    
    return redirect('home')






def order(request):

    order=orders_data.objects.filter(user=request.user)


    return render(request,'orders.html',{'order':order})

# def orders_delete(request, id):
#     order_instance = get_object_or_404(orders_data, id=id)

#     if request.method == "POST":
#         # Assuming you want to delete the order only if it belongs to the current user
#         if order_instance.user == request.user:
#             order_instance.delete()

#     # Reload orders
#         orders = orders_data.objects.all()

#         return render(request, "orders.html", {'prod': orders})


def orders_delete(request,id):
    items=orders_data.objects.get(id=id)
    items.delete()
    return redirect('orders')

def admin_orders(request):
    user_order=orders_data.objects.all()
    return render(request, 'admin_user_orders.html',{'user_orders':user_order})

def customer_details(request):
    cust_details=User.objects.all()
    return render(request, 'customers_datils.html',{'cust_details':cust_details})