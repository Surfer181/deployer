# -*- coding: utf-8 -*-
from __future__ import absolute_import

import logging
import os
import mimetypes

from django.http import HttpResponse
from django.utils import timezone
from django.db import models
from django.utils.http import urlquote_plus, urlunquote_plus
from rest_framework.response import Response


logger = logging.getLogger(__name__)


class CreateLastUpdateDatetimeAbstractModel(models.Model):
    last_update_datetime = models.DateTimeField(verbose_name=u'最后修改时间', blank=True, null=True, editable=False)
    create_datetime = models.DateTimeField(
        verbose_name=u'创建时间', auto_now_add=True, blank=True, null=True, editable=False
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """ 可以加参数控制的 auto_now """
        if not kwargs.pop('skip_auto_now', False):
            self.last_update_datetime = timezone.now()
        return super(CreateLastUpdateDatetimeAbstractModel, self).save(*args, **kwargs)


class AdminCommonUserCanNotDeleteMixin(object):

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False


class AdminCanNotDeleteMixin(object):

    def has_delete_permission(self, request, obj=None):
        return False


class AdminCommonUserCanNotAddMixin(object):

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return False


class SwappableSerializerMixin(object):
    def get_serializer_class(self):
        try:
            return self.serializer_classes[self.request.method]
        except AttributeError:
            logger.debug('%(cls)s does not have the required serializer_classes'
                         'property' % {'cls': self.__class__.__name__})
            raise AttributeError
        except KeyError:
            logger.debug('request method %(method)s is not listed'
                         ' in %(cls)s serializer_classes' %
                         {'cls': self.__class__.__name__,
                          'method': self.request.method})
            # required if you don't include all the methods (option, etc) in your serializer_class
            return super(SwappableSerializerMixin, self).get_serializer_class()


class ActionSerializerMixin(object):
    """
    Viewset 中根据不同的 action 提供不同的 Serializer

    用法：
    serializer_classes = {'action': 'serializer', ...}
    """
    def get_serializer_class(self):
        try:
            return self.serializer_classes[self.action]
        except AttributeError:
            logger.debug('%(cls)s does not have the required serializer_classes'
                         'property' % {'cls': self.__class__.__name__})
            raise AttributeError
        except KeyError:
            logger.debug('request action %(action)s is not listed'
                         ' in %(cls)s serializer_classes' %
                         {'cls': self.__class__.__name__,
                          'action': self.action})
            # required if you don't include all the methods (option, etc) in your serializer_class
            return super(ActionSerializerMixin, self).get_serializer_class()


class ListModelWithOrWithoutPaginationMixin(object):
    """
    List a queryset.
    """
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if request.query_params.get('no_pagination', 0):
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ResponseDetailMixin(object):
    """
    继承此 mixin 来让 ModelSerializer 返回外键展开的 data

    使用方式：在 serializer 的 Meta 中添加 detail_serializers 属性，格式为：
    {
        'field': serializer,
        ...
    }
    参数：
        field 为需要展开的字段，如果为 list 记得添加 __many 后缀，比如 'users__many'；
        serializer 为要使用的 serializer
    """

    def to_representation(self, obj):
        data = super(ResponseDetailMixin, self).to_representation(obj)
        if hasattr(self.Meta, 'detail_serializers'):
            for field, serializer in self.Meta.detail_serializers.items():
                try:
                    if field.endswith('__many'):
                        field = field[:-6]
                        data[field] = serializer(getattr(obj, field),
                                                 many=True,
                                                 context=self.context).data
                    else:
                        data[field] = serializer(getattr(obj, field),
                                                 context=self.context).data
                except Exception as e:
                    print e
        return data


class DownloadFileMixin(object):
    def get_download_file_response(self, from_share=False):
        obj = self.get_object()
        if not from_share:
            fileobject = obj.file
            filename = obj.name
        else:
            fileobject = obj.target.file
            filename = obj.target.name

        redirect = urlunquote_plus(fileobject.url).encode('utf-8')
        response = HttpResponse(charset='utf-8')
        response['Content-Length'] = fileobject.size
        response['Content-Disposition'] = "attachment; filename=\"%s\"" % urlquote_plus(filename, safe="()/,&=@#%*")
        response['Content-Type'] = mimetypes.guess_type(fileobject.path)[0]
        response['Content-Length'] = os.path.getsize(fileobject.path)
        response['X-Accel-Redirect'] = redirect
        return response
