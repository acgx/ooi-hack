from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.views.generic import View
from django.views.generic.edit import FormView
from django.template.response import TemplateResponse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login

from . import models
from . import forms
from .mixins import LoginRequiredMixin


class Register(FormView):
    form_class = forms.RegisterForm
    template_name = 'oh_users/register.html'
    success_url = reverse_lazy('user-register-done')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return TemplateResponse(request, 'warning.html',
                                    {'title': '用户注册错误',
                                     'message': '您已经是OOI社区的用户了，不需要再注册新的用户。'})
        else:
            return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        form.create_user()
        return TemplateResponse(self.request, 'success.html',
                                {'title': '用户注册完成',
                                 'message': '注册OOI社区用户成功，请前往您的邮箱查收邮件并验证您的账号。'})


class Verify(View):
    def get(self, *args, **kwargs):
        code = self.kwargs['code']
        try:
            verify = models.OUserEmailVerification.objects.get(code=code)
            user = verify.user
            user.is_active = True
            user.save()
            verify.delete()
            return TemplateResponse(self.request, 'success.html',
                                    {'title': '邮箱验证成功',
                                     'message': '您邮箱已验证成功，请返回首页登录OOI社区享受生活。'})
        except models.OUserEmailVerification.DoesNotExist:
            return TemplateResponse(self.request, 'warning.html',
                                    {'title': '邮箱验证失败',
                                     'message': '在我们的数据库中找不到匹配的邮箱验证码。'})


class Login(FormView):
    form_class = forms.LoginForm
    template_name = 'oh_users/login.html'
    success_url = settings.LOGIN_REDIRECT_URL

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            return super().get(request, *args, **kwargs)

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return self.success_url

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super().form_valid(form)


class PasswordModify(LoginRequiredMixin, FormView):
    form_class = forms.PasswordModifyForm
    template_name = 'oh_users/password_modify.html'
    success_url = settings.LOGIN_REDIRECT_URL

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        form.modify_password()
        return TemplateResponse(self.request, 'success.html',
                                {'title': '修改密码成功',
                                 'message': '您的密码已成功修改，请使用新密码重新登录。'})


class PasswordRetrieve(FormView):
    form_class = forms.PasswordRetrieveForm
    template_name = 'oh_users/password_retrieve.html'

    def form_valid(self, form):
        form.retrieve()
        return TemplateResponse(self.request, 'success.html',
                                {'title': '找回密码成功',
                                 'message': '指导您找回密码的邮件已发送到您的邮箱，请前往您的邮箱查收邮件并按提示进行操作。'})


class PasswordReset(FormView):
    form_class = forms.PasswordResetForm
    template_name = 'oh_users/password_reset.html'

    def get(self, request, *args, **kwargs):
        code = self.kwargs['code']
        try:
            reset = models.OUserPasswordReset.objects.get(code=code)
            form = self.get_form()
            return TemplateResponse(request, self.template_name, {'username': reset.user.username, 'form': form})
        except models.OUserPasswordReset.DoesNotExist:
            return TemplateResponse(request, 'warning.html',
                                    {'title': '重置密码失败',
                                     'message': '在我们的数据库中找不到这个重置密码请求。'})

    def form_valid(self, form):
        code = self.kwargs['code']
        reset = models.OUserPasswordReset.objects.get(code=code)
        reset.user.set_password(form.cleaned_data['password'])
        reset.user.save()
        reset.delete()
        return TemplateResponse(self.request, 'success.html',
                                {'title': '重置密码成功',
                                 'message': '您的密码已成功重置，请使用新密码重新登录。'})
