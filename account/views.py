from django.shortcuts import render,redirect,HttpResponse
from .forms import RegisterForm,LoginForm,UserProfileUpdateForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Account
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode
# Create your views here.
# Define the home view
def home(request):
    # Render the home.html template
    return render(request,'home.html')

# Define the register view
def register(request):
    # Initialize the registration form
    form = RegisterForm()
    # Check if the request method is POST
    if request.method == 'POST':
        # If it is, populate the form with the data from the request
        form = RegisterForm(request.POST)
        # Check if the form is valid
        if form.is_valid():
            # If it is, save the user and redirect to the login page
            user = form.save(commit=False)
            user.save()
            return redirect('login')
    else:
        # If the request method is not POST, initialize an empty form
        form = RegisterForm()
    # Render the registration page with the form
    return render(request,'account/register.html',{'form':form})

# Define the login view
def login_view(request):
    # Initialize the login form with the data from the request
    form = LoginForm(request.POST)
    # Check if the request method is POST
    if request.method == 'POST':
        # If it is, check if the form is valid
        if form.is_valid():
            # If it is, authenticate the user
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            # If the user is authenticated, log them in and redirect to the profile page
            if user:
                login(request, user)
                return redirect('profile')
    # Render the login page with the form
    return render(request,'account/login.html',{'form':form})

# Define the profile view, which requires the user to be logged in
@login_required
def profile(request):
    # Get the current user
    user = Account.objects.get(username=request.user.username)
    # Check if the request method is POST
    if request.method == 'POST':
        # If it is, populate the form with the data from the request and the current user
        form = UserProfileUpdateForm(request.POST, instance=user)
        # Check if the form is valid
        if form.is_valid():
            # If it is, get the old and new passwords from the form
            old_password = form.cleaned_data.get('old_password')
            new_password1 = form.cleaned_data.get('new_password1')
            new_password2 = form.cleaned_data.get('new_password2')
            # If the old and new passwords are provided, change the user's password
            if old_password and new_password1 and new_password2:
                user.set_password(new_password1)
                user.save()
                # Update the session auth hash to prevent the user from being logged out
                update_session_auth_hash(request, user)
                # Show a success message and redirect to the profile page
                messages.success(request, 'Your account has been updated Successfully.')
                return redirect('profile')
            # Save the form and redirect to the profile page
            form.save()
            return redirect('profile')
    else:
        # If the request method is not POST, initialize the form with the current user's data
        form = UserProfileUpdateForm(instance=user)
    # Render the profile page with the user and form
    return render(request,'account/profile.html',{'user':user,'form':form})

# Define the logout view
def logout_view(request):
    # Log the user out
    logout(request)
    # Redirect to the login page
    return redirect('login')

# Define the account activation view
def activate_account(request, uidb64, token):
    try:
        # Decode the user ID from the URL
        uid = force_str(urlsafe_base64_decode(uidb64))
        # Get the user with the decoded ID
        user = Account.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        # If any errors occur, set the user to None
        user = None

    # If the user exists and the token is valid, activate the user's account
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        # Log the user in
        login(request, user)
        # Show a success message and redirect to the home page
        messages.success(request, 'Your account has been activated.')
        return redirect('home')
    else:
        # If the user does not exist or the token is invalid, show an error message and redirect to the login page
        messages.error(request, 'Activation link is invalid.')
        return redirect('login')