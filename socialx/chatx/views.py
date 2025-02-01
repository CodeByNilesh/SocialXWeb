from django.shortcuts import render
from .models import Chat
from .forms import ChatForm, UserRegistrationForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

# Create your views here.
def index(request):
    return render (request, 'index.html')

def chat_list(request):
    chats = Chat.objects.all().order_by('-created_at')
    return render(request, 'chat_list.html', {'chats': chats})

@login_required
def chat_create(request):
    if request.method == "POST":
        form = ChatForm(request.POST, request.FILES)
        if form.is_valid():
            chat = form.save(commit=False)
            chat.user = request.user
            chat.save()
            return redirect('chat_list')
    else:
        form = ChatForm()
    return render(request, 'chat_form.html', {'form':form})

@login_required
def chat_edit(request, chat_id):
    chat = get_object_or_404(Chat, pk=chat_id, user=request.user)
    if request.method == "POST":
        form = ChatForm(request.POST, request.FILES, instance=chat)
        if form.is_valid():
            chat = form.save(commit=False)
            chat.user = request.user
            chat.save()
            return redirect('chat_list')
    else:
        form = ChatForm(instance=chat)
    return render(request, 'chat_form.html', {'form':form})

@login_required    
def chat_delete(request, chat_id):
    chat = get_object_or_404(Chat, pk=chat_id, user=request.user)
    if request.method == "POST":
            chat.delete()
            return redirect('chat_list')
    return render(request, 'chat_confirm_delete.html', {'chat':chat})

def register(request):
    if request.method == "POST" :
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('chat_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form':form})