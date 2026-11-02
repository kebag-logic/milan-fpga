#!/usr/bin/env python3
"""usage: collect.py HEAD_OWNED_PROCESS REVIEWS_DIR ROUND1_MUTATE ROUND4_MATRIX3 OUT_JSON

Collect every mutant of scripts/owned_process.py published for #833: both
reviewers' rounds 1-4 and the author's round 1 and round 3 tables. Apply each
to the head file (each edit must match exactly once) and group mutants whose
mutated file is byte-identical. Writes OUT_JSON: a list of
{text_sha, sources: [source/name...], edits: [[old, new]...]} and prints a report.
"""
import hashlib, json, sys
from pathlib import Path

head = Path(sys.argv[1]).read_text()
rev, round1, matrix3, out = Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4]), Path(sys.argv[5])


def literal(path: Path, start: str, end: str) -> dict:
    src = path.read_text()
    ns: dict = {}
    exec(src[src.index(start):src.index(end, src.index(start))], ns)
    return ns


def edits_of(value):
    # R764 tables are (edits, test, expect); the others are bare edit lists.
    if isinstance(value, tuple) and len(value) == 3 and isinstance(value[1], str):
        return value[0], value[1]
    return value, "suite"


sources = {}
for tag, path, start, end, name in [
        ("R763-1", rev / "R763-1/scripts/mutate.py", "MUTANTS = {", "\nrepo, out", "MUTANTS"),
        ("R763-2", rev / "R763-2/scripts/make_mutants.py", "MUTANTS = {", "\nfor name", "MUTANTS"),
        ("R763-3", rev / "R763-3/scripts/mutants.py", "FIX = ", "\nfor name", "MUT"),
        ("R763-4", rev / "R763-4/scripts/spot_mutants.py", "MUT = {", "\nfor name", "MUT"),
        ("R764-1", rev / "R764-1/scripts/mutate.py", "MUT = {", "\nNS = ", "MUT"),
        ("R764-2", rev / "R764-2/scripts/mutate_r2.py", "MUT = {", "\nNS = ", "MUT"),
        ("R764-3", rev / "R764-3/scripts/mutate_r3.py", "MUT = {", "\nNS = ", "MUT"),
        ("R764-4", rev / "R764-4/scripts/mutants.py", "GUARD = ", "\nfor name", "MUT"),
        ("A726c", matrix3, "OWN = {", "\nsrc = ", "OWN")]:
    for key, value in literal(path, start, end)[name].items():
        edits, test = edits_of(value)
        if test != "suite":
            continue
        sources[f"{tag}/{key}"] = [list(e) for e in edits]

# The author's round 1 table: each entry is the whole mutated text of its head.
src = round1.read_text()
r1_head = Path(sys.argv[6]).read_text() if len(sys.argv) > 6 else None
ns = {}
calls = []


def sub(old, new, text=None):
    calls.append((old, new))
    return (old, new)


ns["sub"] = sub
ns["good"] = ""
exec(src[src.index("MUT = {"):src.index("\n}", src.index("MUT = {")) + 2], ns)
for key, value in ns["MUT"].items():
    sources[f"A726/{key}"] = [list(value)]

groups: dict = {}
bad = []
for name, edits in sources.items():
    text = head
    ok = True
    for old, new in edits:
        if text.count(old) != 1:
            bad.append((name, old[:70], text.count(old)))
            ok = False
            break
        text = text.replace(old, new)
    if not ok:
        continue
    digest = hashlib.sha256(text.encode()).hexdigest()[:12]
    g = groups.setdefault(digest, {"text_sha": digest, "sources": [], "edits": edits})
    g["sources"].append(name)
out.write_text(json.dumps(list(groups.values()), indent=1) + "\n")
print(len(sources), "source mutants,", len(groups), "distinct texts,", len(bad), "not applicable")
for b in bad:
    print("NOT APPLICABLE", b)
for g in groups.values():
    print(g["text_sha"], " ".join(g["sources"]))
