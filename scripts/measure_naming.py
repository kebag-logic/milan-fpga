#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Measure boundary names that hide a unit, and hold the count down.

Why this exists. Rule 4 of the maintainability guide
(docs/development/CODE_QUALITY.md) asks that boundary types make width,
signedness, direction and units explicit. A general naming linter cannot help
here: it would fight the `_r` / `_w` / `_p` / `_S` / `_C` / `_P` suffixes
`CONTRIBUTING.md` mandates, and it has no idea what a signal means.

So the evidence is the port's OWN documentation. The house style requires every
port to be documented inline with `//!`, and those comments say what the value
IS - "Egress latency correction, ns", "hiCredit clamp, signed bytes". When the
comment names a unit of measure and the identifier does not, the unit is known
and simply absent from the name. That is a finding a reader can check in one
line, and it needs no taste.

FALSE POSITIVES WERE MEASURED BEFORE ANY GATE, and they dominated the naive
form of this check: 180 of 1757 ports matched a unit word in their comment, and
most were not findings at all. Three exclusion classes, each with a reason:

  * SHAPE, not unit. "1-cycle pulse", "single-cycle strobe", "flips every
    eth_rx cycle" describe the SHAPE of a signal. That is what the `_p` suffix
    already encodes, and demanding `_cyc` on a pulse would fight the house
    convention Rule 4 explicitly defers to.
  * PROTOCOL-FIXED identifiers. `s_axi_awaddr` is documented as a byte offset
    and must keep its name: it is AXI's, not ours. Renaming it would break the
    thing the name exists for.
  * SINGLE-BIT ports. A one-bit port carries no quantity, so a unit cannot be
    missing from it.

Applying those three excludes 100 of the 180 and leaves 80 candidates. The
residual set still contains judgement calls - `now_i` on a module whose entire
subject is nanoseconds is arguable - so this is a RATCHET and not a verdict.
The count may not rise. New boundaries state their units; existing debt is
inventoried and paid down deliberately.

`--excluded` prints every filtered match with its reason, because a filter
nobody can see is how a check quietly stops checking.

Usage:
    python3 scripts/measure_naming.py             # the candidate list
    python3 scripts/measure_naming.py --check     # ratchet (exit 1 if it rose)
    python3 scripts/measure_naming.py --excluded  # what was filtered, and why
    python3 scripts/measure_naming.py --selftest  # fixture arms

Exit 0 = at or under the ratchet.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BUDGET = Path(__file__).resolve().parent / "naming.budget"

EXCLUDED_PREFIXES = ("third_party/", "external/", "protocol-processor/",
                     "gptp-processor/", "gen/", "build/")

#: A UNIT OF MEASURE, as written in a port's own `//!` comment. Singular forms
#: are included deliberately: they are most of what the exclusion classes below
#: have to filter, and a vocabulary too narrow to SEE a false positive cannot
#: be said to have measured any.
#:
#: `bit`, `bits` and `word` are deliberately NOT units here. A port's bit width
#: is already explicit in its SystemVerilog type, so "8x3 bits" in a comment is
#: describing the declared width or a table shape, never a unit of the value;
#: and "word" is used in this tree both as a count ("31 words") and as a noun
#: for the value itself ("configuration word"), so it cannot distinguish a
#: missing unit from ordinary prose.
UNIT = re.compile(
    r"\b(nanoseconds?|microseconds?|milliseconds?|ns|us|cycles?|bytes?|octets?"
    r"|hertz|Hz|ppb|ppm|samples?|seconds?|bits/s|bit/s|bps)\b")

#: the same unit, already carried by the identifier
NAME_UNIT = re.compile(
    r"(^|_)(ns|us|ms|cyc|cycles|bytes?|hz|ppb|ppm|smp|samples?|sec|secs|bps)(_|$)",
    re.I)

#: SHAPE phrasing - `_p` already encodes this, and Rule 4 defers to the
#: existing suffix convention rather than competing with it.
SHAPE = re.compile(
    r"\b\d+\s*-?\s*(cycle|clock)\b|\bone[- ]cycle\b|\bsingle[- ]cycle\b"
    r"|\bper[- ]cycle\b|\bevery\b.*\bcycle\b", re.I)

#: identifiers a published protocol owns. Renaming these breaks the contract
#: the name exists to state.
PROTOCOL = re.compile(
    r"^(s_axi|m_axi|s_axis|m_axis)_"
    r"|_(tvalid|tready|tlast|tdata|tkeep|tuser|tdest|tstrb)$")

PORT = re.compile(
    r"^\s*(input|output|inout)\s+(?:wire|logic|var)?\s*(?:signed\s+)?"
    r"(\[[^\]]*\]\s*)?(\w+)")


def sources():
    out = subprocess.run(["git", "ls-files", "hdl"], cwd=REPO,
                         capture_output=True, text=True, check=True).stdout.split()
    return [p for p in out if p.endswith(".sv") and not p.startswith(EXCLUDED_PREFIXES)]


def scan_text(text):
    """Return (candidates, excluded, total_ports) for one source.

    candidates: [(name, unit, doc)] - documented unit missing from the name.
    excluded:   [(name, unit, reason)] - matched, then filtered, with why.
    """
    candidates, excluded, total = [], [], 0
    lines = text.splitlines()
    for i, line in enumerate(lines):
        m = PORT.match(line)
        if not m:
            continue
        total += 1
        width, name = m.group(2), m.group(3)
        same = re.search(r"//!(.*)$", line)
        if same:
            doc = same.group(1)
        elif i and "//!" in lines[i - 1]:
            doc = lines[i - 1].split("//!", 1)[1]
        else:
            doc = ""
        unit = UNIT.search(doc)
        if not unit or NAME_UNIT.search(name):
            continue
        if PROTOCOL.search(name):
            excluded.append((name, unit.group(0), "protocol-fixed identifier"))
        elif not width:
            excluded.append((name, unit.group(0), "single-bit port carries no quantity"))
        elif SHAPE.search(doc):
            excluded.append((name, unit.group(0), "shape, not a unit (the _p suffix owns this)"))
        else:
            candidates.append((name, unit.group(0), doc.strip()))
    return candidates, excluded, total


def scan_repo():
    rows, drops, total = [], [], 0
    for rel in sources():
        c, e, n = scan_text((REPO / rel).read_text(errors="replace"))
        total += n
        rows += [(rel,) + r for r in c]
        drops += [(rel,) + r for r in e]
    return rows, drops, total


def read_budget():
    if not BUDGET.is_file():
        return None
    for line in BUDGET.read_text().splitlines():
        line = line.split("#", 1)[0].strip()
        if line.isdigit():
            return int(line)
    return None


FIXTURES = [
    ("a documented unit missing from the name is a candidate",
     "  input wire [31:0] pres_ofs_i,  //! presentation offset ns", 1, 0),
    ("a name that already carries the unit is not",
     "  input wire [31:0] pres_ofs_ns_i,  //! presentation offset ns", 0, 0),
    ("a one-cycle pulse is a shape, not a unit",
     "  input wire [3:0] arm_i,  //! 1-cycle pulse: arm the chain", 0, 1),
    ("a single-bit port carries no quantity",
     "  input wire go_i,  //! start, ns aligned", 0, 1),
    ("a protocol-fixed identifier is left alone",
     "  input wire [11:0] s_axi_awaddr,  //! Write address (byte offset)", 0, 1),
    ("a port with no unit in its comment is not a candidate",
     "  input wire [31:0] thing_i,  //! some opaque configuration word", 0, 0),
    ("an undocumented port is not a candidate",
     "  input wire [31:0] thing_i,", 0, 0),
    ("the comment may sit on the line above",
     "  //! ring size (bytes)\n  input wire [31:0] ring_len_i,", 1, 0),
]


def selftest():
    failures = 0
    for name, src, want_c, want_e in FIXTURES:
        c, e, _ = scan_text(src)
        if len(c) == want_c and len(e) == want_e:
            print(f"[PASS] {name}")
        else:
            failures += 1
            print(f"[FAIL] {name}: got {len(c)} candidate(s) / {len(e)} excluded, "
                  f"want {want_c} / {want_e}")

    # the exclusions must be REPORTED, not silently dropped: a filter nobody
    # can see is how a check quietly stops checking
    _c, e, _n = scan_text(FIXTURES[2][1])
    if e and e[0][2].startswith("shape"):
        print("[PASS] an exclusion names its reason")
    else:
        failures += 1
        print(f"[FAIL] an exclusion names its reason: {e}")

    # and the scan must find something in the real tree - an inert scan would
    # ratchet to zero and stay green forever
    rows, drops, total = scan_repo()
    if total > 500 and rows:
        print(f"[PASS] the live scan reads the tree ({total} ports)")
    else:
        failures += 1
        print(f"[FAIL] the live scan reads the tree: {total} ports, {len(rows)} candidates")

    n = len(FIXTURES) + 2
    print(f"\n{n} checks: {n - failures} PASS, {failures} FAIL")
    return 1 if failures else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="ratchet: fail if the count rose")
    ap.add_argument("--excluded", action="store_true", help="show what was filtered, and why")
    ap.add_argument("--selftest", action="store_true", help="run the fixture arms")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    rows, drops, total = scan_repo()

    if args.excluded:
        print(f"{len(drops)} match(es) filtered, by reason:")
        for reason in sorted({d[3] for d in drops}):
            group = [d for d in drops if d[3] == reason]
            print(f"\n  {reason} ({len(group)}):")
            for rel, name, unit, _r in group[:12]:
                print(f"    {name:<28} [{unit}]  {rel}")
            if len(group) > 12:
                print(f"    ... and {len(group) - 12} more")
        return 0

    for rel, name, unit, doc in rows:
        print(f"{rel}: {name} — documented in {unit}, not named for it: {doc}")

    budget = read_budget()
    tail = (f"{len(rows)} boundary name(s) hide a documented unit "
            f"({total} ports scanned, {len(drops)} match(es) excluded with a reason)")
    if not args.check:
        print(f"\n{tail}")
        return 0

    if budget is None:
        print(f"\nNO RATCHET: {BUDGET.relative_to(REPO)} is missing or unreadable")
        return 1
    if len(rows) > budget:
        print(f"\nNAMING RATCHET: FAIL ({len(rows)} > ratchet {budget}). A new "
              f"boundary must state its unit in its name.")
        return 1
    print(f"\nNAMING RATCHET: PASS ({tail}; ratchet {budget})")
    if len(rows) < budget:
        print(f"  the ratchet can be lowered to {len(rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
