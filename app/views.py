from django.shortcuts import render,redirect
from .models import *
from random import randint
from functools import wraps
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.

# decorators
def login_required(view_func):
    @wraps(view_func)
    def wrapper(request,*args,**kwargs):
        if 'id' not in request.session:
            return redirect('login')
        return view_func(request,*args,**kwargs)
    return wrapper
 
def company_login_required(view_func):
    @wraps(view_func)
    def wrapper(request,*args,**kwargs):
        if request.session.get('role') != "Company":
            return redirect('home')
        return view_func(request,*args,**kwargs)
    return wrapper



def LoginPage(request):
    return render(request,"app/LoginPage.html")

def RegistrationPage(request):
    return render(request,"app/SignupPage.html")

def HomePage(request):
    return render(request,"app/index.html")

def OtpPage(request):
    if request.method == 'POST':
        otp_entered = request.POST.get('otp')
        email = request.POST.get('email')

        try:
            user = UserMaster.objects.get(email=email)
        except UserMaster.DoesNotExist:
            return render(request,'app/Otp.html',{"msg":"Invalid user"})
        
        if str(user.otp) == otp_entered:
            user.is_verified = True
            user.otp = None
            user.save()
            return redirect('loginuser')
        else:
            return render(request,"app/Otp.html",{"msg":"Invalid otp"})
    return render(request,"app/Otp.html")





def RegisterUser(request):
    if request.method != "POST":
        return redirect('signup')

    role = request.POST.get('role','')
    fname = request.POST.get('firstname','')
    lname = request.POST.get('lastname','')
    email = request.POST.get('email','')
    password = request.POST.get('password','')
    cpassword = request.POST.get('cpassword','')

    user = UserMaster.objects.filter(email=email)

    if user:
        message = "Account Already Exist"
        return render(request,"app/SignupPage.html",{'msg':message})

    if password != cpassword:
        return render(request,"app/SignupPage.html",{'msg':"Passwords do not match"})

    otp = randint(100000,999999)
    request.session["otp"] = otp
    request.session["email"]=email

    newuser = UserMaster.objects.create(role=role,otp=otp,email=email,password=password)

    if role == "Candidate":
        Candidate.objects.create(user_id=newuser,firstname=fname,lastname=lname)
    elif role == "Company":
        Company.objects.create(user_id=newuser,firstname=fname,lastname=lname)

    return render(request,"app/Otp.html",{'email':email,'otp':otp})

def LoginUser(request):

    if request.method == "GET":
        return render(request,"app/LoginPage.html")

    if request.POST.get('role','') == "Candidate" or request.POST.get('role','') == "Company":
        email = request.POST.get('email','')
        password = request.POST.get('password','')
        try:
            user = UserMaster.objects.get(email=email)
        except UserMaster.DoesNotExist:
            return render(request,"app/LoginPage.html",{'msg':"User does not exist"})

        if not user.is_verified:
            return render(request,"app/LoginPage.html",{'msg':"Please verify OTP first"})

        if user.password == password:

            request.session['id'] = user.id
            request.session['role'] = user.role
            request.session['email'] = user.email

            if user.role == "Candidate":
                can = Candidate.objects.get(user_id=user)
                request.session['firstname']= can.firstname
                request.session['lastname'] = can.lastname

            elif user.role == "Company":
                company = Company.objects.get(user_id=user)
                request.session['firstname'] = company.firstname
                request.session['lastname'] = company.lastname

            return redirect('home')

        else:
            return render(request,"app/LoginPage.html",{'msg':"Incorrect password"})

    return render(request,"app/LoginPage.html")


@login_required
def ProfilePage(request,pk):
    if request.method == "POST":
        upload_file = request.FILES.get('profile_pic')

        if upload_file:
            print(upload_file.name)
    user = UserMaster.objects.get(pk=pk)
    if user.role == "Candidate":
        can = Candidate.objects.get(user_id=user)
        return render(request,'app/Profile.html',{'user':user,'can':can})
    elif user.role == "Company":
        company = Company.objects.get(user_id=user)
        return render(request,'app/Profile.html',{'user':user,'company':company})
    return redirect('login')
    
def UpdateProfile(request,pk):
    user = UserMaster.objects.get(pk = pk)
    if request.method != "POST":
        return redirect('home')
    if user.role == "Candidate":
        can = Candidate.objects.get(user_id = user)
        can.city = request.POST.get('city')
        # can.jobtype = request.POST.get('type')
        # can.jobcategory = request.POST.get('category')
        can.highest_edu = request.POST.get('highestedu')
        can.experience = request.POST.get('experience')
        can.country = request.POST.get('country')
        # can.website = request.POST.get('website')
        shift = request.POST.get('shift')
        if shift:
            can.shift = shift
        can.jobdescription = request.POST.get('job-description')
        min_salary = request.POST.get('min-sal')
        max_salary = request.POST.get('max-sal')
        can.min_salary = int(min_salary) if min_salary else None
        can.max_salary = int(max_salary) if max_salary else None
        can.contact = request.POST.get('contact')
        gender = request.POST.get('gender')
        if gender:
            can.gender = gender
        profile_pic = request.FILES.get('profile_pic')
        if profile_pic:
            can.profile_pic = profile_pic
        can.save()
        url = f'/profile/{pk}'
    if user.role == "Company":
        company = Company.objects.get(user_id=user)
        company.city = request.POST.get('city')
        company.company_name = request.POST.get('companyname')
        company.contact = request.POST.get('contact')
        company.address = request.POST.get('address')

        logo = request.FILES.get('logo_pic')
        if logo:
            company.logo_pic = logo

        company.save()
        url = f'/profile/{pk}'

    return redirect(url)

# @company_login_required
@login_required
@company_login_required
def post_job(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        location = request.POST.get('location')
        salary = request.POST.get('salary')
        requirements = request.POST.get('requirements')
        deadline = request.POST.get('deadline','')

        user_id = request.session['id']
        company = Company.objects.get(user_id=user_id)
       
        Job.objects.create(
            company = company,
            job_title = title,
            job_description = description,
            location = location,
            salary = salary,
            requirements = requirements,
            deadline = deadline
        )
        return redirect('home')
    return render(request,"app/post_job.html")



def job_list(request):
    from django.db.models import Q
    jobs = Job.objects.all()
    applied_jobs = []

    query = request.GET.get('q')
    if query:
        jobs = Job.objects.filter(
            Q(job_title__icontains=query) |
            Q(location__icontains=query)
        )
    else:
        jobs = Job.objects.all()

    if 'id' in request.session and request.session.get('role') == "Candidate":
        user_id = request.session['id']
        candidate = Candidate.objects.get(user_id=user_id)
        applications = Application.objects.filter(candidate=candidate)
        applied_jobs = [app.job.id for app in applications]
    

    return render(request,"app/Jobs.html",{
        "jobs":jobs,
        "applied_jobs" : applied_jobs
    })

@login_required
def apply_job(request,pk):
    user_id = request.session['id']
    job = Job.objects.get(id=pk)
    
    candidate = Candidate.objects.get(user_id = user_id)

    Application.objects.get_or_create(
        job=job,
        candidate=candidate
    )

    return redirect("jobs")


# dashboard

@login_required
def dashboard(request):
    user_id = request.session.get("id")
    if not user_id:
        return redirect('login')
    candidate = Candidate.objects.get(user_id=user_id)
    applications = Application.objects.filter(candidate=candidate)
    return render(request,"app/dashboard.html",{"applications":applications})

def logout(request):
    request.session.flush()
    return redirect('login')

def Contact_View(request):
    return render(request,'app/contact-page.html')


# company employee features

@login_required
@company_login_required
def company_dashboard(request):
    user_id = request.session.get("id")
    if not user_id:
        return redirect('login')
    company = Company.objects.get(user_id = user_id)
    jobs = Job.objects.filter(company=company)
    return render(request,"app/company-dashboard.html",{"jobs":jobs,"company": company})


# edit job by company user
@login_required
@company_login_required
def edit_job(request,pk):
    user_id = request.session.get("id")
    company = Company.objects.get(user_id=user_id)
    job = Job.objects.get(id=pk,company=company)

    if request.method == "POST":
        job.job_title = request.POST.get('job_title')
        job.job_description = request.POST.get('job_description')
        job.requirements = request.POST.get('job_requirements')
        job.salary = request.POST.get('salary')
        job.location = request.POST.get('job_location')

        deadline = request.POST.get('deadline')
        job.deadline = deadline if deadline else None

        job.save()
        return redirect('company-dashboard')
    return render(request,'app/edit-job.html',{"job":job})

# def company_dashboard(request):
#     return render(request,'app/company-dashboard.html')
    
@login_required
@company_login_required
def delete_job(request,pk):
    user_id = request.session.get("id")
    company = Company.objects.get(user_id=user_id)
    job = Job.objects.get(id=pk,company=company)

    if request.method == "POST":
        job.delete()
        return redirect('company-dashboard')
    return redirect('company-dashboard')



def ViewApplicants(request):
    return render(request,'app/view_applicants.html')