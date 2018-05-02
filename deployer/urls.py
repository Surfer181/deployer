# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
# from rest_framework.documentation import include_docs_urls


from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Deployer API')


if settings.DEBUG:
    urlpatterns_debug = [
        # url(r'^docs/', include_docs_urls(
        #     title='Deployer Documents', public=False,
        #     authentication_classes=[], permission_classes=[]
        # )),
        url(r'^docs/', schema_view),
        url(r'^admin/', admin.site.urls),
        url(r'^api-auth/', include('rest_framework.urls')),
    ]
else:
    urlpatterns_debug = []

urlpatterns = urlpatterns_debug + [
    url(r'^api/v1/account/', include('account.urls', namespace='account')),
    url(r'^api/v1/sshkey/', include('sshkey.urls', namespace='sshkey')),
]
