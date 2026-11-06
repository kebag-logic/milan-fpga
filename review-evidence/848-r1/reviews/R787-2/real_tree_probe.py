#!/usr/bin/env python3
"""Probe docs_inventory.py on a disposable clone of the reviewed tree.

Usage: real_tree_probe.py CLONE. Reports the lane files against the page's rows, the rows a text search
misses, and what each length change does to the page. Restores every page with `git checkout` between probes.
"""
import pathlib
import re
import subprocess
import sys
import tempfile

clone = pathlib.Path(sys.argv[1]).resolve()
tool = [sys.executable, "-I", str(clone / "scripts/docs_inventory.py")]
page = clone / "docs/DOCUMENTATION_AUDIT.md"
committed = page.read_text(encoding="utf-8")


def sh(*argv):
    return subprocess.run(argv, cwd=clone, capture_output=True, text=True)


def restore():
    sh("git", "checkout", "-q", "--", ".")
    sh("git", "clean", "-fdq")


tracked = [p for p in sh("git", "ls-files", "-z").stdout.split("\0") if p]
documents = [p for p in tracked if (p.endswith(".md") or pathlib.PurePosixPath(p).name.upper().startswith("README"))
             and p != "docs/DOCUMENTATION_AUDIT.md" and (clone / p).is_file()]
print(f"documents probed: {len(documents)}")

findings = committed.split("\n## Findings\n", 1)[1]
rows = [line for line in findings.split("\n") if re.match(r"\| D0-\d+ \|", line)]
print(f"page rows: {len(rows)}; on page {sum('| on page |' in r for r in rows)}; "
      f"re-verify {sum('re-verify' in r for r in rows)}")

with tempfile.TemporaryDirectory() as lanes:
    done = subprocess.run(tool + ["--findings-dir", lanes], capture_output=True, text=True, cwd=clone)
    print("--findings-dir rc", done.returncode)
    print(done.stdout.replace(lanes, "DIR").strip())
    entries = []
    for lane in sorted(pathlib.Path(lanes).glob("*.md")):
        text = lane.read_text(encoding="utf-8")
        for match in re.finditer(r"^## (D0-\d+): (.+):(\d+|\?)\n\n- Statement: (.*)\n- Contradicted by: (.*)\n"
                                 r"- Correction: (.*)$", text, re.M):
            entries.append((lane.name, *match.groups()))
print(f"lane entries: {len(entries)}; unlocated {sum(e[3] == '?' for e in entries)}")

page_keys = sorted((r.split(" | ")[0][2:], re.search(r"\[(.+?)(?: \(historical\))?\]", r).group(1)) for r in rows)
lane_keys = sorted((e[1], e[2]) for e in entries)
print("page rows equal lane entries:", page_keys == lane_keys)

missed = []
for lane, ident, path, line, statement, source, correction in entries:
    if line == "?":
        continue
    text = (clone / path).read_text(encoding="utf-8", errors="replace")
    number = int(line)
    if statement not in text:
        missed.append((ident, path, number))
print(f"rows a literal text search misses: {len(missed)}")
for row in missed:
    print("  ", *row)


def change(name, edit):
    restore()
    edit()
    done = subprocess.run(tool + ["--check"], capture_output=True, text=True, cwd=clone)
    fresh = None
    if done.returncode == 1:
        subprocess.run(tool + ["--write"], capture_output=True, text=True, cwd=clone)
        fresh = page.read_text(encoding="utf-8")
    moved = []
    if fresh:
        old, new = committed.split("\n"), fresh.split("\n")
        moved = [(a, b) for a, b in zip(old, new) if a != b]
    print(f"{name}: --check rc {done.returncode}, page lines moved {len(moved)}, line count {len(committed.split(chr(10)))}"
          f"->{len((fresh or committed).split(chr(10)))}")
    for a, b in moved[:60]:
        ca, cb = a.split(" | "), b.split(" | ")
        delta = [(x[:60], y[:60]) for x, y in zip(ca, cb) if x != y]
        print("   ", ca[0][:48], delta[:3])
    restore()


def edit_all(transform):
    def edit():
        for path in documents:
            target = clone / path
            target.write_text(transform(target.read_text(encoding="utf-8", errors="surrogateescape")),
                              encoding="utf-8", errors="surrogateescape")
    return edit


change("append 1 line to every document", edit_all(lambda t: t + "Added.\n"))
change("append 500 lines to every document", edit_all(lambda t: t + "Added.\n" * 500))
change("prepend 1 blank line to every document", edit_all(lambda t: "\n" + t))
change("prepend 6 blank lines to every document", edit_all(lambda t: "\n" * 6 + t))
change("prepend 7 blank lines to every document", edit_all(lambda t: "\n" * 7 + t))
change("prepend 20 blank lines to every document", edit_all(lambda t: "\n" * 20 + t))
