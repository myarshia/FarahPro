from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('when', 'who', 'what')
    readonly_fields = ('when',)
    ordering = ('-when',)
