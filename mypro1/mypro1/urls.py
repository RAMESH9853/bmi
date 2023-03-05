"""mypro1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from rest_framework import routers
from myapp import views

router = routers.DefaultRouter()
# router.register(r'profiles', views.ProfileViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    # path('signup/', views.signup, name='signup'),
    # path('login/', views.user_login, name='login'),
    # path('logout/', views.user_logout, name='logout'),
    # path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    # path('password_reset/', views.password_reset_request, name='password_reset'),
    # path('password_reset/done/', views.password_reset_done, name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    # path('reset/done/', views.password_reset_complete, name='password_reset_complete'),
    # path('profile/', views.profile_detail, name='profile'),
    # path('profile/edit/', views.profile_edit, name='profile-edit'),
    # path('api/', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]






