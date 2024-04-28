from django.urls import path
from . import views
from django.contrib.auth.views import (
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

urlpatterns = [
# Map the URL 'home/' to the home view
    path('home/',views.home,name='home'),
# Map the URL 'register/' to the register view
    path("register/", views.register),
# Map the URL 'login/' to the login view
    path('login/',views.login_view,name='login'),
# Map the URL 'profile/' to the profile view
    path('profile/',views.profile,name='profile'),
# Map the URL 'logout/' to the logout view
    path('logout/',views.logout_view),
 # Map the URL 'register/' to the register view
    path('register/', views.register, name='register'),
# Map the URL 'activate/<uidb64>/<token>/' to the activate_account view
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),
    # Map the URL 'password-reset/' to the PasswordResetView
    path('password-reset/', PasswordResetView.as_view(template_name="password_reset/password_reset.html"),
         name='password-reset'),
 # Map the URL 'password-reset/done/' to the PasswordResetDoneView
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='password_reset/password_reset_done.html'),
         name='password_reset_done'),
 # Map the URL 'password-reset-confirm/<uidb64>/<token>/' to the PasswordResetConfirmView
    path('password-reset-confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='password_reset/password_reset_confirm.html'),
         name='password_reset_confirm'),
# Map the URL 'password-reset-complete/' to the PasswordResetCompleteView
    path('password-reset-complete/',
         PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_complete.html'),
         name='password_reset_complete'),
]