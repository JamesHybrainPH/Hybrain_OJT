from django.contrib import admin
from .models import Users

# Define a custom ModelAdmin class for the Users model
class UsersAdmin(admin.ModelAdmin):
    # Define a list_display attribute to specify which fields to display in the admin list view
    list_display = ['useraccess', 'employee_id', 'salt','isActive', 'created_by', 'created_datetime']
    # Define a readonly_fields attribute to specify which fields should be displayed as read-only in the admin view
    readonly_fields = ['salt', 'created_datetime']

# Register the Users model with the custom ModelAdmin class
admin.site.register(Users, UsersAdmin)
