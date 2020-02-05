from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import RedirectView
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

from ex4d4.core.models import Permit
from ex4d4.core.views import WebsiteContextMixin


class IndexView(RedirectView):
    url = reverse_lazy('users:signin')

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('content:main'))
        return super().get(request, *args, **kwargs)


class MainView(LoginRequiredMixin, WebsiteContextMixin, TemplateView):
    template_name = 'content/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permits'] = {}
        for row in Permit.objects.values('username', 'app'):
            if not row['app'] in context['permits']:
                context['permits'][row['app']] = []
            context['permits'][row['app']].append(row['username'])
        return context
