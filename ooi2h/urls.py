from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static

import avatar.urls
import captcha.urls

import oh_pages.views
import oh_users.urls
import oh_discussion.urls

urlpatterns = [
    url(r'^$', oh_pages.views.Index.as_view(), name='index'),
    url(r'^home/$', oh_pages.views.Home.as_view(), {'module': 'home'}, name='home'),
    url(r'^user/', include(oh_users.urls)),
    url(r'^discussion/', include(oh_discussion.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^avatar/', include(avatar.urls)),
    url(r'^captcha/', include(captcha.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
