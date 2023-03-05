from django.urls import path
from rest_auth.views import PasswordResetConfirmView
from .views import forgot_password, reset_password
from .views import profile, profile_list, profile_create, profile_update, profile_delete


urlpatterns = [
    path('forgot-password/', forgot_password),
    path('reset-password/', reset_password),
    path('reset-password/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('profile/', profile, name='profile'),
    path('profile/list/', profile_list, name='profile_list'),
    path('profile/create/', profile_create, name='profile_create'),
    path('profile/update/<int:pk>/', profile_update, name='profile_update'),
    path('profile/delete/<int:pk>/', profile_delete, name='profile_delete'),
]

