# database'i yönettiğin yer
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.crypto import get_random_string
from django.utils import timezone


# Create your models here.
class Projects(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=100, blank=False, null=False) # proje isimleri eşsiz olacağı için her seferinde yeni proje ismi üretiyor
    description = models.TextField(max_length=500, blank=True)
    finished = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now, blank=True)

class Todos(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="todos")
    Project = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name="todos")

    title = models.CharField(max_length=100, blank=False, null=False )
    description = models.TextField(max_length=1000, blank=True)
    finished = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now, blank=True)

    # Todoların isimlerini veritabanında göstermek için:
    def __str__(self):  # string representation for object
        return (
            self.title
        )  # Burada veri tabanında todoların isimleri çıksın diye bunu yapıyoruz




