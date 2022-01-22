from main_app.models import Post, Comment
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms


class PostForm(forms.ModelForm):
    photos = forms.ImageField(label='Фотографии', widget=forms.FileInput(attrs={
        'class': 'form-control',
        'multiple': 'multiple'
    }))

    class Meta:
        model = Post
        fields = ['title', 'image', 'description', 'address', 'contacts']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'contacts': forms.TextInput(attrs={'class': 'form-control'}),
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['rate', 'text']
        widgets = {
            'rate': forms.Select(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
        }


class UserSignupForm(UserCreationForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'})
        }


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'forms-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'forms-control'}))
