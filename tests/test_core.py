from decimal import Decimal

import pytest

from unit_converter import ConversionError, categories, convert, format_result


@pytest.mark.parametrize(
    ("value", "source", "target", "expected"),
    [
        ("1", "km", "m", "1000"),
        ("100", "cm", "m", "1"),
        ("12", "in", "ft", "1"),
        ("1", "mi", "m", "1609.344"),
        ("1", "kg", "g", "1000"),
        ("1", "lb", "kg", "0.45359237"),
        ("2", "h", "min", "120"),
        ("1", "day", "s", "86400"),
        ("1", "L", "mL", "1000"),
        ("1", "gal_us", "L", "3.785411784"),
        ("1", "KiB", "B", "1024"),
        ("1", "GB", "MB", "1000"),
        ("0", "C", "K", "273.15"),
        ("32", "F", "C", "0"),
        ("100", "C", "F", "212"),
        ("273.15", "K", "C", "0"),
        ("-40", "C", "F", "-40"),
        ("0", "K", "K", "0"),
        ("0.1", "m", "cm", "10"),
    ],
)
def test_conversions(value, source, target, expected):
    assert convert(value, source, target) == Decimal(expected)


@pytest.mark.parametrize(
    ("value", "source", "target"),
    [
        ("1", "unknown", "m"),
        ("1", "m", "unknown"),
        ("1", "m", "kg"),
        ("hello", "m", "cm"),
        ("NaN", "m", "cm"),
        ("Infinity", "m", "cm"),
        ("-1", "K", "C"),
        ("-274", "C", "C"),
        ("-460", "F", "C"),
    ],
)
def test_invalid(value, source, target):
    with pytest.raises(ConversionError):
        convert(value, source, target)


def test_categories():
    result = categories()
    assert "length" in result
    assert "km" in result["length"]
    assert "C" in result["temperature"]


def test_format():
    assert format_result(Decimal("12.5000")) == "12.5"
    assert format_result(Decimal("12.567"), 2) == "12.57"
    assert format_result(Decimal("100")) == "100"


def test_bad_precision():
    with pytest.raises(ConversionError):
        format_result(Decimal("1"), 21)
