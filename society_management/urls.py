"""
URL configuration for society_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from society import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    #path('flat-owner/dashboard/', views.flat_owner_dashboard, name='flat_owner_dashboard'),
    # path('tenant/dashboard/', views.tenant_dashboard, name='tenant_dashboard'),
    path('', include('society.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),  # Add login URL
    path('accounts/profile/', views.profile, name='profile'),  # Add login URL
    path('accounts/signup/', views.signup, name='signup'),  # Add this line
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),  # Add logout URL
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/profile/', views.profile, name='profile'),

]
