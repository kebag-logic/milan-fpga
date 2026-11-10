#!/usr/bin/env python3
"""Reviewer-planted defects in the head act_ci.py, each run as a flat installed self-test.

Usage: python3 -I plant_defects.py <head act_ci.py> <head worktree> <output dir> [jobs]

Each mutant is one exact-text replacement that must occur exactly once in the
committed runner. Every mutant copy is installed mode 0555 into its own
directory and run as `python3 -I <copy> --selftest --worktree <head>`, at most
`jobs` at once. A mutant is KILLED when the self-test exits nonzero and prints
at least one FAIL line (or a traceback, recorded separately); SURVIVED when it
exits 0. Writes <out>/<id>.log and a summary to stdout.
"""
from __future__ import annotations

import concurrent.futures
import os
import pathlib
import subprocess
import sys

MUTANTS: list[tuple[str, str, str, str]] = [
    ("M01", "memory bound off by one (>= instead of >)",
     "        if memory > SLOT_MEMORY_GIB:\n", "        if memory >= SLOT_MEMORY_GIB:\n"),
    ("M02", "CPU bound off by one (>= instead of >)",
     "        if cpus > REPLAY_CPU_LIMIT:\n", "        if cpus >= REPLAY_CPU_LIMIT:\n"),
    ("M03", "memory bound compared against slot cap plus service share",
     "        if memory > SLOT_MEMORY_GIB:\n", "        if memory > SLOT_MEMORY_GIB + SLOT_SERVICE_MEMORY_GIB:\n"),
    ("M04", "width 8 also accepts 16-CPU ranges",
     "JOB_CPU_WIDTHS: dict[int, tuple[int, ...]] = {16: (16, 12), 8: (8,), 6: (6,)}",
     "JOB_CPU_WIDTHS: dict[int, tuple[int, ...]] = {16: (16, 12), 8: (16, 8), 6: (6,)}"),
    ("M05", "fallback width is the widest accepted width, not the narrowest",
     "        return self.range_widths[-1]\n", "        return self.range_widths[0]\n"),
    ("M06", "container memory in upper-case size syntax",
     '        return f"{self.memory_gib}g"\n', '        return f"{self.memory_gib}G"\n'),
    ("M07", "--concurrent-jobs is the booked range count, not min(jobs, ranges)",
     "        str(min(geometry.jobs, len(BOOKED_CPU_RANGES.get()))),\n",
     "        str(len(BOOKED_CPU_RANGES.get())),\n"),
    ("M08", "job_cpu_ranges selects only `concurrency` ranges",
     "    return ranges[:jobs]\n", "    return ranges[:concurrency]\n"),
    ("M09", "per-job memory cap may reach 16 GiB",
     "MAX_CONTAINER_MEMORY_GIB = 8\n", "MAX_CONTAINER_MEMORY_GIB = 16\n"),
    ("M10", "geometry type check admits bool/int subclasses",
     "            if type(value) is not int:\n", "            if not isinstance(value, int):\n"),
    ("M11", "workflow concurrency ignores the chosen geometry",
     "    return min(JOB_GEOMETRY.get().jobs, count)\n", "    return min(DEFAULT_JOB_GEOMETRY.jobs, count)\n"),
    ("M12", "job_cpu_ranges bounds concurrency by the default job count",
     "    jobs = JOB_GEOMETRY.get().jobs\n", "    jobs = DEFAULT_JOB_GEOMETRY.jobs\n"),
    ("M13", "--selftest no longer refuses --job-memory",
     "            or args.job_memory is not None\n        ):\n", "        ):\n"),
    ("M14", "CPU bound counts the fallback width, not the job width",
     "        cpus = self.jobs * self.cpus\n", "        cpus = self.jobs * self.range_widths[-1]\n"),
    ("M15", "the command line's --job-memory is ignored",
     '("jobs", jobs), ("cpus", cpus), ("memory_gib", memory_gib))',
     '("jobs", jobs), ("cpus", cpus))'),
    ("M16", "range alignment checked against 16 only",
     "        if first % width:\n", "        if first % (16 if width == 16 else 2):\n"),
    ("M17", "OOM refusal names the default cap, not the run's",
     "a job container's {JOB_GEOMETRY.get().container_memory} ",
     "a job container's {DEFAULT_JOB_GEOMETRY.container_memory} "),
    ("M18", "job count lower bound dropped (0 jobs accepted)",
     "        if not 1 <= self.jobs <= MAX_CONCURRENT_JOBS:\n", "        if not self.jobs <= MAX_CONCURRENT_JOBS:\n"),
]


def run(mutant: tuple[str, str, str, str], source: str, worktree: str, out: pathlib.Path) -> tuple[str, str, int, list[str], bool]:
    ident, title, old, new = mutant
    assert source.count(old) == 1, f"{ident}: anchor occurs {source.count(old)} times"
    directory = out / "copies" / ident
    directory.mkdir(parents=True, exist_ok=True)
    copy = directory / "act_ci.py"
    if copy.exists():
        copy.chmod(0o644)
    copy.write_text(source.replace(old, new), encoding="utf-8")
    copy.chmod(0o555)
    result = subprocess.run([sys.executable, "-I", str(copy), "--selftest", "--worktree", worktree],
                            cwd=worktree, capture_output=True, text=True, timeout=900)
    log = result.stdout + result.stderr
    (out / f"{ident}.log").write_text(log, encoding="utf-8")
    fails = [line.strip() for line in log.splitlines() if line.lstrip().startswith("FAIL")]
    return ident, title, result.returncode, fails, "Traceback" in log


def main() -> int:
    head, worktree, out = sys.argv[1], sys.argv[2], pathlib.Path(sys.argv[3])
    jobs = int(sys.argv[4]) if len(sys.argv) > 4 else 16
    out.mkdir(parents=True, exist_ok=True)
    source = pathlib.Path(head).read_text(encoding="utf-8")
    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as pool:
        results = list(pool.map(lambda m: run(m, source, worktree, out), MUTANTS))
    survived = 0
    for (ident, title, rc, fails, tb), mutant in zip(results, MUTANTS):
        verdict = "KILLED" if rc != 0 else "SURVIVED"
        survived += rc == 0
        print(f"{ident} {verdict} rc={rc} fail_lines={len(fails)} traceback={tb} -- {title}")
        for line in fails[:6]:
            print(f"    {line[:240]}")
    print(f"planted: {len(MUTANTS)} killed: {len(MUTANTS) - survived} survived: {survived}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
