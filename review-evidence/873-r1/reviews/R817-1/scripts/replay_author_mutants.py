#!/usr/bin/env python3
"""Re-run the author's published planted defects with a reviewer-owned harness.

Usage: python3 -I replay_author_mutants.py <mutants.json> <head act_ci.py> <head worktree> <out dir> [jobs]

Reads only the data fields (`mutant`, `old`, `new`, `fails`) of the published
mutants.json; the author's script is not executed. Each `old` must occur
exactly once in the committed head runner. Each copy runs as a flat installed
`python3 -I <copy> --selftest --worktree <head>`. Reports, per mutant, the
exit status, the reviewer-observed FAIL lines, any uncaught Refusal, and
whether the observed FAIL set equals the published one.
"""
from __future__ import annotations

import concurrent.futures
import json
import pathlib
import subprocess
import sys


def main() -> int:
    mutants = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
    source = pathlib.Path(sys.argv[2]).read_text(encoding="utf-8")
    worktree, out = sys.argv[3], pathlib.Path(sys.argv[4])
    jobs = int(sys.argv[5]) if len(sys.argv) > 5 else 16
    out.mkdir(parents=True, exist_ok=True)

    def run(entry: dict) -> tuple[str, int, list[str], str, bool]:
        name, old, new = entry["mutant"], entry["old"], entry["new"]
        if source.count(old) != 1:
            return name, -1, [f"anchor occurs {source.count(old)} times"], "", False
        directory = out / "copies" / name
        directory.mkdir(parents=True, exist_ok=True)
        copy = directory / "act_ci.py"
        if copy.exists():
            copy.chmod(0o644)
        copy.write_text(source.replace(old, new), encoding="utf-8")
        copy.chmod(0o555)
        result = subprocess.run([sys.executable, "-I", str(copy), "--selftest", "--worktree", worktree],
                                cwd=worktree, capture_output=True, text=True, timeout=900)
        log = result.stdout + result.stderr
        (out / f"{name}.log").write_text(log, encoding="utf-8")
        fails = [line.strip() for line in log.splitlines() if line.lstrip().startswith("FAIL")]
        uncaught = next((line for line in reversed(log.splitlines()) if line.startswith("Refusal:")), "")
        published = entry["fails"] if isinstance(entry["fails"], list) else json.loads(entry["fails"])
        return name, result.returncode, fails, uncaught, sorted(fails) == sorted(published)

    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as pool:
        results = list(pool.map(run, mutants))
    survived = 0
    for name, rc, fails, uncaught, same in results:
        survived += rc == 0
        print(f"{name} {'KILLED' if rc not in (0, -1) else ('SURVIVED' if rc == 0 else 'ANCHOR')} rc={rc} "
              f"fail_lines={len(fails)} matches_published={same}" + (f" uncaught={uncaught[:160]!r}" if uncaught else ""))
        for line in fails[:8]:
            print(f"    {line[:220]}")
    print(f"author planted: {len(mutants)} killed: {sum(1 for r in results if r[1] not in (0, -1))} "
          f"survived: {survived} anchor problems: {sum(1 for r in results if r[1] == -1)} "
          f"fail sets equal to published: {sum(1 for r in results if r[4])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
