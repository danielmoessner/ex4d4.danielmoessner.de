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
]
