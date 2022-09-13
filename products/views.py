from django.shortcuts import render, HttpResponse
from rest_framework.response import Response
from products.serializers import *
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
import requests
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.contrib.auth.models import User, auth, Permission
from products.custompermissions import AdminPermission, ManagerPermission, AdminOrManagerPermission


@api_view(['POST'])
def register(request):    
    ser = UserSerializer(data=request.data)        
    if ser.is_valid():
        print(ser.data)
        passwd = make_password(ser.data['password'])
        u = User(username = ser.data['username'], email = ser.data['email'], password=passwd)
        u.save()
        up = UserProfile(user_id=u.id, phone=ser.data['phone'],role_id=ser.data['role'])
        up.save()
        return Response(ser.data, status=status.HTTP_201_CREATED)
    else:
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    if request.method=='POST':
        email = request.data['email']
        password = request.data['password']
        u = User.objects.get(email=email)
        user = auth.authenticate(username=u.username, password=password)
        #print(user)
        if user is not None and user.is_active:
            auth.login(request, user)
            token = requests.post('http://127.0.0.1:8000/api/token/', {"username":user.username, "password":password})
            #print(token.text)
            return Response(token.text, status=status.HTTP_200_OK)
        else:
            return Response("User credentials are wrong", status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([AdminPermission])
def product_save(request):
    p = ProductSerializer(data=request.data)    
    if p.is_valid():
        p.save()
        return Response(p.data, status=status.HTTP_201_CREATED)
    else:
        return Response(p.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([AdminOrManagerPermission])
def product_list(request):
    products = Products.objects.all()
    p = ProductSerializer(products, many=True)    
    if p:        
        return Response(p.data, status=status.HTTP_201_CREATED)
    else:
        return Response(p.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([AdminPermission])
def product_update(request):
    id= int(request.POST['id'])
    product = Products.objects.get(id=id)
    p = ProductSerializer(product, data=request.data)    
    if p.is_valid():
        p.save()
        return Response(p.data, status=status.HTTP_200_OK)
    else:
        return Response(p.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([AdminPermission])
def product_delete(request):
    id = int(request.POST['id'])
    product = Products.objects.get(id=id)
    product.delete()
    return Response("Deleted successfully", status=status.HTTP_200_OK)
