"""qcqualitycontrol URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.conf.urls import include
from django.contrib import admin
from django.conf import settings
from django.urls import path


urlpatterns = [
    path('users/', include('ex4d4.users.urls')),
    path('fpioli/', include('ex4d4.fpioli.urls')),
    path('postforms/', include('ex4d4.postforms.urls')),
    path('gelbeseiten/', include('ex4d4.gelbeseiten.urls')),
    path('', include('ex4d4.content.urls')),
    path('', include('ex4d4.core.urls')),
    path('admin/', admin.site.urls),
]


handler400 = "ex4d4.core.views.error_400_view"
handler403 = "ex4d4.core.views.error_403_view"
handler404 = "ex4d4.core.views.error_404_view"
handler500 = "ex4d4.core.views.error_500_view"


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls)), ]
