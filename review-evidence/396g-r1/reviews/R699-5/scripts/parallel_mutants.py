#!/usr/bin/env python3
"""Run the tracked release-control mutants in parallel, with the driver's own kill rule.

Usage: python3 -I parallel_mutants.py <repo> <workdir> <jobs> [name-substring ...]

Each mutant runs on its own copy of tb/tools/torture_campaign.py under <workdir>;
the repository is only read. A mutant is killed when the self-test exits 1 and
names its test as FAIL, exactly as tb/tools/torture_release_mutants.py requires.
"""
import concurrent.futures
import hashlib
import subprocess
import sys
import time
from pathlib import Path


def main() -> int:
    repo, work, jobs = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), int(sys.argv[3])
    only = sys.argv[4:]
    sys.path.insert(0, str(repo / "tb" / "tools"))
    from torture_release_mutants import MUTANTS  # noqa: E402
    source = repo / "tb" / "tools" / "torture_campaign.py"
    original = source.read_bytes()
    text = original.decode("utf-8")
    print("source sha256", hashlib.sha256(original).hexdigest(), "mutants", len(MUTANTS), flush=True)
    work.mkdir(parents=True, exist_ok=True)
    chosen = [(i, m) for i, m in enumerate(MUTANTS) if not only or any(s in m[0] for s in only)]

    def one(item):
        i, (name, old, new, test) = item
        if text.count(old) != 1:
            return i, name, "ANCHOR", 0.0, ""
        d = work / f"m{i:03d}"
        d.mkdir(exist_ok=True)
        cand = d / "torture_campaign.py"
        cand.write_text(text.replace(old, new), encoding="utf-8")
        t = time.monotonic()
        try:
            r = subprocess.run([sys.executable, "-B", str(cand), "--self-test"], capture_output=True,
                               text=True, timeout=600, cwd=d)
        except subprocess.TimeoutExpired:
            return i, name, "TIMEOUT", time.monotonic() - t, test
        dt = time.monotonic() - t
        ok = r.returncode == 1 and f"FAIL: {test} " in r.stderr
        return i, name, "KILLED" if ok else f"SURVIVED rc={r.returncode}", dt, test

    bad = 0
    with concurrent.futures.ThreadPoolExecutor(jobs) as pool:
        for i, name, status, dt, test in pool.map(one, chosen):
            bad += status != "KILLED"
            print(f"{status}\t{dt:6.1f}s\t#{i}\t{name}\t{test}", flush=True)
    if source.read_bytes() != original:
        print("FAIL: source changed")
        return 2
    print(f"{'PASS' if not bad else 'FAIL'}: {len(chosen) - bad} of {len(chosen)} killed", flush=True)
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
