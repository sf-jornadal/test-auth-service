import logging

from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from authservice.models import User, Permission, Role, UserRole, RolePermission
from django.db.models import Q
from django.urls import reverse

from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password, check_password

logger = logging.getLogger(__name__)

def showErrorMessage(request, path, errorMessage):
    logger.info(errorMessage)
    return render(request, path, {
        'errorMessage': errorMessage,
    })

def signup(request):
    logger.info('Received signup request')
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        existingUser = User.objects.filter(Q(username = username) | Q(email = email)).exists()

        if existingUser:
            errorMessage = 'Username / email already existing!'
            return showErrorMessage(request, 'authservice/signup.html', errorMessage)
        else:
            u = User(username = username, email = email, password = make_password(password))
            u.save()
            return HttpResponseRedirect(reverse('authservice:login'))
    else: 
        context = {}
        return render(request, 'authservice/signup.html', context)

def login(request):
    if request.method == 'POST':
        usernameOrEmail = request.POST['usernameOrEmail']
        password = request.POST['password']

        user = User.objects.filter(Q(username = usernameOrEmail) | Q(email = usernameOrEmail)).first()
        if user:
            correctCredentials = check_password(password, user.password)

            if correctCredentials:
                userId = user.id       
                return HttpResponseRedirect(reverse('authservice:userpermissions', args=(userId,)))
            else:
                errorMessage = 'Incorrect credentials!'
                return showErrorMessage(request, 'authservice/login.html', errorMessage)
        else:
            errorMessage = 'Incorrect credentials!'
            return showErrorMessage(request, 'authservice/login.html', errorMessage)
    else:
        context = {}
        return render(request, 'authservice/login.html', context)

def permissions(request):
    if request.method == 'POST':
        description = request.POST['description']
        endpoint = request.POST['endpoint']
        requestMethod = request.POST['requestMethod']

        p = Permission(description = description, endpoint = endpoint, requestMethod = requestMethod)
        p.save()

        return HttpResponseRedirect(reverse('authservice:permissions'))
    else:
        permissionList = Permission.objects.all()

        context = {
            'permissionList': permissionList
        }
        return render(request, 'authservice/permissions.html', context)

def roles(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']

        r = Role(name = name, description = description)
        r.save()

        return HttpResponseRedirect(reverse('authservice:roles'))
    else:
        roleList = Role.objects.all()

        context = {
            'roleList': roleList
        }
        return render(request, 'authservice/roles.html', context)

@api_view(['GET', 'POST'])
def userroles(request, userId):
    if request.method == 'POST':
        user = get_object_or_404(User, pk=userId)
        roleids = request.data

        for roleid in roleids:
            role = get_object_or_404(Role, pk=roleid)
            ur = UserRole(user = user, role = role)
            ur.save()

        return HttpResponseRedirect(reverse('authservice:roles'))
    else:
        roleIdList = UserRole.objects.filter(user__in=User.objects.filter(id=userId)).values_list('role')
        roleList = Role.objects.filter(id__in=roleIdList)

        context = {
            'roleList': roleList
        }
        return render(request, 'authservice/roles.html', context)

@api_view(['GET', 'POST'])
def userpermissions(request, userId):
    if request.method == 'POST':
        permissionIds = request.data

        roleIdList = UserRole.objects.filter(user__in=User.objects.filter(id=userId)).values_list('role')
        permissionIdList = list(RolePermission.objects.filter(role__in=roleIdList).values_list('permission', flat = True).distinct())
        allowedPermissionIds = list(set(permissionIdList) & set(permissionIds))
        notAllowedPermissionIds = list(set(permissionIds) - set(permissionIdList))

        permissionList = Permission.objects.filter(id__in=allowedPermissionIds)
        context = {
            'permissionList': permissionList
        }
        return render(request, 'authservice/permissions.html', context)
    else:
        roleIdList = UserRole.objects.filter(user__in=User.objects.filter(id=userId)).values_list('role')

        permissionIdList = RolePermission.objects.filter(role__in=roleIdList).values_list('permission').distinct()
        permissionList = Permission.objects.filter(id__in=permissionIdList)

        context = {
            'permissionList': permissionList
        }
        return render(request, 'authservice/permissions.html', context)