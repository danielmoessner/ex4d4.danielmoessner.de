from django.views.decorators.csrf import csrf_exempt
from django.urls import path

from . import views


app_name = 'postforms'
urlpatterns = [
    path('<slug:url>/', views.CustomFormView.as_view(), name='custom_form'),
    path('pzmode/form',
         csrf_exempt(views.PzmodeForm.as_view()),
         name='pzmode_form'),
]
