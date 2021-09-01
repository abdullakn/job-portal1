from superadmin.models import CategoryDomain
from django.db.models.base import Model
from companies.models import JobDetails
from accounts.models import UserCompanies
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from froala_editor.fields import FroalaField
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
    created_at=models.DateField(auto_now_add=True,null=True,blank=True)


class CoverLetter(models.Model):
    user=models.ForeignKey(EmployeeProfile,on_delete=models.CASCADE)
    coverletter=FroalaField()  


class EducationDetails(models.Model):
    user=models.ForeignKey(EmployeeProfile,on_delete=models.CASCADE) 
    title=models.CharField(max_length=200,null=True,blank=True)
    startyear=models.IntegerField()
    endyear=models.IntegerField()
    institute=models.CharField(max_length=200,null=True,blank=True)


class ExperienceDetails(models.Model):
    user=models.ForeignKey(EmployeeProfile,on_delete=models.CASCADE) 
    title=models.CharField(max_length=200,null=True,blank=True)
    years=models.IntegerField() 
    present=models.CharField(max_length=200,null=True,blank=True,default=False)
    company=models.CharField(max_length=200,blank=True,null=True)



class SkillsDetails(models.Model):
    user=models.ForeignKey(EmployeeProfile,on_delete=models.CASCADE) 
    skill=models.CharField(max_length=200,null=True,blank=True)
    percentage=models.IntegerField() 


class AwardsDetails(models.Model):
    user=models.ForeignKey(EmployeeProfile,on_delete=models.CASCADE) 
    award=models.CharField(max_length=200,null=True,blank=True) 
    years=models.IntegerField()   
    company=models.CharField(max_length=200,blank=True,null=True)


class SkillBadges(models.Model):
    user=models.ForeignKey(EmployeeProfile,on_delete=models.CASCADE) 
    category=models.ForeignKey(CategoryDomain,on_delete=models.CASCADE)
    badge=models.CharField(max_length=200,null=True,blank=True)

    score=models.IntegerField()
  


class NeededFilesMachineTest(models.Model):
    machinetest=models.ForeignKey(MachineTestfiles,on_delete=models.CASCADE)
    # machinetest=models.CharField(max_length=200,null=True,blank=True)
    github=models.CharField(max_length=200,blank=True,null=True)
    compressed=models.CharField(max_length=200,null=True,blank=True)
    # compressed=models.FileField(upload_to='machine_test',null=True,blank=True)    
    host=models.CharField(max_length=200,null=True,blank=True)



class ReplyMachineTest(models.Model):  
    machinetest=models.ForeignKey(MachineTestfiles,on_delete=models.CASCADE)
    github=models.CharField(max_length=200,blank=True,null=True) 
    compressed=models.FileField(upload_to='machine_test',null=True,blank=True)    
    host=models.CharField(max_length=200,null=True,blank=True)
  

    

