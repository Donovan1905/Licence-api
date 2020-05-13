from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('companies', include('app_companies.urls')),
    path('licences/', include('app_licences.urls')),
    path('users/', include('app_users.urls'))
]