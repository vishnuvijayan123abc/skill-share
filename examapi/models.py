from django.db import models
from api.models import User

# Create your models here.
class Topic(models.Model):
    skills=models.CharField(max_length=200)

    def __str__(self):
        return self.skills

class Qusetion(models.Model):
    topic=models.ForeignKey(Topic,on_delete=models.CASCADE)
    qusetion=models.CharField(max_length=500)

    def __str__(self):
        return self.qusetion

class Answer(models.Model):

    user=models.ForeignKey(User,on_delete=models.CASCADE)
    answer_sheet=models.FileField(upload_to="answer_sheet")
    option=(
        ("pending","pending"),
        ("pass","pass"),
        ("failed","failed")
    )

    
    status=models.CharField(max_length=200,default="pending",choices=option)

    def __str__(self):
        return self.status




