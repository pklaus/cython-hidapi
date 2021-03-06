#!/usr/bin/python
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import os
import sys

hidapi_topdir = os.path.join(os.getcwd(), 'hidapi')
hidapi_include = os.path.join(hidapi_topdir, 'hidapi')
def hidapi_src(platform):
    return os.path.join(hidapi_topdir, platform, 'hid.c')

if sys.platform.startswith('linux'):
    modules = [
        Extension('hid',
                  sources = ['hid.pyx', 'chid.pxd', hidapi_src('libusb')],
                  include_dirs = [hidapi_include, '/usr/include/libusb-1.0'],
                  libraries = ['usb-1.0', 'udev', 'rt'],
        ),
        Extension('hidraw',
                  sources = ['hidraw.pyx', hidapi_src('linux')],
                  include_dirs = [hidapi_include],
                  libraries = ['udev', 'rt'],
        )
    ]

if sys.platform.startswith('darwin'):
    os.environ['CFLAGS'] = '-framework IOKit -framework CoreFoundation'
    os.environ['LDFLAGS'] = ''
    modules = [
        Extension('hid',
                  sources = ['hid.pyx', 'chid.pxd', hidapi_src('mac')],
                  include_dirs = [hidapi_include],
                  libraries = [],
        )
    ]

if sys.platform.startswith('win'):
    modules = [
        Extension('hid',
            sources = ['hid.pyx', 'chid.pxd', hidapi_src('windows')],
            include_dirs = [hidapi_include],
            libraries = ['setupapi'],
        )
    ]

setup(
    name = 'hidapi',
    version = '0.7.99-5',
    description = 'A Cython interface to the hidapi from https://github.com/signal11/hidapi',
    author = 'Gary Bishop',
    author_email = 'gb@cs.unc.edu',
    maintainer = 'Pavol Rusnak',
    maintainer_email = 'stick@gk2.sk',
    url = 'https://github.com/trezor/cython-hidapi',
    package_dir = {'hid': 'hidapi/*'},
    classifiers = [
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
    ],
    cmdclass = {'build_ext': build_ext},
    ext_modules = modules
)
