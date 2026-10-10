# SPDX-License-Identifier: Apache-2.0
"""Apply reviewer plants to copies of a source tree and record the behave outcome.

Usage: python3 -I plants.py --tree DIR --spec SPEC.json --work NEW_DIR --prefix CGREEN [--jobs N]
Each spec entry: {"label", "file", "old", "new"}; "old" must occur exactly once.
An entry with "file": null runs the unmodified tree.
"""

import argparse
import concurrent.futures
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys


def failed_scenarios(output):
    names, listing = set(), False
    for line in output.splitlines():
        if line in ("Failing scenarios:", "Errored scenarios:"):
            listing = True
        elif listing and line.startswith("  "):
            names.add(line.split("  ")[-1])
        else:
            listing = False
    return sorted(names)


def run_one(entry, tree, work, prefix):
    label = entry["label"]
    root = work / label
    src = root / "src"
    shutil.copytree(tree, src)
    if entry.get("file"):
        path = src / entry["file"]
        text = path.read_text()
        if text.count(entry["old"]) != 1:
            return {"label": label, "error": "target occurs %d times" % text.count(entry["old"])}
        path.write_text(text.replace(entry["old"], entry["new"]))
    build = root / "build"
    env = os.environ.copy()
    env["LD_LIBRARY_PATH"] = str(prefix / "lib")
    env["SHLAN_LIBRARY"] = str(build / "libshlan.so")
    log = []
    for cmd in (["cmake", "-S", str(src), "-B", str(build), "-DCMAKE_BUILD_TYPE=Debug",
                 "-DCMAKE_PREFIX_PATH=" + str(prefix)],
                ["cmake", "--build", str(build), "--target", "shlan", "--parallel", "2"]):
        r = subprocess.run(cmd, capture_output=True, text=True)
        log.append(r.stdout + r.stderr)
        if r.returncode:
            (root / "build.log").write_text("\n".join(log))
            return {"label": label, "error": "build rc=%d" % r.returncode}
    r = subprocess.run([sys.executable, "-m", "behave", "--no-color", "tests/features"],
                       cwd=src, env=env, capture_output=True, text=True, timeout=300)
    out = r.stdout + r.stderr
    (root / "behave.log").write_text(out)
    asserts = sorted({line.strip() for line in out.splitlines()
                      if "Assertion Failed:" in line or "HOOK-ERROR" in line
                      or "no longer matches" in line})
    return {"label": label, "behave_rc": r.returncode, "failed": failed_scenarios(out),
            "assertions": asserts,
            "summary": [l for l in out.splitlines() if " passed, " in l]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tree", type=Path, required=True)
    ap.add_argument("--spec", type=Path, required=True)
    ap.add_argument("--work", type=Path, required=True)
    ap.add_argument("--prefix", type=Path, required=True)
    ap.add_argument("--jobs", type=int, default=4)
    a = ap.parse_args()
    a.work.mkdir(parents=True)
    spec = json.loads(a.spec.read_text())
    with concurrent.futures.ThreadPoolExecutor(a.jobs) as pool:
        results = list(pool.map(lambda e: run_one(e, a.tree.resolve(), a.work.resolve(),
                                                  a.prefix.resolve()), spec))
    print(json.dumps(results, indent=1))


if __name__ == "__main__":
    main()
