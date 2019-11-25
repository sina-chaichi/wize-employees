from django.contrib import admin

from .models import Role, Organization, Employee, Token, Application


class RoleAdmin(admin.ModelAdmin):
    model = Role
    exclude = ('created_at', 'updated_at', 'deleted_at', )

class OrganizationAdmin(admin.ModelAdmin):
    model = Organization
    exclude = ('created_at', 'updated_at', 'deleted_at', )

class EmployeeAdmin(admin.ModelAdmin):
    model = Employee
    exclude = ('created_at', 'updated_at', 'deleted_at', )

class TokenAdmin(admin.ModelAdmin):
    model = Token
    exclude = ('created_at', 'updated_at', 'deleted_at', )

class ApplicationAdmin(admin.ModelAdmin):
    model = Application
    exclude = ('created_at', 'updated_at', 'deleted_at', )

    
admin.site.register(Role, RoleAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Token, TokenAdmin)
admin.site.register(Application, ApplicationAdmin)


