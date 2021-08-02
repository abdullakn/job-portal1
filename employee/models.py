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
    experience=models.CharField(max_length=200,null=True,blank=True)
    gender=models.CharField(max_length=200,null=True,blank=True)
    description=models.CharField(max_length=400,null=True,blank=True)
    specialization=models.CharField(max_length=200,null=True,blank=True)
    dob=models.DateField(null=True,blank=True)


class employeePro(models.Model):
    user=models.OneToOneField(EmployeeProfile,on_delete=models.CASCADE) 
    pro_pic=models.ImageField(upload_to='pro_pics', null=True, blank=True)

class AppliedUsers(models.Model):
    user=models.ForeignKey(EmployeeProfile,on_delete=models.CASCADE)
    job=models.ForeignKey(JobDetails,on_delete=models.CASCADE) 


class EmployeeCV(models.Model):
    user=models.ForeignKey(EmployeeProfile,on_delete=models.CASCADE)
    cv=models.FileField(upload_to='employee_cv',null=True,blank=True)

class FavouriteJob(models.Model):
    user=models.ForeignKey(EmployeeProfile,on_delete=models.CASCADE)
    job=models.ForeignKey(JobDetails,on_delete=models.CASCADE) 


class MachineTestfiles(models.Model):
    machinetest=models.FileField(upload_to='machine_test',null=True,blank=True)
    user=models.ForeignKey(EmployeeProfile,on_delete=models.CASCADE)
    job=models.ForeignKey(JobDetails,on_delete=models.CASCADE) 

