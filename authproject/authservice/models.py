from django.db import models

class Permission(models.Model):
    description = models.CharField(max_length=50)
    endpoint = models.CharField(max_length=50)
    requestMethod = models.CharField(max_length=6)

    def __str__(self):
        return self.description

class Role(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class User(models.Model):
    username = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=30)

    def __str__(self):
        return self.username

class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
