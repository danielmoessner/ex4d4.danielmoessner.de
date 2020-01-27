from django.contrib import admin

from .models import BtvClub
from .models import ScrapeFile
from .models import ScrapeRun
from .models import GelbeSeitenCompany


admin.site.register(BtvClub)
admin.site.register(ScrapeFile)
admin.site.register(ScrapeRun)
admin.site.register(GelbeSeitenCompany)
