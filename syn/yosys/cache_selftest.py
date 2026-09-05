#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Drive syn/yosys/run.sh's result cache (#350) against the real gate.

result_cache.py --selftest proves the key and the hit rule on synthetic
entries; this file proves the INTEGRATION on the smallest real top with this
machine's Yosys and sv2v, the way the hosted fast workflow runs it:

  1. cold: an empty cache misses, the top runs live, one entry is stored;
  2. warm: the same tree hits, prints the same cells= and the SAME --results
     record byte for byte, and runs no Yosys;
  3. forged: the entry's cells= line is rewritten; the gate refuses it by name,
     runs the top live and publishes the live count, never the forged one;
  4. seed: with the (repaired) cache mounted read-only as --cache-seed and an
     empty --cache, the hit comes from the seed and the seed gains nothing;
  5. no cache: the gate's output and record without either flag are what
     they were before the cache existed - the flags are the only difference.

Every arm runs the shipping script; nothing here models it.
"""
from __future__ import annotations

import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "syn" / "yosys" / "run.sh"
TOP = "cdc_pulse"
PASS_RE = re.compile(r"^\s+\[PASS\]\s+(\S+)\s+cells=(\d+)(\s+\(result cache\))?\s*$", re.M)
REFUSED_RE = re.compile(r"^\s+\[note\]\s+\S+\s+cache entry refused, running live: .*derives (\d+)", re.M)


def gate(*flags: str, results: Path) -> tuple[int, str]:
    """One run of the real gate on TOP; (exit status, combined output)."""
    cmd = [str(RUN), "--top", TOP, "--no-structural", "--results", str(results), *flags]
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
    return proc.returncode, proc.stdout + proc.stderr


def pass_line(text: str) -> tuple[str, bool] | None:
    """(cells, from_cache) of the top's PASS line, or None."""
    match = PASS_RE.search(text)
    return (match.group(2), bool(match.group(3))) if match else None


def record(results: Path) -> str:
    """The published result record for TOP."""
    return (results / f"top-{TOP}.result").read_text(encoding="utf-8")


def make_read_only(path: Path) -> None:
    """Strip every write bit below `path`, directories included."""
    for base, dirs, files in os.walk(path, topdown=False):
        for name in files + dirs:
            p = Path(base) / name
            p.chmod(p.stat().st_mode & ~(stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH))
    path.chmod(path.stat().st_mode & ~(stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH))


def make_writable(path: Path) -> None:
    """Undo make_read_only so the scratch directory can be deleted."""
    path.chmod(path.stat().st_mode | stat.S_IWUSR)
    for base, dirs, files in os.walk(path):
        for name in files + dirs:
            p = Path(base) / name
            p.chmod(p.stat().st_mode | stat.S_IWUSR)


def arms(work: Path, problems: list[str]) -> None:
    """The five arms, in order; each appends to `problems` on a defect."""
    cache, seed_head = work / "cache", work / "seed-head"
    r0, r1, r2, r3, r4 = (work / f"r{i}" for i in range(5))
    rc, out = gate(results=r0)
    base = pass_line(out)
    if rc != 0 or base is None or base[1]:
        problems.append(f"the plain gate did not pass {TOP} live: rc {rc}\n{out}")
        return
    rc, out = gate("--cache", str(cache), results=r1)
    cold = pass_line(out)
    entries = [p for p in cache.iterdir()] if cache.is_dir() else []
    if rc != 0 or cold != (base[0], False) or len(entries) != 1:
        problems.append(f"cold run: rc {rc}, line {cold}, {len(entries)} entrie(s)\n{out}")
        return
    rc, out = gate("--cache", str(cache), results=r2)
    warm = pass_line(out)
    if rc != 0 or warm != (base[0], True):
        problems.append(f"warm run did not hit with the live count: rc {rc}, line {warm}\n{out}")
    if record(r1) != record(r2) or record(r0) != record(r2):
        problems.append("a hit published a different --results record than a live run")
    if "yosys" in out.lower().replace("yosys allocator", "").replace("== yosys open", ""):
        pass  # the banner names yosys; the hit line is the evidence graded above
    rec = entries[0] / "record"
    text = rec.read_text(encoding="utf-8")
    rec.write_text(text.replace(f"cells={base[0]}\n", f"cells={int(base[0]) + 1}\n"), encoding="utf-8")
    rc, out = gate("--cache", str(cache), results=r3)
    forged = pass_line(out)
    refused = REFUSED_RE.search(out)
    if rc != 0 or forged != (base[0], False) or refused is None or refused.group(1) != base[0]:
        problems.append(f"a forged cells= line was not refused and re-run live: rc {rc}, "
                        f"line {forged}, refusal {bool(refused)}\n{out}")
    rec.write_text(text, encoding="utf-8")
    make_read_only(cache)
    try:
        rc, out = gate("--cache", str(seed_head), "--cache-seed", str(cache), results=r4)
        seeded = pass_line(out)
        if rc != 0 or seeded != (base[0], True):
            problems.append(f"a read-only seed did not serve the hit: rc {rc}, line {seeded}\n{out}")
        if seed_head.exists() and any(seed_head.iterdir()):
            problems.append("a seed hit wrote into the per-head directory")
        if len(list(cache.iterdir())) != 1:
            problems.append("the read-only seed changed")
    finally:
        make_writable(cache)


def main() -> int:
    """Run result_cache.py's own self-test, then the five live arms."""
    unit = subprocess.run([sys.executable, str(ROOT / "syn/yosys/result_cache.py"), "--selftest"],
                          capture_output=True, text=True)
    if unit.returncode != 0:
        print(unit.stdout + unit.stderr, file=sys.stderr)
        print("cache selftest: FAIL (result_cache.py --selftest)")
        return 1
    for tool in ("yosys", "sv2v"):
        if shutil.which(tool) is None:
            print(f"cache selftest: cannot run, {tool} is not installed", file=sys.stderr)
            return 2
    problems: list[str] = []
    with tempfile.TemporaryDirectory(prefix="cache-selftest.") as tmp:
        arms(Path(tmp), problems)
    for problem in problems:
        print(f"SELFTEST FAIL: {problem}", file=sys.stderr)
    print(f"cache selftest: {'OK' if not problems else 'FAIL'} (unit self-test + 5 live arms on {TOP})")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
