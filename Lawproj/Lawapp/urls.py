from django.urls import path 
from . import views


from .forms import UserLoginForm
urlpatterns=[
    # path("", views.index, name='main'),
    path("signup/", views.SignUp.as_view(), name='signup'),
    path("logout/", views.logout_view, name="logout"),
    path("", views.LoginView.as_view(), name="login"),
]