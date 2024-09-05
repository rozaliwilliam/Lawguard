from django.urls import path 
from . import views


from .forms import UserLoginForm
urlpatterns=[
    path("", views.LoginView.as_view(), name="login"),
    path("signup/", views.SignUp.as_view(), name='signup'),
    path("index/", views.index, name='main'),
    path("logout/", views.logout_view, name="logout"),
    
]