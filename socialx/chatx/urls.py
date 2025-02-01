from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_list, name='chat_list'),
    path('create/', views.chat_create, name='chat_create'),
    path('<int:chat_id>/edit/', views.chat_edit, name='chat_edit'),
    path('<int:chat_id>/delete/', views.chat_delete, name='chat_delete'),
    path('register/', views.register, name='register'),
]