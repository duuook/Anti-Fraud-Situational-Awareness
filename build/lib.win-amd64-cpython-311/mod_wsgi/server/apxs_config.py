
import os
import posixpath

WITH_HTTPD_PACKAGE = False

if WITH_HTTPD_PACKAGE:
    from mod_wsgi_packages.httpd import __file__ as PACKAGES_ROOTDIR
    PACKAGES_ROOTDIR = posixpath.dirname(PACKAGES_ROOTDIR)
    BINDIR = posixpath.join(PACKAGES_ROOTDIR, 'bin')
    SBINDIR = BINDIR
    LIBEXECDIR = posixpath.join(PACKAGES_ROOTDIR, 'modules')
    SHLIBPATH = posixpath.join(PACKAGES_ROOTDIR, 'lib')
else:
    BINDIR = 'D:\Apache\Apache24/bin'
    SBINDIR = ''
    LIBEXECDIR = 'D:\Apache\Apache24/modules'
    SHLIBPATH = ''

MPM_NAME = ''
PROGNAME = 'httpd.exe'
SHLIBPATH_VAR = ''

if os.path.exists(posixpath.join(SBINDIR, PROGNAME)):
    HTTPD = posixpath.join(SBINDIR, PROGNAME)
elif os.path.exists(posixpath.join(BINDIR, PROGNAME)):
    HTTPD = posixpath.join(BINDIR, PROGNAME)
else:
    HTTPD = PROGNAME

if os.path.exists(posixpath.join(SBINDIR, 'rotatelogs')):
    ROTATELOGS = posixpath.join(SBINDIR, 'rotatelogs')
elif os.path.exists(posixpath.join(BINDIR, 'rotatelogs')):
    ROTATELOGS = posixpath.join(BINDIR, 'rotatelogs')
else:
    ROTATELOGS = 'rotatelogs'

