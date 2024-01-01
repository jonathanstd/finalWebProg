import contextlib
import json
from django.shortcuts import render, redirect
from .models import Product, models
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from .models import UserProfile
from django.contrib import messages
from .models import Order

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Add other fields as needed

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')

        # Create User
        user = User.objects.create_user(username=username, password=password)
        user.save()

        # Create UserProfile
        profile = UserProfile(user=user)
        # Add other UserProfile fields as needed
        profile.save()

        # Optional: Log the user in directly after registration
        auth_login(request, user)

        return redirect('home')  # Redirect to home or another appropriate page
    else:
        return render(request, 'register.html')  # Replace 'register.html' with your template

def add_to_cart(request, product_id):
    # Get the product details based on the product_id
    # Perform any necessary validation and logic here

    # Initialize an empty cart if it doesn't exist in the session
    cart = request.session.get('cart', {})

    # Add the product to the cart or update its quantity if it's already in the cart
    cart[product_id] = cart.get(product_id, 0) + 1

    # Save the updated cart in the session
    request.session['cart'] = cart

    # Return a JSON response indicating success or failure
    response_data = {'success': True, 'message': 'Item added to cart'}
    return JsonResponse(response_data)

def view_cart(request):
    # Retrieve the cart from the session
    cart = request.session.get('cart', {})

    # Calculate the total price of items in the cart
    total_price = calculate_total_price(cart)  # Implement this function

    # Render the cart template with the cart data and total price
    return render(request, 'cart.html', {'cart': cart, 'total_price': total_price})

def remove_from_cart(request, product_id):
    # Get the cart from the session
    cart = request.session.get('cart', {})

    # Remove the product from the cart if it exists
    if product_id in cart:
        del cart[product_id]

    # Save the updated cart in the session
    request.session['cart'] = cart

    # Redirect back to the cart page
    return redirect('view_cart')

def calculate_total_price(cart):
    total_price = 0
    for product_id, quantity in cart.items():
        # Retrieve the product price based on the product_id from the database
        product = Product.objects.get(id=product_id)
        product_price = product.price
        subtotal = product_price * quantity
        total_price += subtotal
    return total_price


def home_view(request):
    return render(request, 'home.html')


def canoncam_view(request):
    return render(request, 'canoncam.html')


def canonlens_view(request):
    return render(request, 'canonlens.html')


def sonycam_view(request):
    return render(request, 'sonycam.html')


def sonylens_view(request):
    return render(request, 'sonylens.html')

def cart_view(request):
    cart = request.session.get('cart', {})
    total_price = calculate_total_price(cart)
    return render(request, 'cart.html', {'cart': cart, 'total_price': total_price})

def account_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if action == 'register':
            # Registration logic
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                return render(request, 'account.html', {'error': 'Username already exists'})
            user = User.objects.create_user(username=username, password=password)
            user.save()
            profile = UserProfile(user=user)
            profile.save()
            messages.success(request, 'Account created successfully')

        elif action == 'login':
            # Login logic
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('member')
            else:
                return render(request, 'member.html', {'error': 'Invalid username or password.'})

    return render(request, 'account.html')

def member_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('member')
        else:
            context = {'error': 'Invalid username or password.'}
            return render(request, 'account.html', context)
    else:
        return render(request, 'member.html')

def orders_view(request):
    # Query your orders data here, for example:
    user_orders = Order.objects.filter(user=request.user)

    context = {'user_orders': user_orders}
    return render(request, 'orders.html', context)

def create_order(request):
    if request.method == 'POST':
        # Extract order data from the request
        items = request.POST.getlist('items[]')  # This depends on your form data structure
        total_price = request.POST.get('total_price')

        try:
            # Create a new order instance and save it to the database
            order = Order.objects.create(total_price=total_price)

            # Loop through the submitted items and create order items
            for item in items:
                # Parse the item data, assuming it's in JSON format
                item_data = json.loads(item)
                product_name = item_data.get('name')
                quantity = item_data.get('quantity')
                price = item_data.get('price')

                # Create an order item and associate it with the order
                order_item = OrderItem.objects.create(
                    order=order,
                    product_name=product_name,
                    quantity=quantity,
                    price=price
                )

            # Return a JSON response indicating success
            response_data = {'success': True, 'message': 'Order created successfully'}
            return JsonResponse(response_data)

        except Exception as e:
            # Handle any errors that may occur during order creation
            response_data = {'success': False, 'message': str(e)}
            return JsonResponse(response_data, status=400)