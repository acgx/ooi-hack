import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = os.environ.get('OH_SECRET', 'DEFAULT COOKIE SECRET FOR DEVELOPING')
DEBUG = bool(os.environ.get('OH_DEBUG', False))
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'avatar',
    'captcha',
    'crispy_forms',
    'mptt',
    'oh_pages',
    'oh_users',
    'oh_discussion',
)
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)
APPEND_SLASH = True
ROOT_URLCONF = 'ooi2h.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
WSGI_APPLICATION = 'ooi2h.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': os.environ.get('OH_DB_HOST', '127.0.0.1'),
        'PORT': os.environ.get('OH_DB_PORT', '3306'),
        'NAME': os.environ.get('OH_DB_NAME', 'ooihack'),
        'USER': os.environ.get('OH_DB_USER', 'ooihack'),
        'PASSWORD': os.environ.get('OH_DB_PASSWORD', 'ooihack'),
        'OPTIONS': {
            'autocommit': True,
        },
    },
}

LANGUAGE_CODE = 'zh-cn'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/s/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/m/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
CRISPY_TEMPLATE_PACK = 'bootstrap3'

AUTH_USER_MODEL = 'oh_users.OUser'
LOGIN_URL = '/user/login/'
LOGIN_REDIRECT_URL = '/home/'
AVATAR_GRAVATAR_BACKUP = False
AVATAR_DEFAULT_URL = 'img/avatar.png'

EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
EMAIL_HOST = os.environ.get('OH_MAIL_HOST')
EMAIL_PORT = int(os.environ.get('OH_MAIL_PORT', 465))
EMAIL_HOST_USER = os.environ.get('OH_MAIL_USER', 'webmaster@ooi.moe')
EMAIL_HOST_PASSWORD = os.environ.get('OH_MAIL_PASSWORD')
