"""Reviewer-designed planted defects for scripts/act_ci.py at the reviewed head.

Each mutant is (id, description, old, new): `old` must occur exactly once in the
committed runner; the copy with `new` in its place is installed flat (mode 0555)
and its offline --selftest is run against the clean worktree inside sbx.sh.
Usage: python3 -I mutants.py <clean-worktree> <out-dir> <sbx.sh> [jobs]
"""
import concurrent.futures, os, pathlib, re, subprocess, sys

MUTANTS = [
    ("M01", "default fallback reported as the widest width (16, not 12)",
     "return self.range_widths[-1]", "return self.range_widths[0]"),
    ("M02", "--concurrent-jobs no longer capped by the number of booked ranges",
     "str(min(geometry.jobs, len(BOOKED_CPU_RANGES.get()))),", "str(geometry.jobs),"),
    ("M03", "job_cpu_ranges selects only `concurrency` ranges, not the geometry's job count",
     "    return ranges[:jobs]\n", "    return ranges[:concurrency]\n"),
    ("M04", "memory bound off by one (>=): a geometry exactly filling the slot is refused",
     "if memory > SLOT_MEMORY_GIB:", "if memory >= SLOT_MEMORY_GIB:"),
    ("M05", "CPU bound computed on the fallback width instead of the geometry width",
     "cpus = self.jobs * self.cpus\n", "cpus = self.jobs * self.range_widths[-1]\n"),
    ("M06", "alignment enforced only at the 16/12 widths (6/8 unaligned accepted)",
     "        if first % width:\n", "        if width in (16, 12) and first % width:\n"),
    ("M07", "integer check accepts bool",
     "if type(value) is not int:", "if not isinstance(value, int):"),
    ("M08", "8-CPU geometry also accepts 6-CPU ranges",
     "8: (8,), 6: (6,)}", "8: (8, 6), 6: (6,)}"),
    ("M09", "job_cpu_ranges bounds concurrency by the 8-job maximum, not the geometry",
     "    if not 1 <= concurrency <= jobs:\n", "    if not 1 <= concurrency <= MAX_CONCURRENT_JOBS:\n"),
    ("M10", "service share shrunk to 1 GiB",
     "SLOT_SERVICE_MEMORY_GIB = 4\n", "SLOT_SERVICE_MEMORY_GIB = 1\n"),
    ("M11", "--selftest silently accepts --job-memory",
     "            or args.job_memory is not None\n", ""),
    ("M12", "--jobs ignored by the command-line geometry",
     '(("jobs", jobs), ("cpus", cpus)', '(("cpus", cpus)'),
    ("M13", "act command built from the default geometry, not the chosen one",
     "    geometry = JOB_GEOMETRY.get()\n    artifact_path", "    geometry = DEFAULT_JOB_GEOMETRY\n    artifact_path"),
    ("M14", "host bound skipped at the 6/8 widths",
     "        if last >= host_cpus:\n", "        if last >= host_cpus and width in (16, 12):\n"),
    ("M15", "swap cap left at the default 8g while memory follows the geometry",
     "--memory-swap={geometry.container_memory}\",\n        \"--network\"", "--memory-swap={DEFAULT_JOB_GEOMETRY.container_memory}\",\n        \"--network\""),
    ("M16", "replay concurrency bounded by the 8-job maximum, not the geometry",
     "return min(JOB_GEOMETRY.get().jobs, count)", "return min(MAX_CONCURRENT_JOBS, count)"),
    ("M17", "per-job memory cap admits 0 GiB",
     "if not 1 <= self.memory_gib <= MAX_CONTAINER_MEMORY_GIB:", "if not 0 <= self.memory_gib <= MAX_CONTAINER_MEMORY_GIB:"),
    ("M18", "per-job memory ceiling raised to 16 GiB",
     "MAX_CONTAINER_MEMORY_GIB = 8\n", "MAX_CONTAINER_MEMORY_GIB = 16\n"),
    ("M19", "replay CPU limit raised to 80",
     "REPLAY_CPU_LIMIT = 64\n", "REPLAY_CPU_LIMIT = 80\n"),
    ("M20", "overlap check dropped",
     "    if shared:\n        raise Refusal(\"CPU ranges overlap: \" + shared[0])\n", ""),
    ("M21", "default container memory format changes to 8G (upper-case unit)",
     'return f"{self.memory_gib}g"', 'return f"{self.memory_gib}G"'),
    ("M22", "geometry refusal not caught in main (escapes as a traceback, after nothing ran)",
     "    try:\n        JOB_GEOMETRY.set(job_geometry_arguments(args.jobs, args.job_cpus, args.job_memory))\n",
     "    JOB_GEOMETRY.set(job_geometry_arguments(args.jobs, args.job_cpus, args.job_memory))\n    try:\n"),
    ("M23", "the slot OOM reason names the default cap, not the run's",
     "a job container's {JOB_GEOMETRY.get().container_memory} ", "a job container's {DEFAULT_JOB_GEOMETRY.container_memory} "),
    ("B02", "BASE twin of M02: --concurrent-jobs not capped by booked ranges",
     "str(min(CONCURRENT_JOB_LIMIT, len(BOOKED_CPU_RANGES.get()))),", "str(CONCURRENT_JOB_LIMIT),"),
    ("B09", "BASE twin of M09: job_cpu_ranges bound raised to 8",
     "    if not 1 <= concurrency <= CONCURRENT_JOB_LIMIT:\n", "    if not 1 <= concurrency <= 8:\n"),
    ("M24", "6-CPU geometry keeps a 12-CPU fallback",
     "8: (8,), 6: (6,)}", "8: (8,), 6: (12, 6)}"),
]

def run(mutant, clean, out, sbx):
    ident, desc, old, new = mutant
    source = (pathlib.Path(clean) / "scripts/act_ci.py").read_text()
    count = source.count(old)
    d = pathlib.Path(out) / ident
    d.mkdir(parents=True, exist_ok=True)
    if count != 1:
        return ident, desc, f"NOT-APPLIED (old occurs {count}x)", []
    target = d / "act_ci.py"
    if target.exists():
        target.chmod(0o644)
    target.write_text(source.replace(old, new))
    target.chmod(0o555)
    subprocess.run([sbx, str(d / "run"), clean, sys.executable, "-I", str(target), "--selftest",
                    "--worktree", clean], check=False)
    rc = (d / "run.rc").read_text().strip()
    log = (d / "run.log").read_text(errors="replace")
    fails = [re.sub(r"^\s*FAIL\s+", "", l) for l in log.splitlines() if re.match(r"^\s*FAIL\s", l)]
    tail = log.strip().splitlines()[-1] if log.strip() else ""
    killed = rc != "0" or bool(fails)
    return ident, desc, f"{'KILLED' if killed else 'SURVIVED'} rc={rc} fails={len(fails)} last={tail[:120]!r}", fails

def main():
    clean, out, sbx = sys.argv[1:4]
    jobs = int(sys.argv[4]) if len(sys.argv) > 4 else 12
    only = set(sys.argv[5].split(",")) if len(sys.argv) > 5 else None
    global MUTANTS
    MUTANTS = [m for m in MUTANTS if only is None or m[0] in only]
    with concurrent.futures.ThreadPoolExecutor(jobs) as pool:
        results = list(pool.map(lambda m: run(m, clean, out, sbx), MUTANTS))
    for ident, desc, verdict, fails in results:
        print(f"{ident} {verdict} :: {desc}")
        for f in fails[:6]:
            print(f"    FAIL {f[:220]}")
        if len(fails) > 6:
            print(f"    ... {len(fails) - 6} more")

main()
