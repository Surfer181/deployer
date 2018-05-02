# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Robot, User


class RobotAdmin(admin.ModelAdmin):
    list_display = ('name', 'private_key_path')


admin.site.register(User)
admin.site.register(Robot, RobotAdmin)
