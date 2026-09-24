"""R272-5 closure probe, run inside gate 1b's own namespace by
scripts/r1/probe_gate1b.py (anchor: accepted). It grades NO firmware through
assert_boot_contract(); it writes a table and returns no cases.

Part A re-measures the gate's own 2520-cell character-closure table: every
cell template of `_CLOSURE_POSITIONS` crossed with every byte 0-255 and every
sequence of `_CLOSURE_SEQUENCES`, GCC's answer taken HERE by one direct
`gcc -std=gnu99 -E -P` per cell (not by the gate's lexer_measured()), then
compared with `_CLOSURE_KEPT`, with S's verdict and with the gate's readers.

Part B is this reviewer's own extension: positions the table does not hold,
at comment and literal BOUNDARIES (a byte splitting `/*`, `*/`, `//`, between
a backslash and a line end in a comment and in code, after an escape
backslash in a string and a character literal, between a raw prefix and its
quote, before a quote after a digit, at end of file), crossed with every byte
0-255, the gate's 24 sequences, 10 more of this reviewer's, and the empty
string. Payload variants put U+00B7 where the lexer's comment would hide it.

Environment: R272_GCC = the pinned riscv32-linux-gcc; R272_OUT = output dir.
"""
import concurrent.futures
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path

INT_RE = re.compile(r"\bint\s+(\w+)\s*;", re.ASCII)

EXTRA = (b"", b"\xef\xbf\xbe", b"\xc2\xad", b"\xe2\x81\xa0", b"\xe2\x80\xae",
         b"\xf4\x90\x80\x80", b"\x80", b"\xc2", b"\xe0\x80\x80",
         "\u00b7".encode(), b"\\\n")

BOUNDARY = (
    ("B1 byte splitting a block-comment opener",
     "int a;\n/{X}* \n#define FOO\n */\n#ifdef FOO\nint b;\n#endif\nint z;\n",
     True),
    ("B1p ... with U+00B7 where the comment would be",
     "int a;\n/{X}* \u00b7\n#define FOO\n */\n#ifdef FOO\nint b;\n#endif\n"
     "int z;\n", True),
    ("B2 byte splitting a block-comment closer",
     "int a;\n/* c *{X}/\n#define FOO\n/* */\n#ifdef FOO\nint b;\n#endif\n"
     "int z;\n", False),
    ("B3 byte splitting a line-comment opener",
     "int a;\n/{X}/ /*\n#define FOO\n// */\n#ifdef FOO\nint b;\n#endif\n"
     "int z;\n", True),
    ("B3p ... with U+00B7 where the line comment would be",
     "int a;\n/{X}/ \u00b7 /*\n#define FOO\n// */\n#ifdef FOO\nint b;\n"
     "#endif\nint z;\n", True),
    ("B4 byte ending a line comment",
     "int a;\n// c{X}\n#define FOO\n#ifdef FOO\nint b;\n#endif\nint z;\n",
     False),
    ("B5 byte between a backslash and the line end of a line comment",
     "int a;\n// c\\{X}\n#define FOO\n#ifdef FOO\nint b;\n#endif\nint z;\n",
     False),
    ("B6 byte between a backslash and the line end in a #define",
     "int a;\n#define BAR \\{X}\n#define FOO\n#ifdef FOO\nint b;\n#endif\n"
     "int z;\n", True),
    ("B7 byte after an escape backslash in a string literal",
     "int a;\nconst char *s = \"\\{X}\"; /* \";\n#define FOO\n// */\n"
     "#ifdef FOO\nint b;\n#endif\nint z;\n", False),
    ("B8 byte after an escape backslash in a character literal",
     "int a;\nint c = '\\{X}'; /* ';\n#define FOO\n// */\n#ifdef FOO\n"
     "int b;\n#endif\nint z;\n", False),
    ("B9 byte between a raw prefix and its quote",
     "int a;\nconst char *s = R{X}\"x(\";\n#define FOO\n// )x\";\n"
     "#ifdef FOO\nint b;\n#endif\nint z;\n", True),
    ("B10 byte before a quote after a digit (digit separator?)",
     "int a;\nint n = 1{X}'2; /* ';\n#define FOO\n// */\n#ifdef FOO\n"
     "int b;\n#endif\nint z;\n", True),
    ("B11 byte at end of file after a line comment",
     "int a;\n#ifdef FOO\nint b;\n#endif\nint z;\n// c{X}", False),
    ("B12 byte at end of file in code",
     "int a;\n#ifdef FOO\nint b;\n#endif\nint z;\n{X}", True),
    ("B13 byte before a string's closing quote then a comment opener",
     "int a;\nconst char *s = \"{X}\"; /* \";\n#define FOO\n// */\n"
     "#ifdef FOO\nint b;\n#endif\nint z;\n", False),
    ("B14 byte after an #include-like < in skipped code",
     "int a;\n#ifdef NEVER\n#include <{X}/*>\n#endif\n#define FOO\n// */\n"
     "#ifdef FOO\nint b;\n#endif\nint z;\n", True),
)


def gcc_keeps(gcc, texts):
    def one(item):
        index, text = item
        with tempfile.TemporaryDirectory(prefix="r272-5-") as tmp:
            path = Path(tmp) / f"c{index:05d}.c"
            path.write_bytes(text.encode("utf-8", errors="surrogateescape"))
            run = subprocess.run([gcc, "-std=gnu99", "-E", "-P", str(path)],
                                 capture_output=True)
        if run.returncode:
            return None, run.stdout
        return tuple(INT_RE.findall(run.stdout.decode("utf-8", "replace"))), \
            run.stdout
    with concurrent.futures.ThreadPoolExecutor(8) as pool:
        return list(pool.map(one, enumerate(texts)))


def s_verdict(ns, text):
    try:
        ns["assert_within_lexical_subset"](text)
    except AssertionError as exc:
        return "allowlist" if ns["SUBSET_CHARACTER_PIN"] in str(exc) \
            else "other:" + str(exc)[:60]
    return "admitted"


def reader(ns, name, text):
    try:
        return ns["lexer_readers"][name](text)
    except Exception as exc:  # a reader that throws is recorded, not hidden
        return ("EXC", type(exc).__name__)


def cases(ns):
    tb = ns  # gate locals; module-level names come from the module globals
    import test_builder as mod
    gcc = os.environ["R272_GCC"]
    out = Path(os.environ["R272_OUT"])
    out.mkdir(parents=True, exist_ok=True)
    outcomes = mod._LEXER_OUTCOMES
    # ---- Part A: the gate's own table, re-measured independently
    spelled = [(f"byte 0x{b:02x}", bytes([b])) for b in range(256)]
    for seq in mod._CLOSURE_SEQUENCES:
        try:
            spelled.append((f"U+{ord(seq.decode('utf-8')):04X}", seq))
        except UnicodeDecodeError:
            spelled.append(("bytes " + seq.hex(" "), seq))
    cells = []
    for where, template, rd, _in_code in mod._CLOSURE_POSITIONS:
        for name, seq in spelled:
            text = template.replace(
                "{X}", seq.decode("utf-8", errors="surrogateescape"))
            cells.append((f"{name} {where}", text, rd))
    assert len(cells) == len(mod._CLOSURE_KEPT) == 2520, len(cells)
    measured = gcc_keeps(gcc, [t for _l, t, _r in cells])
    counts = {"allowlist": 0, "other": 0, "admitted": 0,
              "recorded_vs_gcc_mismatch": 0, "admitted_disagree": 0,
              "allowlist_reader_differs": 0}
    rows = []
    for (label, text, rd), letter, (found, _stdout) in zip(
            cells, mod._CLOSURE_KEPT, measured):
        recorded = outcomes[letter]
        verdict = s_verdict(tb, text)
        read = reader(tb, rd, text)
        kind = verdict.split(":")[0]
        counts[kind] += 1
        if found != recorded:
            counts["recorded_vs_gcc_mismatch"] += 1
        if kind == "admitted" and read != found:
            counts["admitted_disagree"] += 1
        if kind == "allowlist" and read != found:
            counts["allowlist_reader_differs"] += 1
        rows.append({"cell": label, "S": verdict, "reader": read,
                     "gcc": found, "recorded": recorded})
    (out / "partA-closure-remeasured.json").write_text(
        json.dumps({"counts": counts, "rows": rows}, indent=0,
                   default=str) + "\n", encoding="utf-8")
    print("PART A", json.dumps(counts), flush=True)
    # ---- Part B: boundary positions the table does not hold
    xs = [(f"byte 0x{b:02x}", bytes([b])) for b in range(256)]
    xs += [(n, s) for n, s in spelled[256:]]
    xs += [("extra " + (s.hex(" ") or "EMPTY"), s) for s in EXTRA]
    bcells = []
    for where, template, in_code in BOUNDARY:
        for name, seq in xs:
            text = template.replace(
                "{X}", seq.decode("utf-8", errors="surrogateescape"))
            bcells.append((f"{name} | {where}", text, in_code))
    bmeasured = gcc_keeps(gcc, [t for _l, t, _c in bcells])
    bcounts = {"allowlist": 0, "other": 0, "admitted": 0,
               "admitted_disagree": 0, "payload_in_code_admitted": 0}
    brows, holes = [], []
    for (label, text, _in_code), (found, stdout) in zip(bcells, bmeasured):
        verdict = s_verdict(tb, text)
        read = reader(tb, "keeps", text)
        kind = verdict.split(":")[0]
        bcounts[kind] += 1
        payload = "\u00b7".encode() in (stdout or b"") and \
            label.split(" | ")[1].startswith(("B1p", "B3p"))
        row = {"cell": label, "S": verdict, "reader": read, "gcc": found,
               "payload_in_gcc_output": payload}
        brows.append(row)
        if kind == "admitted" and read != found:
            bcounts["admitted_disagree"] += 1
            holes.append(row)
        if kind == "admitted" and payload:
            bcounts["payload_in_code_admitted"] += 1
            holes.append(row)
    (out / "partB-boundary.json").write_text(
        json.dumps({"counts": bcounts, "holes": holes, "rows": brows},
                   indent=0, default=str) + "\n", encoding="utf-8")
    print("PART B", len(bcells), "cells", json.dumps(bcounts), flush=True)
    for row in holes[:40]:
        print("  HOLE", json.dumps(row, default=str)[:300], flush=True)
    return ()
