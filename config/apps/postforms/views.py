from django.views.generic.detail import SingleObjectMixin, DetailView
from django.views.generic.edit import ModelFormMixin, ProcessFormView
from django.views.generic import FormView
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django import forms
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


from .models import CustomForm
from .forms import KostenvoranschlagForm, KontaktForm, DynamicForm
from .forms import PzmodeForm as FormsPzmodeForm

import mimetypes
import logging

logger = logging.getLogger('postman')


class KuesGutachterDeKostenvoranschlag(FormView):
    template_name = 'postforms/kuesgutachterde_kostenvoranschlag.html'
    form_class = KostenvoranschlagForm

    def form_invalid(self, form):
        logger.error('postforms:kuesgutachterde:kostenvoranschlag: {}'.format(form.errors))
        return JsonResponse({'is_form_valid': False})

    def form_valid(self, form):
        subject = 'Neue Anfrage über die Webseite: kues-gutachter.de'
        message = ''
        for key, value in form.cleaned_data.items():
            message += '{}: {}\n'.format(key, value)
        attachments = []
        for i in range(1, 7):
            data = form.cleaned_data['bild{}'.format(i)]
            if data:
                attachments.append(data)
        recipient_list = ['projekte@tortuga-webdesign.de']
        email = EmailMessage(subject=subject, body=message, from_email='projekte@tortuga-webdesign.de',
                             to=recipient_list)
        for data in attachments:
            email.attach(data.name, data.file.read(), mimetypes.guess_type(data.name)[0])
        email.send()
        logger.error('postforms:kuesgutachterde:kostenvoranschlag: email sent')
        return JsonResponse({'is_form_valid': True})


class TortugaWebdesignDeKontakt(FormView):
    template_name = 'postforms/tortugawebdesignde_kontakt.html'
    form_class = KontaktForm

    def form_invalid(self, form):
        logger.error('postforms:tortugawebdesignde:kontakt: {}'.format(form.errors))
        return JsonResponse({'is_form_valid': False})

    def form_valid(self, form):
        subject = 'Neue Anfrage über die Webseite: tortuga-webdesign.de'
        message = ''
        for key, value in form.cleaned_data.items():
            message += '{}: {}\n'.format(key, value)
        recipient_list = ['kontakt@tortuga-webdesign.de']
        email = EmailMessage(subject=subject, body=message, from_email='projekte@tortuga-webdesign.de',
                             to=recipient_list)
        if '<a' in message or '</a>' in message:
            logger.error('postforms:tortugawebdesignde:kontakt: email denied because of links')
            return JsonResponse({'is_form_valid': False})
        email.send()
        logger.error('postforms:tortugawebdesignde:kontakt: email sent')
        return JsonResponse({'is_form_valid': True})


class PzmodeForm(FormView):
    template_name = 'postforms/pzmode_form.html'
    form_class = FormsPzmodeForm

    def form_invalid(self, form):
        logger.error('postforms:pzmode:form: {}'.format(form.errors))
        return JsonResponse({'is_form_valid': False})

    def form_valid(self, form):
        subject = 'Neue Anfrage über die Webseite: pz-mo.de'
        message = ''
        for key, value in form.cleaned_data.items():
            message += '{}: {}\n'.format(key, value)
        recipient_list = ['projekte@tortuga-webdesign.de']
        email = EmailMessage(subject=subject, body=message, from_email='projekte@tortuga-webdesign.de',
                             to=recipient_list)
        email.send()
        logger.error('postforms:pzmode:form: email sent')
        return JsonResponse({'is_form_valid': True})


class CustomFormView(SingleObjectMixin, FormView):
    model = CustomForm
    template_name = 'postforms/dynamic_form.html'
    slug_url_kwarg = 'url'
    slug_field = 'url'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CustomFormView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_form_class(self):
        fields = {}
        for field in self.object.custom_fields.all():
            fields[field.name] = field.get_field()
        custom_form_class = type('dynamic_form', (DynamicForm,), fields)
        return custom_form_class

    def form_invalid(self, form):
        logger.error('postforms:{}: {}'.format(self.object.website, form.errors))
        return JsonResponse({'is_form_valid': False})

    def form_valid(self, form):
        subject = self.object.subject
        message = ''
        for key, value in form.cleaned_data.items():
            message += '{}: {}\n'.format(key, value)
        recipient_list = [self.object.recipient1]
        if self.object.recipient2:
            recipient_list += [self.object.recipient2]
        email = EmailMessage(subject=subject, body=message, from_email='projekte@tortuga-webdesign.de',
                             to=recipient_list)
        email.send()
        return JsonResponse({'is_form_valid': True})
