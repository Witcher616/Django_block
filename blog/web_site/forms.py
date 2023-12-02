from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Article, Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ваш комментарий'
            }),
        }


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'short_description', 'full_description', 'photo', 'category']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Напишите заголовок статьи'
            }),
            'short_description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Напишите краткое описание статьи'
            }),
            'full_description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Напишите полное описание статьи'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control',
            }),
            'category': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Выберите категорию'
            })
        }


class UserAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Введите ваш username"
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Введите ваш пароль"
    }))

    class Meta:
        model = User


class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Введите ваш пароль"
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Введите ваш пароль"
    }))

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        widgets = {
            "username": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Введите ваш username"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Введите ваш email"
            }),
            # "password1": forms.PasswordInput(attrs={
            #     "class": "form-control",
            #     "placeholder": "Ваш пароль"
            # }),
            # "password2": forms.PasswordInput(attrs={
            #     "class": "form-control",
            #     "placeholder": "Подтвердить пароль"
            # }),
        }