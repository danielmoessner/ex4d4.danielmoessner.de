from django.urls import path
from . import views


app_name = 'fpioli'
urlpatterns = [
    # btv-tool
    path('btv-tool/', views.BtvToolView.as_view(), name='btvtool'),
    path('btv-tool/fetch/', views.BtvToolFetchView.as_view(), name='btvtool_fetch'),
    path('btv-tool/download/', views.BtvToolDownloadView.as_view(), name='btvtool_download'),
    path('btv-tool/clubs/', views.BtvToolClubsView.as_view(), name='btvtool_clubs'),
    path('btv-tool/messages/', views.BtvToolMessagesView.as_view(), name='btvtool_messages'),
    path('btv-tool/message/<pk>', views.BtvToolMessageView.as_view(), name='btvtool_message'),
    path('btv-tool/club/<pk>', views.BtvToolClubView.as_view(), name='btvtool_club'),
    # gelbe-seiten-tool
    path('gelbe-seiten-tool', views.GelbeSeitenToolView.as_view(), name='gelbeseitentool'),
    path('gelbe-seiten-tool/fetch', views.GelbeSeitenToolFetchView.as_view(), name='gelbeseitentool_fetch'),
    path('gelbe-seiten-tool/messages', views.GelbeSeitenToolMessagesView.as_view(), name='gelbeseitentool_messages'),
    path('gelbe-seiten-tool/companies', views.GelbeSeitenToolCompaniesView.as_view(), name='gelbeseitentool_companies'),
    path('gelbe-seiten-tool/download', views.GelbeSeitenToolDownloadView.as_view(), name='gelbeseitentool_download'),
    path('gelbe-seiten-tool/message/<pk>', views.GelbeSeitenToolMessageView.as_view(), name='gelbeseitentool_message'),
    path('gelbe-seiten-tool/company/<pk>', views.GelbeSeitenToolCompanyView.as_view(), name='gelbeseitentool_company'),
]
