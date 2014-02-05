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
"""Setup for zojax.content.permissions package

$Id$
"""
import sys, os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version='1.0.3dev'


setup(name='zojax.content.permissions',
      version=version,
      description="Content permission management.",
      long_description=(
          'Detailed Documentation\n' +
          '======================\n'
          + '\n\n' +
          read('CHANGES.txt')
          ),
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Framework :: Zope3'],
      author='Nikolay Kim',
      author_email='fafhrd91@gmail.com',
      url='http://zojax.net/',
      license='ZPL 2.1',
      packages=find_packages('src'),
      package_dir = {'':'src'},
      namespace_packages=['zojax', 'zojax.content'],
      install_requires = ['setuptools',
                          'zope.interface',
                          'zope.component',
                          'zope.schema',
                          'zope.proxy',
                          'zope.location',
                          'zope.security',
                          'zope.securitypolicy',
                          'zope.i18n',
                          'zope.i18nmessageid',
                          'zope.publisher',
                          'zope.traversing',
                          'zope.app.security',
                          'zope.app.component',
                          'zope.configuration',
                          'zope.lifecycleevent',
                          'zojax.layout',
                          'zojax.layoutform',
                          'zojax.content.type',
                          'zojax.content.space',
                          'zojax.principal.field',
                          'zojax.principal.profile',
                          'zojax.permissionsmap',
                          'zojax.statusmessage',
                          'zojax.widget.radio',
                          'zojax.security',
                          ],
      extras_require = dict(test=['zope.app.testing',
                                  'zope.app.zcmlfiles',
                                  'zope.securitypolicy',
                                  'zope.testing',
                                  'zope.testbrowser',
                                  'zojax.autoinclude',
                                  'zojax.authentication',
                                  'zojax.content.browser',
                                  'zojax.principal.users',
                                  ]),
      include_package_data = True,
      zip_safe = False
      )
