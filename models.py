from __future__ import unicode_literals

import datetime
import random
import string

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from phoneuser.managers import PhoneUserManager


class PhoneUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user which uses a phone number field as username
    """
    phone = PhoneNumberField(max_length=20, unique=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff status'), default=False)

    USERNAME_FIELD = 'phone'

    objects = PhoneUserManager()

    def __unicode__(self):
        return self.phone.__str__()


class OTP(models.Model):
    """
    Model containing OTP values for each user
    """
    created = models.DateTimeField(auto_now=True)
    otp = models.CharField(max_length=10)
    user = models.OneToOneField(PhoneUser)
    valid = models.BooleanField(default=True)

    @staticmethod
    def check_otp(user, otp):
        """Check if OTP is valid for a user"""
        try:
            otp_obj = OTP.objects.get(user=user)
        except ObjectDoesNotExist:
            return False

        utc_now = timezone.now()
        if not otp_obj.valid or otp_obj.created < utc_now - datetime.timedelta(seconds=600):
            return False

        # Invalidate token
        otp_obj.valid = False
        otp_obj.save()
        return otp_obj.otp == otp

    @staticmethod
    def generate_otp(number, otp_len):
        """Generate OTP for a phone number given length of OTP"""

        try:
            user = PhoneUser.objects.get(phone=number)
        except ObjectDoesNotExist:
            return None

        try:
            otp_model = OTP.objects.get(user=user)
        except ObjectDoesNotExist:
            otp_model = OTP(user=user)
        otp_model.otp = ''.join(random.choice(string.digits) for _ in range(otp_len))
        otp_model.valid = True
        otp_model.save()
        return otp_model.otp

    @staticmethod
    def send_msg_twilio(phone_no, msg):
        """
        Send a custom message to a given phone number using Twilio service
        Throws a TwilioRestException if the message couldn't be sent
        """
        from twilio.rest import TwilioRestClient
        client = TwilioRestClient(settings.TWILIO_SID, settings.TWILIO_TOKEN)

        message = client.messages.create(body=msg,
                                         to=phone_no,
                                         from_=settings.TWILIO_PHONE)