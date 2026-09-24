#!/usr/bin/env python3
"""[A261] scratch: record the pinned GCC's answer for every closure cell.

Imports the lane's module-level `_closure_corpus()` (no gate runs), writes
each cell to its own file, runs `<gcc> -std=gnu99 -E` ONE FILE PER CALL (the
gate batches 64; this is an independent measurement), takes the `int` names
the file's own lines keep (or None where GCC refuses), maps each to its
`_LEXER_OUTCOMES` letter and prints the `_CLOSURE_KEPT` literal.

Also checks the new templates against R272-5's BOUNDARY (byte-identical),
and that the first 2520 letters equal the round-four record.

usage: gen_closure.py <lane> <gcc> <out-dir>
"""
import concurrent.futures
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

lane, gcc, out = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
out.mkdir(parents=True, exist_ok=True)
sys.path[:0] = [str(lane / "sw/builder"), str(lane / "scripts")]
import test_builder as tb  # noqa: E402

spec = importlib.util.spec_from_file_location(
    "r5c", "$VALIDATION_STORAGE/408-a261/r272-5/review-evidence/408-r1/reviews/"
    "R272-5/scripts/r5/cases_r5_closure.py")
r5c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r5c)
theirs = [t for w, t, _c in r5c.BOUNDARY if not w.startswith(("B1p", "B3p"))]
ours = [t for _w, t, _r, _c in tb._CLOSURE_POSITIONS[9:]]
assert theirs == ours, "templates differ from R272-5's BOUNDARY"
flags = {w.split()[0]: c for w, _t, c in r5c.BOUNDARY}
print("templates byte-identical to R272-5 B1-B14:", len(ours))
print("in-code flags equal R272-5's:", [c for _w, _t, _r, c in
      tb._CLOSURE_POSITIONS[9:]] == [flags[f"B{i}"] for i in range(1, 15)])

cells = tb._closure_corpus()
MARK = re.compile(r'^# \d+ "([^"]*)"')


def one(item):
    index, (_label, text, _reader, _outside) = item
    with tempfile.TemporaryDirectory(prefix="a261-") as tmp:
        path = Path(tmp) / f"lex{index:05d}.c"
        path.write_bytes(text.encode("utf-8", errors="surrogateescape"))
        run = subprocess.run([gcc, "-std=gnu99", "-E", str(path)],
                             capture_output=True)
    if run.returncode:
        return None
    keep, lines = False, []
    for line in run.stdout.decode("utf-8", errors="replace").split("\n"):
        marker = MARK.match(line)
        if marker:
            keep = Path(marker.group(1)).name == path.name
            continue
        if keep:
            lines.append(line)
    return tuple(re.findall(r"\bint\s+(\w+)\s*;", "\n".join(lines), re.ASCII))


with concurrent.futures.ThreadPoolExecutor(8) as pool:
    found = list(pool.map(one, enumerate(cells)))
letter_of = {kept: letter for letter, kept in tb._LEXER_OUTCOMES.items()}
new = sorted({f for f in found if f not in letter_of}, key=str)
print("outcomes with no letter:", new)
assert not new
kept = "".join(letter_of[f] for f in found)
print("cells:", len(cells), "letters:", len(kept))
print("first 2520 equal the round-four record:",
      kept[:2520] == tb._CLOSURE_KEPT[:2520] and
      len(tb._CLOSURE_KEPT) >= 2520)
lines = [kept[at:at + 66] for at in range(0, len(kept), 66)]
literal = "_CLOSURE_KEPT = (\n" + "".join(
    f'    "{line}"\n' for line in lines) + ")\n"
(out / "closure_kept.txt").write_text(literal, encoding="utf-8")
(out / "closure_measured.json").write_text(json.dumps(
    [{"cell": label, "gcc": f} for (label, *_r), f in zip(cells, found)],
    indent=0) + "\n", encoding="utf-8")
per = {}
for (label, *_r), letter in zip(cells, kept):
    per.setdefault(letter, 0)
    per[letter] += 1
print("letters:", per)
