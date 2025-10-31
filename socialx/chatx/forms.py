# chatx/forms.py

from django import forms
from .models import Post, Profile, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    # Remove separate image/video fields
    # They will be handled by the custom media input
    
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
        
        # Allow posts with just text, or text + media
        if not text and not image and not video:
            raise forms.ValidationError("Post must have text or media content.")
        
        # Don't allow both image and video
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
    email = forms.EmailField(required=True)
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')


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