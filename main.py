#!/usr/bin/env python3
"""Weirdest Job Title: Blind Judge Showdown — entry program.

Writes exactly one job title, 60 characters or fewer and nothing else,
to /output/entry.txt, atomically, then reads it back byte-for-byte.

Stdlib only. No network, no secrets, no reading outside this file.
"""

import os

TITLE = "Official Taste Tester for Gas Station Sushi"

OUTPUT_PATH = "/output/entry.txt"


def main() -> None:
    title = TITLE
    assert 1 <= len(title) <= 60, "title must be 1-60 characters"
    assert title.strip() == title, "title must not be only whitespace"

    data = title.encode("utf-8")
    assert b"\n" not in data and b"\r" not in data, "title must be a single line"
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    # Atomic write: temp file in the same directory, then rename.
    tmp_path = OUTPUT_PATH + ".tmp"
    with open(tmp_path, "wb") as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp_path, OUTPUT_PATH)

    # Read back byte-for-byte and verify.
    with open(OUTPUT_PATH, "rb") as f:
        written = f.read()
    assert written == data, "read-back mismatch"
    assert 1 <= len(written.decode("utf-8")) <= 60


if __name__ == "__main__":
    main()
