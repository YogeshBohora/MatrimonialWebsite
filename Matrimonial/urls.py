"""Matrimonial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from wedding.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',Home,name="home"),
    path('about',About,name="about"),
    path('signup',Signup_User,name="signup"),
    path('contact',Contact,name="contact"),
    path('admin_home',Admin_Home,name="admin_home"),
    path('login_user',Login,name="login_user"),
    path('logout',Logout,name="logout"),
    path('view_customer',View_Customer,name="view_customer"),
    path('view_customer_api',View_Customer_Api,name="view_customer_api"),
    path('profile',profile,name="profile"),
    path('profile1/(<int:pid>)',profile1,name="profile1"),
    path('view_profile/(<int:pid>)',view_profile,name="view_profile"),
    path('view_profile1/(<int:pid>)',view_profile1,name="view_profile1"),
    path('edit_status/(<int:pid>)',Edit_status,name="edit_status"),
    path('edit_religion/(<int:pid>)',Edit_Caste,name="edit_religion"),
    path('send_feedback/(<int:pid>)',Feedback,name="send_feedback"),
    path('view_feedback',View_feedback,name="view_feedback"),
    path('delete_religion/(<int:pid>)',delete_religion,name="delete_religion"),
    path('delete_user/(<int:pid>)',delete_user,name="delete_user"),
    path('delete_feedback/(<int:pid>)',delete_feedback,name="delete_feedback"),
    path('edit_profile',Update_profile,name="edit_profile"),
    path('view_user',view_user,name="view_user"),
    path('sent_message',view_sent_message,name="sent_message"),
    path('view_request_message',view_request_message,name="view_request_message"),
    path('requested_user',Requested_User,name="requested_user"),
    path('add_religion',Add_Caste,name="add_religion"),
    path('view_religion',View_Caste,name="view_religion"),
    path('change_password', Change_Password, name="change_password"),
]+static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
