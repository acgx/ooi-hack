from django.core.urlresolvers import reverse_lazy
from django.views.generic import View, TemplateView
from django.template.response import TemplateResponse
from django.shortcuts import redirect

from oh_users.mixins import LoginRequiredMixin


class Index(View):
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            return redirect(reverse_lazy('home'))
        else:
            return TemplateResponse(self.request, 'oh_pages/index.html')


class Home(LoginRequiredMixin, TemplateView):
    template_name = 'oh_pages/home.html'
