from django.urls import path
from .views import licence_list, licence_details

urlpatterns = [
    path('', licence_list),
    path('details/<int:pk>', licence_details)
]