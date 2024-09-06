from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from .forms import UserSignUpForm
from django.contrib.auth import login
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