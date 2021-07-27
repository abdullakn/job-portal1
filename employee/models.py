from companies.models import JobDetails
from accounts.models import UserCompanies
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class EmployeeProfile(models.Model):
    user=models.OneToOneField(UserCompanies,on_delete=models.CASCADE)
    name=models.CharField(max_length=200,null=True,blank=True)
    email=models.CharField(max_length=200,null=True,blank=True)
    phone=PhoneNumberField()
    age=models.IntegerField(null=True,blank=True)
    place=models.CharField(max_length=200,null=True,blank=True)
    education=models.CharField(max_length=200,null=True,blank=True)


class AppliedUsers(models.Model):
    user=models.ForeignKey(EmployeeProfile,on_delete=models.CASCADE)
    job=models.ForeignKey(JobDetails,on_delete=models.CASCADE)    
