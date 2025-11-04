# chatx/admin.py

from django.contrib import admin
from .models import Post, Profile, Comment, Notification, EmailVerification

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'text', 'created_at')
    search_fields = ('text', 'author__username')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'email_verified', 'is_private')
    list_filter = ('email_verified', 'is_private')
    search_fields = ('user__username',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'text', 'created_at')
    search_fields = ('text', 'author__username')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'sender', 'notification_type', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read')

@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'otp', 'verified', 'created_at', 'expires_at')
    list_filter = ('verified',)
    search_fields = ('user__username', 'email', 'otp')
    readonly_fields = ('created_at', 'expires_at')