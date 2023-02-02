from django.db import models

# Create your models here.

class Account(models.Model):
    email=models.CharField(max_length=50,null=False,blank=False)
    password = models.CharField(max_length=50,null=False,blank=False)

    def __str__(self):
        return self.email

class Annoncement(models.Model):
    announce=models.TextField(null=False,blank=False)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=10,null=False,blank=False,default="Entered")
    creator = models.CharField(max_length=50,)
    # priority = moels.CharField(max_length=10,null=False,blank=False,default="low")

    
    def values(self):
        return {
            "announce" : self.announce,
            "start_time" : self.start_time,
            "end_time" : self.end_time,
            "status" : self.status,
            "created_by" : self.creator
        }
