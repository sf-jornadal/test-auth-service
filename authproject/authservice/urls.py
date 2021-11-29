from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

app_name = 'authservice'
urlpatterns = [
    # ex: /signup/
    path('signup/', views.signup, name='signup'),       
    # ex: /login/
    path('login/', views.login, name='login'),      
    # ex: /permissions/
    path('permissions/', views.permissions, name='permissions'),  
    # ex: /roles/
    path('roles/', views.roles, name='roles'),
    # ex: /users/1/roles
    path('users/<int:userId>/roles', csrf_exempt(views.userroles), name='userroles'),    
    # ex: /users/1/permissions
    path('users/<int:userId>/permissions', csrf_exempt(views.userpermissions), name='userpermissions'),
]