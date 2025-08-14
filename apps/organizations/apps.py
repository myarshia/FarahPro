# apps/organizations/apps.py
from django.apps import AppConfig

class OrganizationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.organizations'
    verbose_name = "مدیریت افراد/سازمان‌ها/شرکت‌ها/فروشگاه‌ها"

    def ready(self):
        from apps.auditlog.signals import register_auditlog
        from .models import Organization
        register_auditlog(Organization)

