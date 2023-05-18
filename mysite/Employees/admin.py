from django.contrib import admin
from .models import Employees as MyEmployees,WorkSchedules
# Register your models here.

class MemberAdmin(admin.ModelAdmin):
  list_display = ("firstname", "lastname","middlename", "suffix","birthday","gender","civilstatus","created_date","updated_date")
class WorkSchedulesAdmin(admin.ModelAdmin):
  list_display = ('employee', 'date', 'time_start', 'time_end', 'lunch_break_start', 'lunch_break_end', 'created_by', 'created_datetime')


admin.site.register(MyEmployees, MemberAdmin)
admin.site.register(WorkSchedules, WorkSchedulesAdmin)
