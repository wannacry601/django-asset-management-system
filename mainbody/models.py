from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Asset(models.Model):
    ID = models.CharField(max_length=13,primary_key=True) #Primary key, 13 digit.
    assetname = models.CharField(max_length=100,null=True)
    user = models.CharField(max_length=100,null=True,default='Available')
    location = models.CharField(max_length=100,null=True)
    check_out_date = models.DateTimeField(null=True)
    DEFAULT_USER = "Available"
    def __str__(self):
        return self.assetname
        # This is what to be shown on admin page for preview. 
        
class check_out(models.Model):
    user = models.CharField(max_length=100)
    userID = models.ForeignKey(User,default='0',on_delete=models.CASCADE)
    asset = models.CharField(max_length=100)
    assetID = models.ForeignKey(Asset,on_delete=models.CASCADE,null=False,default='1145141145142')
    checkdate = models.DateTimeField()
    def __str__(self):
        return f"{self.asset}; assigned to '{self.user}' at {self.checkdate}"