from oh_users.mixins import LoginRequiredMixin
from .models import ONode


class ODiscussionMixin(LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = 'discussion'
        context['nodes'] = ONode.objects.all()
        return context


class SimditorMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['extra_css'] = ('css/simditor.css', )
        context['extra_js'] = ('js/simditor/module.min.js',
                               'js/simditor/hotkeys.min.js',
                               'js/simditor/simditor.min.js',
                               'js/simditor/settings.js',
                               )
        return context
