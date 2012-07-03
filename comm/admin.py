# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Comm

class CommAdmin(admin.ModelAdmin):
    list_display = ('user_a', 'user_b', 'description', 'point_a', 'point_b')

admin.site.register(Comm, CommAdmin)
