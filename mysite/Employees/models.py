from django.db import models

# Create your models here.

class Employees(models.Model):
    
    firstname = models.CharField('First Name: ',max_length=255, null=True)
    middlename = models.CharField('Middle Name: ',max_length=255, null=True)
    lastname = models.CharField('Last Name: ',max_length=255, null=True)
    suffix = models.CharField('Suffix: ',max_length=255, null=True)
    birthday = models.DateField('Birthday' ,null=True)
    gender = models.CharField('Gender: ',max_length=255, null=True)
    civilstatus = models.CharField('Civil Status: ',max_length=255, null=True)
    created_date = models.DateTimeField('Created Date: ',auto_now_add=True, null=True)
    updated_date = models.DateTimeField('Updated Data: ',auto_now=True, null=True)
    isRegular = models.BooleanField(default=False)  # new column
    RegularizationDate = models.DateField(null=True)  # new column
    EmploymentDate = models.DateField(null=True)  # new column
    created_by = models.CharField(max_length=255, blank=True, null=True)
    updated_by = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        # Set the name of the database table for this model
        db_table = 'Employees' 
    # Return a string containing the values of the "firstname" and "lastname" attributes
    def __str__(self):
        return f"{self.firstname} {self.lastname} "
# new class WorkSchedules
class WorkSchedules(models.Model):
    # Define a foreign key field that references the Employees table's id column
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE, related_name='WorkSchedules')
    date = models.DateField()  # Date field for the work schedule
    time_start = models.TimeField()  # Start time of work
    time_end = models.TimeField()  # End time of work
    lunch_break_start = models.TimeField()  # Start time of lunch break
    lunch_break_end = models.TimeField()  # End time of lunch break
    created_by = models.CharField(max_length=255)  # Name of the user who created the work schedule
    created_datetime = models.DateTimeField(auto_now_add=True)  # Date and time the work schedule was created

    class Meta:
        db_table = 'WorkSchedules'  # Set the name of the database table for this model
    # Return a string containing the name of the employee and the date
    def __str__(self):
        return f"{self.employee} - {self.date}"
    
def save(self, *args, **kwargs):
    # Check if employee field is empty
    if not self.employee:
        raise ValueError("employee cannot be empty.")
    # Attempt to retrieve the employee object with the id
    try:
        employee = Employees.objects.get(pk=self.employee.id)
    except Employees.DoesNotExist:
        # If the employee does not exist, raise a ValueError
        raise ValueError("employee_id does not exist in Employees table.")
    # Call the save method of the parent class to save the record
    super(WorkSchedules, self).save(*args, **kwargs)


