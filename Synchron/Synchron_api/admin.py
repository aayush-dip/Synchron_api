from django.contrib import admin
from Synchron_api.models import Profile, Team, MemberAndRemarks, StandupCard

# Register your models here.
admin.site.register([Profile, Team, MemberAndRemarks, StandupCard])