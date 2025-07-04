from django.db import models

class Apps(models.Model):
    name=models.CharField(max_length=120,null=False,blank=False,unique=True)
    publisher=models.CharField(max_length=120,null=False,blank=False)
    app_logo=models.ImageField(null=True,blank=True)
    points=models.IntegerField(null=False,blank=False)