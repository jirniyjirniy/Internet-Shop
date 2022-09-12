from django import forms
# from django.forms import ModelForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from .models import Reviews, ContactWithUs


class ReviewsForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ('name', 'email', 'text',)


class ContactForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'id': 'name', 'placeholder': 'Your Name', 'required': 'required', 'data-validation-required-message': 'Please enter your name'}))
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'type': 'email', 'class': 'form-control', 'id': 'email', 'placeholder': 'Your Email', 'required': 'required',
               'data-validation-required-message': 'Please enter your email'}))
    subject = forms.CharField(widget=forms.TextInput(
        attrs={'type': 'text','class': 'form-control', 'id': 'subject', 'placeholder': 'Subject', 'required': 'required',
               'data-validation-required-message': 'Please enter a subject'}))
    massage = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'rows': 8, 'id': 'message', 'placeholder': 'Massage', 'required': 'required',
               'data-validation-required-message': 'Please enter your message'}))


    class Meta:
        model = ContactWithUs
        fields = ('name', 'email', 'subject', 'massage',)


class SignUpForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': "form-control border",
            'id': "name_register",
            'placeholder': "Логин",
            'type': 'text',
            'name': 'name_register',
        }),
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': "form-control border",
            'id': "password_register",
            'placeholder': "Пароль",
            'type': 'password',
            'name': 'password_register',
        }),
    )
    repeat_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': "form-control border",
            'id': "repeat_password_register",
            'placeholder': "Повторите пароль",
            'type': 'password',
            'name': 'repeat_password_register',
        }),
    )

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['repeat_password']

        if password != confirm_password:
            raise forms.ValidationError(
                "Пароли не совпадают"
            )

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
        )
        user.save()
        auth = authenticate(**self.cleaned_data)
        return auth

class SignInForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': "form-control border",
            'id': "contactusername",
            'placeholder': "Логин",
            'type': 'text',
            'name': 'name',
        }),
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': "form-control border",
            'id': "inputPassword",
            'placeholder': "Пароль",
            'type': 'password',
            'name': 'password',
        })
    )

