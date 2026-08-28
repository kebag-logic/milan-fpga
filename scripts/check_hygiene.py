#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Mechanical hygiene: the objective checks, measured before any was adopted.

Why this exists. Rule 9 of the maintainability guide
(docs/development/CODE_QUALITY.md) says let pinned tools enforce objective,
mechanical rules - and measure signal and false positives BEFORE gating, so a
new baseline does not bury real findings or start a fight with the house style.

WHAT WAS MEASURED. Six candidates are run over first-party files in this
superproject and both project-owned processor submodules. Runtime is not a
reason to reject any of them:

  | candidate                | findings | files | verdict |
  |--------------------------|---------:|------:|---------|
  | line over 100 columns    |     1164 |   167 | REJECTED |
  | trailing whitespace      |       44 |    18 | adopted |
  | missing EOF newline      |       14 |    14 | adopted |
  | CRLF line ending         |        0 |     0 | adopted at zero |
  | UTF-8 BOM                |        0 |     0 | adopted at zero |
  | tab in SystemVerilog     |        0 |     0 | adopted at zero |

WHY THE LINE-LENGTH CHECK IS REJECTED, on the record. It is the highest-volume
candidate and it fights two deliberate house rules. `$error` takes later
arguments as VALUES, so an elaboration message MUST be one string literal -
`milan_datapath` and `KL_media_nco` both carry the note saying so, and every one
of those messages is over 100 columns by construction. The curated source lists
in `syn/yosys/run.sh` and `syn/yosys/ooc.sh` are single lines by design, because
a line continuation is what let a shell comment silently shrink one of them
(recorded in `syn/ooc/dp_srcs.py`). Wrapping either would trade a real property
for a cosmetic one. Rejected, not deferred.

The three zero-population checks are adopted BECAUSE they are at zero: holding
a clean property at zero costs nothing, and each carries an arm proving it
bites, so it cannot be an empty gate nobody notices.

GENERATED AND VENDORED SOURCES ARE EXCLUDED. What counts as generated is not
re-decided here: the predicate is imported from `scripts/gen_toc.py`, which
already owns it. Five of the nineteen missing-newline findings are generated
Vivado and simulation scripts; the fix for those is in their generator, never
in the file.

Usage:
    python3 scripts/check_hygiene.py            # the findings
    python3 scripts/check_hygiene.py --check    # ratchets
    python3 scripts/check_hygiene.py --fix      # repair the mechanical ones
    python3 scripts/check_hygiene.py --selftest # fixture arms

Exit 0 = every check at or under its ratchet in scripts/hygiene.budget.
"""

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BUDGET = Path(__file__).resolve().parent / "hygiene.budget"
sys.path.insert(0, str(Path(__file__).resolve().parent))

#: what "generated" means is OWNED by gen_toc.py; a second definition here
#: would be exactly the drift Rule 3 forbids
from gen_toc import GENERATED_RE, GENERATED_SCAN_LINES
from code_quality_scope import PROJECT_SUBMODULES, tracked

SCANNED_SUFFIXES = (".sv", ".svh", ".v", ".py", ".cpp", ".h", ".hpp", ".c",
                    ".sh", ".tcl", ".mk", ".yml", ".yaml")
EXCLUDED_PREFIXES = ("third_party/", "external/", "gen/", "build/")

#: name -> (fixable, description). Order is the report order.
CHECKS = (
    ("trailing whitespace", True, "a line ending in spaces or tabs"),
    ("missing EOF newline", True, "a file whose last line has no newline"),
    ("CRLF line ending", True, "a carriage return before a newline"),
    ("UTF-8 BOM", True, "a byte-order mark at the start of a source file"),
    ("tab in SystemVerilog", False, "a tab character in .sv/.svh (house style is 2 spaces)"),
)


def is_generated(text):
    head = "\n".join(text.splitlines()[:GENERATED_SCAN_LINES])
    return bool(GENERATED_RE.search(head))


def sources():
    out = tracked(*(f"*{suffix}" for suffix in SCANNED_SUFFIXES))
    return [p for p in out
            if p.endswith(SCANNED_SUFFIXES) and not p.startswith(EXCLUDED_PREFIXES)]


def is_project_submodule_path(rel):
    """Whether a finding must be repaired in the owning submodule repository."""
    return rel.startswith(tuple(f"{name}/" for name in PROJECT_SUBMODULES))


def scan_bytes(raw, path="x.sv"):
    """Return {check_name: count} for one file's bytes."""
    found = {name: 0 for name, _f, _d in CHECKS}
    if not raw:
        return found
    text = raw.decode("utf-8", "replace")
    if is_generated(text):
        return found
    found["UTF-8 BOM"] = 1 if raw.startswith(b"\xef\xbb\xbf") else 0
    found["CRLF line ending"] = 1 if b"\r\n" in raw else 0
    found["missing EOF newline"] = 0 if raw.endswith(b"\n") else 1
    lines = text.split("\n")
    found["trailing whitespace"] = sum(
        1 for l in lines if l.strip() and l.rstrip("\r") != l.rstrip())
    if path.endswith((".sv", ".svh")):
        found["tab in SystemVerilog"] = sum(1 for l in lines if "\t" in l)
    return found


def fix_bytes(raw):
    """Repair the mechanical findings. Returns the new bytes."""
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    raw = raw.replace(b"\r\n", b"\n")
    text = raw.decode("utf-8", "replace")
    text = "\n".join(l.rstrip() if l.strip() else l for l in text.split("\n"))
    if text and not text.endswith("\n"):
        text += "\n"
    return text.encode("utf-8")


def audit():
    totals = {name: 0 for name, _f, _d in CHECKS}
    per_file = {}
    skipped = []
    for rel in sources():
        raw = (REPO / rel).read_bytes()
        if raw and is_generated(raw.decode("utf-8", "replace")):
            skipped.append(rel)
            continue
        found = scan_bytes(raw, rel)
        if any(found.values()):
            per_file[rel] = found
        for k, v in found.items():
            totals[k] += v
    return totals, per_file, skipped


def read_budget():
    if not BUDGET.is_file():
        return {}
    out = {}
    for line in BUDGET.read_text().splitlines():
        line = line.split("#", 1)[0].strip()
        if "=" in line:
            k, v = line.split("=", 1)
            if v.strip().isdigit():
                out[k.strip()] = int(v.strip())
    return out


def selftest():
    failures = 0

    def ck(name, ok, detail=""):
        nonlocal failures
        if ok:
            print(f"[PASS] {name}")
        else:
            failures += 1
            print(f"[FAIL] {name}{': ' + detail if detail else ''}")

    ck("trailing whitespace is caught",
       scan_bytes(b"int x;   \n")["trailing whitespace"] == 1)
    ck("a blank line is not trailing whitespace",
       scan_bytes(b"a\n   \nb\n")["trailing whitespace"] == 0,
       "an indented blank line is layout, not a finding")
    ck("a missing EOF newline is caught",
       scan_bytes(b"int x;")["missing EOF newline"] == 1)
    ck("a present EOF newline is not", scan_bytes(b"int x;\n")["missing EOF newline"] == 0)
    ck("CRLF is caught", scan_bytes(b"a\r\nb\n")["CRLF line ending"] == 1)
    ck("a BOM is caught", scan_bytes(b"\xef\xbb\xbfa\n")["UTF-8 BOM"] == 1)
    ck("a tab in SystemVerilog is caught",
       scan_bytes(b"\tx <= 1;\n", "a.sv")["tab in SystemVerilog"] == 1)
    ck("a tab in a makefile is not judged",
       scan_bytes(b"\tx <= 1;\n", "a.mk")["tab in SystemVerilog"] == 0,
       "a tab IS the syntax there")
    ck("a generated file is skipped entirely",
       scan_bytes(b"# This is a generated script based on design: x\nint y;   ")
       == {n: 0 for n, _f, _d in CHECKS})

    # -- the fixer must repair exactly what the scanner reports --------------
    dirty = b"\xef\xbb\xbfint x;   \r\nint y;\t \r\nint z;"
    clean = fix_bytes(dirty)
    ck("the fixer clears every mechanical finding",
       all(v == 0 for v in scan_bytes(clean).values()), f"{scan_bytes(clean)}")
    ck("the fixer preserves the content",
       clean == b"int x;\nint y;\nint z;\n", f"{clean!r}")
    ck("the fixer is idempotent", fix_bytes(clean) == clean)

    totals, per_file, skipped = audit()
    ck("the live scan reads the tree", sum(totals.values()) >= 0 and len(sources()) > 100,
       f"{len(sources())} files")
    ck("the live scan reaches both project processor submodules",
       any(p.startswith("protocol-processor/") for p in sources())
       and any(p.startswith("gptp-processor/") for p in sources()))
    ck("generated files are actually being skipped", bool(skipped),
       "nothing was skipped - the generated predicate is not firing")
    ck("project-submodule fixes are owned upstream",
       is_project_submodule_path("protocol-processor/hdl/example.sv")
       and not is_project_submodule_path("hdl/example.sv"))

    n = 16
    print(f"\n{n} checks: {n - failures} PASS, {failures} FAIL")
    return 1 if failures else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="ratchet every check")
    ap.add_argument("--fix", action="store_true", help="repair the mechanical findings")
    ap.add_argument("--selftest", action="store_true", help="run the fixture arms")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    if args.fix:
        changed = 0
        upstream = 0
        for rel in sources():
            path = REPO / rel
            raw = path.read_bytes()
            if not raw or is_generated(raw.decode("utf-8", "replace")):
                continue
            new = fix_bytes(raw)
            if new != raw:
                if is_project_submodule_path(rel):
                    upstream += 1
                    print(f"needs upstream fix in project submodule: {rel}")
                    continue
                path.write_bytes(new)
                changed += 1
                print(f"fixed {rel}")
        print(f"\n{changed} file(s) repaired. A tab in SystemVerilog is NOT fixed "
              f"automatically: re-indenting is a judgement about layout.")
        if upstream:
            print(f"{upstream} project-submodule file(s) were not rewritten; "
                  "repair them in their owning repository and update the pin.")
        return 1 if upstream else 0

    totals, per_file, skipped = audit()
    for rel in sorted(per_file):
        bits = ", ".join(f"{k} x{v}" for k, v in per_file[rel].items() if v)
        print(f"{rel}: {bits}")

    print(f"\n{len(sources())} first-party file(s) scanned across the superproject "
          f"and processor submodules, {len(skipped)} generated "
          f"file(s) skipped (their fix is in their generator)")
    for name, _fixable, _desc in CHECKS:
        print(f"  {name:<24} {totals[name]}")

    if not args.check:
        return 0

    budget = read_budget()
    bad = False
    for name, _fixable, _desc in CHECKS:
        limit = budget.get(name)
        if limit is None:
            print(f"\nNO RATCHET for {name!r} in {BUDGET.relative_to(REPO)}")
            bad = True
        elif totals[name] > limit:
            print(f"\nFAIL: {name} {totals[name]} > ratchet {limit}")
            bad = True
    if bad:
        return 1
    print("\nHYGIENE RATCHET: PASS (" +
          ", ".join(f"{n} {totals[n]}<={budget[n]}" for n, _f, _d in CHECKS) + ")")
    return 0


if __name__ == "__main__":
    sys.exit(main())
