#
# Copyright (c) nexB Inc. and others. All rights reserved.
# ScanCode is a trademark of nexB Inc.
# SPDX-License-Identifier: Apache-2.0
# See http://www.apache.org/licenses/LICENSE-2.0 for the license text.
# See https://github.com/nexB/typecode for support or download.
# See https://aboutcode.org for more information about nexB OSS projects.
#

import os

from commoncode.testcase import FileDrivenTesting

from filetype_test_utils import build_tests
from filetype_test_utils import load_filetype_tests

test_env = FileDrivenTesting()
test_env.test_data_dir = os.path.join(os.path.dirname(__file__), "data")


class TestFileTypesDataDriven(FileDrivenTesting):
    # test functions are attached to this class at module import time
    pass


build_tests(
    filetype_tests=load_filetype_tests(os.path.join(test_env.test_data_dir, "filetest")),
    clazz=TestFileTypesDataDriven,
    test_data_dir=test_env.test_data_dir,
    regen=False,
)
