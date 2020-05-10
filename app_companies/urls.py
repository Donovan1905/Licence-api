from django.urls import path
from .views import company_list, company_details

urlpatterns = [
    path('companies', company_list),
    path('companies/details/<int:pk>', company_details)
]