from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.my_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.my_logout, name='logout'),
    path('confirm/', views.user_confirm),
]
