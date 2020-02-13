from django.views.generic import FormView
from django.core.mail import EmailMessage
from django.http import JsonResponse

from .forms import KostenvoranschlagForm
from .forms import KontaktForm
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
