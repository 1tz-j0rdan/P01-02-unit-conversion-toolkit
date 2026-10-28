# P01-02 — Unit Conversion Toolkit

A zero-runtime-dependency Python unit converter with a CLI, interactive shell, and reusable API. Built for Phase 1 of the Ultimate Technical Engineering Roadmap.

## Features

- **6 categories:** length, mass, time, volume, data storage, and temperature.
- **32 unit symbols**, including metric/imperial units, decimal/binary bytes, and Celsius/Fahrenheit/Kelvin.
- Uses Python's `Decimal` for precise numeric input and conversion factors.
- Rejects incompatible categories, unknown units, non-finite values, and temperatures below absolute zero.
- Supports one-shot commands and an interactive prompt.
- Supports optional rounding (`--places`).
- Includes automated tests, lint configuration, and GitHub Actions CI.

**Unit symbols are case-sensitive.** For example, `m` is meters and `min` is minutes. Volume units `gal_us`, `qt_us`, and `cup_us` are US customary units. `KB` is 1,000 bytes; `KiB` is 1,024 bytes. Temperature values are absolute temperatures, not temperature *differences*.

## Installation (Windows PowerShell)

```powershell
py -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

Alternatively, use `.\.venv\Scripts\python.exe` directly without activation.

## Usage

```powershell
python -m unit_converter --list
python -m unit_converter 10 km mi --places 4
python -m unit_converter 32 F C
python -m unit_converter 1 GiB MB
python -m unit_converter
```

Interactive mode:

```text
units> 5 mi km
5 mi = 8.04672 km
units> list
units> quit
```

Installed entry point: `unit-convert 10 km mi`.

## Python API

```python
from unit_converter import convert

print(convert("10", "km", "m"))  # 10000
```

## Tests and quality checks

```powershell
python -m pytest -v
python -m ruff check .
```

## Design notes

- Conversion factors are defined relative to a base unit per category.
- Temperature is handled separately because it needs an offset as well as scaling.
- This is an educational engineering project, not a certified metrology tool.
- Results depend on Decimal's active arithmetic context (default precision: 28 significant digits).

## Learning objectives

Python packaging, dictionaries, dataclasses, type hints, exceptions, decimal arithmetic, CLI design, unit tests, and CI.

## Roadmap

- [x] v0.1.0: CLI, six categories, tests, lint, CI
- [ ] v0.2.0: aliases and user-defined conversion profiles
- [ ] v0.3.0: JSON batch input and CSV export
