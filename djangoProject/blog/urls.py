from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('about/', views.about, name='blog-about'),
    path('about2/<name>', views.about2),
    path('login/', views.singin, name='blog-login'),
    path('logout/', views.signOut, name='blog-logout'),
    path('post/', views.post, name='blog-post'),
    path('delete/<int:id>', views.delete, name='blog-delete'),
    path('edit/<int:id>', views.edit, name='blog-edit'),
    path('allPost', views.allPost),
]
