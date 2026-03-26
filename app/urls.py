from django.urls import path,include
from . import views

urlpatterns = [
    path("login/",views.LoginPage,name="login"),
    path("Signup/",views.RegistrationPage,name="Signup"),
    path("",views.HomePage,name="home"),
    path("register/",views.RegisterUser,name="register"),
    path("otp",views.OtpPage,name="otp"),
    path("loginuser/",views.LoginUser,name="loginuser"),
    path("profile/<int:pk>",views.ProfilePage,name="profile"),
    path("updateProfile/<int:pk>",views.UpdateProfile,name="updateprofile"),
    path("post-job/",views.post_job,name="post-job"),
    path("jobs/",views.job_list,name="jobs"),
    path("apply/<int:pk>",views.apply_job,name="apply"),
    path("dashboard/",views.dashboard,name="dashboard"),
    path("logout/",views.logout,name="logout"),
    path("contact/",views.Contact_View,name="contact"),
    # path("jobs-posted",views.jobs_posted,name="jobs-posted"),
    path("edit-job/<int:pk>",views.edit_job,name="edit-job"),
    path("company-dashboard/",views.company_dashboard,name="company-dashboard"),
    path("delete/<int:pk>",views.delete_job,name="delete-job"),
    path("applicants/<int:pk>/",views.ViewApplicants,name="applicants"),
    path("withdraw/<int:pk>/",views.withdraw_application,name="withdraw-application"),
    
]
