from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'mobile', "first_name", "last_name", "password", "is_active", "is_staff",
                  "is_superuser", "last_login", "date_joined", ]
        read_only_fields = ["id", "is_active", "is_staff", "is_superuser", "last_login", "date_joined"]

    def create(self, validated_data):
        # user = User(
        #     username=validated_data['username'],
        #     email=validated_data['email'],
        #     mobile=validated_data.get('mobile', ''),
        #     first_name=validated_data.get('first_name', ''),
        #     last_name=validated_data.get('last_name', '')
        # )
        # user.set_password(validated_data['password'])
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        # for attr, value in validated_data.items():
        #     if attr == 'password':
        #         instance.set_password(value)
        #     else:
        #         setattr(instance, attr, value)
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
