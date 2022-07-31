from django.contrib import admin

from .models import Tag, Website, Report

admin.site.register(Tag)
admin.site.register(Website)
admin.site.register(Report)