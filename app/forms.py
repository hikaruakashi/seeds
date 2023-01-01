from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Post
from django import forms


# class NewQuestionForm(forms.ModelForm):
#     class Meta:
#         model = Port
#         fields = ['title', 'body']
#         widgets = {
#             'title': forms.TextInput(attrs={
#                 'autofocus': True,
#                 'placeholder': 'How to create a Q&A website with Django?'
#             })
#         }
        
class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title','image','topic','description','link']
        widgets = {
            'title': forms.TextInput(attrs={
                'autofocus': True,
                'placeholder': '作品名'
            }),
            
            'description': forms.Textarea(attrs={
                'autofocus': True,
                'placeholder': '説明…'
            }),
            
            'link': forms.TextInput(attrs={
                'autofocus': True,
                'placeholder': '作品のGithubリンク'
            })
        }

class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'email': forms.EmailInput(attrs={
                'required': True,
                'placeholder': 'example@st.kyusan-u.ac.jp',
                'autofocus': True
            }),
            'username': forms.TextInput(attrs={
                'placeholder': 'yamada',
            })
        }

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs = {'placeholder': 'password'}
        self.fields['password2'].widget.attrs = {'placeholder': 'confirm password'}

class LoginForm(AuthenticationForm):
    class Meta:
        fields = '__all__'