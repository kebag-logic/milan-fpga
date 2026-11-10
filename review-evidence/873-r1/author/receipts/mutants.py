#!/usr/bin/env python3
"""Plant one defect per copy of the committed act_ci.py and run its offline self-test.

usage: mutants.py <lane> <head sha> <out dir>
Each mutant replaces exactly one text (refused otherwise), is installed flat, and runs
`python3 -I <copy> --selftest --worktree <clean clone>`, as docs.yml's gate_42 second call does.
"""
import concurrent.futures
import json
import pathlib
import subprocess
import sys

lane, head, out = sys.argv[1], sys.argv[2], pathlib.Path(sys.argv[3])
out.mkdir(parents=True, exist_ok=True)
source = subprocess.run(["git", "-C", lane, "show", f"{head}:scripts/act_ci.py"],
                        check=True, capture_output=True, text=True).stdout
worktree = out / "wt"
if not worktree.exists():
    subprocess.run(["git", "clone", "-q", "--shared", "--no-checkout", lane, str(worktree)], check=True)
    subprocess.run(["git", "-C", str(worktree), "-c", "advice.detachedHead=false", "checkout", "-q",
                    "--detach", head], check=True)
assert subprocess.run(["git", "-C", str(worktree), "rev-parse", "HEAD"], capture_output=True,
                      text=True).stdout.strip() == head

MUTANTS = {
    "M1-no-memory-check": ("        if memory > SLOT_MEMORY_GIB:\n", "        if False:\n"),
    "M2-no-service-share": ("memory = self.jobs * self.memory_gib + SLOT_SERVICE_MEMORY_GIB",
                            "memory = self.jobs * self.memory_gib"),
    "M3-no-cpu-check": ("        if cpus > REPLAY_CPU_LIMIT:\n", "        if False:\n"),
    "M4-cpu-limit-128": ("REPLAY_CPU_LIMIT = 64\n", "REPLAY_CPU_LIMIT = 128\n"),
    "M5-concurrent-jobs-4": ("str(min(geometry.jobs, len(BOOKED_CPU_RANGES.get())))",
                             "str(min(4, len(BOOKED_CPU_RANGES.get())))"),
    "M6-fallback-12": ('"MILAN_CI_FALLBACK_CPUS=" + str(geometry.fallback_cpus)',
                       '"MILAN_CI_FALLBACK_CPUS=" + str(12)'),
    "M7-memory-8g": ('{boundary.token} "\n        f"--memory={geometry.container_memory} '
                     '--memory-swap={geometry.container_memory}"',
                     '{boundary.token} "\n        "--memory=8g --memory-swap=8g"'),
    "M8-select-4-ranges": ("    return ranges[:jobs]\n", "    return ranges[:4]\n"),
    "M9-widths-ignore-geometry": ("    widths = JOB_GEOMETRY.get().range_widths\n",
                                  "    widths = (16, 12, 8, 6)\n"),
    "M10-ranges-before-geometry": (
        "        JOB_GEOMETRY.set(job_geometry_arguments(args.jobs, args.job_cpus, args.job_memory))\n"
        "        BOOKED_CPU_RANGES.set(parse_cpu_ranges(args.cpu_ranges))\n",
        "        BOOKED_CPU_RANGES.set(parse_cpu_ranges(args.cpu_ranges))\n"
        "        JOB_GEOMETRY.set(job_geometry_arguments(args.jobs, args.job_cpus, args.job_memory))\n"),
    "M11-max-jobs-16": ("MAX_CONCURRENT_JOBS = 8\n", "MAX_CONCURRENT_JOBS = 16\n"),
    "M12-default-width-8": ("    cpus: int = 16\n", "    cpus: int = 8\n"),
    "M13-default-memory-4": ("    memory_gib: int = MAX_CONTAINER_MEMORY_GIB\n", "    memory_gib: int = 4\n"),
    "M14-no-job-count-bound": ("    if not 1 <= concurrency <= jobs:\n", "    if not 1 <= concurrency:\n"),
    "M15-no-range-count-check": ("    if len(ranges) < concurrency:\n", "    if False:\n"),
    "M16-no-alignment-check": ("        if first % width:\n", "        if False:\n"),
    "M17-memory-minimum-2": ("        if not 1 <= self.memory_gib <= MAX_CONTAINER_MEMORY_GIB:\n",
                             "        if not 2 <= self.memory_gib <= MAX_CONTAINER_MEMORY_GIB:\n"),
    "M18-memory-bound-inclusive": ("        if memory > SLOT_MEMORY_GIB:\n", "        if memory >= SLOT_MEMORY_GIB:\n"),
    "M19-guard-lets-jobs-through": ("            or args.jobs is not None\n", ""),
    "M20-guard-lets-job-cpus-through": ("            or args.job_cpus is not None\n", ""),
    "M21-guard-lets-job-memory-through": ("            or args.job_memory is not None\n", ""),
    "M22-concurrency-fixed-4": ("    return min(JOB_GEOMETRY.get().jobs, count)\n", "    return min(4, count)\n"),
}
if sys.argv[4:]:
    MUTANTS = {name: MUTANTS[name] for name in sys.argv[4:]}


def run(name: str) -> dict[str, object]:
    """Install one mutant flat and run its self-test; its log, rc and FAIL lines."""
    old, new = MUTANTS[name]
    assert source.count(old) == 1, f"{name}: expected one site, found {source.count(old)}"
    directory = out / name
    directory.mkdir(exist_ok=True)
    copy = directory / "act_ci.py"
    copy.write_text(source.replace(old, new))
    log = directory / "selftest.log"
    with open(log, "w") as stream:
        try:
            rc = subprocess.run(["python3", "-I", str(copy), "--selftest", "--worktree", str(worktree)],
                                stdout=stream, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                                cwd=directory, timeout=420).returncode
        except subprocess.TimeoutExpired:
            rc = "timeout after 420 s"
    lines = log.read_text(errors="replace").splitlines()
    copy.unlink()
    return {"mutant": name, "old": old.strip(), "new": new.strip(), "rc": rc,
            "fails": [line.strip() for line in lines if line.lstrip().startswith("FAIL")],
            "last": lines[-1] if lines else ""}


with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    results = list(pool.map(run, MUTANTS))
(out / ("mutants.json" if not sys.argv[4:] else "mutants-" + "-".join(sys.argv[4:]) + ".json")).write_text(json.dumps(results, indent=1) + "\n")
survivors = [r["mutant"] for r in results if r["rc"] == 0]
for r in results:
    print(f"{r['mutant']}: rc={r['rc']} fails={len(r['fails'])} last={r['last'][:100]}")
print("survivors:", survivors or "none")
sys.exit(1 if survivors else 0)
