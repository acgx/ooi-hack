import uuid

from django import forms
from django.core.mail import send_mail
from captcha.fields import CaptchaField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import OUser, OUserEmailVerification


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20, min_length=2, label='用户名',
                               help_text='用户名可由英文字母、数字、汉字或假名组成，长度不超过20')
    email = forms.EmailField(max_length=80, min_length=6, label='DMM登录邮箱',
                             help_text='该邮箱为您登录DMM时所使用的邮箱，用于绑定OOI社区用户和您的舰娘账号')
    password = forms.CharField(max_length=20, min_length=8, label='密码', widget=forms.PasswordInput,
                               help_text='该密码用于登录OOI社区,至少要包含8个字符，请不要使用和DMM账号一样的密码')
    confirm_password = forms.CharField(max_length=20, min_length=8, label='重复密码', widget=forms.PasswordInput)
    captcha = CaptchaField(label='认证码')

    error_messages = {
        'duplicate_username': '用户名已被使用',
        'duplicate_email': '电子邮件已被使用',
        'password_mismatch': '两次输入的密码不匹配',
    }

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            OUser.objects.get(username=username)
        except OUser.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            OUser.objects.get(email=email)
        except OUser.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages['duplicate_email'])

    def clean_confirmed_password(self):
        password = self.cleaned_data['password']
        confirmed_password = self.cleaned_data['confirmed_password']
        if password == confirmed_password:
            return confirmed_password
        else:
            raise forms.ValidationError(self.error_messages['password_mismatch'])

    def create_user(self):
        user = OUser.objects.create_user(username=self.cleaned_data['username'],
                                         email=self.cleaned_data['email'],
                                         password=self.cleaned_data['password'])
        user.is_active = False
        user.save()
        verfication = OUserEmailVerification.objects.create(user=user, code=uuid.uuid4().hex)
        mail_subject = 'OOI社区用户邮箱验证'
        mail_body = '%s，您好！\n感谢您注册成为OOI社区用户，请用下面的链接激活您的账号：\n\n' + \
                    'https://hack.ooi.moe/user/verify/%s\n\n本邮件由系统自动发送，请勿回复'
        mail_from = 'webmaster@ooi.moe'
        mail_to = [user.email, ]
        send_mail(mail_subject, mail_body % (user.username, verfication.code), mail_from, mail_to)

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_method = 'POST'
        helper.add_input(Submit('submit', '注册'))
        helper.form_class = 'form-horizontal'
        helper.label_class = 'col-md-2'
        helper.field_class = 'col-md-7'
        return helper
