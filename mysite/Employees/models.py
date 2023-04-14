from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import models

CIVIL_STATUS_CHOICES = [
    ('single', 'Single'),
    ('married', 'Married'),
    ('widowed', 'Widowed'),
    ('divorced', 'Divorced'),
]

class Employees(models.Model):
    first_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200)
    suffix = models.CharField(max_length=200, null=True, blank=True)
    Birthday = models.DateField(null=True)
    civil_status = models.CharField(max_length=200, choices=CIVIL_STATUS_CHOICES)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(null=True, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    hire_date = models.DateField(auto_now_add=True)
    is_Regular = models.BooleanField(default=False)
    RegularizationDate = models.DateField(null=True)
    EmploymentDate = models.DateField(null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def clean(self):
        """
        Validate RegularizationDate is greater than or equal to hire_date
        """
        if self.isRegular and self.RegularizationDate > self.hire_date:
            raise ValidationError('Regularization date cannot be earlier than hire date.')

        if self.Birthday and self.Birthday > timezone.now().date():
            raise ValidationError("Birthdate cannot be in the future.")
        
class WorkSchedule(models.Model):
    # Define a foreign key field that references the Employees table's id column
    employee = models.ForeignKey('Employees', on_delete=models.CASCADE, related_name='workschedules')
    date = models.DateField()  # Date field for the work schedule
    time_start = models.TimeField()  # Start time of work
    time_end = models.TimeField()  # End time of work
    lunch_break_start = models.TimeField()  # Start time of lunch break
    lunch_break_end = models.TimeField()  # End time of lunch break
    created_by = models.CharField(max_length=255)  # Name of the user who created the work schedule
    created_datetime = models.DateTimeField(auto_now_add=True)  # Date and time the work schedule was created

    class Meta:
        db_table = 'WorkSchedule'  # Set the name of the database table for this model
    # Return a string containing the name of the employee and the date
    def str(self):
        return f"{self.employee} - {self.date}"

    def save(self, *args, **kwargs):
        # Check if employee_id field is empty
        if not self.employee_id:
            raise ValueError("employee_id cannot be empty.")
        # Attempt to retrieve the employee object with the employee_id
        try:
            employee = Employees.objects.get(pk=self.employee_id)
        except Employees.DoesNotExist:
            # If the employee does not exist, raise a ValueError
            raise ValueError("employee_id does not exist in Employees table.")
        # Call the save method of the parent class to save the record
        super(WorkSchedule, self).save(*args, **kwargs)
    