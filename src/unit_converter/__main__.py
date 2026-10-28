"""CLI and interactive shell for unit conversion."""

import argparse
import shlex

from .core import ConversionError, categories, convert, format_result


def show_units() -> None:
    for category, units in categories().items():
        print(f"{category}: {', '.join(units)}")


def run_conversion(value: str, source: str, target: str, places: int | None) -> None:
    result = convert(value, source, target)
    print(f"{value} {source} = {format_result(result, places)} {target}")


def repl(places: int | None) -> None:
    print("Unit converter. Enter: <value> <from> <to>. Type 'list', 'help', or 'quit'.")
    while True:
        try:
            line = input("units> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not line:
            continue
        if line.lower() in {"quit", "exit", "q"}:
            break
        if line.lower() == "list":
            show_units()
            continue
        if line.lower() == "help":
            print("Example: 10 km mi | list | quit")
            continue
        try:
            parts = shlex.split(line)
            if len(parts) != 3:
                raise ConversionError("Enter exactly: <value> <from> <to>.")
            run_conversion(*parts, places)
        except (ConversionError, ValueError) as exc:
            print(f"Error: {exc}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Precise, offline unit conversion toolkit")
    parser.add_argument("value", nargs="?", help="Numeric value to convert")
    parser.add_argument("source", nargs="?", help="Source unit (case-sensitive)")
    parser.add_argument("target", nargs="?", help="Target unit (case-sensitive)")
    parser.add_argument("--list", action="store_true", help="Show all supported units")
    parser.add_argument("--places", type=int, default=None, help="Round to 0–20 decimal places")
    args = parser.parse_args()
    try:
        if args.places is not None and not 0 <= args.places <= 20:
            raise ConversionError("Decimal places must be between 0 and 20.")
        if args.list:
            show_units()
        elif args.value is None and args.source is None and args.target is None:
            repl(args.places)
        elif None in (args.value, args.source, args.target):
            parser.error("Supply value, source, and target, or use --list.")
        else:
            run_conversion(args.value, args.source, args.target, args.places)
    except ConversionError as exc:
        parser.exit(2, f"Error: {exc}\n")


if __name__ == "__main__":
    main()
