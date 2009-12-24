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
from zope import interface
from zope.component import getAdapters, getUtilitiesFor
from zope.security.proxy import removeSecurityProxy
from zope.securitypolicy.interfaces import \
    Allow, Unset, Deny, IPrincipalPermissionManager

from zojax.batching.session import SessionBatch
from zojax.layoutform import PageletEditSubForm
from zojax.security.utils import getPrincipals
from zojax.security.interfaces import IPermissionCategoryType
from zojax.principal.field.utils import searchPrincipals
from zojax.content.type.interfaces import IDraftedContent
from zojax.principal.profile.interfaces import IPersonalProfile
from zojax.statusmessage.interfaces import IStatusMessage

from zojax.content.permissions.utils import updatePermissions
from zojax.content.permissions.interfaces import _, IContentPermission


class ContentPermissions(PageletEditSubForm):

    permissions = []

    def getPrincipals(self):
        principals = searchPrincipals()
        batch = SessionBatch(
            principals, size=10,
            context=self.context, request=self.request, prefix='security')
        principals = getPrincipals([p.id for p in batch])

        return principals, batch

    def update(self):
        super(ContentPermissions, self).update()

        context = self.context
        request = self.request

        if IDraftedContent.providedBy(context):
            return

        # get principals
        bprincipals, batch = self.getPrincipals()
        if not bprincipals:
            return

        self.batch = batch

        principals = []
        principalIds = []
        for principal in bprincipals:
            name = principal.id.replace('.', '_')
            principalIds.append(principal.id)
            principals.append(
                {'id': principal.id,
                 'name': name,
                 'title': IPersonalProfile(principal).title})

        self.principals = principals

        # get permissions
        categories = []
        allpermissions = []
        for categoryName, category in getUtilitiesFor(IPermissionCategoryType):
            permissions = []
            for name, perm in getAdapters((context,), category):
                if perm.isAvailable():
                    permOb = perm.permission
                    permissions.append((permOb.title, permOb.description, perm))
                    allpermissions.append(perm)

            if not permissions:
                continue

            permissions.sort()
            categories.append(
                (categoryName, category.__doc__,
                 [{'id': perm.permissionId, 'object': perm,
                   'settings':perm.principals,'title':title,'desc':description}
                  for title, description, perm in permissions]))

        categories.sort()
        self.permissions = [
            {'name': name, 'desc':desc, 'perms': perms}
            for name, desc, perms in categories]

        # process form
        if 'form.updatePrincipalPermissions' in request:
            permissions = {}
            for principal in principals:
                for perm in request.get('principal-%s'%principal['name'], ()):
                    data = permissions.setdefault(perm, [])
                    data.append(principal['id'])

            for permission in allpermissions:
                permission.unsetAll()
                if permission.permissionId in permissions:
                    permission.allow(permissions[permission.permissionId])

            updatePermissions(context, permissions.keys())

            IStatusMessage(request).add(_('Permissions have been updated.'))

            for info in self.permissions:
                for perm in info['perms']:
                    perm['settings'] = perm['object'].principals

    def isAvailable(self):
        return self.permissions and self.principals

    def postUpdate(self):
        pass
