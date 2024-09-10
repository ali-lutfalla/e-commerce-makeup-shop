from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from .forms import UserSignUpForm, UserSignInForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .models import Category, Product, ProductColors, ProductEntry, CartItem
# Create your views here.

def Home(request):
    featured_products = Product.objects.filter(featured=True)
    featured_products_with_prices = []

    for product in featured_products:
        product_entry = ProductEntry.objects.filter(productId=product).first()

        # colors = [entry.colorId for entry in product_entries]

        product.price = product_entry.price
        product.sku = product_entry.sku
        product.sale_price = product_entry.sale_price

        featured_products_with_prices.append({
        'product': product,
            })
    return render(request, 'home.html', {'products': featured_products_with_prices})

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

def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    product_of_the_cart = []
    total_price = 0  # Initialize total price

    for cart_item in cart_items:
        try:
            product_entry = ProductEntry.objects.get(sku=cart_item.sku)
            product_info = Product.objects.get(productId=product_entry.productId.productId)
        except ProductEntry.DoesNotExist:
            product_entry = None
        except Product.DoesNotExist:
            product_info = None

        if product_entry and product_info:
            item_total = product_entry.price * cart_item.quantity  # Calculate total for this item
            total_price += item_total  # Add to total price

            items = {
                'product_info': product_info,
                'product_prices': product_entry,
                'quantity': cart_item.quantity,
                'item_total': item_total,
                'id_of_the_item': cart_item.cart_item_id
            }

            product_of_the_cart.append({
                'items': items
            })

    total_items = len(product_of_the_cart)

    return render(request, "cart/cart.html", {'cart_items': product_of_the_cart, 'total_items': total_items, 'total_price': total_price})


def add_to_cart(request):
    if request.method == "POST":
        sku = request.POST.get('sku')
        if sku:
            try:
                product_entry = ProductEntry.objects.get(sku=sku)
                cart_item, created = CartItem.objects.get_or_create(user=request.user, sku=product_entry)
                if not created:
                    cart_item.quantity += 1
                cart_item.save()
            except ProductEntry.DoesNotExist:
                # Handle the case where the product entry doesn't exist
                pass
            except Exception as e:
                # Log the exception or handle other errors
                print(f"Error adding to cart: {e}")
    return redirect('home')

def update_cart(request, cartItemId):
    cart_item = CartItem.objects.get(cart_item_id=cartItemId)
    new_quantity = request.POST.get('quantity')

    if new_quantity and new_quantity.isdigit():
        new_quantity = int(new_quantity)
        if new_quantity > 0:
            cart_item.quantity = new_quantity
            cart_item.save()
        
        else:
            cart_item.delete()
    
    cart_items = CartItem.objects.filter(user=request.user)
    product_of_the_cart = []
    total_price = 0  # Initialize total price

    for cart_item in cart_items:
        try:
            product_entry = ProductEntry.objects.get(sku=cart_item.sku)
            product_info = Product.objects.get(productId=product_entry.productId.productId)
        except ProductEntry.DoesNotExist:
            product_entry = None
        except Product.DoesNotExist:
            product_info = None

        if product_entry and product_info:
            item_total = product_entry.price * cart_item.quantity  # Calculate total for this item
            total_price += item_total  # Add to total price

            items = {
                'product_info': product_info,
                'product_prices': product_entry,
                'quantity': cart_item.quantity,
                'item_total': item_total,
                'id_of_the_item': cart_item.cart_item_id
            }

            product_of_the_cart.append({
                'items': items
            })

    total_items = len(product_of_the_cart)

    return render(request, "cart/cart.html", {'cart_items': product_of_the_cart, 'total_items': total_items, 'total_price': total_price})


def show_product(request, sku):
    product_to_find = ProductEntry.objects.get(sku = sku)

    product = {
        'price': product_to_find.price,
        'sale_price': product_to_find.sale_price,
    }

    product_info = Product.objects.get(productId = product_to_find.productId.productId)

    product.update({
        'title': product_info.title,
        'product_type': product_info.product_type,
        'image': product_info.image,
        'description': product_info.description,
        'category': product_info.category,
        'brand': product_info.brand
    })

    return render(request, 'products/product-show.html', {'product': product})


    

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