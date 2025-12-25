from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}

    def save_password(self, user, password):
        if password:
            user.set_password(password)
            user.save()

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = super().create(validated_data)
        self.save_password(user, password)
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        self.save_password(user, password)
        return user
