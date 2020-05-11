from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .models import Licence
from .serializers import LicenceSerializer
from django.views.decorators.csrf import csrf_exempt
from app_companies.models import Company
from app_users.models import FakeUser
from django.utils.crypto import get_random_string


@csrf_exempt
def licence_list(request):
    if request.method == 'GET':
        licences = Licence.objects.all()
        serializer = LicenceSerializer(licences, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        return HttpResponse('cannot create a licence from json you nedd to buy it from /buy/<commpany_name>/<quantity>')
        '''
        data = JSONParser().parse(request)
        serializer = LicenceSerializer(data = data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = 201)
        return JsonResponse(serializer.errors, status = 400)
        '''


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
        licence.delete()
        return HttpResponse(status=204)


def ask_licence(request, pk):
    try:
        user = FakeUser.objects.get(pk=pk)
        try:
            licence = Licence.objects.get(user_id=user.pk)
            release_licence(request='fake_request', pk=user.pk)
        except Licence.DoesNotExist:
            pass
        licence = Licence.objects.filter(company=user.company, user_id=0).first()
    except Licence.DoesNotExist:
        return HttpResponse("Sorry your company doesn't have licence", status=400)


    if request.method == 'GET':
        licence.user_id = user.pk
        licence.save()
        serializer = LicenceSerializer(licence)
        return JsonResponse(serializer.data, safe=False)


def release_licence(request, pk):
    try:
        user = FakeUser.objects.get(pk=pk)
        try:
            licence = Licence.objects.get(user_id=user.pk)
        except Licence.DoesNotExist:
            return HttpResponse("User doesn't have any licence to release", status=400)
    except FakeUser.DoesNotExist:
        HttpResponse('no user found', status=400)

    if request == 'fake_request' or request.method == 'GET':
        licence.user_id = 0
        licence.save()
        return HttpResponse('Licence release for user {}'.format(user.pk))
        

    

def buy_licences(request, company_name, quantity):
    if request.method == 'GET':
        for i in range(quantity):
            key = get_random_string(length=20)
            company = Company.objects.get(name=company_name)
            licence = Licence(key=key, company=company)
            licence.save()
        return HttpResponse('licence registred')
    else:
        return HttpResponse('Sorry only GET request is allowed to this route', status=400)