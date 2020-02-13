from django.views.decorators.csrf import csrf_exempt
from django.urls import path

from . import views


app_name = 'postforms'
urlpatterns = [
    path('kuesgutachterde/kostenvoranschlag',
         csrf_exempt(views.KuesGutachterDeKostenvoranschlag.as_view()),
         name='kuesgutachterde_kostenvoranschlag'),
    path('tortugawebdesignde/kontakt',
         csrf_exempt(views.TortugaWebdesignDeKontakt.as_view()),
         name='tortugawebdesignde_kontakt'),
    path('pzmode/form',
         csrf_exempt(views.PzmodeForm.as_view()),
         name='pzmode_form'),
]
