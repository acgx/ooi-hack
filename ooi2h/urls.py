from django.conf.urls import include, url
from django.contrib import admin
import captcha.urls

import oh_pages.views
import oh_users.urls

urlpatterns = [
    url(r'^$', oh_pages.views.Index.as_view(), name='index'),
    url(r'^home$', oh_pages.views.Home.as_view(), name='home'),
    url(r'^user/', include(oh_users.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^captcha/', include(captcha.urls)),
]
