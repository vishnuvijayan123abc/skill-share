from django.urls import path
from examapi import views
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register("topic",views.TopicView,basename="topic")
router.register("question",views.QuestionView,basename="question")
router.register("answer",views.AnswerAddView,basename="answer")

from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import download_answer

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
     path('add-question/',views.AddQuestionView.as_view(), name='add-question'),
     path('questions/<int:topic_id>/',views.QuestionByTopicView.as_view(), name='questions-by-topic'),
     path('download_answer/<int:answer_id>/', download_answer, name='download_answer'),
]+router.urls
