from django.db import models

class Path(models.Model):
    path = models.CharField(max_length=500)