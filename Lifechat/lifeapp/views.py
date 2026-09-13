from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from lifeapp.serializers import RegisterSerializer
from rest_framework.response import Response
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