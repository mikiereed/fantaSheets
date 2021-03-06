from .forms import UserRegistrationForm, UserEditForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            messages.success(
                request, 'Registration Successful, Please Login')
            return render(request,
                          'registration/login.html',
                          {'new_user': new_user})
        else:
            messages.error(request, user_form.errors)
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'registration/register.html',
                  {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Account Updated Successfully')
        else:
            messages.error(request, user_form.errors)
    else:
        user_form = UserEditForm(instance=request.user)
    return render(request,
                  'registration/edit.html',
                  {
                      'user_form': user_form,
                  })
