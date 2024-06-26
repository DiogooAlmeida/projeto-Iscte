from django.db import models

# Create your models here.
class EncryptedFile(models.Model):
    filename = models.CharField(max_length=255, unique=True)
    data = models.BinaryField()
    saved_month = models.DateTimeField(auto_now_add=True)