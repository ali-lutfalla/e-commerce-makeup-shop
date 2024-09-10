from django.urls import path
from . import views # Import views to connect routes to view functions
from . import views

urlpatterns = [
    # Routes will be added here
    path('', views.Home , name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/signin/', views.signin.as_view(), name='signin'),
    path('product/<str:sku>/',views.show_product, name='show_product') ,
    path('addtocart/', views.add_to_cart, name='addtocart'),
    path('cart/', views.cart , name='cart'),
]