from django.contrib import admin

from .models import Content, Feed, Source, Tag

admin.site.register(Tag)
admin.site.register(Source)
admin.site.register(Feed)
admin.site.register(Content)
