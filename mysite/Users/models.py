from django.db import models
from  Employees.models import Employees


class UserAccount(models.Model):
    id = models.AutoField(primary_key=True)
    employee_id = models.ForeignKey(Employees, on_delete=models.CASCADE)
    isActive = models.BooleanField(default=False)
    useraccess = models.CharField(max_length=255)
    passphrase = models.CharField(max_length=255)
    salt = models.CharField(max_length=255)
    created_by = models.CharField(max_length=255)
    created_datetime = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        db_table = 'UserAccount'
    def __str__(self):
        return self.useraccess
