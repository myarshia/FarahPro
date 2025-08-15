from rest_framework import viewsets, permissions
from django.contrib.auth import get_user_model
from .serializers import UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        ثبت‌نام (create) بدون لاگین ممکن است.
        حذف کاربران فقط برای ادمین‌ها مجاز است.
        سایر عملیات برای کاربران لاگین شده است.
        """
        if self.action == "create":
            return [permissions.AllowAny()]
        if self.action == "destroy":
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]
