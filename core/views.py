from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from .forms import ProfileForm
from .models import Profile
from django.views import View
from django.views.generic import UpdateView, DetailView, DeleteView
from django.urls import reverse, reverse_lazy
from django.urls import reverse_lazy


@login_required
def home(request):
    return render(request, 'core/home.html')


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
            return redirect('password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'core/password.html', {'form': form})


class ProfileUpdateView(UpdateView):
    form_class = ProfileForm
    template_name_suffix = '_form'

    def get_object(self, queryset=None):
        obj, created = Profile.objects.get_or_create(user=self.request.user)
        return obj


class ProfileDetailsView(DetailView):
    template_name = 'core/details.html'

    def get_object(self):
        return get_object_or_404(Profile, pk=self.request.user.profile.pk)


class ProfileDeleteView(DeleteView):
    model = Profile
    success_url = reverse_lazy('home')

    def get_object(self):
        return get_object_or_404(Profile, pk=self.request.user.profile.pk)