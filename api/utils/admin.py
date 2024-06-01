from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.shortcuts import resolve_url
from django.utils.html import format_html


def get_admin_link(obj):
    assert obj is not None, (
        'obj is required'
    )
    return format_html(
        '<a href="{}">{}</a>',
        resolve_url(admin_urlname(obj._meta, 'change'), obj.id),
        obj
    )
