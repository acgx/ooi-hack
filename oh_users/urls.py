from django.conf.urls import url
from django.contrib.auth.views import logout

from . import views

urlpatterns = [
    url(r'^register/$', views.Register.as_view(), name='user-register'),
    url(r'^verify/(?P<code>\w{32})/$', views.Verify.as_view(), name='user-verify'),
    url(r'^password/modify/$', views.PasswordModify.as_view(), name='user-password-modify'),
    url(r'^password/retrieve/$', views.PasswordRetrieve.as_view(), name='user-password-retrieve'),
    url(r'^password/reset/(?P<code>\w{32})/$', views.PasswordReset.as_view(), name='user-password-reset'),
    url(r'^login/$', views.Login.as_view(), name='user-login'),
    url(r'^logout/$', logout, {'template_name': 'oh_users/logout.html'}, name='user-logout'),
]
