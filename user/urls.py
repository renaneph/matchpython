from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('dashboard/', views.admin, name='admin'),
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('user/list', views.user_list, name='list'),
    path('user/register/', views.users_register, name='register'),
    path('user/delete/<int:pk>', views.users_delete, name='delete'),
    path('user/edit/<int:pk>', views.users_edit, name='edit'),
]
