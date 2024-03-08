from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework import authentication,permissions
from examapi.serializers import TopicSerializer,QuetionSerializer,AnswerSerializer
from examapi.models import Topic,Qusetion,Answer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from rest_framework import status
# Create your views here.

class TopicView(viewsets.ModelViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAdminUser]
    serializer_class=TopicSerializer
    queryset=Topic.objects.all()

class AddQuestionView(generics.CreateAPIView):
    queryset =Qusetion.objects.all()
    serializer_class =QuetionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
class  QuestionView(viewsets.ModelViewSet):
    serializer_class=QuetionSerializer
    queryset=Qusetion.objects.all()
    
class QuestionByTopicView(generics.ListAPIView):
    serializer_class =QuetionSerializer

    def get_queryset(self):
        topic_id = self.kwargs.get('topic_id')
        return Qusetion.objects.filter(topic_id=topic_id)    
class AnswerAddView(viewsets.ModelViewSet):
    authentication_classes = (authentication.TokenAuthentication,)  # Note the comma
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

def download_answer(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)

    authentication.TokenAuthentication
    permissions.IsAdminUser
    
    # Assuming 'answer' is the FileField in your model
    with open(answer.answer.path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename={answer.answer.name}'
        return response        

    
