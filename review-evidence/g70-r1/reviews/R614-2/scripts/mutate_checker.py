#!/usr/bin/env python3
"""Reviewer mutation sweep of syn/ooc/check_ooc_clock.py.

Usage: python3 -I mutate_checker.py <path/to/check_ooc_clock.py> <workdir> [--jobs N]

Each mutant is one exact textual replacement (the original text must occur
exactly once). A mutant is KILLED when `--selftest` exits nonzero, SURVIVED
when it exits zero. The unmutated control must exit zero.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import subprocess
import sys
from pathlib import Path

MUTANTS: list[tuple[str, str, str, str]] = [
    ("S1", "script: read_xdc-before rule disabled",
     "    if not any(words == [\"read_xdc\", XDC_READ] for _line, words in before):",
     "    if False:"),
    ("S2", "script: read_xdc accepted by basename",
     "words == [\"read_xdc\", XDC_READ]",
     "(words[0] == \"read_xdc\" and words[-1].endswith(XDC))"),
    ("S3", "script: synth_design count only requires >=1",
     "    if len(synth) != 1:", "    if len(synth) < 1:"),
    ("S4", "constraint set loses read_xdc",
     "{\"create_clock\", \"create_generated_clock\", \"read_xdc\", \"source\"}",
     "{\"create_clock\", \"create_generated_clock\", \"source\"}"),
    ("S5", "constraint set loses create_clock",
     "{\"create_clock\", \"create_generated_clock\", \"read_xdc\", \"source\"}",
     "{\"create_generated_clock\", \"read_xdc\", \"source\"}"),
    ("S6", "constraint set loses create_generated_clock",
     "{\"create_clock\", \"create_generated_clock\", \"read_xdc\", \"source\"}",
     "{\"create_clock\", \"read_xdc\", \"source\"}"),
    ("S7", "constraint set loses source",
     "{\"create_clock\", \"create_generated_clock\", \"read_xdc\", \"source\"}",
     "{\"create_clock\", \"create_generated_clock\", \"read_xdc\"}"),
    ("S8", "script: post-synth scan skips the first command after synth_design",
     "    for line, words in commands[synth[0] + 1:]:",
     "    for line, words in commands[synth[0] + 2:]:"),
    ("X1", "xdc: more than one create_clock accepted",
     "    if len(clocks) != 1 or clocks[0] is None:",
     "    if len(clocks) < 1 or clocks[0] is None:"),
    ("X2", "xdc: period not checked",
     "    if float(period) != PERIOD_NS or port != CLOCK_PORT:",
     "    if port != CLOCK_PORT:"),
    ("X3", "xdc: port not checked",
     "    if float(period) != PERIOD_NS or port != CLOCK_PORT:",
     "    if float(period) != PERIOD_NS:"),
    ("T1", "timing: Clock Summary row only needs to be present",
     "    if summary != [CLOCK_SUMMARY]:", "    if CLOCK_SUMMARY not in summary:"),
    ("T2", "timing: Clock Summary not checked",
     "    if summary != [CLOCK_SUMMARY]:", "    if False:"),
    ("T3", "timing: clk source not checked",
     "    if sources != [[CLOCK_PORT]]:", "    if False:"),
    ("T4", "timing: clk source only needs to include clk_i",
     "    if sources != [[CLOCK_PORT]]:", "    if not any(CLOCK_PORT in s for s in sources) and sources:"),
    ("T5", "timing: no_clock not checked",
     "    if no_clock[:1] != [\"0\"]:", "    if False:"),
    ("T6", "timing: absent no_clock line passes",
     "    if no_clock[:1] != [\"0\"]:", "    if no_clock and no_clock[0] != \"0\":"),
    ("T7", "timing: table keeps only its first row",
     "            rows.append(\" \".join(line.split()))",
     "            rows.append(\" \".join(line.split()))\n            break"),
    ("L1", "log: read_xdc echo before Command not required",
     "    if first(lines, LOG_READ_RE, 0, command) is None:", "    if False:"),
    ("L2", "log: XDC parse matched by basename",
     "    parse = re.compile(r\"^Parsing XDC File \\[\" + re.escape(str(xdc)) + r\"\\]$\")",
     "    parse = re.compile(r\"^Parsing XDC File \\[.*\" + re.escape(xdc.name) + r\"\\]$\")"),
    ("L3", "log: XDC parse accepted anywhere before done (not before mapping)",
     "    if first(lines, parse, start, done if mapping is None else mapping) is None:",
     "    if first(lines, parse, 0, len(lines)) is None:"),
    ("L4", "log: XDC parse rule disabled",
     "    if first(lines, parse, start, done if mapping is None else mapping) is None:",
     "    if False:"),
    ("L5", "log: post-synth constraint echo scan disabled",
     "        if echo and echo.group(1) in CONSTRAINT_COMMANDS:",
     "        if False:"),
    ("L6", "log: CRITICAL WARNING line scan disabled",
     "        if LOG_CRITICAL_RE.match(line):", "        if False:"),
    ("L7", "log: CRITICAL WARNING scan narrowed to Vivado-prefixed IDs",
     "LOG_CRITICAL_RE = re.compile(r\"^CRITICAL WARNING:\")",
     "LOG_CRITICAL_RE = re.compile(r\"^CRITICAL WARNING: \\[Vivado\")"),
    ("L8", "log: session count uses the first count line",
     "LOG_COUNT_RE.match(lines[counts[-1]])", "LOG_COUNT_RE.match(lines[counts[0]])"),
    ("L9", "log: missing session count passes",
     "        findings.append(f\"{name}: no session message count\")", "        pass"),
    ("L10", "log: nonzero session count passes",
     ").group(1)) != \"0\":", ").group(1)) == \"never\":"),
    ("L11", "log: post-synth echo scan starts one line late",
     "    for index in range(done + 1, len(lines)):",
     "    for index in range(done + 2, len(lines)):"),
    ("L12", "log: synthesis-not-completed check removed (falls through)",
     "    if done is None:\n        return [f\"{name}: synth_design did not complete\"]",
     "    if done is None:\n        done = len(lines) - 1"),
    ("P1", "post: timing report not checked",
     "    return log_findings(log, xdc) + timing_findings(report)",
     "    return log_findings(log, xdc)"),
    ("P2", "post: log not checked",
     "    return log_findings(log, xdc) + timing_findings(report)",
     "    return timing_findings(report)"),
    ("P3", "timing: missing report passes",
     "        return [f\"{name}: missing\"]\n    lines = path.read_text(encoding=\"utf-8\", errors=\"replace\").splitlines()\n    findings: list[str] = []\n    summary",
     "        return []\n    lines = path.read_text(encoding=\"utf-8\", errors=\"replace\").splitlines()\n    findings: list[str] = []\n    summary"),
]


def run(checker: Path, work: Path, mid: str, desc: str, old: str, new: str) -> tuple[str, str, str, str]:
    text = checker.read_text(encoding="utf-8")
    if mid != "CONTROL":
        count = text.count(old)
        if count != 1:
            return (mid, desc, "INVALID", f"original text occurs {count} times")
        text = text.replace(old, new)
    d = work / mid
    d.mkdir(parents=True, exist_ok=True)
    target = d / "check_ooc_clock.py"
    target.write_text(text, encoding="utf-8")
    proc = subprocess.run([sys.executable, "-I", str(target), "--selftest"],
                          capture_output=True, text=True, timeout=120)
    out = (proc.stdout + proc.stderr).strip().splitlines()
    tail = out[-1] if out else ""
    if mid == "CONTROL":
        status = "PASS" if proc.returncode == 0 else "CONTROL-FAILED"
    else:
        status = "KILLED" if proc.returncode != 0 else "SURVIVED"
    return (mid, desc, status, f"rc={proc.returncode} {tail}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("checker", type=Path)
    ap.add_argument("work", type=Path)
    ap.add_argument("--jobs", type=int, default=16)
    a = ap.parse_args()
    jobs = [("CONTROL", "unmutated", "", "")] + MUTANTS
    with cf.ThreadPoolExecutor(max_workers=a.jobs) as ex:
        results = list(ex.map(lambda m: run(a.checker, a.work, *m), jobs))
    for r in results:
        print(" | ".join(r))
    killed = sum(r[2] == "KILLED" for r in results)
    survived = [r[0] for r in results if r[2] == "SURVIVED"]
    invalid = [r[0] for r in results if r[2] == "INVALID"]
    print(f"SUMMARY control={results[0][2]} killed={killed}/{len(MUTANTS)} "
          f"survived={survived} invalid={invalid}")
    return 0 if results[0][2] == "PASS" and not invalid else 1


if __name__ == "__main__":
    sys.exit(main())
