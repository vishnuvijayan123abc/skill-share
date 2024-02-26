from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Userprofile,Product

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["id","username","email","password"]
        read_only_fields=["id"]

    def create(self, validated_data):
      return User.objects.create_user(**validated_data)     

class UserProfileSerializer(serializers.ModelSerializer):
   class Meta:
      model=Userprofile
      fields="__all__" 
      read_only_fields=["id"]  

class ProductSerializer(serializers.ModelSerializer):
   class Meta:
      model=Product
      fields="__all__" 
      read_only_fields=["id","created_date","user"]   
