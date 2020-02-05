from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models.functions import Length
from django.views.generic import TemplateView
from django.views.generic import FormView
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from ex4d4.core.views import WebsiteContextMixin
<<<<<<< HEAD
from .models import GelbeSeitenCompany
from .models import ScrapeFile
from .models import BtvClub
from .models import ScrapeRun
from .forms import GelbeSeitenForm
=======
from .models import ScrapeFile
from .models import BtvClub
from .models import ScrapeRun
>>>>>>> 3a235621e8a019edead4fe74e2c13b2cef1c748d
from .forms import StartEndForm

from background_task.models import Task


class FPioliTestMixin(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_superuser or self.request.user.username == 'f.pioli':
            return True
        return False


class BtvToolView(FPioliTestMixin, WebsiteContextMixin, TemplateView):
    template_name = 'fpioli/btvtool.html'


class BtvToolClubsView(FPioliTestMixin, WebsiteContextMixin, TemplateView):
    template_name = 'fpioli/btvtool_clubs.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clubs'] = BtvClub.objects.order_by('number')
        return context


class BtvToolMessagesView(FPioliTestMixin, WebsiteContextMixin, TemplateView):
    template_name = 'fpioli/btvtool_messages.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['runs'] = ScrapeRun.objects.filter(tool='BTV').order_by('-created_at')
        return context


class BtvToolMessageView(FPioliTestMixin, WebsiteContextMixin, TemplateView):
    template_name = 'fpioli/btvtool_message.html'
    model = ScrapeRun

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['btvrun'] = get_object_or_404(ScrapeRun, pk=kwargs['pk'])
        return context


class BtvToolClubView(FPioliTestMixin, WebsiteContextMixin, TemplateView):
    template_name = 'fpioli/btvtool_club.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['club'] = get_object_or_404(BtvClub, pk=kwargs['pk'])
        return context


class BtvToolFetchView(FPioliTestMixin, FormView, WebsiteContextMixin, TemplateView):
    template_name = 'fpioli/btvtool_fetch.html'
    form_class = StartEndForm
    success_url = reverse_lazy('fpioli:btvtool_fetch')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects\
            .filter(queue='scrape_queue')\
            .annotate(text_len=Length('last_error'))\
            .filter(text_len__lt=10)
        context['runningtasks'] = context['tasks'].exclude(locked_by=None)
        context['failedtasks'] = Task.objects.annotate(text_len=Length('last_error')).filter(text_len__gte=10)
        return context

    def form_valid(self, form):
        start = int(form.cleaned_data['first_number'])
        end = int(form.cleaned_data['last_number'])
        BtvClub.scrape(start, end)
        return super().form_valid(form)


class BtvToolDownloadView(FPioliTestMixin, FormView, WebsiteContextMixin, TemplateView):
    template_name = 'fpioli/btvtool_download.html'
    form_class = StartEndForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['files'] = ScrapeFile.objects.filter(tool='BTV').order_by('-created_at')[:10]
        return context

    def form_valid(self, form):
        start = int(form.data['first_number'])
        end = int(form.data['last_number'])
        BtvClub.to_csv(start, end)
        BtvClub.to_xlsx(start, end)
        return HttpResponseRedirect(reverse_lazy('fpioli:btvtool_download'))
