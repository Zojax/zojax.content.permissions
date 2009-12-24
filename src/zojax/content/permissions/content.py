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
from zope.component import getUtility

from zojax.content.type.interfaces import IContentType
from zojax.content.type.constraints import checkContentType

from permission import ContentPermission as BaseContentPermission


class ContentPermission(BaseContentPermission):

    def isAvailable(self):
        try:
            checkContentType(
                self.context, getUtility(IContentType, self.contenttype))
        except:
            return False

        return super(ContentPermission, self).isAvailable()
