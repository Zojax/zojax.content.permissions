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
from zope import interface, schema
from zope.component import getUtility
from zope.location import Location
from zope.security import checkPermission
from zope.security.proxy import removeSecurityProxy
from zope.security.interfaces import IPermission
from zope.securitypolicy.interfaces import Allow, IPrincipalPermissionManager

from interfaces import IContentPermission


class ContentPermission(Location):
    interface.implements(IContentPermission)

    def __init__(self, context):
        self._context = context
        self.__parent__ = context

        self.context = removeSecurityProxy(context)
        self._permissions = removeSecurityProxy(
            IPrincipalPermissionManager(context))

    @property
    def __name__(self):
        return self.name

    @property
    def permission(self):
        return getUtility(IPermission, self.permissionId)

    def isAvailable(self):
        return checkPermission(self.managepermission, self._context)

    def allow(self, principals):
        for pid in principals:
            self._permissions.grantPermissionToPrincipal(self.permissionId, pid)

    def unset(self, principals):
        for pid in principals:
            self._permissions.unsetPermissionForPrincipal(self.permissionId, pid)

    def unsetAll(self):
        permission = self.permissionId
        permissions = self._permissions

        for pid, setting in permissions.getPrincipalsForPermission(permission):
            permissions.unsetPermissionForPrincipal(permission, pid)

    @property
    def roles(self):
        return [pid for pid, setting in \
                    self._roles.getRolesForPermission(self.permissionId)
                if setting == Allow]

    @property
    def principals(self):
        return [pid for pid, setting in \
                    self._permissions.getPrincipalsForPermission(
                self.permissionId) if setting == Allow]


def PermissionType(permission, category, managepermission, class_, provides=[]):
    cdict = {}
    cdict['permissionId'] = permission
    cdict['managepermission'] = managepermission

    class_name = 'Permission<%s>'%permission

    if class_ is None:
        bases = (ContentPermission,)
    else:
        bases = (class_,)

    PermissionClass = type(str(class_name), bases, cdict)

    interface.classImplements(PermissionClass, *provides)
    return PermissionClass
