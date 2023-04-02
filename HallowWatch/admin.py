from django.contrib import admin

from .models import Tag, Source, Feed, Content

admin.site.register(Tag)
admin.site.register(Source)
admin.site.register(Feed)
admin.site.register(Content)