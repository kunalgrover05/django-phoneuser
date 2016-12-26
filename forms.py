from django.forms import CharField, forms

from phoneuser.models import PhoneUser


class RegistrationForm(forms.Form):
    """
    Custom registration form for PhoneUser model
    """
    phone = CharField(required=True)
    password1 = CharField(required=False)
    password2 = CharField(required=False)

    def clean(self):
        data = self.cleaned_data
        phone = data.get('phone', None)
        if len(PhoneUser.objects.filter(phone=phone).all()) > 0:
            self._errors['phone'] = ["Phone number already in use"]
            del data['phone']

        if data.get('password1', None) != data.get('password2', None):
            self._errors["password1"] = ["Password do not match"]
            del data['password1']

        return data

    def save(self, **kwargs):
        user = PhoneUser(phone=self.cleaned_data['phone'])
        password = self.cleaned_data.get('password1', None)
        if password:
            user.set_password(self.cleaned_data["password1"])
        else:
            user.set_unusable_password()

        user.save()
        return user
