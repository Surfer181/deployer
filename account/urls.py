# -*- coding: utf-8 -*-

from django.conf.urls import url
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)


urlpatterns = [
    url(r'^login/$', views.LoginView.as_view(), name='login'),
]
urlpatterns += router.urls

