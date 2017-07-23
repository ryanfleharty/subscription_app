from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Provide a valid email address.')
    store_location = forms.ChoiceField(choices=(
        ('LAGRANGE', 'La Grange'),
        ('OAKLAWN', 'Oak Lawn'),
    ), required=False)
    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        if username and User.objects.filter(username__iexact=username).exists():
            self.add_error('username', 'A user with that username already exists.')
        if email and User.objects.filter(email__iexact=email).exists():
            self.add_error('email', 'That email is already registered with an account')
        return cleaned_data

    class Meta:
        model = User
        fields = ('first_name','last_name','store_location','email','username', 'password1', 'password2')

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')
