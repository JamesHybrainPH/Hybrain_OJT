from django.contrib import admin
from .models import UserAccount

class UsersAdmin(admin.ModelAdmin):
    # Define a list_display attribute to specify which fields to display in the admin list view
    list_display = ['employee_id', 'salt','isActive', 'created_by', 'created_datetime']
    # Define a readonly_fields attribute to specify which fields should be displayed as read-only in the admin view
    readonly_fields = ['salt', 'created_datetime']

# Register the Users model with the custom ModelAdmin class
admin.site.register(UserAccount, UsersAdmin)