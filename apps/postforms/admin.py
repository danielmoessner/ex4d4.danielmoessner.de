from django.contrib import admin

from .models import CustomField, CustomForm, CustomFilter


admin.site.register(CustomForm)
admin.site.register(CustomField)
admin.site.register(CustomFilter)
