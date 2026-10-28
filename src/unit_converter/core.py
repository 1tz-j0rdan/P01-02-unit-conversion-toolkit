"""Unit conversions using Decimal arithmetic and explicit unit definitions."""
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation


class ConversionError(ValueError):
    """Raised for unsupported or invalid conversions."""


@dataclass(frozen=True)
class Unit:
    category: str
    factor: Decimal
    offset: Decimal = Decimal("0")


def _d(value: str) -> Decimal:
    return Decimal(value)


UNITS: dict[str, Unit] = {
    "m": Unit("length", _d("1")),
    "km": Unit("length", _d("1000")),
    "cm": Unit("length", _d("0.01")),
    "mm": Unit("length", _d("0.001")),
    "mi": Unit("length", _d("1609.344")),
    "yd": Unit("length", _d("0.9144")),
    "ft": Unit("length", _d("0.3048")),
    "in": Unit("length", _d("0.0254")),
    "kg": Unit("mass", _d("1")),
    "g": Unit("mass", _d("0.001")),
    "mg": Unit("mass", _d("0.000001")),
    "lb": Unit("mass", _d("0.45359237")),
    "oz": Unit("mass", _d("0.028349523125")),
    "s": Unit("time", _d("1")),
    "min": Unit("time", _d("60")),
    "h": Unit("time", _d("3600")),
    "day": Unit("time", _d("86400")),
    "L": Unit("volume", _d("1")),
    "mL": Unit("volume", _d("0.001")),
    "gal_us": Unit("volume", _d("3.785411784")),
    "qt_us": Unit("volume", _d("0.946352946")),
    "cup_us": Unit("volume", _d("0.2365882365")),
    "B": Unit("data", _d("1")),
    "KB": Unit("data", _d("1000")),
    "MB": Unit("data", _d("1000000")),
    "GB": Unit("data", _d("1000000000")),
    "KiB": Unit("data", _d("1024")),
    "MiB": Unit("data", _d("1048576")),
    "GiB": Unit("data", _d("1073741824")),
    "K": Unit("temperature", _d("1")),
    "C": Unit("temperature", _d("1"), _d("273.15")),
    "F": Unit("temperature", _d("0.5555555555555555555555555556"), _d("255.3722222222222222222222222")),
}


def convert(value: str | int | float | Decimal, source: str, target: str) -> Decimal:
    """Convert between compatible units; preserve precision with Decimal."""
    if source not in UNITS:
        raise ConversionError(f"Unknown source unit: {source}. Use 'list' to see units.")
    if target not in UNITS:
        raise ConversionError(f"Unknown target unit: {target}. Use 'list' to see units.")
    src, dst = UNITS[source], UNITS[target]
    if src.category != dst.category:
        raise ConversionError(f"Incompatible categories: {src.category} and {dst.category}.")
    try:
        amount = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ConversionError(f"Invalid numeric value: {value!r}.") from exc
    if not amount.is_finite():
        raise ConversionError("Value must be finite.")
    if source == target:
        result = amount
    elif src.category == "temperature":
        if source == "F":
            kelvin = (amount - Decimal("32")) * Decimal("5") / Decimal("9") + Decimal("273.15")
        else:
            kelvin = amount * src.factor + src.offset
        if target == "F":
            result = (kelvin - Decimal("273.15")) * Decimal("9") / Decimal("5") + Decimal("32")
        else:
            result = (kelvin - dst.offset) / dst.factor
        if kelvin < 0:
            raise ConversionError("Temperature cannot be below absolute zero.")
    else:
        result = amount * src.factor / dst.factor
    if src.category == "temperature" and source == target:
        kelvin = amount if source == "K" else (amount + Decimal("273.15") if source == "C" else (amount - Decimal("32")) * Decimal("5") / Decimal("9") + Decimal("273.15"))
        if kelvin < 0:
            raise ConversionError("Temperature cannot be below absolute zero.")
    return result


def categories() -> dict[str, list[str]]:
    """Return available units grouped by category."""
    result: dict[str, list[str]] = {}
    for name, unit in UNITS.items():
        result.setdefault(unit.category, []).append(name)
    return {key: sorted(names) for key, names in sorted(result.items())}


def format_result(result: Decimal, places: int | None = None) -> str:
    """Format a conversion without unnecessary trailing zeros."""
    if places is not None:
        if not 0 <= places <= 20:
            raise ConversionError("Decimal places must be between 0 and 20.")
        result = round(result, places)
    return format(result, "f").rstrip("0").rstrip(".") if "." in format(result, "f") else format(result, "f")
