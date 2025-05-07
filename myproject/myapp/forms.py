from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from .models import product_model,contactform,CustomerProfile


# class userform(forms.Form):
#     name=forms.CharField(max_length=100)
#     address=forms.CharField(max_length=200)
#     contact=forms.IntegerField()
#     email=forms.EmailField()
#     password=forms.CharField()

class userregisterationform(UserCreationForm):
    # phone_no = forms.CharField(max_length=15)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].help_text = ''
        self.fields['first_name'].help_text = ''
        self.fields['last_name'].help_text = ''
        self.fields['email'].help_text = ''
        # self.fields['phone_no'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
    
    class Meta:
        model=User
        fields=['username','first_name','last_name','email','password1','password2']

class loginform(AuthenticationForm):
    class meta:
        model=User
        fields=['username','password']

class product_form(forms.ModelForm):
    class Meta:
        model=product_model
        fields=['title','desc','image','price','cat']

        labels={
            'title':'Enter Title',
            'desc':'Enter Description',
            'image':'Upload Image',
            'price':'Enter Price',
            'cat':'Select Category'
        }
 
        widgets={
            'title':forms.TextInput(attrs={"class":"form-control"}),
            'desc':forms.TextInput(attrs={"class":"form-control"}),
            'image':forms.FileInput(),
            'price':forms.NumberInput(),
            'cat':forms.Select(attrs={"class":"form-control"})
        }

class contact(forms.ModelForm):
    class Meta:
        model=contactform
        fields=['problems','full_name','email','phone','message']

        widgets={
            "problems":forms.Select(attrs={"class":"form-control","placeholder":"How can we help you"}),
            "full_name":forms.TextInput(attrs={"class":"form-control","placeholder":"Enter your full name"}),
            "email":forms.EmailInput(attrs={"class":"form-control","placeholder":"Enter your email"}),
            "phone":forms.TextInput(attrs={"class":"form-control","placeholder":"Enter your phone no"}),
            "message":forms.TextInput(attrs={"class":"form-control","placeholder":"Enter your message"})
        }

# class product(forms.ModelForm):
#     class Meta:
#         model=product_model
#         fields=['title','desc','image','price','cat']

#         labels={
#             'title':'Enter Title',
#             'desc':'Enter Description',
#             'image':'Upload Image',
#             'price':'Enter Price',
#             'cat':'Select Category'
#         }


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ['profile_picture']

        labels={
            'profile_picture':'Upload Image'
        }