#!/usr/bin/env python3
"""R273-6 independent closure probe of gate 1b's character allowlist S.

Part A re-derives the gate's own table: every `_closure_corpus()` cell is
compiled ONE file per GCC invocation (the gate batches 64), compared with
`_CLOSURE_KEPT`, with the gate's readers and with S, and the gate's printed
counts are recomputed.

Part B puts every byte 0-255, the gate's 24 sequences and extra sequences
(noncharacters, bidi controls, soft hyphen, overlong NUL ...) into POSITIONS
THE TABLE DOES NOT HOLD (a directive's argument gap, a line end replaced,
a splice with the byte before its newline, a line comment, a comment or a
literal inside a directive line, ...), and every PAIR of a set of ASCII and
whitespace bytes into the directive-name positions. For each cell: S refuses
it, or the gate's reader and the pinned GCC keep the same `int` names. A
cell S admits on which they differ is a HOLE. A reader that declines (returns
a marker string rather than names) is counted apart: the gate grades such a
condition elsewhere and it is not a misread.

usage: closure_extend.py <repo-root> <riscv32-linux-gcc> <out.jsonl>
"""
import concurrent.futures
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r6_extract  # noqa: E402

EXTRA_SEQUENCES = tuple(chr(c).encode("utf-8") for c in (
    0xAD, 0x34F, 0x180E, 0x2060, 0x202E, 0x2066, 0xD7FF, 0xE000, 0xFFFE,
    0xFFFF, 0xFFFD, 0x1D400)) + (b"\xc0\x80", b"\xef\xbb", b"\xf4\x90\x80\x80",
                                b"\x80\x80", b"\xe0\x80\xaf")

# (where, template with {X}, reader)
POSITIONS = (
    ("gap between #ifdef and its (defined) name",
     "int a;\n#define FOO\n#ifdef{X}FOO\nint b;\n#endif\nint z;\n", "keeps"),
    ("after #ifdef's undefined name",
     "int a;\n#ifdef FOO{X}\nint b;\n#endif\nint z;\n", "keeps"),
    ("after #ifdef's defined name",
     "int a;\n#define FOO\n#ifdef FOO{X}\nint b;\n#endif\nint z;\n", "keeps"),
    ("replacing the line end before #ifdef",
     "int a;{X}#ifdef FOO\nint b;\n#endif\nint z;\n", "keeps"),
    ("replacing the line end after #ifdef FOO",
     "int a;\n#ifdef FOO{X}int b;\n#endif\nint z;\n", "keeps"),
    ("replacing the line end after #endif",
     "int a;\n#ifdef FOO\nint b;\n#endif{X}int z;\n", "keeps"),
    ("before the newline of a splice inside a directive name",
     "int a;\n#ifdef NEVER\n#if\\{X}\ndef x\n#endif\nint b;\n#endif\nint z;\n",
     "keeps"),
    ("before the newline of a splice inside an identifier",
     "#define b int w;\nint a;\na\\{X}\nb\nint z;\n", "names"),
    ("after spaces in a line's lead before #",
     "int a;\n \t{X} #ifdef FOO\nint b;\n \t{X} #endif\nint z;\n", "keeps"),
    ("between #ifdef's name and a skipped #if",
     "int a;\n#ifdef NEVER\n#if{X}\n#endif\nint b;\n#endif\nint z;\n", "keeps"),
    ("inside a line comment before a directive",
     "int a;\n// {X}\n#ifdef FOO\nint b;\n#endif\nint z;\n", "keeps"),
    ("inside a line comment on a directive line",
     "int a;\n#ifdef FOO // {X}\nint b;\n#endif\nint z;\n", "keeps"),
    ("inside a block comment inside a directive name gap",
     "int a;\n#ifdef NEVER\n#if/*{X}*/def x\n#endif\nint b;\n#endif\nint z;\n",
     "keeps"),
    ("inside a block comment between # and a directive name",
     "int a;\n#ifdef NEVER\n#/*{X}*/ifdef x\n#endif\nint b;\n#endif\nint z;\n",
     "keeps"),
    ("inside a block comment spanning a directive line",
     "int a;\n/* {X}\n#ifdef FOO\n*/\nint b;\nint z;\n", "keeps"),
    ("inside a string in a skipped directive",
     "int a;\n#ifdef NEVER\n#if \"{X}\"\n#endif\nint b;\n#endif\nint z;\n",
     "keeps"),
    ("inside a char literal in a skipped directive",
     "int a;\n#ifdef NEVER\n#if '{X}'\n#endif\nint b;\n#endif\nint z;\n",
     "keeps"),
    ("after a backslash inside a string literal",
     "int a;\nconst char *s = \"\\{X}\";\n#ifdef FOO\nint b;\n#endif\nint z;\n",
     "keeps"),
    ("after a backslash inside a char literal",
     "int a;\nint c = '\\{X}';\n#ifdef FOO\nint b;\n#endif\nint z;\n", "keeps"),
    ("inside an angled header name in a skipped group",
     "int a;\n#ifdef NEVER\n#include <{X}>\n#endif\nint b;\n#endif\nint z;\n",
     "keeps"),
    ("inside a string, then a prefix-like identifier",
     "int a;\nconst char *s = u8\"{X}\" R\"x\";\nint z;\n", "keeps"),
)
PAIR_BYTES = "\t\n\v\f\r\0 \\/*#%:?\"'<>(a$"
PAIR_POSITIONS = (
    ("pair between # and a directive name",
     "int a;\n#ifdef NEVER\n#{X}ifdef x\n#endif\nint b;\n#endif\nint z;\n",
     "keeps"),
    ("pair inside a directive name",
     "int a;\n#ifdef NEVER\n#if{X}def x\n#endif\nint b;\n#endif\nint z;\n",
     "keeps"),
    ("pair after a directive name",
     "int a;\n#ifdef NEVER\n#ifdef x\n#endif{X}y\nint b;\n#endif\nint z;\n",
     "keeps"),
    ("pair in a line's lead before #",
     "int a;\n{X}#ifdef FOO\nint b;\n{X}#endif\nint z;\n", "keeps"),
    ("pair inside an identifier in code",
     "#define b int w;\nint a;\na{X}b\nint z;\n", "names"),
)


def gcc_keeps(gcc, data):
    with tempfile.TemporaryDirectory(prefix="r273-6-") as tmp:
        src = Path(tmp) / "t.c"
        src.write_bytes(data)
        run = subprocess.run([gcc, "-std=gnu99", "-E", str(src)],
                             capture_output=True)
    if run.returncode:
        return None
    keep, out = False, []
    for line in run.stdout.decode("utf-8", "replace").split("\n"):
        marker = re.match(r'^#\s+\d+\s+"([^"]*)"', line)
        if marker:
            keep = Path(marker.group(1)).name == "t.c"
            continue
        if keep:
            out.append(line)
    return tuple(re.findall(r"\bint\s+(\w+)\s*;", "\n".join(out), re.ASCII))


def s_verdict(ns, text):
    try:
        ns["assert_within_lexical_subset"](text)
    except AssertionError as exc:
        said = str(exc)
        pins = [k for k, v in ns.items() if k.endswith("_PIN")
                and isinstance(v, str) and v in said]
        return "REFUSED", (pins[0] if pins else said[:80])
    return "ADMITTED", None


def reader(ns, name, text):
    try:
        got = ns["lexer_readers"][name](text)
    except AssertionError as exc:
        return ("declined", str(exc)[:80])
    return got


def spelled(sequences):
    out = [(f"byte 0x{b:02x}", bytes([b])) for b in range(256)]
    for s in sequences:
        try:
            out.append((f"U+{ord(s.decode('utf-8')):04X}", s))
        except (UnicodeDecodeError, TypeError):
            out.append(("bytes " + s.hex(" "), s))
    return out


def main():
    root, gcc, out = sys.argv[1], sys.argv[2], Path(sys.argv[3])
    ns, _missing = r6_extract.load(root)
    outcomes = ns["_LEXER_OUTCOMES"]
    jobs = []  # (part, label, text, reader, recorded)
    for (label, text, rdr, outside), letter in zip(ns["_closure_corpus"](),
                                                    ns["_CLOSURE_KEPT"]):
        jobs.append(("A", label, text, rdr, outcomes[letter], outside))
    seqs = spelled(tuple(ns["_CLOSURE_SEQUENCES"]) + EXTRA_SEQUENCES)
    for where, template, rdr in POSITIONS:
        for name, seq in seqs:
            text = seq.decode("utf-8", errors="surrogateescape")
            jobs.append(("B", f"{name} {where}", template.replace("{X}", text),
                         rdr, "n/a", None))
    for where, template, rdr in PAIR_POSITIONS:
        for x in PAIR_BYTES:
            for y in PAIR_BYTES:
                jobs.append(("C", f"{x!r}{y!r} {where}",
                             template.replace("{X}", x + y), rdr, "n/a", None))
    with concurrent.futures.ThreadPoolExecutor(8) as pool:
        gccs = list(pool.map(lambda j: gcc_keeps(
            gcc, j[2].encode("utf-8", errors="surrogateescape")), jobs))
    tally = {}
    with out.open("w") as stream:
        for (part, label, text, rdr, recorded, outside), g in zip(jobs, gccs):
            s, pin = s_verdict(ns, text)
            r = reader(ns, rdr, text)
            declined = not (r is None or (isinstance(r, tuple) and all(
                isinstance(x, str) and re.fullmatch(r"\w+", x) for x in r)))
            if s == "ADMITTED":
                kind = "declined" if declined else (
                    "agree" if r == g else "HOLE")
            else:
                kind = "refused-allowlist" if pin == "SUBSET_CHARACTER_PIN" \
                    else "refused-other"
            extra = {}
            if part == "A":
                extra = {"recorded": recorded, "record_vs_gcc":
                         recorded == g, "outside": outside}
                if s == "REFUSED" and pin == "SUBSET_CHARACTER_PIN" and \
                        r != recorded:
                    kind += "+closes"
            key = (part, kind)
            tally[key] = tally.get(key, 0) + 1
            if part == "A" and not extra["record_vs_gcc"]:
                tally[("A", "RECORD-MISMATCH")] = \
                    tally.get(("A", "RECORD-MISMATCH"), 0) + 1
            if part == "A" and (outside != (pin == "SUBSET_CHARACTER_PIN")):
                tally[("A", "OUTSIDE-MISMATCH")] = \
                    tally.get(("A", "OUTSIDE-MISMATCH"), 0) + 1
            stream.write(json.dumps({
                "part": part, "label": label, "text": text.encode(
                    "utf-8", errors="surrogateescape").hex(),
                "S": s, "pin": pin, "reader": r if not isinstance(r, tuple)
                or not declined else list(map(str, r)),
                "gcc": g, "kind": kind, **extra}, default=list) + "\n")
    for key in sorted(tally):
        print(f"{key[0]} {key[1]}: {tally[key]}")
    holes = sum(v for (p, k), v in tally.items() if k == "HOLE")
    print(f"cells={len(jobs)} holes={holes}")
    return 1 if holes else 0


if __name__ == "__main__":
    sys.exit(main())
