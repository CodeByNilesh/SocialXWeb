# chatx/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import random
import string

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=280)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    video = models.FileField(upload_to='post_videos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    saves = models.ManyToManyField(User, related_name='saved_posts', blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return f'Post by {self.author.username} at {self.created_at.strftime("%Y-%m-%d %H:%M")}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    bio = models.TextField(blank=True)
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False, blank=True)
    is_private = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)  # NEW

    def __str__(self):
        return f'{self.user.username} Profile'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f'Comment by {self.author.username} on {self.post}'


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('follow', 'Follow'),
    )
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.sender.username} {self.notification_type} - {self.recipient.username}'


class EmailVerification(models.Model):
    """Store OTP for email verification"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()  # Remove null=True, blank=True
    verified = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        # Set expiration BEFORE saving
        if not self.pk and not self.expires_at:  # Only on creation
            self.expires_at = timezone.now() + timedelta(minutes=10)
        super().save(*args, **kwargs)
    
    def is_valid(self):
        """Check if OTP is still valid"""
        if self.verified:
            return False
        if not self.expires_at:
            return False
        return timezone.now() < self.expires_at
    
    @staticmethod
    def generate_otp():
        """Generate 6-digit OTP"""
        return ''.join(random.choices(string.digits, k=6))
    
    def __str__(self):
        return f'OTP for {self.email} - {self.otp}'
    
    class Meta:
        ordering = ['-created_at']