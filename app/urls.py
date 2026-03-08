from django.urls import path,include
from . import views

urlpatterns = [
    path("/login",views.LoginPage,name="login"),
    path("Signup/",views.RegistrationPage,name="Signup"),
    path("home/",views.HomePage,name="home"),
    path("register/",views.RegisterUser,name="register"),
    path("otp",views.OptPage,name="otp"),
    path("loginuser/",views.LoginUser,name="loginuser"),
    path("profile/<int:pk>",views.ProfilePage,name="profile"),
    path("updateProfile/<int:pk>",views.UpdateProfile,name="updateprofile"),
]