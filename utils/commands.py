# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os


def check_make_local_dir(dir_path, mode=0755):
    """
    检查文件夹是否存在, 不存在则创建
    :param dir_path: 文件夹路径
    :param mode: 文件夹权限
    :return: 存在为 True, 不存在为 False
    """
    if os.path.isdir(dir_path):
        return True
    else:
        os.makedirs(dir_path, mode=mode)
        return False


def get_mode(dir_or_file_path):
    """
    获取文件(夹)权限
    :param dir_or_file_path: 文件(夹)路径
    :return: mask (str)
    """
    return oct(os.stat(dir_or_file_path).st_mode & 0777)
