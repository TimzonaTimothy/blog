from django.conf.urls import re_path
from django.urls import path
from accounts.views import Register,sign_in,user_logout
from django.conf import settings
from django.contrib.auth import views as auth_views
from . import  views
from django.conf.urls.static import static

app_name = 'members'

urlpatterns = [
    re_path(r'^logout/$',user_logout,name='logout'),
    re_path(r'^register/$',Register.as_view(),name='register'),
    re_path(r'^login/$',sign_in,name='login'),
    re_path(r'^reset_password/$',auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'),name='reset_password'),
    re_path(r'^reset_password_sent/$',auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_sent.html'),name='password_reset_sent'),
    re_path(r'^reset/(<upkb64>)/<token>/$',auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_form.html'),name='password_reset_confirm'),
    re_path(r'^reset_password_complete/$',auth_views.PasswordResetCompleteView.as_view(template_name='registration/reset_password_complete.html'),name='password_reset_complete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
