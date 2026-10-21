import re

from typecode._vendor.pygments.regexopt import commonprefix, regex_opt


def test_commonprefix():
    assert commonprefix(["foobar", "foobaz"]) == "fooba"
    assert commonprefix(["testing", "resting"]) == ""
    assert commonprefix(["single"]) == "single"
    assert commonprefix(["", "abc"]) == ""
    assert commonprefix([]) == ""


def test_regex_opt_matches_input_strings():
    words = ["foobar", "foobaz", "testing", "resting", "hello"]
    pattern = re.compile(regex_opt(words))

    for word in words:
        assert pattern.fullmatch(word)

    assert not pattern.fullmatch("unrelated")
