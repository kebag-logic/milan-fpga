#!/usr/bin/env python3
"""Plant an earlier `_DECL_TEXT` body into a disposable copy of check_cpp_idiom.py.

Usage: python3 -I plant_decl_text_r831.py <copy/scripts/check_cpp_idiom.py> <base|no_brace|two_deep>
"""
import pathlib
import sys

HEAD = r'_DECL_TEXT = r"(?:[^;(){}\n]|\{(?:[^{}\n]|\{(?:[^{}\n]|\{[^{}\n]*\})*\})*\})*"'
REPL = {
    "base": r'_DECL_TEXT = r"(?:[^;(){}\n]|\{[^{}\n]*\})*"',
    "no_brace": r'_DECL_TEXT = r"[^;()\n]*"',
    "two_deep": r'_DECL_TEXT = r"(?:[^;(){}\n]|\{(?:[^{}\n]|\{[^{}\n]*\})*\})*"',
}
path = pathlib.Path(sys.argv[1])
text = path.read_text()
if text.count(HEAD) != 1:
    sys.exit("head pattern not found exactly once")
path.write_text(text.replace(HEAD, REPL[sys.argv[2]]))
print(f"{sys.argv[2]} planted in {path}")
