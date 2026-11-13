#!/usr/bin/env python3
"""Rebuild every model the engine arm builds against an existing cache,
without simulating, and report ccache's counters for those builds alone.

usage: warm_build_probe.py <mutants.py> <work-root> <jobs>

Imports the arm from its own file. Stages the control and each RTL mutant
(generator mutants reuse the control's build) exactly as run_mutant does,
each in a new temporary directory under <work-root>, and builds each with
the arm's own build(), <jobs> at a time. CCACHE_DIR, OBJCACHE and PATH are
the caller's. Prints the build count, failures, and the counters.
"""
import importlib.util
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


def counters() -> dict[str, int]:
    """ccache's nonzero hit and miss counters."""
    out = subprocess.run(["ccache", "--print-stats"], capture_output=True, text=True)
    result = {}
    for line in out.stdout.splitlines():
        key, _, value = line.partition("\t")
        if value.isdigit() and int(value) and key.endswith(("hit", "miss")):
            result[key] = int(value)
    return result


def main() -> int:
    driver, root, jobs = sys.argv[1], Path(sys.argv[2]), int(sys.argv[3])
    spec = importlib.util.spec_from_file_location("arm", driver)
    arm = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(arm)
    entries = [("clean", None)] + [
        ("".join(c if c.isalnum() else "_" for c in m[0]), (m[1], arm.edits_of(m[2], m[3])))
        for m in arm.MUTATIONS if m[1] != arm.GENERATOR]
    subprocess.run(["ccache", "--zero-stats"], capture_output=True)

    def one(entry: tuple) -> bool:
        tag, mutate = entry
        own = Path(tempfile.mkdtemp(prefix="warm-", dir=root))
        return arm.build(arm.stage(own, tag, mutate), own, tag) is not None

    with ThreadPoolExecutor(max_workers=jobs) as pool:
        built = list(pool.map(one, entries))
    print(f"builds: {len(entries)}, built: {sum(built)}, failed: {len(entries) - sum(built)}")
    stats = counters()
    hits = sum(v for k, v in stats.items() if k in ("direct_cache_hit", "preprocessed_cache_hit"))
    print(f"ccache: {stats}")
    print(f"compilations from the cache: {hits}, misses: {stats.get('cache_miss', 0)}")
    return 0 if all(built) else 1


if __name__ == "__main__":
    sys.exit(main())
