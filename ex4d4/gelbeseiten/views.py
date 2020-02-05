from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models.functions import Length
from django.views.generic import TemplateView
from django.views.generic import FormView
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from .models import Entry
from .models import File
from .models import Fetch
from .forms import GelbeSeitenForm

from background_task.models import Task


class TestMixin(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_superuser or self.request.user.username == 'f.pioli':
            return True
        return False


class IndexView(TestMixin, TemplateView):
    template_name = 'gelbeseiten_index.html'


class FetchView(TestMixin, FormView):
    template_name = 'gelbeseiten_fetch.html'
    form_class = GelbeSeitenForm
    success_url = reverse_lazy('gelbeseiten:fetch')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.filter(queue='gelbeseiten_queue').annotate(text_len=Length('last_error')).filter(text_len__lt=10)
        context['runningtasks'] = context['tasks'].exclude(locked_by=None)
        context['failedtasks'] = Task.objects.annotate(text_len=Length('last_error')).filter(text_len__gte=10)
        context['runs'] = Fetch.objects.order_by('-created_at')
        return context

    def form_valid(self, form):
        category = form.cleaned_data['category']
        location = form.cleaned_data['location']
        Entry.scrape(category, location)
        return super().form_valid(form)


class DownloadView(TestMixin, FormView):
    template_name = 'gelbeseiten_download.html'
    form_class = GelbeSeitenForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['files'] = File.objects.order_by('-created_at')[:10]
        return context

    def form_valid(self, form):
        category = form.cleaned_data['category']
        location = form.cleaned_data['location']
        Entry.to_csv(category, location)
        Entry.to_xlsx(category, location)
        return HttpResponseRedirect(reverse_lazy('gelbeseiten:download'))


class DataView(TestMixin, TemplateView):
    template_name = 'gelbeseiten_data.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['companies'] = Entry.objects.order_by('name')
        return context


class FetchDetailView(TestMixin, TemplateView):
    template_name = 'gelbeseiten_fetch_detail.html'
    model = Fetch

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['run'] = get_object_or_404(Fetch, pk=kwargs['pk'])
        return context


class DataDetailView(TestMixin, TemplateView):
    template_name = 'gelbeseiten_data_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = get_object_or_404(Entry, pk=kwargs['pk'])
        return context
