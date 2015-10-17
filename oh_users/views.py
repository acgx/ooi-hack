from django.core.urlresolvers import reverse_lazy
from django.views.generic import View, TemplateView
from django.views.generic.edit import FormView
from django.shortcuts import render

from . import models
from . import forms


class Register(FormView):
    form_class = forms.RegisterForm
    template_name = 'oh_users/register.html'
    success_url = reverse_lazy('user-register-done')

    def form_valid(self, form):
        form.create_user()


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
        return render(self.request, 'success.html', context=context)
