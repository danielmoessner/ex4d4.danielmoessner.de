from django.views.decorators.csrf import csrf_exempt
from django.views.generic.detail import SingleObjectMixin
from django.utils.decorators import method_decorator
from django.views.generic import FormView
from django.core.mail import EmailMessage
from django.http import JsonResponse

from .models import CustomForm
from .forms import DynamicForm

import logging

logger = logging.getLogger('postman')


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
            fields[field.name].required = False
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
