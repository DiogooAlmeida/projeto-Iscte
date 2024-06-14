from django.db import models


class Path(models.Model):
    path = models.CharField(max_length=500)

# Retira a informação dos logs da base de dados
class LogFilesEncrypted(models.Model):
    data = models.TextField()
    filename = models.CharField(max_length=255)
    saved_month = models.DateTimeField(auto_now_add=True)
