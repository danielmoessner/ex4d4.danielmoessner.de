from django.contrib import admin

from .models import BtvClub
from .models import ScrapeFile
from .models import ScrapeRun


admin.site.register(BtvClub)
admin.site.register(ScrapeFile)
admin.site.register(ScrapeRun)
