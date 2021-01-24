TypeCode
========

- license: Apache-2.0
- copyright: copyright (c) nexB. Inc. and others
- homepage_url: https://github.com/nexB/typecode
- keywords: filetype, mimetype, libmagic, scancode-toolkit, typecode

TypeCode provides comprehensive filetype and mimetype detection using multiple
detectors including libmagic (included as a dependency for Linux, Windows and
macOS) and Pygments. It started as library in scancode-toolkit.
Visit https://aboutcode.org and https://github.com/nexB/ for support and download.


To install this package with its full capability (where the binaries for
libmagic are installed), use the `full` option::

    pip install typecode[full]

If you want to use the version of libmagic (possibly) provided by your operating
system, use the `minimal` option::

    pip install typecode


To set up the development environment::

    source configure

To run unit tests::

    pytest -vvs -n 2

To clean up development environment::

    ./configure --clean

