from django.db import models


# Create your models here.
class OpenaiFiles(models.Model):
    pdf = models.FileField()
