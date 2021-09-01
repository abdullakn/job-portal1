from django.db import models
from django.db.models.aggregates import Count
from django.db.models.fields import DateTimeField
from accounts.models import *
from phonenumber_field.modelfields import PhoneNumberField
import geocoder


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


class Subscription(models.Model):
    user=models.ForeignKey(CompanyProfile,on_delete=models.CASCADE)
    expiry_date=DateTimeField()
    subscription_type=models.CharField(max_length=200,null=True,blank=True)    
    job_remaining=models.IntegerField()





class CompanySocial(models.Model):
    user=models.OneToOneField(CompanyProfile,on_delete=models.CASCADE)
    twitter=models.CharField(max_length=200,null=True,blank=True)
    facebook=models.CharField(max_length=200,null=True,blank=True)
    google=models.CharField(max_length=200,null=True,blank=True)
    linkedin=models.CharField(max_length=200,null=True,blank=True)


class CompanyExtra(models.Model):
    user=models.OneToOneField(CompanyProfile,on_delete=models.CASCADE)
    company_size=models.CharField(max_length=200,null=True,blank=True)

    categorie=models.CharField(max_length=200,null=True,blank=True)
    founded=models.CharField(max_length=200,null=True,blank=True)
    revenue=models.CharField(max_length=200,null=True,blank=True)



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

      
                







mapbox_access_token = 'pk.eyJ1IjoiYWJkdWxsYWtuIiwiYSI6ImNrczRnMTFlYjAxeWUydnFpbjNyY2llNXYifQ.Xnf-vVT3fcwwzpo4BL9-cw'    

class JobLocation(models.Model):
    user=models.OneToOneField(JobDetails,on_delete=models.CASCADE)
    address = models.TextField()
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)

    def save(self, *args, **kwargs):
        g = geocoder.mapbox(self.address, key=mapbox_access_token)
        g = g.latlng  # returns => [lat, long]
        self.lat = g[0]
        self.long = g[1]
        return super(JobLocation, self).save(*args, **kwargs)





# class CompanyGallery(models.Model):
#     user=models.ForeignKey(CompanyProfile,on_delete=models.CASCADE)

class Gallery(models.Model):
    user=models.ForeignKey(CompanyProfile,on_delete=models.CASCADE)
    gallery=models.ImageField(upload_to='gallery', null=True, blank=True) 






    








     
