from django.conf import settings
from django.urls import re_path
from django.urls import path

from . import views

app_name = "core"
urlpatterns = [
    path('page/<slug:slug>', views.PageView.as_view(), name='page')
]


if settings.DEBUG:
    urlpatterns += [
        re_path(r'^(?!static).*(js|images|css|fonts).*$', views.StaticRedirectView.as_view(), name='static_redirect'),
        re_path(r'[a-z]*(/[a-z])*.html$', views.AnyHtmlView.as_view(), name='html_redirect')
    ]
