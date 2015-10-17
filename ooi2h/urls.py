from django.conf.urls import include, url
from django.contrib import admin

import oh_pages.views

urlpatterns = [
    url(r'^$', oh_pages.views.Index.as_view(), name='index'),
    url(r'^admin/', include(admin.site.urls)),
]
