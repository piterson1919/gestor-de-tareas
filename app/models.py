from django.db import models 
from django.contrib.auth.models import User 

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=100)
    importance = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    

    
