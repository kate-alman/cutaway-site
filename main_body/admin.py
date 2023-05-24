from django.contrib import admin

from accounts.models import *
from main_body.models import *
from services.models import *


class NewsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "time_create", "image", "is_published")
    list_display_links = ("id", "title")
    search_fields = ("title", "content")
    list_editable = ("is_published",)
    list_filter = ("is_published", "time_create")
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(News)
admin.site.register(Tag)
admin.site.register(Weather)
admin.site.register(Menu)
admin.site.register(Profile)
admin.site.register(FavoriteRelationship)
admin.site.register(PageVisits)
