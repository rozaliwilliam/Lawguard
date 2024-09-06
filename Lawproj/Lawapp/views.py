from django.shortcuts import render, redirect
from .forms import SignUpForm, UserLoginForm
from django.views.generic import CreateView, DeleteView, FormView
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse




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


def index(request):
    return render(request,"pages/index.html")



import torch
from django.shortcuts import render
from django.http import JsonResponse
from transformers import BertTokenizer, BertForQuestionAnswering

# Load the model and tokenizer
MODEL_PATH = 'qa/bert_model/model'
TOKENIZER_PATH = 'qa/bert_model/tokenizer'

tokenizer = BertTokenizer.from_pretrained(TOKENIZER_PATH)
model = BertForQuestionAnswering.from_pretrained(MODEL_PATH)

# The view that processes the user's question
def answer_question(request):
    if request.method == 'POST':
        # Get the user input question
        question = request.POST.get('question')
        
        # Your context can come from a predefined text or another input
        context = "Django is a high-level Python web framework that allows rapid development of secure and maintainable websites."

        # Encode the inputs
        inputs = tokenizer.encode_plus(question, context, add_special_tokens=True, return_tensors="pt")
        input_ids = inputs["input_ids"]
        attention_mask = inputs["attention_mask"]

        # Get model outputs
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        start_idx = torch.argmax(outputs.start_logits)
        end_idx = torch.argmax(outputs.end_logits) + 1

        # Decode the answer
        answer_ids = input_ids[0][start_idx:end_idx]
        answer = tokenizer.convert_ids_to_tokens(answer_ids)
        answer = tokenizer.convert_tokens_to_string(answer)

        # Pass the question and answer to the template for rendering
        return render(request, 'chat.html', {
            'question': question,
            'answer': answer,
        })

    return render(request, 'chat.html')