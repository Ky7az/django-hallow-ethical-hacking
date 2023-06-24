from django.contrib import admin

from .models import Report, Tag, Website

admin.site.register(Tag)
admin.site.register(Website)
admin.site.register(Report)