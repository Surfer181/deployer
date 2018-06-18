# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.conf.urls import url
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register(r'repo', views.SourceCodeRepoViewSet)
router.register(r'version', views.CodeVersionViewSet)
router.register(r'version-group', views.CodeVersionGroupViewSet)


urlpatterns = [

]

urlpatterns += router.urls
