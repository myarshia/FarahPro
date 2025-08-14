# apps/auditlog/signals.py
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db import connection
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import AuditLog

# مدل‌هایی که لاگ براشون ثبت می‌کنیم
_registered_models = set()

def is_table_exists(table_name):
    """Check if a table exists in the database (useful during tests)."""
    return table_name in connection.introspection.table_names()

@receiver(post_save)
def log_save(sender, instance, created, **kwargs):
    if sender not in _registered_models or sender == AuditLog:
        return

    if not is_table_exists(AuditLog._meta.db_table):
        return

    what = f"{sender.__name__} ایجاد شد" if created else f"{sender.__name__} ویرایش شد"

    # جمع‌آوری تغییرات
    changes = {
        field.name: getattr(instance, field.name)
        for field in instance._meta.fields
        if field.name != 'id'
    }
    changes = json.loads(json.dumps(changes, cls=DjangoJSONEncoder))

    # فقط یک رکورد ایجاد کن
    AuditLog.objects.create(
        what=what,
        changes=changes
    )

@receiver(post_delete)
def log_delete(sender, instance, **kwargs):
    if sender not in _registered_models or sender == AuditLog:
        return
    if not is_table_exists(AuditLog._meta.db_table):
        return

    what = f"{sender.__name__} حذف شد"
    changes = {
        field.name: getattr(instance, field.name)
        for field in instance._meta.fields
        if field.name != 'id'
    }
    changes = json.loads(json.dumps(changes, cls=DjangoJSONEncoder))

    AuditLog.objects.create(
        what=what,
        changes=changes
    )

def register_auditlog(model):
    """Register a model for audit logging."""
    if model not in _registered_models:
        _registered_models.add(model)
