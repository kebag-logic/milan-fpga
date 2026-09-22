#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Consistency checks for the compliance review: REQ rows, GAP ids, Ver vocabulary."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REVIEW = ROOT / "docs" / "00_MILAN_COMPLIANCE_REVIEW.md"
VER_VOCAB = {"DIR", "MTXW", "TOL", "TIM", "RND", "STORM", "NVM", "—", "lint"}
MAND_VOCAB = {"shall", "should", "may", "rec", "design", "—"}
REQ_ROW = re.compile(r"^\|\s*(REQ-[A-Z]+-\d{3})\s*\|(.*)$", re.M)
GAP_DEF = re.compile(r'<a id="(gap-\d+)">')
GAP_REF = re.compile(r"\(#(gap-\d+)\)")


def main() -> int:
    """The gate: every REQ row complete and spelled in the vocabulary, every
    GAP defined, referenced and owned by a REQ row; 1 on any finding."""
    body = REVIEW.read_text(encoding="utf-8")
    problems, seen = [], {}
    req_gaps = set()

    for req, rest in REQ_ROW.findall(body):
        cols = [c.strip() for c in rest.split("|")]
        if req in seen:
            problems.append(f"duplicate {req}")
        seen[req] = cols
        # clause, requirement, mandate, coverage, finding, arch, doc, ver
        if len(cols) < 8:
            problems.append(f"{req}: only {len(cols)} columns")
            continue
        for idx, label in ((0, "clause"), (1, "requirement"), (2, "mandate"),
                           (3, "coverage"), (5, "arch"), (6, "doc")):
            if not cols[idx]:
                problems.append(f"{req}: empty {label}")
        mand = cols[2].split("(")[0].strip()
        if mand and mand.split()[0] not in MAND_VOCAB:
            problems.append(f"{req}: unknown Mand '{cols[2]}'")
        cov = cols[3].strip()
        if cov and cov[0] not in "CPAI":
            problems.append(f"{req}: unknown Cov '{cols[3]}'")
        req_gaps.update(GAP_REF.findall(cols[4]))
        ver = cols[7].strip()
        if ver and ver not in VER_VOCAB:
            problems.append(f"{req}: unknown Ver category '{ver}'")

    defined = set(GAP_DEF.findall(body))
    referenced = set(GAP_REF.findall(body))
    for gap in sorted(referenced - defined):
        problems.append(f"{gap}: referenced but never defined")
    for gap in sorted(defined - referenced):
        problems.append(f"{gap}: defined but never referenced (needs a disposition row)")
    for gap in sorted(defined - req_gaps):
        problems.append(f"{gap}: no REQ row covers it (the release gate never reaches it)")

    for line in problems:
        print(f"MATRIX FAIL: {line}")
    print(f"matrix: {len(seen)} REQ rows, {len(defined)} GAP findings, "
          f"{'OK' if not problems else str(len(problems)) + ' FAILURES'}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
