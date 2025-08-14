from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class AuditLog(models.Model):
    who = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="کاربر")
    what = models.CharField(max_length=255, verbose_name="نوع عملیات")
    when = models.DateTimeField(auto_now_add=True, verbose_name="زمان عملیات")
    changes = models.JSONField(null=True, blank=True, verbose_name="جزئیات تغییرات")

    def __str__(self):
        return f"{self.when} - {self.who} - {self.what}"

    class Meta:
        verbose_name = "گزارش تغییرات"
        verbose_name_plural = "گزارش‌های تغییرات"
        ordering = ['-when']
