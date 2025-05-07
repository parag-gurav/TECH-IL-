from django.contrib import admin
from .models import customer,product_model,category_model,contactform,subjects,orders_data,CustomerProfile

# Register your models here.
@admin.register(customer)
class adminmodel(admin.ModelAdmin):
    list_display=('id','cust_name','cust_address','cust_contact','cust_email','cust_password')

@admin.register(category_model)
class adminmodel(admin.ModelAdmin):
    list_display=['title','desc']

@admin.register(product_model)
class adminmodel(admin.ModelAdmin):
    list_display=['title','desc','unit','price','image','cat']

@admin.register(subjects)
class adminmodel(admin.ModelAdmin):
    list_display=['cont']

@admin.register(contactform)
class adminmodel(admin.ModelAdmin):
    list_display=['problems']

admin.site.register(orders_data)
    
@admin.register(CustomerProfile)
class adminmodel(admin.ModelAdmin):
    list_display=['profile_picture']