from django.db import models
from accounts.models import *
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.

class CompanyProfile(models.Model):
    user=models.OneToOneField(UserCompanies,on_delete=models.CASCADE)
    company_name=models.CharField(max_length=200,null=True,blank=True)
    email=models.EmailField(max_length=200,null=True,blank=True)
    phone_number=PhoneNumberField()
    website=models.URLField(max_length=200,null=True,blank=True)
    descriptiion=models.CharField(max_length=200,null=True,blank=True)
    logo=models.ImageField(upload_to='logos', null=True, blank=True) 
    country=models.CharField(max_length=200,null=True,blank=True)
    state=models.CharField(max_length=200,null=True,blank=True)
    district=models.CharField(max_length=200,null=True,blank=True)
    postcode=models.CharField(max_length=200,null=True,blank=True)


class CompanySocial(models.Model):
    user=models.OneToOneField(CompanyProfile,on_delete=models.CASCADE)
    twitter=models.CharField(max_length=200,null=True,blank=True)
    facebook=models.CharField(max_length=200,null=True,blank=True)
    google=models.CharField(max_length=200,null=True,blank=True)
    linkedin=models.CharField(max_length=200,null=True,blank=True)


class JobDetails(models.Model):
    user=models.ForeignKey(CompanyProfile,on_delete=models.CASCADE)
    job_title=models.CharField(max_length=200,null=True,blank=True)    
    location=models.CharField(max_length=200,null=True,blank=True)    
    category=models.CharField(max_length=200,null=True,blank=True)  
    industry=models.CharField(max_length=200,null=True,blank=True)  
    description=models.CharField(max_length=200,null=True,blank=True)    
    job_type=models.CharField(max_length=200,null=True,blank=True)    
    salary_min=models.IntegerField()   
    salary_max=models.IntegerField() 
    experience=models.IntegerField()   
    qualification=models.CharField(max_length=200,null=True,blank=True)    
    req_skills=models.CharField(max_length=200,null=True,blank=True)
    create_at=models.DateTimeField(auto_now_add=True) 
    closing_date=models.DateField()
    additional_files=models.FileField(upload_to='job_additional',null=True,blank=True)
    slug=models.SlugField(max_length=200,null=True,blank=True)


# class CompanyGallery(models.Model):
#     user=models.ForeignKey(CompanyProfile,on_delete=models.CASCADE)






    








     
