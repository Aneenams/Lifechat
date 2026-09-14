from django.shortcuts import render
from rest_framework.generics import CreateAPIView,ListAPIView
from lifeapp.serializers import RegisterSerializer,LoginSerializer,ConnectionRequestSerializer,ConnectionSerialzer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token 

from rest_framework import authentication,permissions,status
from django.db.models import Q
from lifeapp.models import Connection
# Create your views here.
class UserRegisterView(CreateAPIView):
    serializer_class=RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        return Response(
            {'msg':"Registration successful","username":user.username}
        )

class LoginView(APIView):
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {'msg':'Login successful', 'token': token.key, 'username': user.username}
        )    

class SendConnectionRequestView(CreateAPIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]   
    serializer_class=ConnectionRequestSerializer 