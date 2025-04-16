from django.forms import ModelForm
from .models import Tareas

class TaskForm(ModelForm):
    class Meta:
        model = Tareas
        fields = ['nombre','descripcion','importancia']