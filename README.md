# django-phoneuser
A Django app providing a Custom User model mapped to a user's phone number

## Features
* Custom user model with Phone number as username and supported authentication with One-Time passwords.
* Integration with Django rest-auth registration. 
* Integration with Twilio API for sending OTP.
* Added PhoneUser form and PhoneUser serializers.

## Installation and usage
Install by adding `'phoneuser'` to list of `INSTALLED_APPS` in `settings.py`

Make the following changes in settings.py

    AUTH_USER_MODEL = 'phoneuser.PhoneUser'
    ACCOUNT_USER_MODEL_USERNAME_FIELD = 'phone'

Register urls in your urls.py

    url(r'^user/', include('phoneuser.urls'))

Access using `YOURSERVER/user/register-form` or `YOURSERVER/user/register-rest`

## Using with Django rest-auth registration

    REST_AUTH_REGISTER_SERIALIZERS = {
            'REGISTER_SERIALIZER': 'phoneuser.serializers.RegisterSerializer',
    }

## Using OTP for login
Use this logic in your views to generate OTP for a registered phone number.
    from phoneuser.models import OTP
    
    # Generate an OTP for phone with length 4
    otp = OTP.generate_otp(phone, 4)

Add the following to your `settings.py` to use the custom OTP for logging in. The ModelBackend is needed if you want to continue using password based authentication.
    
    AUTHENTICATION_BACKENDS = [
        'phoneuser.backends.OTPBackend',
        'django.contrib.auth.backends.ModelBackend',
    ]

## Usage with django-rest-framework-jwt
You will need to use a custom Payload handler, so add it your JWT_AUTH in `settings.py`

    JWT_AUTH += {
        'JWT_PAYLOAD_HANDLER': 'phoneuser.serializers.jwt_payload_handler'
    }

## Using Twilio API to send messages
Add the following details to your `settings.py`
    
    TWILIO_SID = "YOUR SID HERE"
    TWILIO_TOKEN = "YOUR TOKEN HERE"
    TWILIO_PHONE = "YOUR TWILIO NUMBER"

Now you can send messages using
 
    from phoneuser.models import OTP
    from twilio import TwilioRestException

    try:
        OTP.send_msg_twilio(phone, "Your Msg with OTP here")
    except TwilioRestException as e:
        print(e)
        
