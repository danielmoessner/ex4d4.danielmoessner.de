from django.urls import path
from . import views


app_name = 'gelbeseiten'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('fetch', views.FetchView.as_view(), name='fetch'),
    path('data', views.DataView.as_view(), name='data'),
    path('download', views.DownloadView.as_view(), name='download'),
    path('fetch/<pk>', views.FetchDetailView.as_view(), name='fetch_detail'),
    path('data/<pk>', views.DataDetailView.as_view(), name='data_detail')
]
