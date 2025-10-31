# chatx/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Post, Profile, Comment, Notification
from .forms import PostForm, UserRegistrationForm, ProfileUpdateForm, CommentForm

# --- Main and Static Pages ---
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')


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
            post.save()
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
            form.save()
            return redirect('post_list')
    else:
        form = PostForm(instance=post)
    return render(request, 'post_form.html', {'form': form, 'post': post})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == "POST":
        post.delete()
        return redirect('post_list')
    return render(request, 'post_confirm_delete.html', {'post': post})

@login_required
def post_detail(request, pk):
    """View single post in detail"""
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
    else:
        post.likes.add(request.user)
        # Create notification
        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                sender=request.user,
                notification_type='like',
                post=post
            )
    
    return redirect(request.META.get('HTTP_REFERER', 'post_list'))

@login_required
def save_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    if post.saves.filter(id=request.user.id).exists():
        post.saves.remove(request.user)
    else:
        post.saves.add(request.user)
    
    return redirect(request.META.get('HTTP_REFERER', 'post_list'))

@login_required
def follow_view(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    
    if user_to_follow == request.user:
        messages.error(request, "You cannot follow yourself!")
        return redirect('profile', username=username)
    
    if request.user.profile.follows.filter(user=user_to_follow).exists():
        request.user.profile.follows.remove(user_to_follow.profile)
    else:
        request.user.profile.follows.add(user_to_follow.profile)
        # Create notification
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
            
            # Create notification
            if post.author != request.user:
                Notification.objects.create(
                    recipient=post.author,
                    sender=request.user,
                    notification_type='comment',
                    post=post,
                    comment=comment
                )
            
            messages.success(request, 'Comment added!')
    
    return redirect(request.META.get('HTTP_REFERER', 'post_list'))


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


# --- User-Specific Pages ---
@login_required
def saved_posts_view(request):
    saved_posts = request.user.saved_posts.all()
    return render(request, 'saved_posts.html', {'posts': saved_posts})

@login_required
def notifications_view(request):
    notifications = request.user.notifications.all()
    # Mark as read
    request.user.notifications.filter(is_read=False).update(is_read=True)
    return render(request, 'notifications.html', {'notifications': notifications})

def help_center_view(request):
    return render(request, 'help_center.html')

@login_required
def search(request):
    query = request.GET.get('q', '')
    
    users = User.objects.filter(username__icontains=query)[:10]
    posts = Post.objects.filter(text__icontains=query)[:20]
    
    context = {
        'query': query,
        'users': users,
        'posts': posts,
    }
    return render(request, 'search.html', context)

@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            
            # Handle the unified media upload
            if 'media' in request.FILES:
                media_file = request.FILES['media']
                # Check if it's an image or video
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


# --- Authentication ---
def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome.')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})