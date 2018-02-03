from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from viewflow.models import Process
@python_2_unicode_compatible  # only if you need to support Python 2

class Faculty(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    dean=models.IntegerField(default=0)
    year=models.CharField(max_length=50)
    #created_at = models.DateTimeField(auto_now_add=True)
    #updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Department(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    dean = models.IntegerField
    year = models.CharField(max_length=50)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    #created_at = models.DateTimeField(auto_now_add=True)
    #updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
