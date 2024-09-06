from django.shortcuts import render, redirect
from .forms import SignUpForm, UserLoginForm
from django.views.generic import CreateView, DeleteView, FormView
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import json

# Load the saved transformer model and tokenizer
model_path = "path/to/your/saved/model"  # Replace with the actual path to your saved model
tokenizer_path = "path/to/your/saved/tokenizer"  # Replace with the actual path to your saved tokenizer

tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
model = AutoModelForCausalLM.from_pretrained(model_path)


class SignUp(CreateView):
    form_class = SignUpForm
    template_name = 'pages/signup.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
        
        return response 

    def form_invalid(self, form):
        # Loop through form errors and display them
        for field, errors in form.errors.items():
            for error in errors:
                messages.warning(self.request, f"{field}: {error}")

        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse("login")



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
    return redirect("login")


# def index(request):
#     #check if user is authenticated
#     if request.user.is_authenticated:
#         if request.method == 'POST':
#             #get user input from the form
#             user_input = request.POST.get('userInput')
#             #clean input from any white spaces
#             clean_user_input = str(user_input).strip()

# Chat page view with authentication required
@login_required
def index(request):
    return render(request,"pages/index.html", {'user': request.user})

# Chat with model view
@csrf_exempt
def chat_with_model(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "")

            # Tokenize the user message
            inputs = tokenizer.encode(user_message, return_tensors="pt")

            # Generate a response using the model
            output = model.generate(inputs, max_length=100, num_return_sequences=1)

            # Decode the generated response
            response = tokenizer.decode(output[0], skip_special_tokens=True)

            return JsonResponse({"response": response})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)