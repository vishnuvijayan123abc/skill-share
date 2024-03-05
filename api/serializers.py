from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Userprofile,Product,Cart,CartItem,Comment,Bids

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

class CartItemSerializer(serializers.ModelSerializer):
   total=serializers.IntegerField(read_only=True)
   product=ProductSerializer(read_only=True)
   class Meta:
      model=CartItem
      fields="__all__"
      read_only_field=["id",
                     "product",
                     "is_active",
                     "created_at",
                     "updated_at",
                     ]
class CartSerializer(serializers.ModelSerializer):
   cart_items=CartItemSerializer(read_only=True,many=True)
   user=serializers.StringRelatedField()
   cart_item_total=serializers.IntegerField(read_only=True)

   class Meta:
      model=Cart
      fields="__all__"
      read_only_fields=["id",
                          "user",
                          "is_active",
                          "created_at",
                          "updated_at",
                          "cartitems"]     
class CommentSerializer(serializers.ModelSerializer):
   class Meta:
      model=Comment
      fields="__all__"
      read_only_fields=["id",
                        "created_at",
                        "user",
                        "product"]    
      
class BidSerializer(serializers.ModelSerializer):
   class Meta:
      model=Bids
      fields="__all__"
      read_only_fields=["id","product","user",]     
  
