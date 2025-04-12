from django import forms
from .models import Post, Profile
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class PostForm(forms.ModelForm):
      class Meta:
              model = Post
              fields = '__all__'



class CreateUserForm(UserCreationForm):
       class Meta:
           model = User
           fields = ['username', 'email', 'password1', 'password2']
       

class ProfileUpdateForm(forms.ModelForm):
      username = forms.CharField(disabled=True)  
      email = forms.EmailField(disabled=True)   
      class Meta:
                model = Profile
                fields = ['username', 'email', 'fname', 'cname' , 'office' , 'phone' , 'insta', 'telegram', 'profile_picture']


