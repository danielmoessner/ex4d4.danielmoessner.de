from django.urls import path
from . import views


app_name = 'users'
urlpatterns = [
    # views
    path('login/', views.SignInView.as_view(), name='signin'),
    path('logout/', views.SignOutView.as_view(), name='signout'),
    path('password-change/', views.CustomPasswordChangeView.as_view(), name='passwordchange'),
    path('password-change-done/', views.CustomPasswordChangeDoneView.as_view(), name='passwordchangedone'),
]
