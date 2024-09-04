from django.shortcuts import render, redirect
from .forms import SignUpForm, UserLoginForm
from django.views.generic import CreateView, DeleteView, FormView
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse


# Create your views here.

class SignUp(CreateView):
    form_class = SignUpForm
    template_name = 'pages/signup.html'

    def form_valid(self, form):
        response = super().form_valid(form)

        username = form.cleaned_data('username')
        password = form.cleaned_data('password')
        user = authenticate(username = username, password= password)
        login(self.request, user)
    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.warning(self.request, f"{field}: {error}")
        return redirect(self.request.META['HTTP_REFERER'])
    def get_success_url(self):
        return reverse("main")
    

class LoginView(FormView):
    form_class = UserLoginForm
    template_name = "pages/login.html"
    def form_valid(self, form):
        response = super().form_valid(form)
        # Get the user's username and password and authenticate
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        # Authenticate the user and log him/her in
        user = authenticate(username=username, password=password)
        login(self.request, user)
        messages.success(self.request, "You are logged in")
        return response
    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.warning(self.request, f"{error}")
        return redirect(self.request.META['HTTP_REFERER'])
    def get_success_url(self):
        return reverse("main")


def logout_view(request):
    logout(request)
    messages.success(request, "Succesfully logged out")
    return redirect("main")


# def index(request):
#     #check if user is authenticated
#     if request.user.is_authenticated:
#         if request.method == 'POST':
#             #get user input from the form
#             user_input = request.POST.get('userInput')
#             #clean input from any white spaces
#             clean_user_input = str(user_input).strip()

