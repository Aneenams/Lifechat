from django.shortcuts import render
from rest_framework.generics import CreateAPIView,ListAPIView
from lifeapp.serializers import RegisterSerializer,LoginSerializer,ConnectionRequestSerializer,ConnectionSerializer
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

class AcceptConnectionRequestView(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def post(self,request,pk):
        try:
            connection=Connection.objects.get(pk=pk,to_user=request.user,status='pending')
        except Connection.DoesNotExist:
            return Response({"msg":"no pending requests found"})
        connection.status='accepted'
        connection.save()
        return Response({"msg":"connection accepted"})

class RejectedConnectionRequestView(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def post(self,request,pk):
        try:
            connection=Connection.objects.get(pk=pk,to_user=request.user,status='pending')
        except Connection.DoesNotExist:
            return Response({"msg":"no pending requests found"},status=status.HTTP_404_NOT_FOUND)
        connection.status='rejected'
        connection.save()
        return Response({"msg":"connection rejected"})


class PendingRequestListView(ListAPIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=ConnectionSerializer

    def get_queryset(self):
        return Connection.objects.filter(to_user=self.request.user,status='pending')
    

class MyConnectionListView(ListAPIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=ConnectionSerializer

    def get_queryset(self):
        user=self.request.user
        return Connection.objects.filter(
            Q(from_user=user) | Q(to_user=user),
            status='accepted'
        )
    
