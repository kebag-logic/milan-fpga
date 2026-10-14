# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Check published service arithmetic against the compiled composition headers."""

from __future__ import annotations

import re
import sys

import fw_gtest
from ctrl_build import ROOT, Outcome, Refusal, Tree, includes, run

PAGE = ROOT / "docs/design/MAILBOX_SPLIT.md"
PATHS = ("an event behind 15 others", "an ACMP command behind a full acmp ring",
         "an ENTITY_AVAILABLE behind a full adp ring", "a response with 7 frames owed ahead of it")
PROBE = r'''#include <stdio.h>
#include "ctrl_app.h"
int main(void) {
    printf("%u %u %u %u %u\n", CTRL_APP_PASS_MAX, CTRL_LOOP_EVT_PASSES,
           ACMP_MBX_RX_PASSES, CTRL_LOOP_RX_PASSES(MBX_CH_ADP_RX_WORDS), ACMP_MBX_OWED_PASSES);
    return 0;
}
'''


def threshold(accesses: int) -> str:
    """The 10 ms limit in microseconds per access, rounded down to two decimal places."""
    hundredths = 1000000 // accesses
    return f"{hundredths // 100}.{hundredths % 100:02}"


def expected(counts: list[list[int]]) -> list[str]:
    """The page's construction: one in-flight pass plus all passes needed to take the input."""
    if len(counts) != 2 or any(len(row) != 5 or any(n <= 0 for n in row) for row in counts):
        raise Refusal("service-bound probe must return two positive five-value rows")
    lines = []
    for index, path in enumerate(PATHS, 1):
        passes = counts[0][index]
        if counts[1][index] != passes:
            raise Refusal("service-bound table needs separate interface pass counts")
        bounds = [(row[index] + 1) * row[0] for row in counts]
        suffix = ", after room returns" if index == 4 else ""
        lines.append(f"| {path} | {passes}{suffix} | {bounds[0]:,} / {bounds[1]:,} | "
                     f"{threshold(bounds[0])} / {threshold(bounds[1])} us |")
    lines += [f"With F4's SRP attached before the loop starts, `CTRL_APP_PASS_MAX` is {counts[0][0]:,}",
              f"accesses at one interface and {counts[1][0]:,} at two, including the F3b freshness queries."]
    events = [(row[1] + 1) * row[0] for row in counts]
    lines.append(f"At 1 us per access, event envelopes are {events[0] / 1000:.3f} / {events[1] / 1000:.3f} ms.")
    if not all(10000 < value <= 20000 for value in events):
        raise Refusal("event bounds changed: reconsider the published 10 ms and 20 ms conclusions")
    lines += ["Neither fits T_svc = 10 ms; neither do the other rows. The 20 ms ACMP",
              "ceiling still covers both event envelopes, but none of the other rows."]
    return lines


def findings(text: str, lines: list[str]) -> list[str]:
    """Require every published row and its dependent conclusions exactly once."""
    return [f"service bounds: missing or repeated {line}" for line in lines if text.count(line) != 1]


def controls(text: str, lines: list[str]) -> tuple[int, int]:
    """Each pass, bound, threshold and prose conclusion has a planted stale-value control."""
    bad = count = 0
    for line in lines:
        parts = line.split("|")
        targets = parts[2:5] if line.startswith("|") else [line]
        variants = [""]
        for part in targets:
            for number in re.finditer(r"[0-9]+(?:,[0-9]{3})*(?:\.[0-9]+)?", part):
                changed = part[:number.start()] + "999999" + part[number.end():]
                variants.append(line.replace(part, changed, 1))
        for changed in variants:
            planted = text.replace(line, changed, 1)
            ok = planted != text and any(line in item for item in findings(planted, lines))
            bad += not ok
            count += 1
    return bad, count


def arm_service_bounds(tree: Tree) -> Outcome:
    """Compile both interface variants, judge the page, then require every planted defect to fail."""
    work = tree.out / "service-bounds"
    work.mkdir(parents=True, exist_ok=True)
    source = work / "counts.c"
    source.write_text(PROBE, encoding="utf-8")
    counts = []
    for interface in (1, 2):
        out = work / f"if{interface}"
        generated = run([sys.executable, str(ROOT / "sw/mailbox/gen_mailbox.py"), "--variant-interfaces",
                         str(interface), "--out", str(out)])
        compiled = run(["gcc", "-std=c11", "-Wall", "-Wextra", "-Werror", *includes(tree),
                        "-include", str(out / "mbx_contract.h"), str(source), "-o", str(out / "counts")])
        if generated.returncode or compiled.returncode:
            raise Refusal("service-bound header compilation failed: " + generated.stderr + compiled.stderr)
        if fw_gtest.EXECUTION.run:
            result = run([str(out / "counts")])
            if result.returncode:
                raise Refusal("service-bound header probe failed")
            counts.append([int(value) for value in result.stdout.split()])
    if not fw_gtest.EXECUTION.run:
        return Outcome("service_bounds", 0, "service bounds: both interface probes BUILT, not run")
    text = PAGE.read_text(encoding="utf-8")
    lines = expected(counts)
    found = findings(text, lines)
    bad, total = controls(text, lines)
    failures = len(found) + bad
    log = "\n".join([*lines, *found, f"service bounds: {total - bad}/{total} planted controls caught",
                     f"== ctrl service bounds: checks: {len(lines) + total}   failures: {failures} ==",
                     "RESULT: FAIL" if failures else "RESULT: PASS"])
    return Outcome("service_bounds", int(bool(failures)), log)
