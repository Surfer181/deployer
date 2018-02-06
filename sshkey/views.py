# -*- coding: utf-8 -*-
from __future__ import absolute_import

# from django.http import HttpResponseRedirect
# from django.views.decorators.http import require_http_methods, require_GET
# from django.shortcuts import get_object_or_404, render
# from django.contrib import messages
# from django.contrib.auth.decorators import login_required
# from django.core.exceptions import PermissionDenied
# from django.urls import reverse
# from django.utils.http import is_safe_url

from rest_framework import parsers, viewsets, status, generics, mixins
from rest_framework.permissions import IsAuthenticated

from .models import UserKey
from . import serializers, settings
from utils.mixins import ActionSerializerMixin


# @login_required
# @require_GET
# def userkey_list(request):
#     userkey_list = UserKey.objects.filter(user=request.user)
#     return render(request, 'sshkey/userkey_list.html',
#                   context={'userkey_list': userkey_list,
#                            'allow_edit': settings.SSHKEY_ALLOW_EDIT}
#                   )
#
#
# @login_required
# @require_http_methods(['GET', 'POST'])
# def userkey_add(request):
#     if request.method == 'POST':
#         userkey = UserKey(user=request.user)
#         userkey.request = request
#         form = UserKeyForm(request.POST, instance=userkey)
#         if form.is_valid():
#             form.save()
#             default_redirect = reverse('simplesshkey:userkey_list')
#             url = request.GET.get('next', default_redirect)
#             if not is_safe_url(url=url, host=request.get_host()):
#                 url = default_redirect
#             message = 'SSH public key %s was added.' % userkey.name
#             messages.success(request, message, fail_silently=True)
#             return HttpResponseRedirect(url)
#     else:
#         form = UserKeyForm()
#     return render(request, 'sshkey/userkey_detail.html',
#                   context={'form': form, 'action': 'add'})
#
#
# @login_required
# @require_http_methods(['GET', 'POST'])
# def userkey_edit(request, pk):
#     if not settings.SSHKEY_ALLOW_EDIT:
#         raise PermissionDenied
#     userkey = get_object_or_404(UserKey, pk=pk)
#     if userkey.user != request.user:
#         raise PermissionDenied
#     if request.method == 'POST':
#         form = UserKeyForm(request.POST, instance=userkey)
#         if form.is_valid():
#             form.save()
#             default_redirect = reverse('simplesshkey:userkey_list')
#             url = request.GET.get('next', default_redirect)
#             if not is_safe_url(url=url, host=request.get_host()):
#                 url = default_redirect
#             message = 'SSH public key %s was saved.' % userkey.name
#             messages.success(request, message, fail_silently=True)
#             return HttpResponseRedirect(url)
#     else:
#         form = UserKeyForm(instance=userkey)
#     return render(request, 'sshkey/userkey_detail.html',
#                   context={'form': form, 'action': 'edit'})
#
#
# @login_required
# @require_GET
# def userkey_delete(request, pk):
#     userkey = get_object_or_404(UserKey, pk=pk)
#     if userkey.user != request.user:
#         raise PermissionDenied
#     userkey.delete()
#     message = 'SSH public key %s was deleted.' % userkey.name
#     messages.success(request, message, fail_silently=True)
#     return HttpResponseRedirect(reverse('simplesshkey:userkey_list'))


class UserKeyViewSet(ActionSerializerMixin, viewsets.ModelViewSet):
    queryset = UserKey.objects.all()
    serializer_class = serializers.UserKeyDetailSerializer
    serializer_classes = {
        'list': serializers.UserKeyListSerializer,
    }
    permission_classes = (IsAuthenticated,)
