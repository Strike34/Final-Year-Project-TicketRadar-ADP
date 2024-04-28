from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.forms import UserChangeForm
from .models import Account
class RegisterForm(UserCreationForm):
    class Meta:
        model = Account
        # fields = '__all__'
        fields = ['first_name','last_name','email','username']


    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input'
            self.fields[field].widget.attrs['placeholder'] = self.fields[field].label
class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        # for field in self.fields:
        self.fields['username'].widget.attrs['class'] = 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'

        self.fields['password'].widget.attrs['class'] = 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'

class UserProfileUpdateForm(UserChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(), required=False, label='Old Password')
    new_password1 = forms.CharField(widget=forms.PasswordInput(), required=False, label='New Password')
    new_password2 = forms.CharField(widget=forms.PasswordInput(), required=False, label='Confirm New Password')

    class Meta:
        model = Account
        fields = ['first_name', 'last_name','username' ,'email']

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get('old_password')
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if (new_password1 or new_password2) and not old_password:
            raise forms.ValidationError('Please enter your old password to change it.')

        if old_password and not self.instance.check_password(old_password):
            raise forms.ValidationError('Incorrect old password.')

        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError('New passwords do not match.')

        return cleaned_data
    def __init__(self, *args, **kwargs):
        super(UserProfileUpdateForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input'
            self.fields[field].widget.attrs[
                'placeholder'] = self.fields[field].label
