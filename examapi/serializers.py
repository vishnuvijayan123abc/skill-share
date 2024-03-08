from rest_framework import serializers
from django.contrib.auth.models import User
from examapi.models import Topic,Qusetion,Answer



class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model=Topic
        fields="__all__"
        read_only_fields=["id"]

class QuetionSerializer(serializers.ModelSerializer):
   
    class Meta:
        model=Qusetion
        fields="__all__"
        read_only_fileds=["id"]      

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Answer
        fields="__all__"
        read_only_fields=["id","status","user"]