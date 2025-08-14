# apps/organizations/admin.py
from django.contrib import admin
from .models import Organization

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("legal_name", "trade_name", "country", "city", "currency_code", "is_active", "created_at")
    search_fields = ("legal_name", "trade_name", "registration_code", "email_address", "phone_number")
    list_filter = ("is_active", "country", "currency_code")
    ordering = ("legal_name",)
    readonly_fields = ("created_at", "updated_at")
