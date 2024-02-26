from django.shortcuts import render
from api.serializers import UserSerializer,UserProfileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import serializers
from api.models import Userprofile


# Create your views here.
class UserSignUpView(APIView):
    def post(self,request,*args, **kwargs):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(data=serializer.errors)
    
class UserProfileUpdateRetiveView(viewsets.ModelViewSet):
    serializer_class=UserProfileSerializer
    queryset=Userprofile.objects.all()


    def create(self, request, *args, **kwargs):
        raise serializers.ValidationError("permission denied")
    
    def destroy(self, request, *args, **kwargs):
        raise serializers.ValidationError("permission denied")

