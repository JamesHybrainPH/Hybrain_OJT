from django.db import models
from  Employees.models import Employees


class UserAccount(models.Model):
    id = models.AutoField(primary_key=True)
    employee_id = models.ForeignKey(Employees, on_delete=models.CASCADE)
    isActive = models.BooleanField(default=True)
    useraccess = models.CharField(max_length=255)
    passphrase = models.TextField()
    salt = models.CharField(max_length=255)
    created_by = models.CharField(max_length=255)
    created_datetime = models.DateTimeField(auto_now_add=True)
    user_type = models.CharField(choices=(('Administrator', 'Administrator'), ('Employee', 'Employee')), max_length=20, default='Employee')

    class Meta:
        db_table = 'UserAccount'
    def __str__(self):
        return self.useraccess
