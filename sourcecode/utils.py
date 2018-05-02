# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os

from django.conf import settings

from .models import CodeVersionGroup
from .exceptions import NotGitRepoError
from utils.ansible_api import Api


def git_clone(code_version_obj):
    """
    clone 某个版本的代码
    :param code_version_obj: CodeVersion
    :return: result dict
    """
    if code_version_obj.repo.type == 'git':
        host_list = None
        # 文件夹名是 repo 带版本号的 uuid
        dest_dir = os.path.join(settings.REPO_ROOT_DIR, code_version_obj.uuid.__str__())

        arg = dict(
            repo=code_version_obj.repo.repo,
            dest=dest_dir,
            version=code_version_obj.version,
            accept_hostkey='yes',
            update='yes',
            force='yes',
            key_file=code_version_obj.repo.access_robot.private_key.key.path
        )
        api = Api()
        result = api.run_cmd(host_list, 'git', arg, remote_user=settings.CURRENT_USER)
        return result
    else:
        raise NotGitRepoError


def get_source_code():
    code_version_group = CodeVersionGroup.objects.first()
    current_user = settings.CURRENT_USER


    # for code in code_version_group.versions.all():