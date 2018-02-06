# -*- coding: utf-8 -*-
from __future__ import absolute_import

from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register(r'users', views.UserKeyViewSet)

urlpatterns = router.urls

