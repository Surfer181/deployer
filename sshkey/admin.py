# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import UserDefaultSSHkey, UserKey

admin.site.register(UserKey)
admin.site.register(UserDefaultSSHkey)
