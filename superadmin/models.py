from django.db import models


from django_random_queryset import RandomManager


# Create your models here.


class CategoryDomain(models.Model):
    category=models.CharField(null=True,blank=True,max_length=200)
    slug=models.CharField(max_length=200,null=True,blank=True)

    def __str__(self):
        return self.category


class Question(models.Model):
    category=models.ForeignKey(CategoryDomain,on_delete=models.CASCADE)
    question=models.CharField(max_length=200,null=True,blank=True)    
    option1=models.CharField(max_length=200,null=True,blank=True)    
    option2=models.CharField(max_length=200,null=True,blank=True)    
    option3=models.CharField(max_length=200,null=True,blank=True)    
    option4=models.CharField(max_length=200,null=True,blank=True)    
    answer=models.CharField(max_length=200,null=True,blank=True)
 

    def __str__(self):
        return self.question



