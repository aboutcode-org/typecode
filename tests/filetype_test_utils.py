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

from collections import OrderedDict
import io
from os import path

import attr
import pytest
import saneyaml

from commoncode.system import on_mac
from commoncode.system import on_windows
from commoncode.testcase import FileDrivenTesting
from commoncode.testcase import get_test_file_pairs
from commoncode.text import python_safe_name
from typecode.contenttype import get_type
from typecode.contenttype import Type

"""
Data-driven file type test utilities.
"""

test_env = FileDrivenTesting()
test_env.test_data_dir = path.join(path.dirname(__file__), 'data')


@attr.s(slots=True)
class FileTypeTest(object):
    """
    A filetype detection test is used to verify that file type detection
    works correctly

    It consists of two files with the same base file name:
    - a file to test for file type named for instance foo.txt
    - a foo.txt.yml YAML file with expected test data

    The following data are from the .yml file:
     - the set of attributes of the typecode.contenttype.Type object
       excluding date and location.
     - notes
    """

    data_file = attr.ib(default=None)
    test_file = attr.ib(default=None)

    # ATTENTION: keep these attributes  in sync with typecode.contenttype.Type
    filetype_file = attr.ib(default='')
    mimetype_file = attr.ib(default='')
    mimetype_python = attr.ib(default='')
    filetype_pygment = attr.ib(default='')
    elf_type = attr.ib(default='')
    programming_language = attr.ib(default='')

    is_file = attr.ib(default=False)
    is_dir = attr.ib(default=False)
    is_regular = attr.ib(default=False)
    is_special = attr.ib(default=False)

    is_link = attr.ib(default=False)
    is_broken_link = attr.ib(default=False)
    link_target = attr.ib(default='')
    size = attr.ib(default=False)
    is_pdf_with_text = attr.ib(default=False)
    is_text = attr.ib(default=False)
    is_text_with_long_lines = attr.ib(default=False)
    is_compact_js = attr.ib(default=False)
    is_js_map = attr.ib(default=False)
    is_binary = attr.ib(default=False)
    is_data = attr.ib(default=False)
    is_archive = attr.ib(default=False)
    contains_text = attr.ib(default=False)
    is_compressed = attr.ib(default=False)
    is_c_source = attr.ib(default=False)
    is_c_source = attr.ib(default=False)
    is_elf = attr.ib(default=False)
    is_elf = attr.ib(default=False)
    is_filesystem = attr.ib(default=False)
    is_java_class = attr.ib(default=False)
    is_java_source = attr.ib(default=False)
    is_media = attr.ib(default=False)
    is_media_with_meta = attr.ib(default=False)
    is_office_doc = attr.ib(default=False)
    is_package = attr.ib(default=False)
    is_pdf = attr.ib(default=False)
    is_script = attr.ib(default=False)
    is_source = attr.ib(default=False)
    is_stripped_elf = attr.ib(default=False)
    is_winexe = attr.ib(default=False)
    is_makefile = attr.ib(default=False)

    expected_failure = attr.ib(default=False)
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
        if isinstance(self.size, str):
            self.size = int(self.size)

    def to_dict(self, filter_empty=False, filter_extra=False):
        """
        Serialize self to an ordered mapping.
        """
        filtered = [field for field in attr.fields(FileTypeTest)
                    if field.name in ('data_file', 'test_file')]
        fields_filter = attr.filters.exclude(*filtered)
        data = attr.asdict(self, filter=fields_filter, dict_factory=OrderedDict)
        data = data.items()
        if filter_empty:
            # skip empty fields
            data = ((k, v) for k, v in data if v)
        if filter_extra:
            data = ((k, v) for k, v in data if k not in ('expected_failure', 'notes'))

        return OrderedDict(data)

    def dumps(self):
        """
        Return a string representation of self in YAML block format.
        """
        return saneyaml.dump(self.to_dict(filter_empty=True))

    def dump(self, check_exists=False):
        """
        Dump a representation of self to a .yml data_file in YAML block format.
        """
        if check_exists and path.exists(self.data_file):
            raise Exception(self.data_file)
        with io.open(self.data_file, 'w', encoding='utf-8') as df:
            df.write(self.dumps())


def load_filetype_tests(test_dir):
    """
    Yield an iterable of FileTypeTest loaded from test data files in `test_dir`.
    """
    all_test_files = get_test_file_pairs(test_dir)

    for data_file, test_file in all_test_files:
        yield FileTypeTest(data_file, test_file)


def check_types_equal(expected, result):
    """
    Compare type data dict expected to type data dict result key by key.
    Return True if they match, false otherwise.
    Check also that the keys are identical.
    Treat text attributes in a special way as we test for "startswith".
    Empty strings are treated the same as None.
    """
    extra_keys = set(expected.keys()).symmetric_difference(set(result.keys()))
    assert not extra_keys

    for expected_key, expected_value in expected.items():
        result_value = result[expected_key]

        # these attributes should be tested with startswith
        if expected_key in Type.text_attributes:
            if result_value and expected_value:
                if not result_value.startswith(expected_value):
                    # on windows we really have weird things
                    return False
            else:
                return result_value == expected_value

        # we have either number, date, None or boolean value and
        # we want both values to be both trueish or falsish
        else:

            if bool(result_value) != bool(expected_value):
                return False
    return True


def make_filetype_test_functions(test, index, test_data_dir=test_env.test_data_dir, regen=False):
    """
    Build and return a test function closing on tests arguments and the function name.
    """

    def closure_test_function(*args, **kwargs):
        results = get_type(test_file).to_dict(include_date=False)

        if regen:
            for key, value in results.items():
                setattr(test, key, value)
                test.dump()

        expected = test.to_dict(filter_empty=False, filter_extra=True)
        passing = check_types_equal(expected, results)

        # this is done to display slightly eaier to handle error traces
        if not passing:
            expected['data file'] = 'file://' + data_file
            expected['test_file'] = 'file://' + test_file
            assert dict(expected) == dict(results)

    data_file = test.data_file
    test_file = test.test_file

    tfn = test_file.replace(test_data_dir, '').strip('\\/\\')
    test_name = 'test_%(tfn)s_%(index)s' % locals()
    test_name = python_safe_name(test_name)

    closure_test_function.__name__ = test_name

    if (test.expected_failure is True
        or (isinstance(test.expected_failure, str)
            and (
                ('windows' in test.expected_failure and on_windows)
                or ('macos' in test.expected_failure and on_mac)
            )
        )
    ):
        closure_test_function = pytest.mark.xfail(closure_test_function)

    return closure_test_function, test_name


def build_tests(filetype_tests, clazz, test_data_dir=test_env.test_data_dir, regen=False):
    """
    Dynamically build test methods from a sequence of FileTypeTest and attach
    these method to the clazz test class.
    """
    for i, test in enumerate(sorted(filetype_tests, key=lambda x:x.test_file)):
        # closure on the test params
        if test.expected_failure:
            actual_regen = False
        else:
            actual_regen = regen
        method, name = make_filetype_test_functions(test, i, test_data_dir, actual_regen)
        # attach that method to our test class
        setattr(clazz, name, method)
