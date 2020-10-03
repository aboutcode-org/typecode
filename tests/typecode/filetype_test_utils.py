#
# Copyright (c) 2018 nexB Inc. and others. All rights reserved.
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

from collections import OrderedDict
import io
from os import path

import attr
import pytest

from commoncode import compat
from commoncode import saneyaml
from commoncode.system import py2
from commoncode.testcase import FileDrivenTesting
from commoncode.testcase import get_test_file_pairs
from commoncode.text import python_safe_name
from typecode.contenttype import get_type


"""
Data-driven file type test utilities.
"""

test_env = FileDrivenTesting()
test_env.test_data_dir = path.join(path.dirname(__file__), 'data')


@attr.s(slots=True)
class FileTypeTest(object):
    data_file = attr.ib(default=None)
    test_file = attr.ib(default=None)
    # one of holders, copyrights, authors
    what = attr.ib(default=attr.Factory(list))
    mime_type = attr.ib(default=attr.Factory(list))
    file_type = attr.ib(default=attr.Factory(list))
    programming_language = attr.ib(default=attr.Factory(list))
    is_binary = attr.ib(default=attr.Factory(list))
    is_text = attr.ib(default=attr.Factory(list))
    is_archive = attr.ib(default=attr.Factory(list))
    is_media = attr.ib(default=attr.Factory(list))
    is_source = attr.ib(default=attr.Factory(list))
    is_script = attr.ib(default=attr.Factory(list))

    expected_failures = attr.ib(default=attr.Factory(list))
    notes = attr.ib(default=None)

    def __attrs_post_init__(self, *args, **kwargs):
        if self.data_file:
            try:
                with io.open(self.data_file, encoding='utf-8') as df:
                    for key, value in saneyaml.load(df.read()).items():
                        if value:
                            setattr(self, key, value)
            except:
                import traceback
                msg = 'file://' + self.data_file + '\n' + repr(self) + '\n' + traceback.format_exc()
                raise Exception(msg)

    def to_dict(self):
        """
        Serialize self to an ordered mapping.
        """
        filtered = [field for field in attr.fields(FileTypeTest)
                    if '_file' in field.name]
        fields_filter = attr.filters.exclude(*filtered)
        data = attr.asdict(self, filter=fields_filter, dict_factory=OrderedDict)
        return OrderedDict([
            (key, value) for key, value in data.items()
            # do not dump false and empties
            if value])

    def dumps(self):
        """
        Return a string representation of self in YAML block format.
        """
        return saneyaml.dump(self.to_dict())

    def dump(self, check_exists=False):
        """
        Dump a representation of self to a .yml data_file in YAML block format.
        """
        if check_exists and path.exists(self.data_file):
            raise Exception(self.data_file)
        with io.open(self.data_file, 'w', encoding='utf-8') as df:
            df.write(self.dumps())


def load_filetype_tests(test_dir=test_env.test_data_dir):
    """
    Yield an iterable of FileTypeTest loaded from test data files in `test_dir`.
    """
    test_dir = path.join(test_dir, 'filetest')

    all_test_files = get_test_file_pairs(test_dir)

    for data_file, test_file in all_test_files:
        yield FileTypeTest(data_file, test_file)


def filetype_detector(location):
    """
    Return detected filetype info
    """
    collector = get_type(location)
    return {
        'mime_type': collector.mimetype_file or None,
        'file_type': collector.filetype_file or None,
        'programming_language': collector.programming_language or None,
        'is_binary': bool(collector.is_binary),
        'is_text': bool(collector.is_text),
        'is_archive': bool(collector.is_archive),
        'is_media': bool(collector.is_media),
        'is_source': bool(collector.is_source),
        'is_script': bool(collector.is_script),
    }


def make_filetype_test_functions(test, index, test_data_dir=test_env.test_data_dir, regen=False):
    """
    Build and return a test function closing on tests arguments and the function name.
    """

    def closure_test_function(*args, **kwargs):
        results = filetype_detector(test_file)

        expected_yaml = test.dumps()

        for wht in test.what:
            setattr(test, wht, results.get(wht))
        results_yaml = test.dumps()

        if regen:
            test.dump()
        if expected_yaml != results_yaml:
            expected_yaml = (
                'data file: file://' + data_file +
                '\ntest file: file://' + test_file + '\n'
            ) + expected_yaml

            assert expected_yaml == results_yaml

    data_file = test.data_file
    test_file = test.test_file
    what = test.what

    tfn = test_file.replace(test_data_dir, '').strip('\\/\\')
    whats = '_'.join(what)
    test_name = 'test_%(tfn)s_%(index)s' % locals()
    test_name = python_safe_name(test_name)

    # onPython2 we need a plain non-unicode string
    if py2 and isinstance(test_name, compat.unicode):
        test_name = test_name.encode('utf-8')

    closure_test_function.__name__ = test_name

    if test.expected_failures:
        closure_test_function = pytest.mark.xfail(closure_test_function)

    return closure_test_function, test_name


def build_tests(filetype_tests, clazz, test_data_dir=test_env.test_data_dir, regen=False):
    """
    Dynamically build test methods from a sequence of FileTypeTests and attach
    these method to the clazz test class.
    """
    for i, test in enumerate(sorted(filetype_tests, key=lambda x:x.test_file)):
        # closure on the test params
        if test.expected_failures:
            actual_regen = False
        else:
            actual_regen = regen
        method, name = make_filetype_test_functions(test, i, test_data_dir, actual_regen)
        # attach that method to our test class
        setattr(clazz, name, method)
