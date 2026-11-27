#!/usr/bin/env python3
"""Build and run the base-vs-head differential for the head core and for chosen probe variants.
Usage: diff_run.py TREE DIFFDIR PROBES_JSON[,PROBES_JSON] NAMES(comma|all) OUT_JSON JOBS MAX_SINKS"""
import json, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
tree, d, pj, names, out, jobs, maxs = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], sys.argv[4], Path(sys.argv[5]), int(sys.argv[6]), sys.argv[7]
probes = {}
for f in pj.split(","):
    probes.update({p["name"]: p for p in json.loads(Path(f).read_text())})
sel = list(probes) if names == "all" else [n for n in names.split(",") if n]
pk = lambda *a: subprocess.run(["pkg-config", *a, "gtest", "gmock"], capture_output=True, text=True, check=True).stdout.split()
cf = ["-O1", "-g", "-Wall", "-Wextra", "-Werror", "-DNDEBUG", "-DCTRL_REENTRY_ASSERT", f"-DACMP_MAX_SINKS={maxs}u",
      "-fsanitize=shift,undefined", "-fno-sanitize-recover=shift,undefined", "-I" + str(tree / "include")]
b = d / f"build{maxs}"; b.mkdir(exist_ok=True)
def sh(cmd, log):
    r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=900); log.append(r.stdout); return r.returncode
log = []
assert sh(["gcc", "-std=c11", *cf, "-include", str(d / "old_rename.h"), "-c", str(d / "old_acmp.c"), "-o", str(b / "old.o")], log) == 0, log
assert sh(["g++", "-std=c++20", *cf, *pk("--cflags"), "-I" + str(tree / "tests"), "-c", str(d / "diff_old_new.cpp"), "-o", str(b / "t.o")], log) == 0, log
def one(name):
    w = b / name; shutil.rmtree(w, ignore_errors=True); w.mkdir()
    src = (tree / "src/acmp.c").read_text()
    if name != "head":
        p = probes[name]; assert src.count(p["old"]) == 1; src = src.replace(p["old"], p["new"])
    (w / "acmp.c").write_text(src); lg = []
    if sh(["gcc", "-std=c11", *cf, "-c", str(w / "acmp.c"), "-o", str(w / "new.o")], lg) or \
       sh(["g++", *cf, str(w / "new.o"), str(b / "old.o"), str(b / "t.o"), *pk("--libs"), "-lgtest_main", "-o", str(w / "t")], lg):
        return {"name": name, "result": "BUILD FAILED", "log": "".join(lg)[-1500:]}
    r = subprocess.run([str(w / "t"), "--gtest_brief=1"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=900)
    (w / "run.log").write_text(r.stdout)
    first = [l for l in r.stdout.splitlines() if "Failure" in l or "step" in l][:4]
    res = {"name": name, "rc": r.returncode, "result": "AGREE" if r.returncode == 0 else "DIVERGE", "first": first,
           "summary": [l for l in r.stdout.splitlines() if l.startswith("[  PASSED") or l.startswith("[  FAILED") or l.startswith("[  SKIPPED")]}
    print(res["result"], name, flush=True); return res
with ThreadPoolExecutor(jobs) as pool:
    res = list(pool.map(one, ["head"] + sel))
out.write_text(json.dumps(res, indent=1) + "\n")
