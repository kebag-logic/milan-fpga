#!/usr/bin/env python3
"""Compare gate 1b's own directive readers (loaded unmodified from the
checkout) with the pinned GCC on (a) the gate's recorded corpus and (b)
spellings outside it. Prints one JSON line per case.

usage: lexer_probe.py <repo-root> <riscv32-linux-gcc>
"""
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lexer_extract  # noqa: E402

EXTRA = (
    ("BOM then #ifdef at file start",
     "﻿#ifdef FOO\nint b;\n#endif\nint z;\n"),
    ("BOM then #define at file start",
     "﻿#define FOO\n#ifdef FOO\nint b;\n#endif\nint z;\n"),
    ("a multi-line comment between # and the name",
     "int a;\n#/* c\n */ifdef FOO\nint b;\n#endif\nint z;\n"),
    ("a lone CR inside a block comment before #",
     "int a;\n/* c\r c */ #ifdef FOO\nint b;\n#endif\nint z;\n"),
    ("CRLF splice inside #else",
     "#ifdef FOO\nint a;\n#el\\\r\nse\nint b;\n#endif\nint z;\n"),
    ("a splice with trailing blanks and CRLF inside #endif",
     "int a;\n#ifdef FOO\nint b;\n#end\\ \t\r\nif\nint z;\n"),
    ("a NUL between / and *",
     "int a; /\x00* c */\n#ifdef FOO\nint b;\n#endif\nint z;\n"),
    ("a string whose escaped backslash is a splice",
     "const char *s = \"a\\\\\n#ifdef FOO\";\nint b;\nint z;\n"),
    ("a form feed and a comment after #",
     "int a;\n#\f/* c */ifdef FOO\nint b;\n#endif\nint z;\n"),
    ("a directive after a line of only form feeds",
     "int a;\n\f\f\n#ifdef FOO\nint b;\n#endif\nint z;\n"),
    ("a comment then a NUL then #",
     "int a;\n/* c */\x00#ifdef FOO\nint b;\n#endif\nint z;\n"),
    ("a splice then a form feed before #",
     "int a;\n\\\n\f#ifdef FOO\nint b;\n#endif\nint z;\n"),
    ("a NEL (U+0085) before #",
     "int a;\n\u0085#ifdef FOO\nint b;\n\u0085#endif\nint z;\n"),
    ("a ZWNBSP (U+FEFF) mid-file before #",
     "int a;\n﻿#ifdef FOO\nint b;\n﻿#endif\nint z;\n"),
    ("a Ctrl-Z before #",
     "int a;\n\x1a#ifdef FOO\nint b;\n\x1a#endif\nint z;\n"),
    ("#elifdef behind a vertical tab",
     "#ifdef BAR\nint a;\n\v#elifdef FOO\nint b;\n#else\nint c;\n#endif\n"
     "int z;\n"),
    ("#ifndef behind a CRLF and a form feed",
     "int a;\r\n\f#ifndef FOO\r\nint b;\r\n#endif\r\nint z;\r\n"),
    ("an apostrophe in a #define then a directive",
     "#define Q 'a'\n#ifdef FOO\nint b;\n#endif\nint z;\n"),
    ("a // comment continued by a splice after CRLF",
     "int a;\r\n// c \\\r\n#ifdef FOO\r\nint b;\r\n#endif\r\nint z;\r\n"),
    ("a splice inside the #define name with CR",
     "#define F\\\rOO\n#ifdef FOO\nint b;\n#endif\nint z;\n"),
)


def own_ints(unit, name):
    keep, out = False, []
    for line in unit.split("\n"):
        marker = re.match(r'^#\s+\d+\s+"([^"]*)"', line)
        if marker:
            keep = Path(marker.group(1)).name == name
            continue
        if keep:
            out.append(line)
    return tuple(re.findall(r"\bint\s+(\w+)\s*;", "\n".join(out)))


def gcc_keeps(gcc, text):
    with tempfile.TemporaryDirectory(prefix="r273-lex-") as tmp:
        src = Path(tmp) / "milan_baremetal.c"
        src.write_bytes(text.encode("utf-8"))
        run = subprocess.run([gcc, "-std=gnu99", "-E", str(src)],
                             capture_output=True)
    if run.returncode:
        return None, run.stderr.decode("utf-8", "replace")[-300:]
    return own_ints(run.stdout.decode("utf-8", "replace"), src.name), ""


def main():
    root, gcc = sys.argv[1], sys.argv[2]
    ns, missing = lexer_extract.load(root)
    if missing:
        print(json.dumps({"missing": sorted(missing)}))
    keeps = ns["lexer_keeps"]
    bad = 0
    for label, text, recorded in ns["lexer_corpus"]:
        gate = keeps(text)
        gcc_read, _ = gcc_keeps(gcc, text)
        ok = gate == (None if recorded is None else tuple(recorded)) and \
            gcc_read == (None if recorded is None else tuple(recorded))
        bad += not ok
        print(json.dumps({"set": "corpus", "label": label, "recorded":
                          recorded, "gate": gate, "gcc": gcc_read,
                          "agree": ok}))
    for label, text in EXTRA:
        gate = keeps(text)
        lexed, findings = ns["c_lexed"](text)
        gcc_read, err = gcc_keeps(gcc, text)
        refused_first = bool(findings) or bool(
            re.search(r"\?\?[=/'()!<>-]", text))
        print(json.dumps({"set": "extra", "label": label, "text": text,
                          "gate": gate, "gcc": gcc_read,
                          "gate_refuses_before_readers": refused_first,
                          "findings": findings,
                          "agree": gate == gcc_read, "gcc_err": err}))
    print(json.dumps({"corpus_disagreements": bad}))


if __name__ == "__main__":
    main()
