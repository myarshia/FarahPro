from rest_framework import viewsets, permissions
from .models import Organization
from .serializers import OrganizationSerializer


class OrganizationViewSet(viewsets.ModelViewSet):
    """
    API endpoint برای مدیریت سازمان‌ها
    """
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]  # بعداً میشه سفارشی کرد
