"""R272-5: S's verdict, and the allowlist's MESSAGE, on files and texts.

At the accepted-loop hook (probe_gate1b.py, --absent is enough: S is text):
  * each file named in R272_FILES (colon-separated) is read as the gate reads
    the firmware (UTF-8, surrogateescape) and put to
    assert_within_lexical_subset(); the verdict and message are printed;
  * crafted texts check that the refusal NAMES the right character and line
    when a splice, CRLF, lone CR or comment precedes the character (the
    message indexes the source with the code text's offsets);
  * a within-S text with every modelled whitespace, and non-ASCII in a
    comment, a string and a character literal, is admitted.
Grades no firmware; returns no cases."""
import os
from pathlib import Path

CRAFTED = (
    ("U+00E9 on line 3 after a splice and CRLFs",
     "int a;\r\nint b; \\\r\nint cé;\n", "U+00E9", "line 3"),
    ("U+00B7 on line 4 after lone CRs",
     "int a;\rint b;\r/* é */\rint c·d;\n", "U+00B7", "line 4"),
    ("U+2028 on line 2 after a multi-line comment",
     "/* a\n */ int x ;\n", "U+2028", "line 2"),
    ("U+FEFF at offset 0", "﻿int z;\n", "U+FEFF", "line 1"),
    ("U+FEFF mid-file on line 2", "int a;\n﻿int z;\n", "U+FEFF",
     "line 2"),
    ("DEL 0x7f on line 2", "int a;\nint b\x7f;\n", "U+007F", "line 2"),
    ("undecoded 0xff on line 2 in a string", "int a;\nchar *s = \"\udcff\";\n",
     "0xff", "line 2"),
)
ADMITTED = (
    "int a;\r\n\t\v\f\0#ifdef FOO\rint b;\n#endif\n/* · \u0085 */\n"
    "//  ‮ \\\nstill comment é\nconst char *s = \"é\\\"‿\";"
    "\nint c = '²';\nint z;\n",
)


def cases(ns):
    check = ns["assert_within_lexical_subset"]
    pin = ns["SUBSET_CHARACTER_PIN"]
    for name in filter(None, os.environ.get("R272_FILES", "").split(":")):
        text = Path(name).read_text(encoding="utf-8", errors="surrogateescape")
        try:
            check(text)
            print(f"SCHECK ADMITTED {Path(name).name}", flush=True)
        except AssertionError as exc:
            print(f"SCHECK REFUSED {Path(name).name} allowlist="
                  f"{pin in str(exc)}: {str(exc)[:160]}", flush=True)
    for label, text, char, line in CRAFTED:
        try:
            check(text)
            print(f"MSG FAIL (admitted) {label}", flush=True)
        except AssertionError as exc:
            msg = str(exc)
            ok = pin in msg and char in msg and f"{line})" in msg or \
                (pin in msg and char in msg and f"{line}" in msg)
            print(f"MSG {'OK' if ok else 'WRONG'} {label}: {msg[:140]}",
                  flush=True)
    for text in ADMITTED:
        try:
            check(text)
            print("ADMITTED-CONTROL OK", flush=True)
        except AssertionError as exc:
            print(f"ADMITTED-CONTROL REFUSED: {exc}", flush=True)
    return ()
