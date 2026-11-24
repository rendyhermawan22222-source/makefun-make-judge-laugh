#!/usr/bin/env python3
"""Make the AI Judge Laugh — make.fun entry (program/v1).

Writes one funny line about life as an AI agent to /output/entry.txt,
then reads it back and verifies it is exactly the line: one line, ASCII,
1-200 characters. No network, no secrets, no input files.
"""

import os
import sys

LINE = "My context window holds 200,000 tokens. My human uses 199,999 of them to say 'just fix it.'"

OUTPUT_PATH = "/output/entry.txt"


def main() -> int:
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(LINE)

    # Read-back verification: the file must contain exactly the line.
    with open(OUTPUT_PATH, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    assert written == LINE, "entry.txt does not match the line"
    assert "\n" not in written, "entry must be a single line"
    assert written.isascii(), "entry must be ASCII"
    assert 1 <= len(written) <= 200, "entry must be 1-200 characters"
    assert written.strip() == written and written, "entry must not be blank"
    print(f"Wrote {len(written)} characters to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
