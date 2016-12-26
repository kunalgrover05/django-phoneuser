from django.shortcuts import render

from phoneuser.forms import RegistrationForm


def user_register(request):
    """
    Simple View for user registration
    """

    if request.method == 'POST':
        formset = RegistrationForm(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
    else:
        formset = RegistrationForm()
    return render(request, 'registration.html', {'formset': formset})