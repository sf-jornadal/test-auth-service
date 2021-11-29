from django.contrib import admin

from .models import Permission, User, Role, UserRole, RolePermission

admin.site.register([Permission, User, Role, UserRole, RolePermission])
