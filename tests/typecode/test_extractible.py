#
# Copyright (c) nexB Inc. and others. All rights reserved.
# http://nexb.com and https://github.com/nexB/scancode-toolkit/
# The ScanCode software is licensed under the Apache License version 2.0.
# Data generated with ScanCode require an acknowledgment.
# ScanCode is a trademark of nexB Inc.
#
# You may not use this software except in compliance with the License.
# You may obtain a copy of the License at: http://apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
#
# When you publish or redistribute any data created with ScanCode or any ScanCode
# derivative work, you must accompany this data with the following acknowledgment:
#
#  Generated with ScanCode and provided on an "AS IS" BASIS, WITHOUT WARRANTIES
#  OR CONDITIONS OF ANY KIND, either express or implied. No content created from
#  ScanCode should be considered or used as legal advice. Consult an Attorney
#  for any legal advice.
#  ScanCode is a free software code scanning tool from nexB Inc. and others.
#  Visit https://github.com/nexB/scancode-toolkit/ for support and download.

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os

from commoncode.system import py3
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
            ('extractible/test.tar.lzma', True if py3 else False),
            ('extractible/test.tar.xz', True if py3 else False),
            ('extractible/test.zip', True),
            ('extractible/win-archive.lib', False),
        )
        for location, expected in tests:
            test_file = self.get_test_loc(location)
            result = extractible._can_extract(test_file)
            assert result == expected, '{} should extractible: {}'.format(location, expected)
