from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .models import FakeUser
from .serializers import UserSerializer
from django.views.decorators.csrf import csrf_exempt
from app_companies.models import Company


@csrf_exempt
def user_list(request):
    if request.method == 'GET':
        users = FakeUser.objects.all()
        serializer = UsersSerializer(users, many=True)
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
        user = FakeUser.objects.get(pk=pk)
    except FakeUser.DoesNotExist:
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