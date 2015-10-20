from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from . import models
from . import forms
from .mixins import ODiscussionMixin, SimditorMixin


class TopicList(ODiscussionMixin, ListView):
    context_object_name = 'topics'
    template_name = 'oh_discussion/topic_list.html'
    paginate_by = 50
    _node = None

    def get_queryset(self):
        queryset = models.OTopic.objects.filter(is_visible=True)
        if 'pk' in self.kwargs:
            try:
                node = models.ONode.objects.get(pk=self.kwargs['pk'])
                self._node = node
                queryset = queryset.filter(node=node)
            except models.ONode.DoesNotExist:
                raise Http404
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_node'] = self._node
        return context


class Topic(ODiscussionMixin, DetailView):
    context_object_name = 'topic'
    template_name = 'oh_discussion/topic_detail.html'

    def get_queryset(self):
        return models.OTopic.objects.filter(is_visible=True)

    def get_object(self, queryset=None):
        topic = super().get_object(queryset)
        topic.clicks += 1
        topic.save(update_fields=['clicks'])
        return topic


class TopicCreate(ODiscussionMixin, SimditorMixin, CreateView):
    model = models.OTopic
    form_class = forms.TopicCreateForm
    template_name = 'oh_discussion/topic_create.html'

    def form_valid(self, form):
        topic = form.save(commit=False)
        topic.author = self.request.user
        topic.save()
        return HttpResponseRedirect(topic.get_absolute_url())


class TopicUpdate(ODiscussionMixin, SimditorMixin, UpdateView):
    model = models.OTopic
    form_class = forms.TopicUpdateForm
    template_name = 'oh_discussion/topic_update.html'

    def get(self, request, *args, **kwargs):
        topic = self.get_object()
        if topic.author == request.user:
            self.success_url = topic.get_absolute_url()
            return super().get(request, *args, **kwargs)
        else:
            raise PermissionDenied
