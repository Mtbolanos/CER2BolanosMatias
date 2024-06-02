from django.db import models
from django.contrib.auth.models import User

class Proyecto(models.Model):
    nombre_proyecto = models.CharField(max_length=100)
    estudiante = models.CharField(max_length=100)
    tema = models.CharField(max_length=100)
    profesor = models.CharField(max_length=100)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre_proyecto
