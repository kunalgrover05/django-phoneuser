from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from phoneuser.forms import RegistrationForm


class RegisterSerializer(serializers.Serializer):
    """
    Custom serializer for Rest framework for user registration.
    Uses RegistrationForm for validations
    """
    phone = serializers.CharField(required=True)
    password1 = serializers.CharField(required=False, write_only=True)
    password2 = serializers.CharField(required=False, write_only=True)

    def create(self, validated_data):
        super(RegisterSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        super(RegisterSerializer, self).update(instance, validated_data)

    def validate(self, data):
        self.form = RegistrationForm(data)
        if self.form.errors:
            raise ValidationError(self.form.errors)
        return self.form.cleaned_data

    def save(self, request):
        return self.form.save()


def jwt_payload_handler(user):
    """
    Custom payload handler for JWT tokens with PhoneUser model
    """
    from rest_framework_jwt.compat import get_username
    from rest_framework_jwt.settings import api_settings
    from calendar import timegm
    from datetime import datetime

    username = get_username(user)

    payload = {
        'user_id': user.pk,
        'username': str(username),
        'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA
    }

    # Include original issued at time for a brand new token,
    # to allow token refresh
    if api_settings.JWT_ALLOW_REFRESH:
        payload['orig_iat'] = timegm(
            datetime.utcnow().utctimetuple()
        )

    if api_settings.JWT_AUDIENCE is not None:
        payload['aud'] = api_settings.JWT_AUDIENCE

    if api_settings.JWT_ISSUER is not None:
        payload['iss'] = api_settings.JWT_ISSUER

    return payload