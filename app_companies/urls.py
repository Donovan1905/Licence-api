from django.urls import path
from .views import company_list, company_details, company_licences

urlpatterns = [
    path('', company_list),
    path('/details/<int:pk>', company_details),
    path('/details/<str:company_name>/licences', company_licences),
]