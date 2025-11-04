# chatx/forms.py

from django import forms
from .models import Post, Profile, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .validators import validate_username, validate_email_unique, validate_username_unique

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'image', 'video']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 4, 
                'placeholder': "What's on your mind?",
                'class': 'form-control'
            }),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'video': forms.FileInput(attrs={'class': 'form-control'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get('image')
        video = cleaned_data.get('video')
        text = cleaned_data.get('text')
        
        if not text and not image and not video:
            raise forms.ValidationError("Post must have text or media content.")
        
        if image and video:
            raise forms.ValidationError("Please upload either an image OR a video, not both.")
        
        return cleaned_data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={
                'placeholder': 'Write a comment...',
                'class': 'form-control'
            }),
        }


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Validate format
        validate_username(username)
        # Check if unique
        validate_username_unique(username)
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Check if unique
        validate_email_unique(email)
        return email


class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=100, 
        required=False, 
        label='First Name',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=100, 
        required=False, 
        label='Last Name',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Profile
        fields = ['image', 'bio', 'is_private']
        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 4, 
                'placeholder': 'Tell us about yourself...',
                'class': 'form-control'
            }),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_private': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'is_private': 'Private Account',
        }
        help_texts = {
            'is_private': 'When enabled, only you can download your media.',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name


class UsernameChangeForm(forms.Form):  # NEW
    """Form to change username"""
    new_username = forms.CharField(
        max_length=30,
        label='New Username',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter new username'
        }),
        help_text='Username must start with a letter and can only contain letters, numbers, dots (.), and underscores (_).'
    )
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
    
    def clean_new_username(self):
        username = self.cleaned_data.get('new_username')
        # Validate format
        validate_username(username)
        # Check if unique (excluding current user)
        validate_username_unique(username, self.user)
        return username


class EmailChangeForm(forms.Form):  # NEW
    """Form to change email"""
    new_email = forms.EmailField(
        label='New Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter new email address'
        })
    )
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
    
    def clean_new_email(self):
        email = self.cleaned_data.get('new_email')
        # Check if unique (excluding current user)
        validate_email_unique(email, self.user)
        return email


class OTPVerificationForm(forms.Form):  # NEW
    """Form to verify OTP"""
    otp = forms.CharField(
        max_length=6,
        min_length=6,
        label='Verification Code',
        widget=forms.TextInput(attrs={
            'class': 'form-control text-center',
            'placeholder': '000000',
            'style': 'font-size: 2rem; letter-spacing: 10px;'
        }),
        help_text='Enter the 6-digit code sent to your email'
    )
    
    def clean_otp(self):
        otp = self.cleaned_data.get('otp')
        if not otp.isdigit():
            raise forms.ValidationError('OTP must contain only digits.')
        return otp