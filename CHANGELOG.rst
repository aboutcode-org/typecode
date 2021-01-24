Release notes
=============

vNext
-----


Version 21.1.21
---------------

*2021-01-21*
- Update typecode-libmagic
- Drop using the standard library mimetypes modules because of
  https://github.com/nexB/typecode/issues/14
- Fix testing issues and testing requirements
- Update documentation and comments
- Uupdate to use latest commoncode


Version 21.1.9.1
----------------

*2021-01-09*
- Work around Python bug https://github.com/nexB/typecode/issues/14


Version 21.1.9
----------------

*2021-01-09*
- Remove Python 2
- Switch to plain Apache license per https://github.com/nexB/scancode-toolkit/issues/2337
- Improve documentation
- Enable Ci on more OS/Python combos


Version 21.1.8.1
----------------

*2021-01-08*
- Upgrade to latest boilerplate skeletton
- Improve detection of Windows executables 


Version 20.10.20
----------------

*2020-10-20*
- Roll back Pygments and vendor with vendy


Version 20.10
-------------

*2020-10-05*
- Code for content-based lexers from Pygments has been updated from v 2.2.0 to v 2.7.1
- Create data driven filetype tests and update test expectations


Version 20.09
-------------

*2020-09-24*
- Initial release.
