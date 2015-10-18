from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.views.generic import View, TemplateView
from django.views.generic.edit import FormView
from django.template.response import TemplateResponse
from django.contrib.auth import authenticate, login

from . import models
from . import forms


class Register(FormView):
    form_class = forms.RegisterForm
    template_name = 'oh_users/register.html'
    success_url = reverse_lazy('user-register-done')

    def form_valid(self, form):
        form.create_user()
        return super().form_invalid(form)


class RegisterDone(TemplateView):
    template_name = 'message.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': '用户注册完成',
                        'message': '注册OOI社区用户成功，请前往您的邮箱查收邮件并验证您的账号。'})
        return context


class Verify(View):
    def get(self, *args, **kwargs):
        code = self.kwargs['code']
        try:
            verify = models.OUserEmailVerification.objects.get(code=code)
            user = verify.user
            user.is_active = True
            user.save()
            verify.delete()
            context = {'title': '邮箱验证成功',
                       'message': '您邮箱已验证成功，请返回首页登录OOI社区享受生活。'}
        except models.OUserEmailVerification.DoesNotExist:
            context = {'title': '邮箱验证失败',
                       'message': '在我们的数据库中找不到匹配的邮箱验证码。'}
        return TemplateResponse(self.request, 'success.html', context=context)


class Login(FormView):
    form_class = forms.LoginForm
    template_name = 'oh_users/login.html'
    success_url = settings.LOGIN_REDIRECT_URL

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        next_url = self.request.GET.get('next')
        if next_url:
            self.success_url = next_url
        return super().form_valid(form)
