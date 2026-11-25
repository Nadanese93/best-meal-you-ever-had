"""Write the contest entry for "The Best Meal You Ever Had" to entry.txt.

Deterministic: no network, no randomness, no clock. The entry is a single
fixed sentence; main.py validates it against the contest gate (1-200
characters, non-blank, single line) before writing it as UTF-8 with no
trailing newline.
"""

import os
import sys


class LengthError(ValueError):
    """Entry is outside the 1-200 character gate."""


class BlankError(ValueError):
    """Entry is blank or whitespace-only."""


class MultiLineError(ValueError):
    """Entry contains more than one line."""


def validate(entry: str) -> None:
    if not (1 <= len(entry) <= 200):
        raise LengthError(f"entry must be 1-200 characters, got {len(entry)}")
    if not entry.strip():
        raise BlankError("entry must not be blank")
    if "\n" in entry or "\r" in entry:
        raise MultiLineError("entry must be a single line")

ENTRY = (
    "The best meal I ever had was cold fried chicken behind the buffet "
    "at my cousin's wedding, the bride crying next door while I licked "
    "salt off my fingers and swore it was my first piece."
)


def main() -> int:
    try:
        output_dir = os.environ["MAKEFUN_OUTPUT_DIR"]
    except KeyError:
        print("error: MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1

    validate(ENTRY)

    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)

    # Read-back verification: the bytes on disk must be exactly the entry.
    with open(path, "rb") as f:
        written = f.read()
    if written != ENTRY.encode("utf-8"):
        raise ValueError("read-back mismatch: entry.txt bytes differ from entry")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
