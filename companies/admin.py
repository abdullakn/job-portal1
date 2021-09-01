from companies.models import  CompanyProfile, Gallery, JobLocation, Subscription
from accounts.models import UserCompanies
from django.contrib import admin
from  accounts.models import UserCompanies

# Register your models here.


admin.site.register(UserCompanies)
admin.site.register(Gallery)
admin.site.register(JobLocation)
admin.site.register(Subscription)
admin.site.register(CompanyProfile)
