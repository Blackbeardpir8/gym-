from django.urls import path
from authapp import views

urlpatterns = [
    path('',views.Home,name = "Home"),
    path('profile', views.profile, name='profile'),
    path('signup',views.signup,name="signup"),
    path('login',views.handlelogin,name="handlelogin"),
    path('logout',views.handellogout,name="handellogout"),
    path('contact',views.contact,name="contact"),
    path('enroll',views.enroll,name="enroll"),
    path('attendance',views.attendance,name = "attendance"),
    path('tracker',views.tracker,name = "tracker"),
    path('services',views.services,name="services")
]