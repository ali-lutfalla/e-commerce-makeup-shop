from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from .forms import UserSignUpForm, UserSignInForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .models import Category, Product, ProductColors, ProductEntry, CartItem, WishlistItem
from .forms import ProductFilterForm
from django.contrib.auth.mixins import LoginRequiredMixin


def Home(request):
    featured_products = Product.objects.filter(featured=True)
    featured_products_with_prices = []

    for product in featured_products:
        product_entry = ProductEntry.objects.filter(productId=product).first()

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
    total_price = 0  

    for cart_item in cart_items:
        try:
            product_entry = ProductEntry.objects.get(sku=cart_item.sku)
            product_info = Product.objects.get(productId=product_entry.productId.productId)
        except ProductEntry.DoesNotExist:
            product_entry = None
        except Product.DoesNotExist:
            product_info = None

        if product_entry and product_info:
            if product_entry.sale_price is not None:
                item_total = product_entry.sale_price * cart_item.quantity  
                total_price += item_total  
            else:
                item_total = product_entry.price * cart_item.quantity  
                total_price += item_total  

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
                CartItem.objects.get_or_create(user=request.user, sku=product_entry, quantity=1)
                
            except ProductEntry.DoesNotExist:
                pass
            except Exception as e:
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
    total_price = 0 

    for cart_item in cart_items:
        try:
            product_entry = ProductEntry.objects.get(sku=cart_item.sku)
            product_info = Product.objects.get(productId=product_entry.productId.productId)
        except ProductEntry.DoesNotExist:
            product_entry = None
        except Product.DoesNotExist:
            product_info = None

        if product_entry and product_info:
            if product_entry.sale_price is not None:
                item_total = product_entry.sale_price * cart_item.quantity  
                total_price += item_total  
            else:
                item_total = product_entry.price * cart_item.quantity  
                total_price += item_total   

            items = {
                'product_info': product_info,
                'product_prices': product_entry,
                'quantity': cart_item.quantity,
                'item_total': item_total,
                'id_of_the_item': cart_item.cart_item_id,
                'sku': cart_item.sku
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
        'sku': product_to_find.sku
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

def product_search(request):
    form = ProductFilterForm(request.GET or None)
    products = Product.objects.all()

    title = None
    categories = None
    price_min = None
    price_max = None
    brands = None
    

    if form.is_valid():
        title = form.cleaned_data.get('title')
        categories = form.cleaned_data.get('category')
        price_min = form.cleaned_data.get('price_min')
        price_max = form.cleaned_data.get('price_max')
        brands = form.cleaned_data.get('brands')
        

    if title is not None:
        products = products.filter(title__icontains=title)
    if categories:
        products = products.filter(category__in=categories)
    if brands:
        products = products.filter(brand__in=brands)
    if price_min is not None:
        products = products.filter(productentry__price__gte=price_min)
    if price_max is not None:
        products = products.filter(productentry__price__lte=price_max)

    if request.headers.get('HX-Request'):
        return render(request, 'products/product_list.html', {'products': products})

    context = {
        'form': form,
        'products': products
    }

    return render(request, 'products/index.html', {'form': form,
        'products': products})


def add_to_wishlist(request):
    if request.method == "POST":
        sku = request.POST.get('sku')
        if sku:
            try:
                product_entry = ProductEntry.objects.get(sku=sku)
                wishlist_item = WishlistItem.objects.get_or_create(user=request.user, sku=product_entry)
                
            except ProductEntry.DoesNotExist:
                pass
            except Exception as e:
                print(f"Error adding to wishlist: {e}")
    return redirect('home')


def view_wishlist(request):
    wishlist_items = WishlistItem.objects.filter(user=request.user)
    products_of_the_wishlist = []

    for wishlist_item in wishlist_items:
        try:
            product_entry = ProductEntry.objects.get(sku=wishlist_item.sku)
            product_info = Product.objects.get(productId=product_entry.productId.productId)

            items = {
                'product_info': product_info,
                'product_prices': product_entry,
                'id_of_the_item': wishlist_item.wishlisit_item_id,
                'sku': wishlist_item.sku
            }

            products_of_the_wishlist.append({
                'items': items
            })

        except ProductEntry.DoesNotExist:
            product_entry = None
        except Product.DoesNotExist:
            product_info = None

    total_items = len(products_of_the_wishlist)

    return render(request, "wishlist/wishlist.html", {'wishlist_items': products_of_the_wishlist, 'total_items': total_items})

def remove_wishlist_item(request):
    if request.method == "POST":
        sku = request.POST.get('sku')
        if sku:
            try: 
                product_entry = ProductEntry.objects.get(sku=sku)
                wishlist_item = WishlistItem.objects.get(user = request.user, sku = product_entry)
                wishlist_item.delete()
            except Exception as e:
                print(f"Error removing from wishlist: {e}")
    
    return redirect('view_wishlist')


