from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProfileForm, UserForm
from .models import Profile
from django.views import View
from django.views.generic import DetailView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from social_django.models import UserSocialAuth


@login_required
def home(request):
    return render(request, 'core/home.html')

@login_required
def settings(request):
    user = request.user

    try:
        github_login = user.social_auth.get(provider='github')
    except UserSocialAuth.DoesNotExist:
        github_login = None

    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    return render(request, 'core/settings.html', {
        'github_login': github_login,
        'can_disconnect': can_disconnect
    })

@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'core/password.html', {'form': form})


class ProfileDetailsView(LoginRequiredMixin, DetailView):
    login_url = 'login'
    redirect_field_name = 'details'
    template_name = 'core/details.html'

    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.pk)


class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    redirect_field_name = 'details'
    model = Profile
    success_url = reverse_lazy('home')

    def get_object(self):
        return get_object_or_404(Profile, pk=self.request.user.profile.pk)


class ProfileUpdateView(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'update_profile'

    def get(self, request):
        profile, _ = Profile.objects.get_or_create(user=request.user)
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)
        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, 'core/profile_form.html', context)

    def post(self, request):
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES,
                                   instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Success')
            return redirect('details')
        else:
            context = {
                'user_form': user_form,
                'profile_form': profile_form
            }
            return render(request, 'core/profile_form.html', context)
