# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls')),

    url(r'^api/v1/account/', include('account.urls', namespace='account')),
]
