#
# Copyright (c) nexB Inc. and others.
# SPDX-License-Identifier: Apache-2.0
#
# Visit https://aboutcode.org and https://github.com/nexB/ for support and download.
# ScanCode is a trademark of nexB Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os

from commoncode.testcase import FileBasedTesting

from typecode import extractible


class TestExtractible(FileBasedTesting):
    test_data_dir = os.path.join(os.path.dirname(__file__), 'data')

    def test__can_extract(self):
        tests = (
            ('extractible/a.tar.gz', True),
            ('extractible/crashing-squashfs', False),
            ('extractible/dbase.fdt', False),
            ('extractible/e.tar.bz2', True),
            ('extractible/e.tar.gz', True),
            ('extractible/e.tar', True),
            ('extractible/file_4.26-1.diff.gz', True),
            ('extractible/posixnotgnu.tar', True),
            ('extractible/sqfs-gz.sqs', False),
            ('extractible/sqfs-lzo.sqs', False),
            ('extractible/sqfs-xz.sqs', False),
            ('extractible/test.tar.lzma', True),
            ('extractible/test.tar.xz', True),
            ('extractible/test.zip', True),
            ('extractible/win-archive.lib', False),
        )
        for location, expected in tests:
            test_file = self.get_test_loc(location)
            result = extractible._can_extract(test_file)
            assert result == expected, '{} should extractible: {}'.format(location, expected)
