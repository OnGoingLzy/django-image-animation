"""djangokeshe1 URL Configuration

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
from django.contrib import admin

from django.urls import path

from djangokeshe1 import views, post

urlpatterns = [
    path('#', admin.site.urls),
    path('test/', views.index, name='index'),
    path('generation/',views.generation,name='generation'),
    path('upload_file/', views.upload_file, name='upload_file'),
    path('generation_file/', post.generation_file, name='generation_file'),
    # 以下为chat的url
    # 匹配 /users/ 这个 URL
    path('users/', post.get_users, name='get_users'),
    path('sign-in/', views.sign_in, name='sign-in'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/price', views.price, name='/dashboard/price'),
    path('api/login/', post.login_view, name='/api/login/'),
    path('api/logout/', post.logout_view, name='/api/logout/'),
    path('register/', views.register, name='register'),
    path('api/register/', post.register, name='/api/register'),
    path('send_sms/', views.send_sms, name='send_sms'),
    path('api/chat_count_data/', views.chat_count_data, name='/api/chat_count_data'),

]
