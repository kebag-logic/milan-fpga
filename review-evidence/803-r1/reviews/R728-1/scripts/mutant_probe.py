#!/usr/bin/env python3
"""Plant one textual defect in a disposable copy of a clean tree, run one
suite command there, and record which of the named checks print FAIL.

Usage:
  mutant_probe.py --clean-tree DIR --work DIR --id ID --file REL
                  --old TEXT --new TEXT --cmd CMD --expect NAME [--expect NAME]
                  [--env K=V] --out JSON

The planted text must match exactly once. The copy is made with `cp -a`,
so the clean tree is never touched. A run is KILLED when every --expect
name appears on a line that also carries FAIL; SURVIVED otherwise.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import time


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--clean-tree", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--id", required=True)
    ap.add_argument("--file", default="")
    ap.add_argument("--old", default="")
    ap.add_argument("--new", default="")
    ap.add_argument("--cmd", required=True)
    ap.add_argument("--expect", action="append", default=[])
    ap.add_argument("--env", action="append", default=[])
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    dst = os.path.join(a.work, a.id)
    if os.path.exists(dst):
        shutil.rmtree(dst)
    subprocess.run(["cp", "-a", a.clean_tree, dst], check=True)
    planted = False
    if a.file:
        path = os.path.join(dst, a.file)
        with open(path, encoding="utf-8") as fh:
            src = fh.read()
        n = src.count(a.old)
        if n != 1:
            print(f"{a.id}: planted text matches {n} times, need 1",
                  file=sys.stderr)
            return 2
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(src.replace(a.old, a.new))
        planted = True

    env = dict(os.environ)
    for kv in a.env:
        k, v = kv.split("=", 1)
        env[k] = v
    log_path = os.path.join(a.work, a.id + ".log")
    t0 = time.time()
    with open(log_path, "w", encoding="utf-8") as log:
        rc = subprocess.run(["bash", "-c", a.cmd], cwd=dst, env=env,
                            stdout=log, stderr=subprocess.STDOUT).returncode
    secs = round(time.time() - t0, 1)
    with open(log_path, encoding="utf-8", errors="replace") as fh:
        lines = fh.read().splitlines()
    fail_lines = [ln for ln in lines if "FAIL" in ln]
    hits = {}
    for name in a.expect:
        hit = [ln for ln in fail_lines if name in ln]
        hits[name] = hit[0][:300] if hit else None
    verdict = ("CLEAN" if not planted else
               ("KILLED" if a.expect and all(hits.values()) else "SURVIVED"))
    tally = [ln for ln in lines if "checks:" in ln or " pass, " in ln][-3:]
    res = {"id": a.id, "file": a.file, "old": a.old, "new": a.new,
           "cmd": a.cmd, "rc": rc, "seconds": secs, "verdict": verdict,
           "named_checks": hits, "fail_line_count": len(fail_lines),
           "tally": tally}
    with open(a.out, "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1)
    print(json.dumps({k: res[k] for k in ("id", "rc", "verdict",
                                            "fail_line_count", "seconds")}))
    shutil.rmtree(dst, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
