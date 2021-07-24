from accounts.models import UserCompanies
from companies.models import CompanyProfile, CompanySocial
from django.http.response import HttpResponse
from django.shortcuts import redirect, render

# Create your views here.


def add_jobs(request):
    return render(request,'companies/add_job.html')


def company_profile(request):
    print("dfdfdfdf")
    if request.method == 'POST':
        print(request.user)
        print("fdfdfdf")
        data=request.POST
        files=request.FILES
        
        if not files:
            try:
                pro=CompanyProfile.objects.get(user=request.user)
                logo=pro.logo
            except:
                logo='\logos\images.png'     
        else:
            logo=files['logo']  
        # if files is None:
        #     pro=CompanyProfile.objects.get(user=request.user)
        #     logo=pro.logo
        # else:
        # if 
        # if CompanyProfile.objects.filter(user=request.user).exists():

        
                
        
        name=data['cname']
        email=data['cemail']
        phone=data['cphone']
        website=data['cwebsite']
        description=data['cdescription']
        country=data['country']
        state=data['state']
        district=data['district']
        pincode=data['postcode']
        twitter=data['twitter']
        facebook=data['facebook']
        google=data['google']
        linkedin=data['linkedin']
        print(twitter,facebook,google)

        print(data)

        if CompanyProfile.objects.filter(user=request.user).exists():
            company=CompanyProfile.objects.get(user=request.user)
            print("asdfghjkl",company)
            
            company.user=request.user
            company.company_name=name
            company.email=email
            company.phone_number=phone
            # company.website=website
            company.descriptiion=description
            company.country=country
            company.state=state
            company.district=district
            company.postcode=pincode
            company.logo=logo
            company.save()
            if CompanySocial.objects.filter(user=company).exists():
                website=CompanySocial.objects.get(user=company)
                print("dfghjklfghjk",website)
                print(website.user,website.facebook,website.twitter,website.google)
                print(company,twitter)
                website.user=company
                website.twitter=twitter
                website.facebook=facebook
                website.google=google
                website.linkedin=linkedin
                website.save()
        else:
            company=CompanyProfile(user=request.user,company_name=name,email=email,phone_number=phone,website=website,descriptiion=description,country=country,state=state,district=district,postcode=pincode,logo=logo)
            company.save()
            website=CompanySocial(user=company,twitter=twitter,facebook=facebook,google=google,linkedin=linkedin)
            website.save()


        
        return redirect(company_profile)
    print(request.user) 
    user=UserCompanies.objects.get(username=request.user)
    print(user)
    try:
        profile=CompanyProfile.objects.get(user=user) 
    except CompanyProfile.DoesNotExist:
        profile=None
      
    try:
        website=CompanySocial.objects.get(user=profile) 
    except CompanySocial.DoesNotExist:
        website=None
    context={
        'user':user,
        'profile':profile,
        'website':website
    }
    return render(request,'companies/company_profile.html',context)    
