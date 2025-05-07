from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class customer(models.Model):
    cust_name=models.CharField(max_length=100)
    cust_address=models.TextField()
    cust_contact=models.IntegerField()
    cust_email=models.EmailField()
    cust_password=models.CharField(max_length=100)

class category_model(models.Model):
    title=models.CharField(max_length=100)
    image=models.ImageField(upload_to='image/',default=0)
    desc=models.CharField(max_length=200)
    
    def __str__(self):
        return self.title
    
class product_model(models.Model):
    title=models.CharField(max_length=100)
    desc=models.CharField(max_length=200)
    unit=models.IntegerField(default=0)
    price=models.IntegerField(default=0)
    image=models.ImageField(upload_to='image/')
    upload_by=models.CharField(max_length=100)
    upload_date=models.DateTimeField(auto_now_add=True)
    cat=models.ForeignKey(category_model,on_delete=models.CASCADE)


class cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(product_model,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.quantity*self.product.price
    

class subjects(models.Model):
    cont=models.CharField(max_length=200,default=None)

    def __str__(self):
        return self.cont
    
class contactform(models.Model):
    problems=models.ForeignKey(subjects,on_delete=models.CASCADE)
    full_name=models.CharField(max_length=100)
    email=models.EmailField(max_length=254)
    phone=models.CharField(max_length=20)
    message=models.TextField(max_length=2000)


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    # Add other fields as needed for the customer profile

    def __str__(self):
        return self.user.username
    

Status_choice=(
    ('APPROVED','APPROVED'),
    ('DELIVERD','DELIVERD')
)

class orders_data(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(product_model,on_delete=models.CASCADE)
    quntity=models.PositiveIntegerField()
    Address=models.TextField()
    status=models.CharField(max_length=100,choices=Status_choice,default='pending')
    total_amount=models.IntegerField()
    fname=models.CharField(max_length=100,default=0)
    
    mobile_no=models.CharField(max_length=100,default=0)
    email=models.EmailField(max_length=100,default=0)


class product_rating(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(product_model,on_delete=models.CASCADE)
    info=models.CharField(max_length=300,default=0)
    rating=models.IntegerField(default=0)