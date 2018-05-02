# -*- coding: utf-8 -*-
from __future__ import absolute_import

import uuid

from django.db import models

from utils.mixins import CreateLastUpdateDatetimeAbstractModel
from utils.constants import MAX_LENGTH


class Host(CreateLastUpdateDatetimeAbstractModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=MAX_LENGTH['name'])
    wan_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name=u'公网IP')
    lan_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name=u'内网IP')
    ansible_host = models.URLField(verbose_name=u'Ansible SSH 地址')  # 由前端控件可选默认填入内网IP或外网IP
    cpu = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name=u'CPU核心数')
    memory = models.PositiveIntegerField(blank=True, null=True, verbose_name=u'内存大小(MB)')  # Max to 2PB
    disk = models.PositiveIntegerField(blank=True, null=True, verbose_name=u'硬盘大小(GB)')  # Max to 2048PB
    band_width = models.PositiveIntegerField(blank=True, null=True, verbose_name=u'带宽(Mb)')
    startup_date = models.DateField(blank=True, null=True, verbose_name=u'创建日期')
    expire_date = models.DateField(blank=True, null=True, verbose_name=u'到期日期')
    enabled = models.BooleanField(default=True, verbose_name=u'是否启用')

    class Meta:
        verbose_name = u"主机"
        verbose_name_plural = u"主机"

    def __unicode__(self):
        return "%s(%s)" % (self.name, self.wan_ip if self.wan_ip else self.lan_ip)
