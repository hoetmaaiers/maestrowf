from contextlib import nullcontext as does_not_raise

import pytest
from pytest import raises
from rich.pretty import pprint
from maestrowf.utils import parse_version
from packaging.version import Version, InvalidVersion


@pytest.mark.parametrize(
    "version_string, expected_version, error",
    [
        ("0.49.0", Version("0.49.0"), does_not_raise()),
        ("0.50.0rc2", Version("0.50.0rc2"), does_not_raise()),
        ("0.49.0-225-g53e087510", Version("0.49.0"), does_not_raise()),
        ("2.0.0-rc.1+build.123", Version("2.0.0-rc.1+build.123"), does_not_raise()),
        ("2.0.0+build.1848", Version("2.0.0+build.1848"), does_not_raise()),
        ("1.2.3-0123", Version("1.2.3-0123"), does_not_raise()),
        ("1.2.3-0123.0123", None, raises(InvalidVersion)),
        ("1.0.0-alpha..1", None, raises(InvalidVersion)),
        ("01.1.1", Version("01.1.1"), does_not_raise()),
        ("9.8.7-whatever+meta+meta", None, raises(InvalidVersion)),
    ],
)
def test_parse_version(version_string, expected_version, error):
    """
    Test version parser that first applies pep440 style with a fallback
    to semantic version parser against subset of semver's tests
    and a few variants of flux core's version strings.
    """
    with error:
        version_parts = parse_version(version_string)
        assert version_parts == expected_version
