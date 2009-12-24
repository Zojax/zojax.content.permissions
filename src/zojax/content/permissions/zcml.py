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
from zope import interface, component, schema
from zope.schema.interfaces import IFromUnicode
from zope.interface.verify import verifyClass, verifyObject
from zope.component.zcml import adapter, utility
from zope.security.zcml import Permission
from zope.security.checker import defineChecker, Checker
from zope.configuration.exceptions import ConfigurationError
from zope.configuration.fields import \
    Tokens, MessageID, GlobalObject, GlobalInterface

from permission import PermissionType
from interfaces import IContentPermission


class IContentPermissionDirective(interface.Interface):

    for_ = GlobalObject(
        title = u'For',
        required = False)

    permission = Permission(
        title = u'Permission',
        required = True)

    class_ = GlobalObject(
        title = u'Class',
        description = u'Custom implementation',
        required = False)

    category = GlobalInterface(
        title = u'Category',
        description = u'Permission category',
        required = True)

    managepermission = Permission(
        title = u'Manage permission',
        required = True)

    provides = Tokens(
        title = u"The interface this permission provides.",
        required = False,
        value_type = GlobalInterface())


IContentPermissionDirective.setTaggedValue('keyword_arguments', True)


def contentPermissionHandler(
    _context, permission, category, managepermission,
    for_=None, class_=None, provides=(), **kwargs):

    if permission == 'zope.Public':
        raise ConfigurationError('zope.Public permission is not allowed.')

    provides = list(provides)
    provides.append(category)

    PermissionClass = PermissionType(
        permission, category, managepermission, class_, provides)

    # set default values
    for iface in provides:
        verifyClass(iface, PermissionClass)

        for fname, field in schema.getFields(iface).items():
            if fname in kwargs:
                if not IFromUnicode.providedBy(field):
                    raise ConfigurationError("Can't convert value", fname)

                setattr(PermissionClass, fname, field.fromUnicode(kwargs[fname]))
            else:
                if field.required and not hasattr(PermissionClass, fname):
                    raise ConfigurationError("Required field is missing", fname)

                if not hasattr(PermissionClass, fname):
                    setattr(PermissionClass, fname, field.default)

    # set up permissions
    required = {}
    for iface in provides + [IContentPermission]:
        for iname in iface:
            required[iname] = managepermission

    defineChecker(PermissionClass, Checker(required))

    # register adapters
    adapter(_context, (PermissionClass,),
            category, (for_,), name=permission)
    adapter(_context, (PermissionClass,),
            IContentPermission, (for_,), name=permission)
