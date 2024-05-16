#
# Copyright (c) nexB Inc. and others. All rights reserved.
# ScanCode is a trademark of nexB Inc.
# SPDX-License-Identifier: Apache-2.0
# See http://www.apache.org/licenses/LICENSE-2.0 for the license text.
# See https://github.com/nexB/typecode for support or download.
# See https://aboutcode.org for more information about nexB OSS projects.
#

import os
from unittest.case import expectedFailure
from unittest.case import skipIf

import pytest

from commoncode.testcase import FileBasedTesting
from commoncode.system import on_linux
from commoncode.system import on_mac
from commoncode.system import on_windows

from typecode.contenttype import get_filetype
from typecode.contenttype import get_pygments_lexer
from typecode.contenttype import get_type

# aliases for testing
get_mimetype_python = lambda l: get_type(l).mimetype_python
get_filetype_pygment = lambda l: get_type(l).filetype_pygment
get_filetype_file = lambda l: get_type(l).filetype_file
get_mimetype_file = lambda l: get_type(l).mimetype_file

is_text = lambda l: get_type(l).is_text
is_archive = lambda l: get_type(l).is_archive
is_compressed = lambda l: get_type(l).is_compressed
is_media = lambda l: get_type(l).is_media
is_source = lambda l: get_type(l).is_source
is_script = lambda l: get_type(l).is_script
is_special = lambda l: get_type(l).is_special
is_binary = lambda l: get_type(l).is_binary

get_link_target = lambda l: get_type(l).link_target
is_link = lambda l: get_type(l).is_link
is_broken_link = lambda l: get_type(l).is_broken_link
size = lambda l: get_type(l).size
contains_text = lambda l: get_type(l).contains_text


class TestContentTypeComplex(FileBasedTesting):
#     test_data_dir = os.path.join(os.path.dirname(__file__), 'data')
    test_data_dir = os.path.join(os.path.dirname(__file__), 'data')

    def test_filetype_file_on_unicode_file_name(self):
        test_zip = self.extract_test_zip('contenttype/unicode/unicode.zip')
        test_dir = os.path.join(test_zip, 'a')
        f = os.listdir(test_dir)[0]
        test_file = os.path.join(test_dir, f)
        assert os.path.exists(test_file)

        expected = 'PNG image data, 16 x 12, 8-bit/color RGBA, interlaced'

        assert get_filetype_file(test_file) == expected

        expected = 'image/png'
        assert get_mimetype_file(test_file) == expected

    @skipIf(not on_linux, 'Windows and macOS have some issues with some non-unicode paths')
    def test_filetype_file_on_unicode_file_name2(self):
        zip_file_name = 'contenttype/unicode/unicode2.zip'

        test_zip = self.extract_test_zip(zip_file_name)
        test_dir = os.path.join(test_zip, 'a')
        f = [f for f in os.listdir(test_dir) if f.startswith('g')][0]
        test_file = os.path.join(test_dir, f)
        assert os.path.exists(test_file)

        expected = 'PNG image data, 16 x 12, 8-bit/color RGBA, interlaced'
        if on_windows:
            # FIXME: this is a very short png file though
            expected = 'Non-ISO extended-ASCII text'
        assert get_filetype_file(test_file) == expected

        expected = 'image/png'
        if on_windows:
            # FIXME: this is a very short png file though
            expected = 'text/plain'
        assert get_mimetype_file(test_file) == expected

    @skipIf(on_windows, 'Windows does not have (well supported) links.')
    def test_symbolink_links(self):
        test_dir = self.extract_test_tar('contenttype/links/links.tar.gz', verbatim=True)

        test_file1 = os.path.join(test_dir, 'prunedirs/targets/simlink_to_dir')
        assert is_link(test_file1)
        assert not is_broken_link(test_file1)
        assert get_link_target(test_file1) == '../sources/subdir'

        test_file2 = os.path.join(test_dir, 'prunedirs/targets/simlink_to_file')
        assert is_link(test_file2)
        assert not is_broken_link(test_file2)
        assert get_link_target(test_file2) == '../sources/a.txt'

        test_file3 = os.path.join(test_dir, 'prunedirs/targets/simlink_to_missing_file')
        assert is_link(test_file3)
        assert is_broken_link(test_file3)
        assert get_link_target(test_file3) == '../sources/temp.txt'

        test_file4 = os.path.join(test_dir, 'prunedirs/targets/simlink_to_missing_dir')
        assert is_link(test_file4)
        assert is_broken_link(test_file4)
        assert get_link_target(test_file4) == '../sources/tempdir'

    @skipIf(not on_windows, 'Hangs for now, for lack of proper sudo access on some test servers.')
    @skipIf(on_windows, 'Windows does not have fifos.')
    def test_contenttype_fifo(self):
        test_dir = self.get_temp_dir()
        myfifo = os.path.join(test_dir, 'myfifo')
        import subprocess
        if subprocess.call(['mkfifo', myfifo]) != 0:
            self.fail('Unable to create fifo')
        assert os.path.exists(myfifo)
        assert is_special(myfifo)
        assert get_filetype(myfifo) == 'FIFO pipe'

    def test_debian_package(self):
        test_file = self.get_test_loc('contenttype/package/libjama-dev_1.2.4-2_all.deb')
        expected = (
            # libmagic 5.38
            'debian binary package (format 2.0), with control.tar.gz, data compression gz',
            # libmagic 5.2x
            'debian binary package (format 2.0)',
        )
        assert get_filetype(test_file).startswith(expected)
        assert is_binary(test_file)
        assert is_archive(test_file)
        assert is_compressed(test_file)
        assert not contains_text(test_file)
        assert get_filetype_pygment(test_file) == ''

    def test_package_json(self):
        test_file = self.get_test_loc('contenttype/package/package.json')
        expected = (
            'ascii text, with very long lines',
            # libmagic 5.39+
            'json data',
            # Apple Silicon Homebrew libmagic
            'json text data',
        )

        assert get_filetype(test_file) in expected
        assert is_text(test_file)
        assert not is_binary(test_file)
        assert get_filetype_pygment(test_file) == ''
        assert not is_source(test_file)

    def test_certificate(self):
        test_file = self.get_test_loc('contenttype/certificate/CERTIFICATE')
        assert is_binary(test_file)
        # assert not is_archive(test_file)
        expected = (
            # libmagic 5.38
            'apple diskcopy 4.2 image',
            # libmagic 5.25
            'data',
        )
        assert get_filetype(test_file).startswith(expected)
        assert get_filetype_pygment(test_file) == ''

    def test_code_c_1(self):
        test_file = self.get_test_loc('contenttype/code/c/c_code.c')
        expected = (
            # incorrect p to libmagic 5.38
            'ti-xx graphing calculator (flash)',
            # correct in libmagic 5.39+
            'c source, ascii text',
        )
        assert get_filetype(test_file) in expected
        assert get_filetype_pygment(test_file) == 'C'
        assert is_source(test_file)
        assert is_text(test_file)

    def test_code_c_7(self):
        test_file = self.get_test_loc('contenttype/code/c/some.c')
        expected = (
            # incorrect p to libmagic 5.38
            'ti-xx graphing calculator (flash)',
            # correct in libmagic 5.39+
            'c source, ascii text',
        )
        assert get_filetype(test_file) in expected
        assert is_source(test_file)
        assert get_filetype_pygment(test_file) == 'C'

    def test_code_python_2(self):
        test_file = self.get_test_loc('contenttype/code/python/extract.py')
        assert is_source(test_file)
        assert is_text(test_file)
        assert get_filetype_pygment(test_file) == 'Python'
        assert get_filetype(test_file) == 'python script, ascii text executable'
        expected = (
            'text/x-python',
            # new in libmagic 5.39
            'text/x-script.python',
        )
        assert get_mimetype_file(test_file) in expected
        assert get_filetype_file(test_file).startswith('Python script')

    def test_compiled_elf_so(self):
        test_file = self.get_test_loc(u'contenttype/compiled/linux/libssl.so.0.9.7')
        assert not is_special(test_file)
        assert not is_text(test_file)
        assert get_filetype_pygment(test_file) == ''
        assert get_mimetype_file(test_file) == 'application/x-sharedlib'
        expected = (
            # correct with libmagic 5.38 and 5.39
            'ELF 32-bit LSB shared object, Intel 80386, version 1 (SYSV), statically linked, stripped',
            # incorrect with libmagic 5.2x
            'ELF 32-bit LSB shared object, Intel 80386, version 1 (SYSV), dynamically linked, stripped',
        )
        assert get_filetype_file(test_file) in expected
        assert get_filetype(test_file) in [t.lower() for t in expected]
        assert get_filetype_pygment(test_file) == ''

    def test_compiled_elf_so_2(self):
        test_file = self.get_test_loc('contenttype/compiled/linux/libnetsnmpagent.so.5')
        assert not is_source(test_file)
        expected = (
            # correct with libmagic 5.38 and 5.39
            'elf 32-bit lsb shared object, intel 80386, version 1 (sysv), statically linked, with debug_info, not stripped',
            # incorrect with libmagic 5.2x
            'elf 32-bit lsb shared object, intel 80386, version 1 (sysv), dynamically linked, with debug_info, not stripped',
        )
        assert get_filetype(test_file) in expected
        assert get_filetype_pygment(test_file) == ''

    @pytest.mark.xfail(
        on_mac or on_windows, reason='Somehow we get really weird results on macOS with libmagic 5.38 and mac, win32 on libmagic 5.39: '
       '[64-bit architecture=6893422] [64-bit architecture=6649701] [architecture=1075809] [architecture=3959150] [architecture=768]')
    def test_compiled_java_classfile_1(self):
        test_file = self.get_test_loc('contenttype/compiled/java/CommonViewerSiteFactory.class')
        assert get_filetype(test_file) == 'compiled java class data, version 46.0 (java 1.2)'
        assert get_filetype_pygment(test_file) == ''

    @pytest.mark.xfail(on_mac or on_windows, reason='Somehow we get really weird results on macOS with libmagic 5.38 and mac, win32 on libmagic 5.39: '
       '[64-bit architecture=6893422] [64-bit architecture=6649701] [architecture=1075809] [architecture=3959150] [architecture=768]')
    def test_compiled_java_classfile_2(self):
        test_file = self.get_test_loc('contenttype/compiled/java/old.class')
        assert is_binary(test_file)
        assert get_filetype(test_file) == 'compiled java class data, version 46.0 (java 1.2)'
        assert get_filetype_pygment(test_file) == ''

    def test_compiled_python_1(self):
        test_dir = self.extract_test_zip('contenttype/compiled/python/compiled.zip')
        test_file = os.path.join(test_dir, 'command.pyc')
        assert get_filetype(test_file) == 'python 2.5 byte-compiled'
        assert not is_source(test_file)
        assert not is_text(test_file)
        expected_mime = (
            'application/octet-stream',
            # libmagic 5.39
            'text/x-bytecode.python',
            # Apple Silicon Homebrew libmagic
            'application/x-bytecode.python',
        )
        assert get_mimetype_file(test_file) in expected_mime
        assert get_filetype_pygment(test_file) == ''

        test_file2 = os.path.join(test_dir, 'contenttype.pyc')
        assert is_binary(test_file2)
        assert get_pygments_lexer(test_file2) is None

        test_file3 = os.path.join(test_dir, 'contenttype.pyo')
        assert is_binary(test_file3)
        assert get_pygments_lexer(test_file3) is None

        test_file4 = os.path.join(test_dir, 'extract.pyc')
        assert get_filetype(test_file4) == 'python 2.5 byte-compiled'
        assert not is_source(test_file4)
        assert not is_text(test_file4)
        assert get_mimetype_file(test_file4) in expected_mime
        assert get_filetype_pygment(test_file4) == ''

    # @pytest.mark.xfail(on_windows or on_mac, reason='Somehow we have incorrect results on win63 with libmagic 5.38: '
    #   'application/octet-stream instead of EPS')
    def test_doc_postscript_eps(self):
        test_file = self.get_test_loc('contenttype/doc/postscript/Image1.eps')
        assert is_binary(test_file)

        results = dict(
            get_filetype_file=get_filetype_file(test_file),
            get_mimetype_file=get_mimetype_file(test_file),
        )
        expected = dict(
            get_filetype_file='DOS EPS Binary File',
            get_mimetype_file=(
                'application/octet-stream',
                'image/x-eps',
            )
        )
        assert expected['get_filetype_file'] in results['get_filetype_file']
        assert results['get_mimetype_file'] in expected['get_mimetype_file']

    def test_media_image_img(self):
        test_file = self.get_test_loc('contenttype/media/Image1.img')
        assert is_binary(test_file)
        assert get_filetype_file(test_file).startswith('GEM Image data')
        expected = (
            # libmagic 5.3.8
            'image/x-gem',
            # libmagic 5.2x
            'application/octet-stream',
        )
        assert get_mimetype_file(test_file) in expected
        assert not get_mimetype_python(test_file)
        assert is_media(test_file)
        assert not is_text(test_file)
        assert not is_archive(test_file)
        assert not contains_text(test_file)

    def test_package_debian(self):
        test_file = self.get_test_loc('contenttype/package/wget-el_0.5.0-8_all.deb')
        expected = (
            # libmagic 5.38
            'debian binary package (format 2.0), with control.tar.gz, data compression gz',
            # libmagic 5.2x
            'debian binary package (format 2.0)',
            # Apple Silicon Homebrew libmagic
            'debian binary package (format 2.0), with control.tar.gz , data compression gz',
        )
        assert get_filetype(test_file) in expected
        assert is_binary(test_file)
        assert is_archive(test_file)
        assert not contains_text(test_file)

    @expectedFailure
    def test_text_rsync_file_is_not_octet_stream(self):
        # this is a libmagic bug: http://bugs.gw.com/view.php?id=473
        test_file = self.get_test_loc('contenttype/text/wildtest.txt')
        assert 'data' != get_filetype_file(test_file)
        assert 'octet' not in get_mimetype_file(test_file)

    @skipIf(on_windows, 'fails because of libmagic bug on windows.')
    def test_archive_squashfs_crashing(self):
        test_file = self.get_test_loc('contenttype/archive/crashing-squashfs')
        assert get_filetype_file(test_file).startswith('Squashfs filesystem, little endian, version')
        assert is_archive(test_file)
        assert is_compressed(test_file)
        assert not contains_text(test_file)
        assert get_filetype_pygment(test_file) == ''

    @skipIf(on_windows, 'fails because of libmagic bug on windows.')
    def test_archive_squashfs_gz(self):
        test_file = self.get_test_loc('contenttype/archive/sqfs-gz.sqs')
        assert get_filetype_file(test_file).startswith('Squashfs filesystem, little endian, version')
        assert is_archive(test_file)
        assert is_compressed(test_file)
        assert not contains_text(test_file)
        assert get_filetype_pygment(test_file) == ''

    @skipIf(on_windows, 'fails because of libmagic bug on windows.')
    def test_archive_squashfs_lzo(self):
        test_file = self.get_test_loc('contenttype/archive/sqfs-lzo.sqs')
        assert get_filetype_file(test_file).startswith('Squashfs filesystem, little endian, version')
        assert is_archive(test_file)
        assert is_compressed(test_file)
        assert not contains_text(test_file)
        assert get_filetype_pygment(test_file) == ''

    @skipIf(on_windows, 'fails because of libmagic bug on windows.')
    def test_archive_squashfs_xz(self):
        test_file = self.get_test_loc('contenttype/archive/sqfs-xz.sqs')
        assert get_filetype_file(test_file).startswith('Squashfs filesystem, little endian, version')
        assert is_archive(test_file)
        assert is_compressed(test_file)
        assert not contains_text(test_file)
        assert get_filetype_pygment(test_file) == ''

    def test_directory(self):
        test_file = self.get_test_loc('contenttype')
        assert not is_binary(test_file)
        assert not is_compressed(test_file)
        assert not contains_text(test_file)
        assert get_filetype_pygment(test_file) == ''

    def test_size(self):
        test_dir = self.get_test_loc('contenttype/size')
        result = size(test_dir)
        assert result == 18
