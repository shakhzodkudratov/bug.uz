from django.contrib import admin
from django.contrib.admin import register

from core.models import Url, UrlStat


@register(Url)
class UrlAdmin(admin.ModelAdmin):
    readonly_fields = ['private_name', 'name']
    pass


@register(UrlStat)
class UrlStatAdmin(admin.ModelAdmin):
    pass
