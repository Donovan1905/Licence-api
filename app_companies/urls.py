from django.urls import path
from .views import company_list, company_details, company_licences

urlpatterns = [
    path('companies', company_list),
    path('companies/details/<int:pk>', company_details),
    path('companies/details/<str:company_name>/licences', company_licences),
]