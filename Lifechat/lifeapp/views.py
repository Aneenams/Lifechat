from django.shortcuts import render
from rest_framework.generics import CreateAPIView,ListAPIView,RetrieveUpdateAPIView
from lifeapp.serializers import RegisterSerializer,LoginSerializer,ConnectionRequestSerializer,ConnectionSerializer,ProfileSerializer,DirectoryProfileSerializer,DonationSerializer,DonationCreateSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token 

from rest_framework import authentication,permissions,status
from django.db.models import Q
from lifeapp.models import Connection,Profile,Donation
from lifeapp.utils import get_compactable_donor_types

from datetime import date 
from django.utils import timezone


from .utils import apply_donation_cooldown, calculate_badge_tier
from .utils import get_compactable_donor_types, refresh_expired_cooldowns

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
    serializer_class = ProfileSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        refresh_expired_cooldowns()
        return Profile.objects.get(user=self.request.user)

class DirectorySearchView(ListAPIView):
    serializer_class = DirectoryProfileSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        refresh_expired_cooldowns()

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


    # 17/sept

class SubmitDonationView(CreateAPIView):
    serializer_class=DonationCreateSerializer
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(donor=self.request.user)

class MyDonationListView(ListAPIView):
    serializer_class = DonationSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Donation.objects.filter(donor=self.request.user).order_by('-created_at')

class PendingDonationListView(ListAPIView):
    serializer_class=DonationSerializer
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAdminUser]    
    queryset=Donation.objects.filter(status='pending').order_by('created_at')

class ApproveDonationView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, pk):
        try:
            donation = Donation.objects.get(pk=pk, status='pending')
        except Donation.DoesNotExist:
            return Response({"msg": "no pending donation found"}, status=status.HTTP_404_NOT_FOUND)

        donation.status = 'approved'
        donation.verified_by = request.user
        donation.verified_at = timezone.now()
        donation.save()

        profile = donation.donor.profile
        profile.verified_donation_count += 1
        profile.badge_tier = calculate_badge_tier(profile.verified_donation_count)
        apply_donation_cooldown(profile)
        profile.save()

        return Response({"msg": "donation approved"}, status=status.HTTP_200_OK)

class RejectDonationView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, pk):
        try:
            donation = Donation.objects.get(pk=pk, status='pending')
        except Donation.DoesNotExist:
            return Response({"msg": "no pending donation found"}, status=status.HTTP_404_NOT_FOUND)

        donation.status = 'rejected'
        donation.admin_notes = request.data.get('admin_notes', '')
        donation.verified_by = request.user
        donation.verified_at = timezone.now()
        donation.save()

        return Response({"msg": "donation rejected"}, status=status.HTTP_200_OK)



#19/sept



