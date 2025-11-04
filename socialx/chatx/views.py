# chatx/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.utils import timezone
from .models import Post, Profile, Comment, Notification, EmailVerification
from .forms import (
    PostForm, UserRegistrationForm, ProfileUpdateForm, CommentForm,
    UsernameChangeForm, EmailChangeForm, OTPVerificationForm
)
from .utils import send_verification_email, verify_otp

# --- Main and Static Pages ---
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')


# --- Authentication & Registration ---
def register(request):
    """
    Registration with mandatory email verification
    Step 1: Collect user data and send OTP
    """
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # DON'T create user yet - store data in session
            request.session['registration_data'] = {
                'username': form.cleaned_data['username'],
                'email': form.cleaned_data['email'],
                'password': form.cleaned_data['password1'],
            }
            
            # Send OTP (using a dummy user object)
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            
            # Generate and save OTP
            from .models import EmailVerification
            otp = EmailVerification.generate_otp()
            
            # Delete old OTPs
            EmailVerification.objects.filter(email=email, verified=False).delete()
            
            # Create verification
            EmailVerification.objects.create(
                user=None,  # User doesn't exist yet
                email=email,
                otp=otp
            )
            
            # Send email
            try:
                from django.core.mail import send_mail
                from django.conf import settings
                
                subject = f'ChatX - Your Verification Code is {otp}'
                message = f"""
Hi {username},

Welcome to ChatX! 

Your verification code is: {otp}

This code will expire in 10 minutes.

If you didn't request this, please ignore this email.

Thanks,
ChatX Team
                """
                
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                
                print(f"✅ OTP sent to {email}: {otp}")  # For development debugging
                
                messages.success(
                    request,
                    f'Verification code sent to {email}. Please check your email (or console in development).'
                )
                return redirect('verify_registration_otp')
                
            except Exception as e:
                print(f"❌ Email error: {e}")
                messages.error(request, 'Failed to send verification email. Please try again.')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})


def verify_registration_otp(request):
    """Registration Step 2: Verify OTP and create account"""
    registration_data = request.session.get('registration_data')
    
    if not registration_data:
        messages.error(request, 'No pending registration. Please register first.')
        return redirect('register')
    
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            email = registration_data['email']
            
            # Verify OTP
            try:
                verification = EmailVerification.objects.get(
                    email=email,
                    otp=otp,
                    verified=False
                )
                
                if verification.is_valid():
                    # CREATE USER NOW
                    user = User.objects.create_user(
                        username=registration_data['username'],
                        email=registration_data['email'],
                        password=registration_data['password']
                    )
                    
                    # Mark email as verified
                    user.profile.email_verified = True
                    user.profile.save()
                    
                    # Mark OTP as used
                    verification.verified = True
                    verification.user = user  # Link to user now
                    verification.save()
                    
                    # Clear session
                    del request.session['registration_data']
                    
                    # Log user in
                    login(request, user)
                    
                    messages.success(
                        request,
                        f'Welcome to ChatX, {user.username}! Your account has been created! 🎉'
                    )
                    return redirect('home')
                else:
                    messages.error(request, 'Verification code has expired. Please register again.')
                    del request.session['registration_data']
                    return redirect('register')
                    
            except EmailVerification.DoesNotExist:
                messages.error(request, 'Invalid verification code. Please try again.')
    else:
        form = OTPVerificationForm()
    
    # Calculate time remaining
    try:
        verification = EmailVerification.objects.filter(
            email=registration_data['email'],
            verified=False
        ).latest('created_at')
        
        time_remaining = max(0, (verification.expires_at - timezone.now()).seconds // 60)
    except EmailVerification.DoesNotExist:
        time_remaining = 0
    
    context = {
        'form': form,
        'email': registration_data['email'],
        'username': registration_data['username'],
        'time_remaining': time_remaining,
    }
    return render(request, 'registration/verify_otp.html', context)


def resend_registration_otp(request):
    """Resend OTP during registration"""
    registration_data = request.session.get('registration_data')
    
    if not registration_data:
        messages.error(request, 'No pending registration.')
        return redirect('register')
    
    email = registration_data['email']
    username = registration_data['username']
    
    # Delete old OTPs
    EmailVerification.objects.filter(email=email, verified=False).delete()
    
    # Generate new OTP
    otp = EmailVerification.generate_otp()
    EmailVerification.objects.create(
        user=None,
        email=email,
        otp=otp
    )
    
    # Send email
    try:
        from django.core.mail import send_mail
        from django.conf import settings
        
        subject = f'ChatX - Your Verification Code is {otp}'
        message = f"""
Hi {username},

Your new verification code is: {otp}

This code will expire in 10 minutes.

Thanks,
ChatX Team
        """
        
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False)
        print(f"✅ New OTP sent to {email}: {otp}")
        messages.success(request, 'New verification code sent!')
    except Exception as e:
        print(f"❌ Email error: {e}")
        messages.error(request, 'Failed to send verification code.')
    
    return redirect('verify_registration_otp')


# --- Post Feed and CRUD ---
@login_required
def post_list(request):
    posts = Post.objects.all()
    comment_form = CommentForm()
    return render(request, 'post_list.html', {
        'posts': posts,
        'comment_form': comment_form
    })

@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            
            # Handle unified media upload
            if 'media' in request.FILES:
                media_file = request.FILES['media']
                if media_file.content_type.startswith('image'):
                    post.image = media_file
                elif media_file.content_type.startswith('video'):
                    post.video = media_file
            
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'post_form.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            
            # Handle media replacement
            if 'media' in request.FILES:
                media_file = request.FILES['media']
                
                # Clear old media
                if post.image:
                    post.image.delete(save=False)
                    post.image = None
                if post.video:
                    post.video.delete(save=False)
                    post.video = None
                
                # Add new media
                if media_file.content_type.startswith('image'):
                    post.image = media_file
                elif media_file.content_type.startswith('video'):
                    post.video = media_file
            
            post.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'post_form.html', {'form': form, 'post': post})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == "POST":
        if post.image:
            post.image.delete(save=False)
        if post.video:
            post.video.delete(save=False)
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('post_list')
    return render(request, 'post_confirm_delete.html', {'post': post})

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comment_form = CommentForm()
    comments = post.comments.all()
    
    context = {
        'post': post,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, 'post_detail.html', context)


# --- User Actions ---
@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                sender=request.user,
                notification_type='like',
                post=post
            )
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'liked': liked, 'likes_count': post.likes.count()})
    
    referer = request.META.get('HTTP_REFERER', 'post_list')
    if '#' in referer:
        return redirect(referer)
    else:
        return redirect(f"{referer}#post-{pk}")

@login_required
def save_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    if post.saves.filter(id=request.user.id).exists():
        post.saves.remove(request.user)
        saved = False
    else:
        post.saves.add(request.user)
        saved = True
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'saved': saved, 'saves_count': post.saves.count()})
    
    referer = request.META.get('HTTP_REFERER', 'post_list')
    if '#' in referer:
        return redirect(referer)
    else:
        return redirect(f"{referer}#post-{pk}")

@login_required
def follow_view(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    
    if user_to_follow == request.user:
        messages.error(request, "You cannot follow yourself!")
        return redirect('profile', username=username)
    
    if request.user.profile.follows.filter(user=user_to_follow).exists():
        request.user.profile.follows.remove(user_to_follow.profile)
        messages.success(request, f'You unfollowed {user_to_follow.username}')
    else:
        request.user.profile.follows.add(user_to_follow.profile)
        messages.success(request, f'You are now following {user_to_follow.username}')
        Notification.objects.create(
            recipient=user_to_follow,
            sender=request.user,
            notification_type='follow'
        )
    
    return redirect('profile', username=username)


# --- Comments ---
@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            
            if post.author != request.user:
                Notification.objects.create(
                    recipient=post.author,
                    sender=request.user,
                    notification_type='comment',
                    post=post,
                    comment=comment
                )
            
            messages.success(request, 'Comment added!')
    
    referer = request.META.get('HTTP_REFERER', '')
    if referer:
        if '#' in referer:
            return redirect(referer)
        else:
            return redirect(f"{referer}#post-{pk}")
    else:
        return redirect('post_detail', pk=pk)


# --- Profile and Settings ---
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=profile_user)
    
    is_following = False
    if request.user.is_authenticated:
        is_following = request.user.profile.follows.filter(user=profile_user).exists()
    
    context = {
        'profile_user': profile_user,
        'posts': posts,
        'is_following': is_following
    }
    return render(request, 'profile.html', context)

@login_required
def settings_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            request.user.first_name = form.cleaned_data.get('first_name')
            request.user.last_name = form.cleaned_data.get('last_name')
            request.user.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {'form': form}
    return render(request, 'settings.html', context)


# --- Username/Email Change ---
@login_required
def change_username(request):
    if request.method == 'POST':
        form = UsernameChangeForm(request.POST, user=request.user)
        if form.is_valid():
            new_username = form.cleaned_data['new_username']
            old_username = request.user.username
            
            request.user.username = new_username
            request.user.save()
            
            messages.success(request, f'Username changed from "{old_username}" to "{new_username}"!')
            return redirect('settings')
    else:
        form = UsernameChangeForm(user=request.user)
    
    return render(request, 'change_username.html', {'form': form})

@login_required
def change_email(request):
    if request.method == 'POST':
        form = EmailChangeForm(request.POST, user=request.user)
        if form.is_valid():
            new_email = form.cleaned_data['new_email']
            
            if send_verification_email(request.user, new_email):
                request.session['pending_email'] = new_email
                messages.success(request, f'Verification code sent to {new_email}.')
                return redirect('verify_email_otp')
            else:
                messages.error(request, 'Failed to send verification email.')
    else:
        form = EmailChangeForm(user=request.user)
    
    return render(request, 'change_email.html', {'form': form})

@login_required
def verify_email_otp(request):
    pending_email = request.session.get('pending_email')
    
    if not pending_email:
        messages.error(request, 'No pending email verification.')
        return redirect('settings')
    
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            
            if verify_otp(request.user, pending_email, otp):
                old_email = request.user.email
                request.user.email = pending_email
                request.user.save()
                
                request.user.profile.email_verified = True
                request.user.profile.save()
                
                del request.session['pending_email']
                
                messages.success(request, f'Email changed from "{old_email}" to "{pending_email}"!')
                return redirect('settings')
            else:
                messages.error(request, 'Invalid or expired verification code.')
    else:
        form = OTPVerificationForm()
    
    try:
        verification = EmailVerification.objects.filter(
            user=request.user,
            email=pending_email,
            verified=False
        ).latest('created_at')
        time_remaining = max(0, (verification.expires_at - timezone.now()).seconds // 60)
    except EmailVerification.DoesNotExist:
        time_remaining = 0
    
    context = {
        'form': form,
        'pending_email': pending_email,
        'time_remaining': time_remaining,
    }
    return render(request, 'verify_email_otp.html', context)

@login_required
def resend_otp(request):
    pending_email = request.session.get('pending_email')
    
    if not pending_email:
        messages.error(request, 'No pending email verification.')
        return redirect('settings')
    
    EmailVerification.objects.filter(user=request.user, email=pending_email, verified=False).delete()
    
    if send_verification_email(request.user, pending_email):
        messages.success(request, 'New verification code sent!')
    else:
        messages.error(request, 'Failed to send verification code.')
    
    return redirect('verify_email_otp')

@login_required
def verify_current_email(request):
    if request.user.profile.email_verified:
        messages.info(request, 'Your email is already verified!')
        return redirect('settings')
    
    if request.method == 'POST':
        if send_verification_email(request.user, request.user.email):
            request.session['verifying_current_email'] = True
            messages.success(request, f'Verification code sent to {request.user.email}')
            return redirect('verify_current_email_otp')
        else:
            messages.error(request, 'Failed to send verification email.')
    
    return render(request, 'verify_current_email.html')

@login_required
def verify_current_email_otp(request):
    if not request.session.get('verifying_current_email'):
        messages.error(request, 'No pending email verification.')
        return redirect('settings')
    
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            
            if verify_otp(request.user, request.user.email, otp):
                request.user.profile.email_verified = True
                request.user.profile.save()
                
                del request.session['verifying_current_email']
                
                messages.success(request, 'Email verified successfully! ✅')
                return redirect('settings')
            else:
                messages.error(request, 'Invalid or expired verification code.')
    else:
        form = OTPVerificationForm()
    
    try:
        verification = EmailVerification.objects.filter(
            user=request.user,
            email=request.user.email,
            verified=False
        ).latest('created_at')
        time_remaining = max(0, (verification.expires_at - timezone.now()).seconds // 60)
    except EmailVerification.DoesNotExist:
        time_remaining = 0
    
    context = {
        'form': form,
        'email': request.user.email,
        'time_remaining': time_remaining,
    }
    return render(request, 'verify_current_email_otp.html', context)


# --- Account Management ---
@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        username = user.username
        
        try:
            for post in user.post_set.all():
                if post.image:
                    post.image.delete(save=False)
                if post.video:
                    post.video.delete(save=False)
            
            if user.profile.image:
                user.profile.image.delete(save=False)
        except Exception as e:
            print(f"Error deleting media: {e}")
        
        logout(request)
        user.delete()
        
        messages.success(request, f'Account "{username}" has been permanently deleted.')
        return redirect('home')
    
    return render(request, 'delete_account.html')


# --- Other Pages ---
@login_required
def saved_posts_view(request):
    saved_posts = request.user.saved_posts.all()
    return render(request, 'saved_posts.html', {'posts': saved_posts})

@login_required
def notifications_view(request):
    notifications = request.user.notifications.all()
    request.user.notifications.filter(is_read=False).update(is_read=True)
    return render(request, 'notifications.html', {'notifications': notifications})

def help_center_view(request):
    return render(request, 'help_center.html')

@login_required
def search(request):
    query = request.GET.get('q', '')
    
    if query:
        users = User.objects.filter(username__icontains=query)[:10]
        posts = Post.objects.filter(text__icontains=query)[:20]
    else:
        users = User.objects.none()
        posts = Post.objects.none()
    
    context = {
        'query': query,
        'users': users,
        'posts': posts,
    }
    return render(request, 'search.html', context)