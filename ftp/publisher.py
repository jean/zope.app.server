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
"""Publisher File System Implementation
"""
__docformat__="restructuredtext"
import posixpath
from cStringIO import StringIO

from zope.interface import implements
from zope.publisher.publish import publish

from interfaces import IFileSystem

class NoOutput(object):
    """An output stream lookalike that warns you if you try to
    dump anything into it."""

    def write(self, data):
        raise RuntimeError, "Not a writable stream"

    def flush(self):
        pass

    close = flush

## this is the old zope.server.ftp.publisher.PublisherFileSystem class
class PublisherFileSystem(object):
    """Generic Publisher FileSystem implementation."""

    implements(IFileSystem)

    def __init__ (self, credentials, request_factory):
        self.credentials = credentials
        self.request_factory = request_factory

    def type(self, path):
        if path == '/':
            return 'd'

        return self._execute(path, 'type')

    def names(self, path, filter=None):
        return self._execute(path, 'names', split=False, filter=filter)

    def ls(self, path, filter=None):
        return self._execute(path, 'ls', split=False, filter=filter)

    def readfile(self, path, outstream, start=0, end=None):
        return self._execute(path, 'readfile', 
                             outstream=outstream, start=start, end=end)

    def lsinfo(self, path):
        return self._execute(path, 'lsinfo')

    def mtime(self, path):
        return self._execute(path, 'mtime')

    def size(self, path):
        return self._execute(path, 'size')

    def mkdir(self, path):
        return self._execute(path, 'mkdir')

    def remove(self, path):
        return self._execute(path, 'remove')

    def rmdir(self, path):
        return self._execute(path, 'rmdir')

    def rename(self, old, new):
        'See IWriteFileSystem'
        old = self._translate(old)
        new = self._translate(new)
        path0, old = posixpath.split(old)
        path1, new = posixpath.split(new)
        assert path0 == path1
        return self._execute(path0, 'rename', split=False, old=old, new=new)

    def writefile(self, path, instream, start=None, end=None, append=False):
        'See IWriteFileSystem'
        return self._execute(
            path, 'writefile',
            instream=instream, start=start, end=end, append=append)

    def writable(self, path):
        'See IWriteFileSystem'
        return self._execute(path, 'writable')

    def _execute(self, path, command, split=True, **kw):
        env = {}
        env.update(kw)
        env['command'] = command

        path = self._translate(path)

        if split:
            env['path'], env['name'] = posixpath.split(path)
        else:
            env['path'] = path
            
        env['credentials'] = self.credentials
        # NoOutput avoids creating a black hole.
        request = self.request_factory(StringIO(''), NoOutput(), env)

        # Note that publish() calls close() on request, which deletes the
        # response from the request, so that we need to keep track of it.
        response = request.response
        publish(request)
        return response.getResult()

    def _translate (self, path):
        # Normalize
        path = posixpath.normpath(path)
        if path.startswith('..'):
            # Someone is trying to get lower than the permitted root.
            # We just ignore it.
            path = '/'
        return path