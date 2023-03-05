from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, resolve_url, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, UpdateView
from .froms import RegistrationForm, LoginForm, ProfileForm, ChangePasswordForm
from .models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin


class LoginView(FormView):
    template_name = 'account/login.html'
    form_class = LoginForm

    def form_valid(self, form):
        user = authenticate(self.request, **form.cleaned_data)
        if user is not None:
            login(self.request, user)

            messages.success(self.request, _('Xush kelibsiz {}').format(user.get_full_name()))
            return redirect('main:index')

        form.add_error('password', _('Login yoki parol notogri'))
        return self.form_invalid(form)


class RegistrationView(CreateView):
    template_name = 'account/registration.html'
    model = User
    form_class = RegistrationForm

    def form_valid(self, form):
        form.instance.set_password(form.cleaned_data.get('password'))
        messages.success(self.request, _('Muvofaqiyatli royxatdan otdingiz.'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('account:login')


class ProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'account/profile.html'
    model = User
    form_class = ProfileForm

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, _('Muvofaqiyatli saqlandi'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('account:profile')


class ChangePasswordView(LoginRequiredMixin, FormView):
    template_name = 'account/change-password.html'
    form_class = ChangePasswordForm

    def form_valid(self, form):
        self.request.user.set_password(form.cleaned_data.get('new_password'))
        self.request.user.save()

        messages.success(self.request, _("Parol muvofiqiyatli ozgartirildi"))
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse_lazy('account:change-password')


@login_required
def logout_view(request):
    messages.success(request, _('Kelib turing {}').format(request.user.get_full_name()))

    logout(request)

    return redirect('main:index')


