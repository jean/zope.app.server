##############################################################################
#
# Copyright (c) 2004 Zope Corporation and Contributors.
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
"""HTTP server factories

$Id$
"""
import twisted.web2.wsgi
import twisted.web2.server

from zope.app.server.server import ServerType, SSLServerType
from zope.app import wsgi


def createHTTPFactory(db):
    resource = twisted.web2.wsgi.WSGIResource(
        wsgi.WSGIPublisherApplication(db))
    
    return twisted.web2.server.Site(resource)


http = ServerType(createHTTPFactory, 8080)

https = SSLServerType(createHTTPFactory, 8443)


def createHTTPFactory(db):
    resource = twisted.web2.wsgi.WSGIResource(
        wsgi.PMDBWSGIPublisherApplication(db))
    
    return twisted.web2.server.Site(resource)

pmhttp = ServerType(createHTTPFactory, 8080)


