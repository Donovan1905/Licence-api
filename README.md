<h1 style="text-align:center; font-weight: 400">Projet de remplacement de stage : Serveur de licences</h1>



Auteur : Donovan Hoang



[toc]



## Rappel du besoin

Une entreprise développant des logiciels destinés aux professionnel, vend actuellement ses logiciels avec un certains nombre d’activations possible pour une licences. Cette méthode pose problème quand les clients change de matériel et donc perdent l’accès aux logiciels qu’ils ont acheté.
L’entreprise souhaite donc développer une API délivrant aux employé des entreprise clientes des licences qui se libérerons une fois l’utilisation finie.



## Installation



## Architecture

<img src="C:\Users\donov\Documents\GitHub\Licence-api\README.assets\image-20200510213132770.png" alt="image-20200510213132770" style="zoom:50%;" />

### project

<img src="C:\Users\donov\Documents\GitHub\Licence-api\README.assets\image-20200510213623571.png" alt="image-20200510213623571" style="zoom: 50%;" />

C'est le projet Django, le cœur du projet. Il est constitué du fichier de configuration ainsi que du fichier des routes (urls). 



### app_companies

<img src="C:\Users\donov\Documents\GitHub\Licence-api\README.assets\image-20200510213715469.png" alt="image-20200510213715469" style="zoom:50%;" />

C'est l'application Django qui gère tout ce qui est en rapport avec les companies. Voici à quoi servent les différents fichiers et répertoire :

- _pycache_ : cache
- migrations : répertoire contenant les migrations de l'application 
- _init_.py : fichier d'initialisation
- admin.py : Fichier visant à définir les informations à afficher sur la page d'administration et son apparence
- apps.py : Configuration de l'application
- models.py : Fichier contenant la définition de nos classes modèles. C'est ce fichier qui va être transformé en migrations et permettre de créer la base de données
- serializers.py : Fichier contenant les "serializers" de l'application. Ils servent à définir les champs à envoyé aux réponses aux requêtes faites à l'API ou les données à chercher dans les informations reçues
- tests.py : Fichier contenant les tests unitaires de l'application
- urls.py : Fichier contenant les urls propre à cette application. Ce fichier doit être inclus dans le urls.py du répertoire du projet
- views.py : Fichier contenant les vues de l'application, des fonctions qui vont définir la logique des actions possible en réponses aux requêtes.



### app_licences

*idem que pour app_companies*



### app_users

*idem que pour app_companies*



### myvenv

L'environnement virtuel python créé avec l'outil venv.



### db.sqlite3

Le fichier de base de données SQLite



### manage.py

Fichier contenant tout les outils utiles aux développement de projet Django. Il permet par exemple de démarrer un serveur de test, de créer et lancer les migrations, de créer des applications...etc..





## Models

### Company

```python
from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
```



### Licence

```python
from django.db import models
from app_companies.models import Company


class Licence(models.Model):
    key = models.CharField(max_length=20)
    company = models.ForeignKey(
        'app_companies.Company',
        on_delete=models.CASCADE
    )
    user_id = models.IntegerField(default=0, null=True)

    def __str__(self):
        return self.key
```



### FakeUser

```python
from __future__ import unicode_literals
from django.db import models
from app_companies.models import Company
from django.utils.translation import ugettext_lazy as _


class FakeUser(models.Model):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    company = models.ForeignKey(
        'app_companies.Company',
        on_delete=models.CASCADE
    )
```



## Endpoints



### Companies

```
GET /companies

POST /companies

GET /companies/details/{id}

PUT /companies/details/{id}

DELETE /companies/details/{id}
```



### Licences

```
GET /licences

POST /licences

GET /licences/details/{id}

PUT /licences/details/{id}

DELETE /licences/details/{id}

GET /licences/get/{user_id}
```



### Users

```
UsersGET /users

POST /users

GET /users/details/{id}

PUT /users/details/{id}

DELETE /users/details/{id}
```



