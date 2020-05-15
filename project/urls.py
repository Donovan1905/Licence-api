from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('companies', include('app_companies.urls')),
    path('licences', include('app_licences.urls')),
    path('users', include('app_users.urls')),
    path('api-token-auth/', views.obtain_auth_token, name='api-token-auth'),
]