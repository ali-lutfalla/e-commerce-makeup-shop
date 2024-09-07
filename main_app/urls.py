from django.urls import path
from . import views # Import views to connect routes to view functions
from . import views

urlpatterns = [
    # Routes will be added here
    path('', views.Home.as_view(), name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/signin/', views.signin.as_view(), name='signin')
]