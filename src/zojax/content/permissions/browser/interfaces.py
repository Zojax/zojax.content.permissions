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
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from zojax.content.permissions.interfaces import _

sharingVocabulary = SimpleVocabulary(
    [SimpleTerm('inherited', 'inherited', _('INHERITED')),
     SimpleTerm('open', 'open', _('OPEN')),
     SimpleTerm('custom', 'custom', _('CUSTOM'))])

sharingVocabulary.getTerm('inherited').description = _(
    'Content item will inherit its permissions from the parent container.')
sharingVocabulary.getTerm('open').description = _(
    'Any user can view this content item.')
sharingVocabulary.getTerm('custom').description = _(
    'You can select groups and users who can view this content.')


class ISharingContent(interface.Interface):

    method = schema.Choice(
        title = _(u'Access control'),
        description = _(u'Who may view this content.'),
        vocabulary = sharingVocabulary,
        required = True)
