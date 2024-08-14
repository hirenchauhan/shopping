from django.db import models
from myadmin.models import *
from django.contrib.auth.models import User

class Register(models.Model):
    contact = models.BigIntegerField()
    dob     = models.DateField()
    gender  = models.CharField(max_length=30)
    address = models.TextField()
    state   = models.ForeignKey(State,on_delete=models.CASCADE)
    city    = models.ForeignKey(City,on_delete=models.CASCADE)
    area    = models.ForeignKey(Area,on_delete=models.CASCADE)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    status = models.CharField(max_length=255,default='Pending')
    date = models.DateField(null=True, blank=True)


    class Meta():
        db_table='register'

class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    contact = models.BigIntegerField()
    message = models.TextField()
    date = models.DateField()

    class Meta():
        db_table = 'contact'

class Saler_reg(models.Model):
    state = models.ForeignKey(State,on_delete=models.CASCADE)
    city = models.ForeignKey(City,on_delete=models.CASCADE)
    area = models.ForeignKey(Area,on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=100)
    shop_address = models.TextField()
    shop_contact = models.BigIntegerField()
    image = models.CharField(max_length=255)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    status = models.CharField(max_length=255,default='Pending')
    date = models.DateField(null=True, blank=True)

    
    class Meta():
        db_table = 'saler_reg'
