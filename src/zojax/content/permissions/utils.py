##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
from zope import event
from zope.component import subscribers, getAdapters, getUtility
from zojax.catalog.interfaces import ICatalog

from interfaces import PermissionsUpdatedEvent
from interfaces import IPermissionContentTypes, IContentPermission


def updatePermissions(context, permissions=None):
    if permissions is None:
        permissions = []
        for name, perm in getAdapters((context,), IContentPermission):
            if perm.isAvailable():
                permissions.append(perm.permission)

    types = set()

    for tps in subscribers((context, permissions), IPermissionContentTypes):
        if tps is not None:
            types.update(tps)

    if types:
        getUtility(ICatalog).updateIndexesByQuery(
            type={'any_of': types},
            indexNames=['draftSubmitTo',
                        'draftPublishTo',
                        'draftPublishable',
                        'allowedRoleAndPrincipals'],
            searchContext=context, noPublishing=True, noSecurityChecks=True)

    event.notify(PermissionsUpdatedEvent(context, permissions))
