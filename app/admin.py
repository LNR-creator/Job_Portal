from django.contrib import admin
from .models import UserMaster,Company,Candidate,Job,Application
# Register your models here.

admin.site.register(UserMaster)
admin.site.register(Candidate)
admin.site.register(Company)
admin.site.register(Job)
admin.site.register(Application)


