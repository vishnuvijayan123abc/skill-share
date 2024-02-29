from django.shortcuts import render
from api.serializers import UserSerializer,UserProfileSerializer,ProductSerializer,CartItemSerializer,CartSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import serializers
from api.models import Userprofile,Product,Cart,CartItem
from rest_framework import authentication,permissions
from rest_framework.decorators import action


# Create your views here.
class UserSignUpView(APIView):
    def post(self,request,*args, **kwargs):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(data=serializer.errors)
    
class UserProfileUpdateRetiveView(viewsets.ModelViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=UserProfileSerializer
    queryset=Userprofile.objects.all()


    def create(self, request, *args, **kwargs):
        raise serializers.ValidationError("permission denied")
    
    def destroy(self, request, *args, **kwargs):
        raise serializers.ValidationError("permission denied")
    
class ProductCreatListUpdateDestroyView(viewsets.ModelViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]


    serializer_class=ProductSerializer
    queryset=Product.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
       instance= self.get_object()
       if request.user==instance.user:
            return super().update(request,*args,**kwargs)
       else:
           return Response("you have no permission")
       
    @action(methods=["post"],detail=True)
   
    def add_to_cart(self, request, *args, **kwargs):
        product_id = kwargs.get("pk")
        product_obj = Product.objects.get(id=product_id)

        # Get or create a cart for the user
        cart_obj, created = Cart.objects.get_or_create(user=request.user)

        # Create a mutable copy of request.data
        mutable_data = request.data.copy()

        # Set the cart field in the mutable copy
        mutable_data['cart'] = cart_obj.id

        serializer = CartItemSerializer(data=mutable_data)
        if serializer.is_valid():
            serializer.save(product=product_obj)
            return Response(data=serializer.data)
        return Response(data=serializer.errors)
    
class CartView(viewsets.ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    def list(self,request,*args, **kwargs):
        qs=request.user.cart 
        serializers=CartSerializer(qs,many=False)
        return Response(data=serializers.data)
    



class CartItemView(viewsets.ModelViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    serializer_class=CartItemSerializer
    queryset=CartItem.objects.all()


    def create(self, request, *args, **kwargs):
        raise serializers.ValidationError("permision denied")    



        
    

