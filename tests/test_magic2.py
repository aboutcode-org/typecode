#
# Copyright (c) nexB Inc. and others. All rights reserved.
# ScanCode is a trademark of nexB Inc.
# SPDX-License-Identifier: Apache-2.0
# See http://www.apache.org/licenses/LICENSE-2.0 for the license text.
# See https://github.com/nexB/typecode for support or download.
# See https://aboutcode.org for more information about nexB OSS projects.
#

from typecode.magic2 import MO_FILE_TYPE_RE
from typecode.magic2 import libmagic_version


def test_load_lib():
    assert float(libmagic_version()) > 5


def _clean_mo_type(val):
    match = MO_FILE_TYPE_RE.match(val)
    return match.group(1) if match else val


def test_mo_file_type_strips_embedded_project_id_version_ascii():
    val = (
        "GNU message catalog (little endian), revision 0.0, 349 messages, "
        "Project-Id-Version: django '%(datetime)s non se puido interpretar na "
        "zona hora horaria %(current_timezone)s; pode ser ambiguo ou non "
        "existir.'"
    )
    assert _clean_mo_type(val) == (
        "GNU message catalog (little endian), revision 0.0, 349 messages"
    )


def test_mo_file_type_strips_embedded_project_id_version_escaped_bytes():
    val = (
        "GNU message catalog (little endian), revision 0.0, 349 messages, "
        "Project-Id-Version: django '%(datetime)s \\343\\201\\257 "
        "%(current_timezone)s \\343\\201\\256\\343\\202\\277\\343\\202\\244"
        "\\343\\203\\240\\343\\202\\276\\343\\203\\274\\343\\203\\263"
        "\\343\\201\\247\\343\\201\\257\\350\\247\\243\\351\\207\\210"
        "\\343\\201\\247\\343\\201\\215\\343\\201\\276\\343\\201\\233"
        "\\343\\202\\223\\343\\201\\247\\343\\201\\227\\343\\201\\237"
        "\\343\\200\\202\\343\\201\\235\\343\\202\\214\\343\\201\\257"
        "\\346\\233\\226\\346\\230\\247\\343\\201\\247\\343\\201\\202"
        "\\343\\202\\213\\343\\201\\213\\343\\200'"
    )
    assert _clean_mo_type(val) == (
        "GNU message catalog (little endian), revision 0.0, 349 messages"
    )


def test_mo_file_type_leaves_unrelated_types_unchanged():
    assert _clean_mo_type("ASCII text") == "ASCII text"
    assert _clean_mo_type("ELF 64-bit LSB executable") == "ELF 64-bit LSB executable"
