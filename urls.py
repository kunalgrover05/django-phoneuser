from django.conf.urls import url
from rest_auth.registration.views import RegisterView

from phoneuser.views import user_register

urlpatterns = [
    url(r'^register-form$', user_register, name='register'),
    url(r'^register-rest', RegisterView.as_view(), name='register_rest')
]