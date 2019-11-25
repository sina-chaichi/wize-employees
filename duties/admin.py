from django.contrib import admin

from .models import Duty

class DutyAdmin(admin.ModelAdmin):
    model = Duty
    exclude = ('created_at', 'updated_at', 'deleted_at', )

admin.site.register(Duty, DutyAdmin)