from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError

class SignInSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ["id", "email", "first_name", "last_name"]
        read_only_fields = fields

User = get_user_model()

class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
    )
    class Meta:
        model = User
        fields = ["email", "username", "password"]
    
    def validate(self, attrs):
        candidate = User(
            email=attrs["email"],
            username=attrs["username"],
        )

        try:
            validate_password(attrs["password"], user=candidate)
        except DjangoValidationError as error:
            raise serializers.ValidationError({
                "password": error.messages,
            })

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
