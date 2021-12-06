from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class Note(models.Model):
    user = models.CharField(max_length=100)
    note = models.CharField(max_length=10000)

    def __str__(self):
        return f"{self.user}: {self.note}"
