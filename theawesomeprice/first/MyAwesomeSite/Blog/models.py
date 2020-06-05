from django.db import models

# Create your models here.

class BlogModels(models.Model):

    title=models.CharField(max_length=250)
    release_data=models.DateField(verbose_name=None)
    Category=models.CharField(max_length=100,default=None,null=True)