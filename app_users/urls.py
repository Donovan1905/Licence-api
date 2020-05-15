from django.urls import path
from .views import user_list, user_details

urlpatterns = [
    path('/', user_list),
    path('/details/<int:pk>', user_details)
]