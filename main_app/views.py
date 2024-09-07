from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from .forms import UserSignUpForm, UserSignInForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
# Create your views here.

class Home(LoginView):
    template_name = 'home.html'

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            error_message = "Invalid sign up - try again"

    form = UserSignUpForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)

class signin(LoginView):
    form_class = UserSignInForm
    template_name = 'signin.html'

# def signin(request):
#     if request.user.is_authenticated:
#         return redirect("home")
#     error_message = ''
#     if request.method == "POST":
#         email = request.POST.get("email")
#         password = request.POST.get("password")

#         try:
#             user = User.objects.get(email=email)
#         except:
#             error_message = "Invalid sign in - try again"

#         user = authenticate(request, email=email, password=password)

#         if user is not None:
#             login(request, user)
#             return redirect("home")
#         else:
#             error_message = "Invalid sign in - try again"

#     context = {'error_message': error_message}
#     return render(request, "signin.html", context)