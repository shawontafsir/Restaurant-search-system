from django.db import models

class Register(models.Model):
    name = models.CharField(max_length=50)
    mobileNo = models.CharField(max_length=15)
    email = models.CharField(max_length=20)
    password = models.CharField(max_length=15)

    def __str__(self):
        return self.name+' - '+self.mobileNo+' - '+self.email
