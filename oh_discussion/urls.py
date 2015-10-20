from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.TopicList.as_view(), name='discussion-index'),
    url(r'^node/(?P<pk>\d+)/$', views.TopicList.as_view(), name='discussion-node'),
    url(r'^topic/(?P<pk>\d+)/$', views.Topic.as_view(), name='discussion-topic'),
    url(r'^topic/create/$', views.TopicCreate.as_view(), name='discussion-topic-create'),
    url(r'^topic/update/(?P<pk>\d+)/$', views.TopicUpdate.as_view(), name='discussion-topic-update'),
    url(r'^reply/create/$', views.ReplyCreate.as_view(), name='discussion-reply-create'),
]
