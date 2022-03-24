import time

from django.db import models


# Create your models here.
class FibModel(models.Model):
    input = models.PositiveBigIntegerField()
    output = models.CharField(max_length=2000, blank=True)
    status = models.CharField(
        choices=[
            ('success', 'SUCCESS'), ('error', 'ERROR'), ('pending', 'PENDING')
        ],
        max_length=20, blank=True, default='pending'
    )
    date_created = models.DateTimeField(auto_now=time.ctime())
    date_modified = models.DateTimeField(auto_now=time.ctime())
