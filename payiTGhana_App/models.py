__author__ = 'Gad Ocansey'
from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
@python_2_unicode_compatible  # only if you need to support Python 2

class Client(models.Model):
     id = models.AutoField(primary_key=True)
     code = models.CharField(max_length=100)
     firstname= models.CharField(max_length=100)
     lastname= models.CharField(max_length=100)
     gender= models.CharField(max_length=10)
     phone= models.IntegerField(max_length=10,unique=True)
     mobile_money_phone= models.IntegerField(max_length=10,unique=True)
     email=models.EmailField(unique=True)
     mobile_money_name = models.CharField(max_length=10,unique=True)
     address = models.CharField(max_length=100)
     date_joined =models.DateTimeField(auto_now_add=True, blank=True)
     referrer =  models.CharField(max_length=100,null=True)
     user_id =  models.ForeignKey(User, unique=True,on_delete=models.CASCADE)
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)

     class Meta:
         ordering = ["created_at"]

     def __str__(self):
         return self.firstname


class Pledge(models.Model):

    id=models.AutoField(primary_key=True)
    pledge_maker_id=models.ForeignKey(Client, on_delete=models.CASCADE)

    pledged_amount= models.DecimalField(max_digits=20, decimal_places=2)
    payment_confirm=models.IntegerField()
    payment_deadline=models.DateTimeField()
    maturity_date=models.DateField()
    transaction_code=models.CharField(unique=True,max_length=10)
    status=models.IntegerField()
    matched=models.IntegerField()
    repledged=models.IntegerField()
    #pledge_receiver_id=models.ForeignKey(Client,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]


class Match(models.Model):

    id=models.AutoField(primary_key=True)
    pledge_id = models.ForeignKey(Pledge, on_delete=models.CASCADE)
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    amount=models.DecimalField(max_digits=20, decimal_places=2)
    type=models.CharField(max_length=20)
    sms=models.IntegerField()
    confirmed=models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]

class Sms(models.Model):

    id=models.AutoField(primary_key=True)
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    status =models.CharField(max_length=20)
    message=models.CharField(max_length=200)
    sender=models.CharField(max_length=90)
    phone=models.CharField(max_length=20)
    type=models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]

