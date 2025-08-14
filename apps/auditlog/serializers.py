from rest_framework import serializers
from .models import AuditLog

class AuditLogSerializer(serializers.ModelSerializer):
    who = serializers.StringRelatedField()

    class Meta:
        model = AuditLog
        fields = ['id', 'who', 'what', 'when', 'changes']
