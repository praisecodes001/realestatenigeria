from tokenize import Number
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.views.generic import View
from django.conf.urls.static import static
from django.utils import timezone
from decimal import Decimal
from django.utils.html import format_html
from django.contrib.auth.models import User
from django.views.generic import View
from django.utils.timezone import now
from datetime import timedelta, datetime



# Create your models here.
class Post(models.Model):
      title = models.CharField(max_length= 100, default ="")
      short = models.CharField(max_length=100, default="")
      CHOICES = [('1', 'For Rent'), ('2', 'For Sale'), ('3', 'Short-Let')]
      category = models.CharField(max_length=1, choices=CHOICES, default='1') 
     
      CHOICES = [('1', 'House'), ('2', 'Land'), ('3', 'commercial property'), ('4', 'Warehouses'), ('5', 'Fuel Stations')]
      building = models.CharField(max_length=1, choices=CHOICES, default='1' )
      
      CHOICES = [('1', 'Duplexes'), ('2', 'Block Of Flats'), ('3', 'Detached Duplexes'), ('4', 'Bungalow'), ('5', 'Mini Flats'), ('6', 'Semi detached Duplexes')]
      subtype = models.CharField(max_length=1, choices=CHOICES, default='1', null=True, blank=True)
     
      CHOICES = [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'),('7', '6+')]
      bedroom = models.CharField(max_length=1, choices=CHOICES, default='1', null=True, blank=True)
     
      CHOICES = [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'),('7', '6+')]
      toilet = models.CharField(max_length=1, choices=CHOICES, default='1', null=True, blank=True)
     
      CHOICES = [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'),('7', '6+')]
      bathroom = models.CharField(max_length=1, choices=CHOICES, default='1', null=True, blank=True)
     
      area = models.CharField(max_length= 100, default ="")
      state = models.CharField(max_length= 100, default ="")
      availability = models.CharField(max_length= 100, default ="")
      totalarea = models.PositiveBigIntegerField(default=0)
      coveredarea = models.PositiveBigIntegerField(default=0)
      currencyfield = models.CharField(max_length=100, default = "")
      description = models.TextField(max_length=1000, default=0)
      url = models.URLField(default="")
      author = models.ForeignKey(User, on_delete=models.CASCADE)
      id = models.AutoField(primary_key=True)
      thumb = models.ImageField(upload_to='thumbnails/', null=True)
      secondary = models.ImageField(upload_to='secondary_images/', null=True)
      secondary_2 = models.ImageField(upload_to='secondary_images/', null=True)
      secondary_3 = models.ImageField(upload_to='secondary_images/', null=True)
      secondary_4 = models.ImageField(upload_to='secondary_images/', null=True)
      secondary_5 = models.ImageField(upload_to='secondary_images/', null=True)
      secondary_6 = models.ImageField(upload_to='secondary_images/', null=True)

      def _str_(self):
             return self.title


      def get_absolute_url(self):
           return reverse ('post-detail', kwargs={'pk': self.pk})
 
class Profile(models.Model):
      user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
      fname = models.CharField(max_length= 100, default= "")
      cname = models.CharField(max_length= 100, default= "")
      username = models.CharField(max_length= 100, default= "")
      office = models.CharField(max_length= 100, default= 0)
      phone = models.CharField(max_length= 100, default= 0)
      email = models.CharField(max_length= 100, default= 0)
      insta = models.CharField(max_length= 100, default= 0)
      telegram = models.CharField(max_length= 100, default= 0)
      profile_picture = models.ImageField(upload_to='profile/', null=True, blank=True, default='estateapp/image/apple.png')
    
      def __str__(self):
        return f"{self.user.username}'s Profile"



class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=50, unique=True)
    price = models.PositiveIntegerField()
    duration = models.IntegerField(help_text="Duration in Days")
    post_limit = models.PositiveIntegerField(help_text="Number of posts allowed")
    call_hours = models.PositiveIntegerField(help_text="Number of call hours allowed")
    feature = models.CharField(max_length=100)
    feature1 = models.CharField(max_length=100, null=True, blank=True)
    feature2 = models.CharField(max_length=100, null=True, blank=True)
    feature3 = models.CharField(max_length=100, null=True, blank=True)
    feature4 = models.CharField(max_length=100, null=True, blank=True)
    feature5 = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class UserPlan(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True)
    verification_document = models.FileField(upload_to='agent_verification/', null=True, blank=True)

    CHOICES = [('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')]
    verification_status = models.CharField(max_length=30, choices=CHOICES, default='pending', null=True, blank=True)
     
    start_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField(null=True, blank=True)

    is_paid_active = models.BooleanField(default=False)
    paystack_reference = models.CharField(max_length=100, unique=True, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Plan"



class Payment(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    price = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True)
    reference = models.CharField(max_length=100, unique=True)
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount}"
    
class Request(models.Model):

    name = models.CharField(max_length=100, default= 0 )
    email = models.CharField(max_length= 100, default= 0)
    phone = models.CharField(max_length= 100, default= 0)

    CHOICES = [('Client', 'Client'), ('Agent', 'Agent')]
    asking = models.CharField(max_length=20, choices=CHOICES, default='Client' )
    
    
    CHOICES = [('Duplexes', 'Duplexes'), ('Block Of Flats', 'Block Of Flats'), ('Detached Duplexes', 'Detached Duplexes') , ('Bungalow', 'Bungalow') , ('Mini Flats', 'Mini Flats') , ('Semi detached Duplexes', 'Semi detached Duplexes')]
    house = models.CharField(max_length=30, choices=CHOICES, default='' )
    

    describe = models.TextField(max_length=1000, default=0)
      