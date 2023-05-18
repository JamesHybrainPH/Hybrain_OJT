from django.db import models
from Employees.models import Employees

class Users(models.Model):

    USER_TYPE_CHOICES = [
        ('Administrator', 'Administrator'),
        ('Employees', 'Employees'),
    ]
    UserType = models.CharField(max_length=255, choices=USER_TYPE_CHOICES,default='Employees')
    employee_id = models.ForeignKey(Employees, on_delete=models.CASCADE)
    isActive = models.BooleanField(default=True)
    useraccess = models.CharField(max_length=255)
    passphrase = models.TextField()
    salt = models.CharField(max_length=255)
    created_by = models.CharField(max_length=255, null=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'users' 
    def __str__(self):
        return self.useraccess

