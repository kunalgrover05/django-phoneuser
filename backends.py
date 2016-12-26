from .models import OTP, PhoneUser


class OTPBackend(object):
    """
    Custom authentication backend to authenticate with OTP
    """
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = PhoneUser.objects.get(phone=kwargs.get('phone', None))
        except PhoneUser.DoesNotExist:
            return None

        # Login with OTP
        otp_valid = OTP.check_otp(user, password)
        if otp_valid:
            return user
        return None

    def get_user(self, user_id):
        try:
            return PhoneUser.objects.get(pk=user_id)
        except PhoneUser.DoesNotExist:
            return None

