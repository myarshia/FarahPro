from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Organization

@receiver(post_save, sender=Organization)
def organization_saved(sender, instance, created, **kwargs):
    if created:
        print(f"سازمان جدید ایجاد شد: {instance.legal_name}")
    else:
        print(f"سازمان بروزرسانی شد: {instance.legal_name}")

@receiver(post_delete, sender=Organization)
def organization_deleted(sender, instance, **kwargs):
    print(f"سازمان حذف شد: {instance.legal_name}")
