from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        try:
            validate_password(password=password, user=user)
        except ValidationError as err:
            raise serializers.ValidationError({'password': err.messages})
        user.set_password(password)
        user.save()
        return user
