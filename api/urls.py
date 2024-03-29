from django.urls import path,include
from api import views
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register("userprofile",views.UserProfileUpdateRetiveView ,basename="userprofile")
router.register("product",views.ProductCreatListUpdateDestroyView,basename="product")
router.register('carts',views.CartView,basename="cart")
router.register("cartitem",views.CartItemView,basename="cartitem")
router.register('comments/(?P<product_id>\d+)',views.CommentView, basename='comment')
router.register('product/bids/(?P<product_id>\d+)',views.BidView,basename="bid")
router.register("bid",views.ListallBid,basename="bidlist")


from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('register/',views.UserSignUpView.as_view()),
    path('send-message/<int:receiver_id>/', views.SendMessageAPIView.as_view(), name='send_message'),
    path('user-chat-messages/',views.UserChatMessagesAPIView.as_view(), name='user_chat_messages'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('token/', views.ObtainTokenView.as_view(), name='token_obtain'),
   
  
     
]+router.urls
