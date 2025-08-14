from rest_framework import viewsets, permissions
from .models import AuditLog
from .serializers import AuditLogSerializer

class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    فقط امکان خواندن لاگ‌ها وجود دارد
    """
    queryset = AuditLog.objects.all().order_by('-when')
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAdminUser] # فقط ادمین‌ها دسترسی دارند
