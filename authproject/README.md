# Overview
* This serves as a sample IAM (Identity access management) service

# Prerequisite
* Python installed
* Django framework installed
* Postman (for testing the endpoints)

# Running locally
* Initialize model migrations
```
python manage.py makemigrations authservice
```

* Migrate model to database
```
python manage.py migrate
```

* Start the server (default port is 8000)
```
py manage.py runserver
```

# API Definitions

## Signup
* POST /api/signup
* Request body
```json
{
    "username": string,
    "email": string,
    "password": string
}
```
* Response
```
Http 200 and page redirect to login page
```

## Login
* POST /api/login
* Request body
```json
{
    "usernameOrEmail": string,
    "password": string
}
```
* Response
```
Http 200 and page redirect to page containing user permissions
```

## Get all permissions
* GET /api/permissions
* Response
```json
"permissionlist": [
    {
        "description": string,
        "endpoint": string,
        "requestMethod": string
    }
]
```

## Create permission
* POST /api/permissions
* Request body
```json
{
    "description": string,
    "endpoint": string,
    "requestMethod": string
}
```
* Response
```
Http 200 and page redirect to permissions dashboard
```

## Get all roles
* GET /api/roles
* Response
```json
"roleList": [
    {
        "name": string,
        "description": string
    }
]
```

## Create permission
* POST /api/roles
* Request body
```json
{
    "name": string,
    "description": string
}
```
* Response
```
Http 200 and page redirect to roles dashboard
```

## Get user roles
* GET /api/{userId}/roles
* Response
```json
"roleList": [
    {
        "name": string,
        "description": string
    }
]
```

## Add roles to user
* POST /api/{userid}/roles
* Request body
```
[roleid1, roleid2, ...]
```
* Response
```
Http 200 and page redirect to roles dashboard
```

## Get user permissions
* GET /api/{userId}/permissions
* Response
```json
"permissionList": [
    {
        "description": string,
        "endpoint": string,
        "requestMethod": string
    }
]
```

## Check allowed user permissions
* POST /api/{userid}/permissions
* Request body
```
[permissionid1, permission1d2, ...]
```
* Response
```json
"permissionList": [
    {
        "description": string,
        "endpoint": string,
        "requestMethod": string
    }
]
```