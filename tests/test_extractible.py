#
# Copyright (c) nexB Inc. and others. All rights reserved.
# ScanCode is a trademark of nexB Inc.
# SPDX-License-Identifier: Apache-2.0
# See http://www.apache.org/licenses/LICENSE-2.0 for the license text.
# See https://github.com/nexB/typecode for support or download.
# See https://aboutcode.org for more information about nexB OSS projects.
#

import os

from commoncode.testcase import FileBasedTesting

from typecode import extractible


class TestExtractible(FileBasedTesting):
    test_data_dir = os.path.join(os.path.dirname(__file__), "data")

    def test__can_extract(self):
        tests = (
            ("extractible/a.tar.gz", True),
            ("extractible/crashing-squashfs", False),
            ("extractible/dbase.fdt", False),
            ("extractible/e.tar.bz2", True),
            ("extractible/e.tar.gz", True),
            ("extractible/e.tar", True),
            ("extractible/file_4.26-1.diff.gz", True),
            ("extractible/posixnotgnu.tar", True),
            ("extractible/sqfs-gz.sqs", False),
            ("extractible/sqfs-lzo.sqs", False),
            ("extractible/sqfs-xz.sqs", False),
            ("extractible/test.tar.lzma", True),
            ("extractible/test.tar.xz", True),
            ("extractible/test.zip", True),
            ("extractible/win-archive.lib", False),
        )
        for location, expected in tests:
            test_file = self.get_test_loc(location)
            result = extractible._can_extract(test_file)
            assert result == expected, "{} should extractible: {}".format(location, expected)
