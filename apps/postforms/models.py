from django.db import models
from django import forms


class CustomFilter(models.Model):
    description = models.CharField(max_length=300)
    custom_filter = models.CharField(max_length=100)

    def __str__(self):
        return self.description

    def is_text_safe(self, text):
        return self.custom_filter in text


class CustomForm(models.Model):
    subject = models.CharField(max_length=500)
    website = models.CharField(max_length=200)
    url = models.SlugField(unique=True)
    recipient1 = models.EmailField(default='projekte@tortuga-webdesign.de')
    recipient2 = models.EmailField(blank=True, null=True)
    custom_filter = models.ManyToManyField(CustomFilter, related_name='custom_forms')

    def __str__(self):
        return self.url


class CustomField(models.Model):
    name = models.SlugField()
    form = models.ForeignKey(CustomForm, related_name='custom_fields', on_delete=models.CASCADE)
    TYPE_CHOICES = (
        ('EMAIL', 'E-Mail'),
        ('DATETIME-LOCAL', 'Date and Time'),
        ('NUMBER', 'Number'),
        ('TEXT', 'Text'),
        ('URL', 'Url'),
        ('TEXTAREA', 'Textarea')
    )
    field_type = models.CharField(choices=TYPE_CHOICES, max_length=100)

    def __str__(self):
        return '{} - {}'.format(self.form, self.name)

    def get_field(self):
        if self.field_type == 'EMAIL':
            return forms.EmailField()
        elif self.field_type == 'DATETIME-LOCAL':
            return forms.DateTimeField(
                widget=forms.DateTimeInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
                input_formats=["%Y-%m-%dT%H:%M"])
        elif self.field_type == 'NUMBER':
            return forms.IntegerField()
        elif self.field_type == 'TEXT':
            return forms.CharField()
        elif self.field_type == 'URL':
            return forms.URLField()
        elif self.field_type == 'TEXTAREA':
            return forms.CharField(widget=forms.Textarea)
        else:
            return forms.CharField()
