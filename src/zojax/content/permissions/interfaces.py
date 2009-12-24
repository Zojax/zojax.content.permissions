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
from zope import schema, interface
from zope.component.interfaces import ObjectEvent, IObjectEvent
from zope.i18nmessageid import MessageFactory
from zojax.security.interfaces import \
    IPermissionCategory, IPermissionCategoryType

_ = MessageFactory('zojax.content.permissions')

INHERITED = '__inherited__'


class IContentPermission(interface.Interface):
    """ permission interface """

    context = interface.Attribute('Context')
    permission = interface.Attribute('Permission object')
    permissionId = interface.Attribute('Permission id')
    managepermission = interface.Attribute('Manage permission id')

    roles = interface.Attribute('Allowed roles')
    principals = interface.Attribute('Allowed principals')

    def allow(principal):
        """ allow permission to principal """

    def unset(principal):
        """ unset permission for principal """

    def unsetAll():
        """ unset permission for all principals """

    def isAvailable():
        """ available permission in context """


# permissions catagories

class IAddPermission(IPermissionCategory):
    """Add content permission."""

    contenttype = schema.TextLine(
        title = u'Content type',
        required = False)


class IGeneralSettingsPermission(IPermissionCategory):
    """General portal settings permissions."""


class IManagementPermission(IPermissionCategory):
    """Permissions for managing permissions categories."""


class IViewPermission(IPermissionCategory):
    """View content permissions."""


class ISubmitPermission(IPermissionCategory):
    """Submit content permissions."""

    contenttype = schema.TextLine(
        title = u'Content type',
        required = False)


# update permissions types

class IPermissionContentTypes(interface.Interface):

    types = schema.Tuple(title = u'Content types')


# update permissions event

class IPermissionsUpdatedEvent(IObjectEvent):

    permissions = interface.Attribute('List of permissions')


class PermissionsUpdatedEvent(ObjectEvent):
    interface.implements(IPermissionsUpdatedEvent)

    def __init__(self, object, permissions):
        self.object = object
        self.permissions = permissions
