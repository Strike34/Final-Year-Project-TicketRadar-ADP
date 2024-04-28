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
    path('home/',views.home,name='home'),
    path("register/", views.register),
    path('login/',views.login_view,name='login'),
    path('profile/',views.profile,name='profile'),
    path('logout/',views.logout_view),

    path('register/', views.register, name='register'),
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),

    path('password-reset/', PasswordResetView.as_view(template_name="password_reset/password_reset.html"),
         name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='password_reset/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='password_reset/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_complete.html'),
         name='password_reset_complete'),
]