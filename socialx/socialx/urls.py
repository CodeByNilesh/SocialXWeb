# socialx/urls.py

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from chatx import views as chatx_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Authentication & Registration
    path('register/', chatx_views.register, name='register'),  # Only ONE register path
    path('register/verify-otp/', chatx_views.verify_registration_otp, name='verify_registration_otp'),
    path('register/resend-otp/', chatx_views.resend_registration_otp, name='resend_registration_otp'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Main Pages
    path('', chatx_views.home, name='home'),
    path('about/', chatx_views.about, name='about'),
    path('feed/', chatx_views.post_list, name='post_list'),
    path('chatx/', chatx_views.post_list, name='chat_list'),
    
    # Posts
    path('post/create/', chatx_views.post_create, name='post_create'),
    path('post/<int:pk>/', chatx_views.post_detail, name='post_detail'),
    path('post/<int:pk>/edit/', chatx_views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', chatx_views.post_delete, name='post_delete'),
    path('post/<int:pk>/like/', chatx_views.like_post, name='like_post'),
    path('post/<int:pk>/save/', chatx_views.save_post, name='save_post'),
    path('post/<int:pk>/comment/', chatx_views.add_comment, name='add_comment'),

    # Profile
    path('profile/<str:username>/', chatx_views.profile_view, name='profile'),
    path('profile/<str:username>/follow/', chatx_views.follow_view, name='follow'),
    
    # Settings
    path('settings/', chatx_views.settings_view, name='settings'),
    path('settings/username/change/', chatx_views.change_username, name='change_username'),
    path('settings/email/change/', chatx_views.change_email, name='change_email'),
    path('settings/email/verify-otp/', chatx_views.verify_email_otp, name='verify_email_otp'),
    path('settings/email/resend-otp/', chatx_views.resend_otp, name='resend_otp'),
    path('settings/email/verify-current/', chatx_views.verify_current_email, name='verify_current_email'),
    path('settings/email/verify-current-otp/', chatx_views.verify_current_email_otp, name='verify_current_email_otp'),
    
    # Account
    path('account/delete/', chatx_views.delete_account, name='delete_account'),
    
    # Other
    path('saved/', chatx_views.saved_posts_view, name='saved_posts'),
    path('notifications/', chatx_views.notifications_view, name='notifications'),
    path('search/', chatx_views.search, name='search'),
    path('help/', chatx_views.help_center_view, name='help_center'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)