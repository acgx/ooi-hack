from django.views.generic import View
from django.shortcuts import render


class Index(View):
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            pass
        else:
            return render(self.request, 'oh_pages/index.html')
