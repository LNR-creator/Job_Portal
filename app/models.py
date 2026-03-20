from django.db import models

# Create your models here.

class UserMaster(models.Model):
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    otp = models.IntegerField(null=True,blank=True)
    role = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

class Candidate(models.Model):
    user_id = models.ForeignKey(UserMaster,on_delete=models.CASCADE)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    contact = models.CharField(max_length=15)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    shift = models.CharField(max_length=20,null=True,blank=True)
    country = models.CharField(max_length=50,null=True,blank=True)
    address = models.CharField(max_length=150)
    dob = models.DateField(null=True,blank=True)
    gender = models.CharField(max_length=50)
    profile_pic = models.ImageField(upload_to="app/img/candidate",null=True,blank=True)
    email = models.EmailField(max_length=50)
    jobdescription = models.CharField(max_length=285,null=True,blank =True)
    min_salary = models.BigIntegerField(null=True,blank=True)
    max_salary = models.BigIntegerField(null=True,blank=True)
    highest_edu = models.CharField(max_length=200,null=True,blank=True)
    experience = models.CharField(max_length=300,null=True,blank=True)

class Company(models.Model):
    user_id = models.ForeignKey(UserMaster,on_delete=models.CASCADE)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    company_name = models.CharField(max_length=150)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    address = models.CharField(max_length=150)
    logo_pic = models.ImageField(upload_to="app/img/company")


class Job(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    job_title = models.CharField(max_length=200)
    job_description = models.TextField()
    location = models.CharField(max_length=100)
    salary = models.CharField(max_length=20,null=True,blank=True)
    created_at = models.DateField(auto_now_add=True)
    requirements = models.TextField(null=True,blank=True)
    deadline = models.DateField(null=True,blank=True)

    def __str__(self):
        return self.job_title

class Application(models.Model):
    job = models.ForeignKey(Job,on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate,on_delete=models.CASCADE)
    applied_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,default="Pending")

