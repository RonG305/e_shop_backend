from django.shortcuts import render
from accounts.serializers import UserSerializer, UserSerializerView
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login as django_login, authenticate, logout

from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import Role
from django.contrib.auth.models import User


# Create your views here.

@api_view(["GET"])
def getCustomers(request):
    customers = User.objects.all().order_by("-date_joined")
    serializer = UserSerializerView(customers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['POST'])
def signup_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def signin_user(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(request, username=username, password=password)

    
    if user is not None:
        django_login(request, user)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        userId = request.user.id
        print("userId", userId)

        try:
            user_role = Role.objects.get(user=request.user).roleName  
           
        except Role.DoesNotExist:
            user_role = 'user'

        return Response({'message': 'Login successful', 'access_token': access_token,  'role': user_role , 'username': username, "userId": userId}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    logout(request)
    return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)     