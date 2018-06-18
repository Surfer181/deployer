# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os

from paramiko import RSAKey


def get_mode(dir_or_file_path):
    """
    获取文件(夹)权限
    :param dir_or_file_path: 文件(夹)路径
    :return: mask (str)
    """
    return oct(os.stat(dir_or_file_path).st_mode & 0777)


def change_mode(dir_or_file_path, mode):
    """
    修改文件（夹）权限
    :param dir_or_file_path: 文件或目录路径
    :param mode: 权限，8进制数
    :return: 无修改返回True，有修改返回False
    """
    origin_mode = get_mode(dir_or_file_path)
    if int(origin_mode, 8) != mode:
        os.chmod(dir_or_file_path, mode)
        return False
    else:
        return True


def check_make_local_dir(dir_path, mode=0755):
    """
    检查文件夹是否存在, 不存在则创建
    :param dir_path: 文件夹路径
    :param mode: 文件夹权限
    :return: 存在为 True, 不存在为 False
    """
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path, mode=mode)
    change_mode(dir_path, mode)  # 坑：os.makedirs() 在Mac上会忽略权限，要手动修改


def ssh_rsa_key_gen(filename, user=None, bit=4096):
    """
    生成SSH RSA 密钥对
    """
    k = RSAKey.generate(bit)
    abs_file_path = os.path.abspath(filename)
    assert os.path.isdir(os.path.dirname(abs_file_path)), "Dir Does not Exist!"
    # 生成私钥
    k.write_private_key_file(abs_file_path)
    change_mode(abs_file_path, 0600)

    public_key_name = abs_file_path + ".pub"
    with open(public_key_name, "w") as public_key:
        pubkey_body = k.get_base64()
        pubkey_name = k.get_name()
        key_user = " %s@deployer" % user if user else ""
        public_key.write("%s %s%s" % (pubkey_name, pubkey_body, key_user))

    return abs_file_path, public_key_name
