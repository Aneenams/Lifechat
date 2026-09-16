from django.shortcuts import render
from rest_framework.generics import CreateAPIView,ListAPIView,RetrieveUpdateAPIView
from lifeapp.serializers import RegisterSerializer,LoginSerializer,ConnectionRequestSerializer,ConnectionSerializer,ProfileSerializer,DirectoryProfileSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token 

from rest_framework import authentication,permissions,status
from django.db.models import Q
from lifeapp.models import Connection,Profile
from lifeapp.utils import get_compactable_donor_types
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

#16/sept    
class MyProfileView(RetrieveUpdateAPIView):
    serializer_class=ProfileSerializer
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

class DirectorySearchView(ListAPIView):
    serializer_class = DirectoryProfileSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        blood_group = self.request.query_params.get('blood_group')
        city = self.request.query_params.get('city')

        compatible_types = get_compactable_donor_types(blood_group)
        queryset = Profile.objects.filter(
            blood_group__in=compatible_types,
            blood_status='available',
        ).exclude(user=self.request.user)

        if city:
            queryset = queryset.filter(city__iexact=city)

        return queryset    