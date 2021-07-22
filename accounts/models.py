from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class UserCompanies(AbstractUser):
    company_name=models.CharField(null=True,blank=True,max_length=200)
    email = models.EmailField(unique=True)
    phone_number=PhoneNumberField()
