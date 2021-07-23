from django.db import models
from accounts.models import *
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class CompanyProfile(models.Model):
    company_name=models.CharField(max_length=200,null=True,blank=True)
    email=models.EmailField(max_length=200,null=True,blank=True)
    phone_number=PhoneNumberField()
    website=models.URLField(max_length=200,null=True,blank=True)
    descriptiion=models.CharField(max_length=200,null=True,blank=True)
