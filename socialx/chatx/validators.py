# chatx/validators.py

import re
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

def validate_username(username):
    """
    Validate username:
    - Must start with a letter
    - Can only contain letters, numbers, dots (.), and underscores (_)
    - Cannot start with a number
    - No special characters except . and _
    """
    # Check if username starts with a letter
    if not username[0].isalpha():
        raise ValidationError(
            'Username must start with a letter (a-z or A-Z).',
            code='invalid_start'
        )
    
    # Check for valid characters
    pattern = re.compile(r'^[a-zA-Z][a-zA-Z0-9._]*$')
    if not pattern.match(username):
        raise ValidationError(
            'Username can only contain letters, numbers, dots (.), and underscores (_).',
            code='invalid_characters'
        )
    
    # Check length
    if len(username) < 3:
        raise ValidationError(
            'Username must be at least 3 characters long.',
            code='too_short'
        )
    
    if len(username) > 30:
        raise ValidationError(
            'Username cannot be more than 30 characters long.',
            code='too_long'
        )
    
    # Check for consecutive dots or underscores
    if '..' in username or '__' in username:
        raise ValidationError(
            'Username cannot contain consecutive dots or underscores.',
            code='consecutive_special'
        )
    
    # Check if username ends with dot or underscore
    if username.endswith('.') or username.endswith('_'):
        raise ValidationError(
            'Username cannot end with a dot or underscore.',
            code='invalid_end'
        )
    
    return username


def validate_email_unique(email, user=None):
    """Check if email is already taken by another user"""
    if user:
        # Exclude current user when checking
        if User.objects.filter(email=email).exclude(id=user.id).exists():
            raise ValidationError(
                'This email is already registered with another account.',
                code='email_taken'
            )
    else:
        if User.objects.filter(email=email).exists():
            raise ValidationError(
                'This email is already registered.',
                code='email_taken'
            )
    return email


def validate_username_unique(username, user=None):
    """Check if username is already taken"""
    if user:
        # Exclude current user when checking
        if User.objects.filter(username=username).exclude(id=user.id).exists():
            raise ValidationError(
                'This username is already taken.',
                code='username_taken'
            )
    else:
        if User.objects.filter(username=username).exists():
            raise ValidationError(
                'This username is already taken.',
                code='username_taken'
            )
    return username