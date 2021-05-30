#
# Copyright (c) nexB Inc. and others. All rights reserved.
# ScanCode is a trademark of nexB Inc.
# SPDX-License-Identifier: Apache-2.0
# See http://www.apache.org/licenses/LICENSE-2.0 for the license text.
# See https://github.com/nexB/typecode for support or download.
# See https://aboutcode.org for more information about nexB OSS projects.
#

from typecode.magic2 import libmagic_version


def test_load_lib():
    assert libmagic_version > 0
