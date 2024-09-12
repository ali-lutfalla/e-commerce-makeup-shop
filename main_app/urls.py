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
    path('cart/', views.view_cart , name='cart'),
    path('updatecart/<str:cartItemId>/', views.update_cart, name="update_cart"),
    path('search/', views.product_search , name="product_search"),
    path('addtowishlist/', views.add_to_wishlist , name="addtowishlist"),
    path('wishlist/', views.view_wishlist , name="view_wishlist"),
    path('removefromwishlist/', views.remove_wishlist_item, name="remove_from_wishlist"),
]