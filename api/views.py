from django.shortcuts import render
from api.serializers import UserSerializer,UserProfileSerializer,ProductSerializer,CartItemSerializer,CartSerializer,CommentSerializer,BidSerializer,ChatSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import serializers
from api.models import Userprofile,Product,Cart,CartItem,Comment,Bids,Chat
from rest_framework import authentication,permissions
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import generics
from examapi.models import Answer
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


# Create your views here.
class UserSignUpView(APIView):
    def post(self,request,*args, **kwargs):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(data=serializer.errors)
    
class ObtainTokenView(APIView):
    permission_classes = [AllowAny]  # Allow any user to obtain a token

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({'error': 'Both username and password are required'}, status=400)

        # Perform authentication
        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Invalid credentials'}, status=400)

        # Create or retrieve token
        token, created = Token.objects.get_or_create(user=user)

        return Response({'token': token.key, 'user_id': user.id})    
    
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

    
    def update(self, request, *args, **kwargs):
       instance= self.get_object()
       if request.user==instance.user:
            return super().update(request,*args,**kwargs)
       else:
           return Response("you have no permission")
    def perform_create(self, serializer):
        # Associate the user making the request with the product
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        # Get the user's Answer status
        answer_status = Answer.objects.filter(user=request.user).first()

        # Check if the user has passed the exam
        if answer_status and answer_status.status == "pass":
            return super().create(request, *args, **kwargs)
        else:
            return Response({"detail": "User hasn't passed the exam. Cannot create a product."}, status=status.HTTP_403_FORBIDDEN)
   
       
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

class CommentView(viewsets.ModelViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    serializer_class=CommentSerializer
    
    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        return Comment.objects.filter(product_id=product_id)


    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_id')
        serializer.save(user=self.request.user, product_id=product_id)
class BidView(viewsets.ModelViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    serializer_class=BidSerializer
    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        return Comment.objects.filter(product_id=product_id)

    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_id')
        serializer.save(user=self.request.user, product_id=product_id)

class ListallBid(viewsets.ModelViewSet):
    serializer_class=BidSerializer
    queryset=Bids.objects.all()        

    def get_queryset(self):
        user = self.request.user
        return Bids.objects.filter(user=user) | Bids.objects.filter(product__user=user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SendMessageAPIView(generics.CreateAPIView):
   

    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes =[authentication.TokenAuthentication]

    def perform_create(self, serializer):
        sender_user = self.request.user  # Extract sender user from the authentication token
        receiver_user_id = self.kwargs.get('receiver_id')
        receiver_user = get_object_or_404(User, id=receiver_user_id)

        serializer.save(send_user=sender_user, receiver_user=receiver_user)

    def get_queryset(self):
        sender_user = self.request.user  # Extract sender user from the authentication token
        receiver_user_id = self.kwargs.get('receiver_id')
        receiver_user = get_object_or_404(User, id=receiver_user_id)

        queryset = Chat.objects.filter(send_user=sender_user, receiver_user=receiver_user)
        return queryset
class UserChatMessagesAPIView(generics.ListAPIView):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get_queryset(self):
        user = self.request.user  # Get the authenticated user
        queryset = Chat.objects.filter(send_user=user) | Chat.objects.filter(receiver_user=user)
        return queryset