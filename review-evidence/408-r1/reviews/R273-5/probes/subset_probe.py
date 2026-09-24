#!/usr/bin/env python3
"""R273-5 differential probe of gate 1b's lexical subset S.

For each spelling: does S (assert_within_lexical_subset, unmodified) refuse
it; if S admits it, do the gate's directive readers (lexer_keeps, the reader
the lexer corpus measures) keep the same `int` names as the pinned GCC at
-std=gnu99 -E? A spelling S admits on which the two disagree is a hole in
"exact on S; outside S refused".

usage: subset_probe.py <repo-root> <riscv32-linux-gcc> <out.jsonl>
"""
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parent))
import subset_extract  # noqa: E402

# A mis-nest shape: FOO and BAR are never defined. If a reader reads the
# `{0}` line as `#if` and the `{1}` line as `#endif` while GCC reads both as
# unknown directives in skipped code, GCC keeps `b` and the reader drops it.
MISNEST = ("int a;\n#ifdef FOO\n#if{0}x\n#endif\nint b;\n#ifdef BAR\n"
           "#endif{0}y\n#endif\nint z;\n")
# The reverse: GCC reads `#if` then a stray character, a nested #if, and
# the reader reads no directive: the reader keeps `b` and GCC does not.
NEST = ("int a;\n#ifdef FOO\n#if{0}\n#endif\nint b;\n#endif\nint z;\n")

CHARS = [
    ("U+0024 dollar (control, refused by S)", "$"),
    ("U+00B7 middle dot", "·"),
    ("U+0387 greek ano teleia", "·"),
    ("U+203F undertie", "‿"),
    ("U+00B5 micro sign", "µ"),
    ("U+00E9 e acute", "é"),
    ("U+00B2 superscript two", "²"),
    ("U+2460 circled one", "①"),
    ("U+00A0 no-break space", " "),
    ("U+0661 arabic-indic one", "١"),
    ("U+FF21 fullwidth A", "Ａ"),
]
SPELLINGS = []
for name, ch in CHARS:
    SPELLINGS.append((f"misnest {name}", MISNEST.format(ch)))
    SPELLINGS.append((f"nest {name}", NEST.format(ch)))
SPELLINGS += [
    ("control: plain misnest with nothing extra", MISNEST.format("")),
    ("control: the S corpus's own within-S firmware",
     "int a;\n#ifdef FOO\nint b;\n#endif\nint z;\n"),
]


def gcc_ints(gcc, text):
    with tempfile.TemporaryDirectory(prefix="r273-5-oracle-") as tmp:
        src = Path(tmp) / "t.c"
        src.write_bytes(text.encode("utf-8"))
        run = subprocess.run([gcc, "-std=gnu99", "-E", str(src)],
                             capture_output=True)
    err = run.stderr.decode("utf-8", "replace")
    if run.returncode:
        return None, err
    keep, out = False, []
    for line in run.stdout.decode("utf-8", "replace").split("\n"):
        marker = re.match(r'^#\s+\d+\s+"([^"]*)"', line)
        if marker:
            keep = Path(marker.group(1)).name == "t.c"
            continue
        if keep:
            out.append(line)
    return tuple(re.findall(r"\bint\s+(\w+)\s*;", "\n".join(out))), err


def main():
    root, gcc, out = sys.argv[1], sys.argv[2], Path(sys.argv[3])
    ns, _missing = subset_extract.load(root)
    holes = 0
    with out.open("w") as stream:
        for label, text in SPELLINGS:
            try:
                ns["assert_within_lexical_subset"](text)
                s_verdict, s_reason = "ADMITTED", ""
            except AssertionError as exc:
                s_verdict, s_reason = "REFUSED", str(exc)[:160]
            gate = ns["lexer_keeps"](text)
            found, err = gcc_ints(gcc, text)
            gate = None if gate is None else list(gate)
            found_l = None if found is None else list(found)
            hole = s_verdict == "ADMITTED" and gate != found_l
            holes += hole
            row = {"label": label, "text": text, "S": s_verdict,
                   "S_reason": s_reason, "reader_keeps": gate,
                   "gcc_keeps": found_l,
                   "gcc_diagnostics": err.strip()[:300],
                   "HOLE": hole}
            stream.write(json.dumps(row, ensure_ascii=True) + "\n")
            print(f"{'HOLE ' if hole else '     '}S={s_verdict:8} "
                  f"reader={gate} gcc={found_l}  {label}")
        stream.write(json.dumps({"summary": {"spellings": len(SPELLINGS),
                                             "holes": holes}}) + "\n")
    print(f"spellings={len(SPELLINGS)} holes={holes}")


if __name__ == "__main__":
    main()
