from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from apps.auditlog.signals import register_auditlog

User = get_user_model()

@receiver(post_save, sender=User)
def log_user_changes(sender, instance, created, **kwargs):
    if created:
        print(f"کاربر جدید ساخته شد: {instance.email}")
    else:
        print(f"کاربر ویرایش شد: {instance.email}")

# ثبت مدل در سیستم لاگ
register_auditlog(User)
