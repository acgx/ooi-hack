import re

from django.conf import settings
from django.core import validators
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class OUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(username=username, email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser,
                          register_time=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password, email, **extra_fields):
        return self._create_user(username, email, password, False, False, **extra_fields)

    def create_superuser(self, username, password, email, **extra_fields):
        return self._create_user(username, email, password, True, True, **extra_fields)


class OUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('用户名', max_length=20, unique=True, db_index=True,
                                help_text='用户名可由英文字母、数字、汉字或假名组成，长度不超过20',
                                validators=[
                                    validators.RegexValidator(re.compile('^[\\w\\d\u2e80-\u9fff]{2,}$'),
                                                              '请输入至少两个字母、数字、汉字或假名', 'invalid')
                                ])
    email = models.EmailField('电子邮件', max_length=254, unique=True,
                              help_text='电子邮件必须真实有效，并且与舰娘游戏的账号对应')
    is_active = models.BooleanField('用户是否可用', default=True)
    is_staff = models.BooleanField('是否为管理用户', default=False)
    register_time = models.DateTimeField('用户注册时间', default=timezone.now)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = OUserManager()

    def get_full_name(self):
        full_name = '%s <%s>' % (self.username, self.email)
        return full_name

    def get_short_name(self):
        return self.username

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __str__(self):
        return self.get_full_name()


class OUserEmailVerification(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='email_verification')
    code = models.CharField('电子邮件验证代码', max_length=32)
    create_time = models.DateTimeField('电子邮件验证请求创建时间', default=timezone.now)

    class Meta:
        verbose_name = '电子邮件确认验证'
        verbose_name_plural = '电子邮件验证请求'

    def __str__(self):
        return '%s 的电子邮件验证请求' % self.user.get_full_name()


class OUserPasswordReset(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='password_reset')
    code = models.CharField('密码重置代码', max_length=32)
    create_time = models.DateTimeField('密码重置请求创建时间', default=timezone.now)

    class Meta:
        verbose_name = '密码重置请求'
        verbose_name_plural = '密码重置请求'

    def __str__(self):
        return '%s 的密码重置请求' % self.user.get_full_name()
