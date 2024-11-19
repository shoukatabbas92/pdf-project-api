from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from .seriallizers import RegisterSerializer,LoginSerializer,UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterView(generics.CreateAPIView):
    # queryset = User.objects.all()
    # permission_classes = (AllowAny,)
    # serializer_class = RegisterSerializer
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data},status=201)
        return Response({
            'data' : serializer.errors,
            'status' : 400
        })


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self,request,*args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('passowrd')
        user = authenticate(email=email,password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            user_serializer = UserSerializer
            return Response({
                'refresh' : str(refresh),
                'access' : str(refresh.access_token),
                'user' : user_serializer.data
            })
        else:
            return Response({
                'detail' : 'invalid Credentials'
                },status=401)
