from django.shortcuts import render,redirect
from .models import *
from random import randint
# Create your views here.


def LoginPage(request):
    return render(request,"app/LoginPage.html")

def RegistrationPage(request):
    return render(request,"app/SignupPage.html")

def HomePage(request):
    return render(request,"app/index.html")

def OptPage(request):
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
    if request.POST.get('role')=="Candidate":
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
        else:
            if password == cpassword:
                otp = randint(100000,999999)
                newuser = UserMaster.objects.create(role=role,otp=otp,email=email,password=password)
                newcand = Candidate.objects.create(user_id = newuser,firstname = fname,lastname=lname)
                return render(request,"app/Otp.html",{'email':email})
    else:
         return render(request,"app/SignupPage.html",{
            'msg':"Company registration not implemented yet"
        })


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

        if user.password == password and user.role == "Candidate":
            can = Candidate.objects.get(user_id=user)
            request.session['id'] = user.id
            request.session['role'] = user.role
            request.session['firstname']= can.firstname
            request.session['lastname'] = can.lastname
            request.session['email'] = user.email
            return redirect('home')
        elif user.password == password and user.role == "Company":
            can = Company.objects.get(user_id = user)
            request.session['id'] = user.id
            request.session['role'] =user.role
            request.session['firstname'] = can.firstname
            request.session['lastname'] = can.lastname
            request.session['email'] = user.email
            return redirect('home')
        else:
            return render(request,"app/LoginPage.html",{'msg':"Incorrect password"})

    return render(request,"app/LoginPage.html")


def ProfilePage(request,pk):
    if request.method == "POST":
        upload_file = request.FILES.get('profile_pic')

        if upload_file:
            print(upload_file.name)
    user = UserMaster.objects.get(pk=pk)
    can = Candidate.objects.get(user_id = user)
    return render(request,'app/Profile.html',{'user':user,'can':can})
    
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
    return redirect(url)


def post_job(request):
    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']
        location = request.POST['location']
        salary = request.POST['salary']

        company = Company.objects.first()

        Job.objects.create(
            company = company,
            job_title = title,
            job_description = description,
            location = location,
            salary = salary
        )
        return redirect('home')
    return render(request,"app/post_job.html")


def job_list(request):
    jobs = Job.objects.all()
    return render(request,"app/Jobs.html",{"jobs":jobs})

def apply_job(request,pk):
    job = Job.objects.get(id=pk)
    candidate = Candidate.objects.first()

    Application.objects.create(
        job=job,
        candidate=candidate
    )

    return redirect("jobs")


# dashboard

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

