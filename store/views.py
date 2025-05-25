from django.shortcuts import render, redirect 
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .forms import SignUpForm, UserUpdateForm, UserPasswordChangeForm, UserInfoForm
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from django import forms
from django.db.models import Q
import json
from cart.cart import Cart


def search(request):
    if request.method == "POST":
        search_term = request.POST.get('searched', '').strip()
        results = []
        if search_term:
            results = Product.objects.filter(
                Q(name__icontains=search_term) | Q(description__icontains=search_term)
            )
            if not results:
                messages.success(request, f'No products found for "{search_term}".')
        else:
            messages.warning(request, 'Please enter a search term.')

        return render(request, 'search.html', {
            'searched': search_term,
            'results': results
        })

    return render(request, 'search.html')


def update_info(request):
    if request.user.is_authenticated:
        #Get the current user
        current_user = Profile.objects.get(user__id=request.user.id)
        #Get the shipping address of the current user
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)

        #Get original user form
        form = UserInfoForm(request.POST or None, instance=current_user)

        #Get Users shipping address
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

        if form.is_valid() or shipping_form.is_valid():
            form.save()#Save the user info
            shipping_form.save() #Save the shipping address
            messages.success(request, ("Your profile has been updated!"))
            return redirect('home')
        return render(request, 'update_info.html', {'form':form, 'shipping_form':shipping_form})
    else:
        messages.success(request, ("You must be logged in to update your profile..."))
        return redirect('home')
   



def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        #Did they fill the form?
        if request.method == "POST":
           ##Get the form
            form = UserPasswordChangeForm(current_user, request.POST)
            #Is the form valid?
            if form.is_valid():
                #Save the new password
                form.save()
                messages.success(request, ("Your password has been updated! Please login again..."))
                #Login the user
                #login(request, current_user)
                return redirect('login')
            else:
                for error in list(form.errors.values()):
                    #If the form is not valid, show the error
                    messages.error(request, error)   
               
                    return redirect('update_password')

        else:
            form = UserPasswordChangeForm(current_user)
            
            return render(request, 'update_password.html', {'form': form})

    else:
        messages.success(request, ("You must be logged in to update your password..."))
        return redirect('login')
        


def update_profile(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UserUpdateForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request, ("Your profile has been updated!"))
            return redirect('home')
        return render(request, 'update_profile.html', {'user_form': user_form})
    else:
        messages.error(request, ("You must be logged in to update your profile..."))
        return redirect('login')



def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {'categories': categories})


def category(request, foo):
    #Replace Hyphens with spaces
    foo = foo.replace('-', ' ')
    #Grab the category from the url 
    try:
        #Look up the Category
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products':products, 'category':category})
    except:
        messages.success(request, ("That category doesnt exist..."))
        return redirect('home')



def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product': product})

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


def about(request):
    return render(request, 'about.html', {})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            #Do shopping cart stuff
            #Get the current user
            current_user = Profile.objects.get(user__id=request.user.id)
            #Get saved cart from the profile model
            saved_cart = current_user.old_cart 
            #Convert the string to a dictionary
            if saved_cart:
                #Convert the string to a dictionary using json
                converted_cart = json.loads(saved_cart)
                #Add the loaded cart to the session
                #Get the cart
                cart = Cart(request)
                #Loop through the cart and add each item to the session from the database
                for key, value in converted_cart.items():
                   cart.db_add(product=key, quantity=value)

            messages.success(request, (f"You have successfully logged in to your account. Welcome Back {username}"))
            return redirect('home')
            
        else:
            messages.success(request, ("There was an error, Please try again..."))
            return redirect('login')
        

    else:
        return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out... Thanks for stopping by..."))
    return redirect('home')


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            #login user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, (f"Your account has been created! Welcome {username}... Kindly update your profile..."))
            return redirect('update_info')
        else:
            messages.success(request, ("Whoops! There was a problem creating your account, please try again..."))
            return redirect('register')


    else:
        return render(request, 'register.html', {'form': form})


