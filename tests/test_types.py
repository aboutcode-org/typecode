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

from commoncode.testcase import FileDrivenTesting

from filetype_test_utils import build_tests
from filetype_test_utils import load_filetype_tests


test_env = FileDrivenTesting()
test_env.test_data_dir = os.path.join(os.path.dirname(__file__), 'data')


class TestFileTypesDataDriven(FileDrivenTesting):
    # test functions are attached to this class at module import time
    pass


build_tests(
    filetype_tests=load_filetype_tests(
        os.path.join(test_env.test_data_dir, 'filetest')),
    clazz=TestFileTypesDataDriven,
    test_data_dir=test_env.test_data_dir,
    regen=False,
)
