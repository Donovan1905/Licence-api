<h1 style="text-align:center; font-weight: 400">Rapport de conception</h1>



[toc]





# Environnement virtuel

Un environnement virtuel est un outil qui permet de séparer les dépendances requises par différents projets en créant pour eux des environnements virtuels python isolés. C'est l'un des outils les plus importants que la plupart des développeurs Python utilisent.



## Création de l'environnement virtuel

```
pip install venv

python -m venv myvenv
```



## Activation de l'environnement virtuel

```
myvenv\Scripts\activate.bat
```



# Setup Django

## Installation de Django

```
pip install django
```



## Création du projet Django

```
django-admin startapp project .
```



## Création des application Django

```
python manage.py startapp app_users
python manage.py startapp app_licences
python manage.py startapp app_companies
```



# Enregistrement des applications

On doit inscire les apps dans *settings.py* dans *INSTALLED_APPS*

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app_users.apps.AppUsersConfig',
    'app_licences.apps.AppLicencesConfig',
    'app_companies.apps.AppCompaniesConfig',
]
```



# Création des Models

- création d'un fichier *models.py* dans chaque application

## app_users

**app_users.models.py**

```python
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from app_companies.models import Company
from .managers import CustomUserManager
  

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    company = models.ForeignKey(
        'app_companies.Company',
        on_delete=models.CASCADE,
        null=True,
        blank = True
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
```

Etant donné que le Model *CustomUser* hérite de AbstractBaseUser (préfait Django) nous devons implementer notre propre UserManager (héritant de celui de Django).

**app_users.managers.py**

```python
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)
```



## app_companies

**app_companies.models.py**

```python
from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
```



## app_licences

**app_licences.models.py**

```python
from django.db import models
from app_companies.models import Company
from app_users.models import CustomUser


class Licence(models.Model):
    key = models.CharField(max_length=20, unique=True)
    company = models.ForeignKey(
        'app_companies.Company',
        on_delete=models.CASCADE
    )
    user = models.OneToOneField(
        'app_users.CustomUser',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.key
```



# Migrations

```
python manage.py makemigrations
python manage.py migrate
```



# Création du super user

```
python manage.py createsuperuser
email : admin@mail.com
password : adminpassword
```



# Mise en place des page admin

## app_users

**app_users.forms.py**

```python
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)
```



**app_users.admin.py**

```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'company', 'is_staff', 'is_active',)
    list_filter = ('email', 'company', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'company', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'company')
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
```



## app_licences

**app_licences.admin.py**

```python
from django.contrib import admin
from .models import Licence

@admin.register(Licence)
class LicenceAdmin(admin.ModelAdmin):
    list_display = ('pk', 'key', 'company')
```



## app_companies

**app_companies.admin.py**

```python
from django.contrib import admin
from .models import Company

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name') 
```



# Installation de django-rest-framework

```
pip install django-rest-framework
```



# Enregistrement de django-rest-framework

Django-rest-framework doit être renseigné dans settings.py au même titre qu'une application.

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'app_users.apps.AppUsersConfig',
    'app_licences.apps.AppLicencesConfig',
    'app_companies.apps.AppCompaniesConfig',
]
```



# Serializers

Les serializers vont nous permettre de normaliser les données que l'on doit envoyer ou recevoir.

## app_users

**app_users.serializers.py**

```python
from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'company']
```



## app_licences

**app_licences.serializers.py**

```python
from rest_framework import serializers
from .models import Licence

class LicenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Licence
        fields = ['key']
```



## app_companies

**app_companies.seralizers.py**

```python
from rest_framework import serializers
from .models import Company

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['name']
```



# Vues

## app_users

**app_users.views.py*

```python
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .models import CustomUser
from .serializers import UserSerializer
from django.views.decorators.csrf import csrf_exempt
from app_companies.models import Company


@csrf_exempt
def user_list(request):
    if request.method == 'GET':
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(data = data)
        serializer = UserSerializer(data = data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = 201)
        return JsonResponse(serializer.errors, status = 400)


@csrf_exempt
def user_details(request, pk):
    try:
        user = CustomUser.objects.get(pk=pk)
    except CustomUser.DoesNotExist:
        return HttpResponse(status=400)
    
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = UserSerializer(user, data = data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return HttpResponse(status = 400)
    elif request.method == 'DELETE':
        user.delete()
        return HttpResponse(status = 204)
```



## app_licences

**app_licences.views.py**

```python
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .models import Licence
from .serializers import LicenceSerializer
from django.views.decorators.csrf import csrf_exempt
from app_companies.models import Company
from app_users.models import CustomUser
from django.utils.crypto import get_random_string


@csrf_exempt
def licence_list(request):
    if request.method == 'GET':
        licences = Licence.objects.all()
        serializer = LicenceSerializer(licences, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        return HttpResponse('cannot create a licence from json you nedd to buy it from /buy/<commpany_name>/<quantity>')


@csrf_exempt
def licence_details(request, pk):
    try:
        licence = Licence.objects.get(pk=pk)
    except Licence.DoesNotExist:
        return HttpResponse(status=400)

    if request.method == 'GET':
        serializer = LicenceSerializer(licence)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = LicenceSerializer(licence, data = data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return HttpResponse(status=400)
    elif request.method == 'DELETE':
        licence.delete()
        return HttpResponse(status=204)


def ask_licence(request, pk):
    try:
        user = CustomUser.objects.get(pk=pk)
        try:
            licence = Licence.objects.get(user=user)
            release_licence(request='fake_request', pk=user.pk)
        except Licence.DoesNotExist:
            pass
        licence = Licence.objects.filter(company=user.company, user_id=0).first()
    except Licence.DoesNotExist:
        return HttpResponse("Sorry your company doesn't have licence", status=400)

    if request.method == 'GET':
        licence.user = user 
        licence.save()
        serializer = LicenceSerializer(licence)
        return JsonResponse(serializer.data, safe=False)


def release_licence(request, pk):
    try:
        user = CustomUser.objects.get(pk=pk)
        try:
            licence = Licence.objects.get(user=user)
        except Licence.DoesNotExist:
            return HttpResponse("User doesn't have any licence to release", status=400)
    except CustomUser.DoesNotExist:
        HttpResponse('no user found', status=400)

    if request == 'fake_request' or request.method == 'GET':
        licence.user = 0
        licence.save()
        return HttpResponse('Licence release for user {}'.format(user.pk))


def buy_licences(request, company_name, quantity):
    if request.method == 'GET':
        for i in range(quantity):
            key = get_random_string(length=20)
            company = Company.objects.get(name=company_name)
            licence = Licence(key=key, company=company)
            licence.save()
        return HttpResponse('licence registred')
    else:
        return HttpResponse('Sorry only GET request is allowed to this route', status=400)
```



## app_companies

**app_companies.views.py**

```python
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .models import Company
from .serializers import CompanySerializer
from django.views.decorators.csrf import csrf_exempt
from app_licences.models import Licence
from app_licences.serializers import LicenceSerializer


@csrf_exempt
def company_list(request):

    if request.method == 'GET':
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        return JsonResponse(serializer.data, safe = False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CompanySerializer(data = data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = 201)
        return JsonResponse(serializer.errors, status = 400 )

@csrf_exempt
def company_details(request, pk):
    try:
        company = Company.objects.get(pk=pk)
    except Company.DoesNotExist:
        return HttpResponse(status=400)

    if request.method == 'GET':
        serializer = CompanySerializer(company)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = CompanySerializer(company, data = data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return HttpResponse(status=400)
    elif request.method == 'DELETE':
        company.delete()
        return HttpResponse(status=204)


def company_licences(request, company_name):
    company = Company.objects.get(name=company_name)
    licences = Licence.objects.filter(company=company)
    serializer = LicenceSerializer(licences, many=True)
    return JsonResponse(serializer.data, safe=False)
```



# Routes (urls)

## project

**project.urls.py**

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('companies', include('app_companies.urls')),
    path('licences/', include('app_licences.urls')),
    path('users/', include('app_users.urls'))
]
```



## app_users

**app_users.urls.py**

```python
from django.urls import path
from .views import user_list, user_details

urlpatterns = [
    path('', user_list),
    path('details/<int:pk>', user_details)
]
```



## app_licences

**app_licences.urls.py**

```python
from django.urls import path
from .views import licence_list, licence_details, ask_licence, buy_licences, release_licence

urlpatterns = [
    path('', licence_list),
    path('details/<int:pk>', licence_details),
    path('get/<int:pk>', ask_licence),
    path('buy/<str:company_name>/<int:quantity>', buy_licences),
    path('release/<int:pk>', release_licence)
]
```



## app_companies

**app_companies.urls.py**

```python
from django.urls import path
from .views import company_list, company_details, company_licences

urlpatterns = [
    path('', company_list),
    path('/details/<int:pk>', company_details),
    path('/details/<str:company_name>/licences', company_licences),
]
```



# Endpoints



## Companies

```
GET /companies  //Renvoi un json contenant toutes les entreprises

POST /companies  //Permet créer une nouvelle entreprise en envoyant les données dans le body en json

GET /companies/details/{id}  //Renvoi un json contenant les détails d'une entreprise

PUT /companies/details/{id}  //Modifie l'entreprise selectionnée avec les informations du body en json

DELETE /companies/details/{id}  //Supprime l'entrerise visée

GET /companies/details/{company_name}/licences //Renvoi un json contenant toutes les licences que l'entreprise séléctionnée possèbe
```



## Licences

```
GET /licences  //Renvoi la liste de toutes les licences existante en json

POST /licences  //Créer une licence avec le json contenu dans le body (cette fonction est désactivé)

GET /licences/details/{id}  //Renvoi les détails de la licence visée en json

PUT /licences/details/{id}  //Modifie la licence visée avec le json du body

DELETE /licences/details/{id}  //Supprime la licence visée

GET /licences/get/{user_id}  //Attribue une licence à l'utilisateur visé (si sa companie en possède et qu'il y en a une de libre)

GET /licences/buy/{company_name}/{quantity}  //Génère un certains nombre de licence pour l'entreprise visée

GET /licences/release/{user_id}  //Libère la licence actuellement possédée par l'utilisateur (un utilisateur ne peux posséder qu'une licence à la fois)
```



## Users

```
GET /users  //Renvoi la liste de tout les utilisateurs en json

POST /users  //Permet de créer un utilisateur avec le json du body

GET /users/details/{id}  //Renvoi les détails de l'utilisateur visé

PUT /users/details/{id}  //Modifie l'utilisateur visé

DELETE /users/details/{id}  //Supprime l'utilisateur visé
```



## Project

```
POST /api-token-auth  //Renvoi un token d'authentification si l'email et le mot de passe correpondent
```

