#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from pastebin.models import Geometry


class GeometryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'date', 'file', 'sourcefile']


admin.site.register(Geometry, GeometryAdmin)
