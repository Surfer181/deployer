# -*- coding: utf-8 -*-
from django.conf.urls import url, include


__all__ = ["addon_urls"]


addon_urls = [
    url(r'^api/v1/sshkey/', include('addons.sshkey.urls', namespace='sshkey')),
]
