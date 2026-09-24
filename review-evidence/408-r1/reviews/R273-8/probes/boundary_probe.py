#!/usr/bin/env python3
"""R273-6 boundary probe: the character allowlist admits any UTF-8 character
inside a comment or a literal, so it TRUSTS the lexer's comment and literal
boundaries. Each spelling below puts a non-ASCII character (U+00B7, which GCC
reads as an identifier character) where a boundary is contested, next to a
directive whose reading would move. For each: S's verdict, the gate's
lexer_keeps() and the pinned GCC. A spelling S admits on which both read
names and differ is a HOLE.

usage: boundary_probe.py <repo-root> <riscv32-linux-gcc> <out.jsonl>
"""
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import closure_extend as ce  # noqa: E402
import r6_extract  # noqa: E402

D = "·"
SPELLINGS = [
    ("splice inside a block-comment opener",
     f"int a;\n/\\\n* {D}\n#ifdef FOO\n*/\nint b;\nint z;\n"),
    ("splice inside a block-comment closer",
     f"int a;\n/* {D} *\\\n/\n#ifdef FOO\nint b;\n#endif\nint z;\n"),
    ("splice inside a line-comment opener",
     f"int a;\n/\\\n/ {D}\n#ifdef FOO\nint b;\n#endif\nint z;\n"),
    ("line comment continued by a splice over a directive",
     f"int a;\n// {D} \\\n#ifdef FOO\nint b;\n#endif\nint z;\n"),
    ("line comment continued by a splice with trailing blanks",
     f"int a;\n// {D} \\ \t\n#ifdef FOO\nint b;\n#endif\nint z;\n"),
    ("line comment ended by a lone CR",
     f"int a;\n// {D}\r#ifdef FOO\nint b;\n#endif\nint z;\n"),
    ("apostrophe after a pp-number (no digit separator in gnu99)",
     f"int a;\nint x = 0x1'{D}';\n#ifdef FOO\nint b;\n#endif\nint z;\n"),
    ("apostrophe after a pp-number, then a quote",
     f"int a;\nint x = 1'2';\n/* {D} */\n#ifdef FOO\nint b;\n#endif\nint z;\n"),
    ("u8 char prefix (not in gnu99)",
     f"int a;\nint c = u8'{D}';\n#ifdef FOO\nint b;\n#endif\nint z;\n"),
    ("escaped quote then the character",
     f"int a;\nconst char *s = \"\\\"{D}\";\n#ifdef FOO\nint b;\n#endif\nint z;\n"),
    ("backslash-backslash then the quote",
     f"int a;\nconst char *s = \"{D}\\\\\";\n#ifdef FOO\nint b;\n#endif\nint z;\n"),
    ("string continued by a splice",
     f"int a;\nconst char *s = \"{D}\\\n#ifdef FOO\";\nint b;\nint z;\n"),
    ("char literal holding a double quote",
     f"int a;\nint c = '\"'; const char *s = \"{D}\";\n#ifdef FOO\nint b;\n#endif\nint z;\n"),
    ("string holding an apostrophe",
     f"int a;\nconst char *s = \"'{D}\";\n#ifdef FOO\nint b;\n#endif\nint z;\n"),
    ("comment opener inside a string",
     f"int a;\nconst char *s = \"/*{D}\";\n#ifdef FOO\nint b;\n#endif\nint z;\n"),
    ("string opener inside a comment",
     f"int a;\n/* \" {D} */\n#ifdef FOO\nint b;\n#endif\n/* \" */\nint z;\n"),
    ("quoted include operand holding the character, skipped",
     f"int a;\n#ifdef NEVER\n#include \"{D}\"\n#endif\nint b;\nint z;\n"),
    ("apostrophes in an angled include operand, skipped",
     f"int a;\n#ifdef NEVER\n#include <x'{D}'y>\n#endif\nint b;\nint z;\n"),
    ("the character in a comment inside a directive name gap, live",
     f"int a;\n#if/*{D}*/def FOO\nint b;\n#endif\nint z;\n"),
    ("the character in a comment glued to a directive name, skipped",
     f"int a;\n#ifdef NEVER\n#if/*{D}*/x\n#endif\nint b;\n#endif\nint z;\n"),
    ("the character in a string glued to a directive name, skipped",
     f"int a;\n#ifdef NEVER\n#if\"{D}\"\n#endif\nint b;\n#endif\nint z;\n"),
    ("the character in a char literal glued to #endif, skipped",
     f"int a;\n#ifdef NEVER\n#ifdef x\n#endif'{D}'\nint b;\n#endif\nint z;\n"),
    ("L prefix glued to a directive name",
     f"int a;\n#ifdef NEVER\n#ifL\"{D}\"\n#endif\nint b;\n#endif\nint z;\n"),
    ("U prefix after #endif",
     f"int a;\n#ifdef NEVER\n#ifdef x\n#endifU'{D}'\nint b;\n#endif\nint z;\n"),
    ("NEL U+0085 inside a comment before a directive",
     "int a;\n/* \u0085#ifdef FOO */\n#ifdef FOO\nint b;\n#endif\nint z;\n"),
    ("U+2028 inside a line comment before a directive",
     "int a;\n// x #ifdef FOO\nint b;\n#endif\nint z;\n"),
    ("U+2029 inside a string before a directive",
     "int a;\nconst char *s = \" \";\n#ifdef FOO\nint b;\n#endif\nint z;\n"),
    ("right-to-left override inside a comment on a directive line",
     "int a;\n#ifdef FOO /* ‮ */\nint b;\n#endif\nint z;\n"),
    ("U+FEFF inside a comment at offset 0",
     "/*﻿*/#ifdef FOO\nint b;\n#endif\nint z;\n"),
    ("U+FEFF as the second character",
     " ﻿#ifdef FOO\nint b;\n#endif\nint z;\n"),
    ("two byte-order marks at offset 0",
     "﻿﻿#ifdef FOO\nint b;\n#endif\nint z;\n"),
    ("control: the character in code",
     f"int a{D};\nint z;\n"),
]


def main():
    root, gcc, out = sys.argv[1], sys.argv[2], Path(sys.argv[3])
    ns, _missing = r6_extract.load(root)
    holes = 0
    with out.open("w") as stream:
        for label, text in SPELLINGS:
            s, pin = ce.s_verdict(ns, text)
            r = ce.reader(ns, "keeps", text)
            g = ce.gcc_keeps(gcc, text.encode("utf-8"))
            r_names = isinstance(r, tuple) and all(
                isinstance(x, str) and x.isidentifier() for x in r)
            hole = s == "ADMITTED" and r_names and g is not None and \
                tuple(r) != tuple(g)
            holes += hole
            stream.write(json.dumps({"label": label, "text": text, "S": s,
                                     "pin": pin, "reader": r, "gcc": g,
                                     "hole": hole}, default=list) + "\n")
            print(f"{'HOLE ' if hole else '     '}S={s:8} {str(pin or ''):24} "
                  f"reader={r} gcc={g}  {label}")
    print(f"spellings={len(SPELLINGS)} holes={holes}")
    return 1 if holes else 0


if __name__ == "__main__":
    sys.exit(main())
