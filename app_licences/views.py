from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .models import Licence
from .serializers import LicenceSerializer
from django.views.decorators.csrf import csrf_exempt
from app_companies.models import Company


@csrf_exempt
def licence_list(request):
    if request.method == 'GET':
        licences = Licence.objects.all()
        serializer = LicenceSerializer(licences, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONPaser().parse(request)
        serializer = LicenceSerializer(data = data)

        if serializer.is_valid():
            serializer.save()
            return JsonReponse(serializer.data, status = 201)
        return JsonResponse(serializer.errors, status = 400)


@csrf_exempt
def licence_details(request, pk):
    try:
        licence = Licence.objects.get(pk=pk)
    except Licence.DoesNotExist:
        return HttpResponse(status=400)

    if request.method == 'GET':
        serializer = LicenceSerializer(licence)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = LicenceSerializer(licence, data = data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return HttpResponse(status=400)
    elif request.method == 'DELETE':
        company.delete()
        return HttpResponse(status=204)