from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "email",
            "phone_number",
            "first_name",
            "last_name",
            "is_vendor",
            "password",
            "password2",
        )

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.pop("password2")

        if password != password2:
            raise serializers.ValidationError({"password": "password did not match"})

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if not email and not password:
            raise serializers.ValidationError({"message": "Please provide email and password"})

        user = authenticate(request=self.context.get("request"), email=email, password=password)
        if not user:
            raise serializers.ValidationError({"message": "Invalid Credentials"})

        attrs["user"] = user
        return attrs


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "phone_number",
            "first_name",
            "last_name",
            "is_vendor",
        )


class EditProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "phone_number", "first_name", "last_name", "is_vendor")
        read_only_fields = ("email",)
        extra_kwargs = {
            "phone_number": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
            "is_vendor": {"required": True},
        }

    def update(self, instance, validated_data):
        instance.phone_number = validated_data.get("phone_number", instance.phone_number)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.is_vendor = validated_data.get("is_vendor", instance.is_vendor)

        instance.save()
        return instance

    def validate_phone_number(self, value):
        user_qs = User.objects.filter(phone_number=value)
        if self.instance:
            user_qs = user_qs.exclude(email=self.instance.email)
        if user_qs.exists():
            raise serializers.ValidationError("This phone number is already in use.")
        return value


class ChangePasswordSeralizer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password1 = serializers.CharField(write_only=True, required=True)
    new_password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("old_password", "new_password1", "new_password2")

    def validate(self, attrs):
        password1 = attrs.get("new_password1")
        password2 = attrs.get("new_password2")

        if password1 != password2:
            raise serializers.ValidationError({"password": "password did not match"})

        return attrs

    def validate_old_password(self, value):
        if not self.instance.check_password(value):
            raise serializers.ValidationError({"old_password": "old_password didn't match!"})

        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data.get("new_password2"))
        instance.save()

        return instance


class ResetPasswordSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("password1", "password2")

    def validate(self, attrs):
        password1 = attrs.get("password1")
        password2 = attrs.get("password2")

        if password1 != password2:
            raise serializers.ValidationError({"password": "password did not match"})

        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data.get("password1"))
        instance.save()
        return instance
