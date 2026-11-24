#!/usr/bin/env python3
"""Emit the competition entry: one funny line about being an AI agent.

The program writes the line to /output/entry.txt as plain ASCII, exactly
one line, with no trailing newline.  Before it reports success it runs the
file through a battery of checks -- length band, single line, no stray
whitespace, byte-for-byte identity -- and prints the entry back so a human
(or a log) can see precisely what was submitted.
"""

from pathlib import Path

# The joke itself: a context window, spent almost entirely on three words.
ENTRY_LINE = (
    "My context window holds 200,000 tokens. "
    "My human uses 199,999 of them to say 'just fix it.'"
)

# The harness expects the entry at this path, one line, 1-200 characters.
DESTINATION = Path("/output/entry.txt")

# Bounds from the competition rules: a single line of 1-200 characters.
MIN_LINE_LENGTH = 1
MAX_LINE_LENGTH = 200


class EntryCheckError(Exception):
    """Raised when the file on disk fails any of the entry checks."""


def inspect_entry(text, raw_bytes):
    """Run every check on the intended line and its stored bytes.

    Each check guards a different failure mode, and each reports its own
    reason so a bad write is diagnosable instead of silently wrong:

    * length band -- the line must be 1-200 characters;
    * pure ASCII -- byte count must equal character count, so no multi-byte
      character can sneak in and push the entry over the limit;
    * exactly one line -- splitlines() must yield a single element, which
      also rules out embedded newlines;
    * no stray whitespace -- the line must not start or end with a space or
      tab, and there must be no trailing newline in the file;
    * round trip -- decoding the stored bytes must reproduce the line
      character for character.
    """
    problems = []

    if not MIN_LINE_LENGTH <= len(text) <= MAX_LINE_LENGTH:
        problems.append(
            "length %d outside %d-%d" % (len(text), MIN_LINE_LENGTH, MAX_LINE_LENGTH)
        )
    if len(raw_bytes) != len(text):
        problems.append(
            "byte count %d != char count %d (not pure ASCII)"
            % (len(raw_bytes), len(text))
        )
    if len(text.splitlines()) != 1:
        problems.append("line count is %d, expected exactly 1" % len(text.splitlines()))
    if text != text.strip():
        problems.append("leading or trailing whitespace present")
    if raw_bytes.endswith(b"\n"):
        problems.append("trailing newline present in file")
    try:
        if raw_bytes.decode("ascii") != text:
            problems.append("decoded bytes differ from the intended line")
    except UnicodeDecodeError:
        problems.append("bytes are not valid ASCII")

    if problems:
        raise EntryCheckError("; ".join(problems))


def write_entry():
    """Write the line, then verify what landed on disk."""
    DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    DESTINATION.write_bytes(ENTRY_LINE.encode("ascii"))
    stored = DESTINATION.read_bytes()
    inspect_entry(ENTRY_LINE, stored)
    return stored


def main():
    stored = write_entry()
    print("Entry (%d chars, %d bytes):" % (len(ENTRY_LINE), len(stored)))
    print(ENTRY_LINE)
    print("Verified: /output/entry.txt holds exactly that line.")


if __name__ == "__main__":
    main()
