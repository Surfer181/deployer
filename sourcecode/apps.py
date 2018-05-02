# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.apps import AppConfig
from django.conf import settings

from utils.commands import check_make_local_dir


class SourcecodeConfig(AppConfig):
    name = 'sourcecode'
    verbose_name = u'代码管理及发布'

    def ready(self):
        # 确保 git 代码仓库根目录存在
        check_make_local_dir(settings.REPO_ROOT_DIR)
