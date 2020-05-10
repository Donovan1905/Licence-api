from django.urls import path
from .views import licence_list, licence_details, ask_licence

urlpatterns = [
    path('', licence_list),
    path('details/<int:pk>', licence_details),
    path('get/<int:pk>', ask_licence)
]