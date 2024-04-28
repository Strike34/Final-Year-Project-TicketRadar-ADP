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
def home(request):
    return render(request,'home.html')
def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request,'account/register.html',{'form':form})

def login_view(request):
    form = LoginForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('profile')
    return render(request,'account/login.html',{'form':form})
@login_required
def profile(request):
    user = Account.objects.get(username=request.user.username)
    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST, instance=user)

        if form.is_valid():
            old_password = form.cleaned_data.get('old_password')
            new_password1 = form.cleaned_data.get('new_password1')
            new_password2 = form.cleaned_data.get('new_password2')

            if old_password and new_password1 and new_password2:
                user.set_password(new_password1)
                user.save()
                update_session_auth_hash(request, user)  # To prevent the user from being logged out
                messages.success(request, 'Your account has been updated Successfully.')
                return redirect('profile')  # or wherever you want to redirect after changing the password

            form.save()
            return redirect('profile')  # or wherever you want to redirect after updating the profile
    else:
        form = UserProfileUpdateForm(instance=user)
    return render(request,'account/profile.html',{'user':user,'form':form})

def logout_view(request):
    logout(request)
    return redirect('login')




def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'Your account has been activated.')
        return redirect('home')  # Redirect to your home page or wherever you want
    else:
        messages.error(request, 'Activation link is invalid.')
        return redirect('login')  # Redirect to your login page or wherever you want

