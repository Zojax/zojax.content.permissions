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
""" zojax.content.browser tests

$Id$
"""
import os, unittest, doctest
from zope import interface, component
from zope.app.rotterdam import Rotterdam
from zope.app.testing import setup, placelesssetup, functional
from zojax.content.type.testing import setUpContents
from zojax.layoutform.interfaces import ILayoutFormLayer
from zojax.authentication.browser.interfaces import ILoginLayer
from zope.securitypolicy.principalpermission import AnnotationPrincipalPermissionManager


zojaxContentPermissionsLayer = functional.ZCMLLayer(
    os.path.join(os.path.split(__file__)[0], 'ftesting.zcml'),
    __name__, 'zojaxContentPermissionsLayer', allow_teardown=True)


class IDefaultSkin(ILayoutFormLayer, ILoginLayer, Rotterdam):
    """ skin """


def setUp(test):
    placelesssetup.setUp(test)
    setUpContents()
    component.provideAdapter(
        AnnotationPrincipalPermissionManager, (interface.Interface,))

    setup.setUpTestAsModule(test, 'zojax.content.permissions.TESTS')


def tearDown(test):
    placelesssetup.tearDown(test)
    setup.tearDownTestAsModule(test)


def test_suite():
    testbrowser = functional.FunctionalDocFileSuite(
        "testbrowser.txt",
        optionflags=doctest.ELLIPSIS|doctest.NORMALIZE_WHITESPACE)
    testbrowser.layer = zojaxContentPermissionsLayer

    return unittest.TestSuite((
            testbrowser,
            doctest.DocFileSuite(
                '../zcml.txt',
                setUp=setUp, tearDown=tearDown,
                optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS),
            ))
