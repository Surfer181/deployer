# -*- coding: utf-8 -*-
from __future__ import absolute_import

import uuid

from django.db import models
from django.contrib.postgres.fields import JSONField

from host.models import Host
from utils.mixins import CreateLastUpdateDatetimeAbstractModel
from utils.constants import MAX_LENGTH
from utils.tools import merge_two_dicts


class Variable(CreateLastUpdateDatetimeAbstractModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=MAX_LENGTH['name'], blank=True)
    key = models.CharField(max_length=MAX_LENGTH['name'])
    value = JSONField(blank=True, null=True)

    @property
    def to_dict(self):
        return {
            self.key: self.value
        }

    def __unicode__(self):
        return "%s: %s" % (self.key, self.value)


class AnsibleInventory(CreateLastUpdateDatetimeAbstractModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=MAX_LENGTH['name'])
    host = models.ForeignKey(Host)
    ansible_port = models.PositiveIntegerField(default=22)
    ansible_user = models.CharField(max_length=MAX_LENGTH['name'])
    ansible_ssh_pass = models.CharField(max_length=MAX_LENGTH['password'], blank=True)
    vars = models.ManyToManyField(Variable, blank=True)

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.host)

    @property
    def merged_vars(self):
        """
        返回一个 Inventory 合并之后所有的vars
        :return: dict
        """
        host_vars = set(self.vars.all())
        group_vars = set([group.vars.all() for group in self.groups.all()])
        group_dict = reduce(merge_two_dicts, [var.to_dict for var in group_vars])
        host_dict = reduce(merge_two_dicts, [var.to_dict for var in host_vars])
        return merge_two_dicts(group_dict, host_dict)


class AnsibleGroup(CreateLastUpdateDatetimeAbstractModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=MAX_LENGTH['name'])
    inventories = models.ManyToManyField(AnsibleInventory, related_name='groups', blank=True)
    vars = models.ManyToManyField(Variable, blank=True)

    def __unicode__(self):
        return self.name


# class AnsiblePlaybook(CreateLastUpdateDatetimeAbstractModel):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     name = models.CharField(max_length=MAX_LENGTH['name'])
    # source = models.ForeignKey()
