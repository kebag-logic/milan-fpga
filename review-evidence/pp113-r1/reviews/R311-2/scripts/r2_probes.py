#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Round-2 reviewer probes for processor issue #113 / PR #115.

Two groups, each exported from the exact head with `git archive` and built
with the processor's own `gsi-build` target, run with `--gsi-internal-only`:

  h-*  the head's own latency mutants, read unmodified from the exported
       tb/pp_top/gsi_mutants.py mutations() list (the trigger removal and
       the six comparator truncations), graded with that runner's rule:
       completed run, rc 1, and a FAIL line starting with the named check;
  x-*  reviewer-chosen comparator weakenings outside the six truncations.

Usage:
  r2_probes.py --repo CLONE --rev SHA --verilator PATH --scratch DIR \
               --out DIR [--workers 2 --jobs 4] [--only name,...]
workers * jobs is the total parallel compile budget (at most 8).
"""

import argparse
import concurrent.futures as cf
import importlib.util
import io
import json
import re
import shutil
import subprocess
import tarfile
from pathlib import Path

SRP = "hdl/srp/KL_srp_listener_fsm.sv"
CMP = "(lat_r[s] != evt_acc_latency_i)"

# name, [(file, old, new, count)], required failing check prefix or None
EXTRA = [
    ("golden", [], None),
    # bit 0 dropped: missed first at the walking-one bit 0 step
    ("x-cmp-no-bit0",
     [(SRP, CMP, "(lat_r[s][31:1] != evt_acc_latency_i[31:1])", 1)],
     "GI LATENCY-WALK-ONE bit 0 step: exactly one unsolicited response"),
    # one interior bit masked out
    ("x-cmp-no-bit17",
     [(SRP, CMP, "((lat_r[s] & ~32'h00020000) != (evt_acc_latency_i & ~32'h00020000))", 1)],
     "GI LATENCY-WALK-ONE bit 17 step: exactly one unsolicited response"),
    # only 0->1 bit flips detected: the walking-one return (1->0) is missed
    ("x-cmp-rise-only",
     [(SRP, CMP, "((evt_acc_latency_i & ~lat_r[s]) != 32'd0)", 1)],
     "GI LATENCY-WALK-ONE bit 0 return: exactly one unsolicited response"),
    # the [2:0] narrowing named by the prior internal round-1 review
    ("x-cmp-low3",
     [(SRP, CMP, "(lat_r[s][2:0] != evt_acc_latency_i[2:0])", 1)],
     "GI LATENCY-WALK-ONE bit 3 step: exactly one unsolicited response"),
    # parity of the difference: every single-bit walk step is odd and so
    # detected; only the original multi-bit (even-weight) cases can kill it
    ("x-cmp-parity",
     [(SRP, CMP, "(^(lat_r[s] ^ evt_acc_latency_i))", 1)],
     "GI LATENCY-CHANGE: exactly one unsolicited response"),
]


def head_mutants(tree: Path):
    spec = importlib.util.spec_from_file_location(
        "head_gsi_mutants", tree / "tb/pp_top/gsi_mutants.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    out = []
    for name, fname, old, new, count, expected in mod.mutations():
        if name.startswith("latency-"):
            out.append(("h-" + name, [(fname, old, new, count)], expected))
    return out


def export(repo: Path, rev: str, dest: Path) -> None:
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    data = subprocess.run(["git", "-C", str(repo), "archive", rev, "hdl",
                           "tb/common", "tb/pp_top"], check=True,
                          stdout=subprocess.PIPE).stdout
    with tarfile.open(fileobj=io.BytesIO(data)) as tar:
        tar.extractall(dest)


def run_variant(args, name, edits, expected):
    tree = Path(args.scratch) / name
    export(Path(args.repo), args.rev, tree)
    for fname, old, new, count in edits:
        p = tree / fname
        text = p.read_text()
        if text.count(old) != count:
            return {"variant": name, "error": f"edit site count {text.count(old)} != {count} in {fname}"}
        p.write_text(text.replace(old, new))
    mk = tree / "tb/pp_top/Makefile"
    mk.write_text(mk.read_text().replace("--build -j 0", f"--build -j {args.jobs}", 1))
    out = Path(args.out)
    blog = out / f"{name}-build.log"
    rlog = out / f"{name}-run.log"
    bench = tree / "tb/pp_top"
    with blog.open("w") as s:
        brc = subprocess.run(["make", "gsi-build", "VERILATOR=" + args.verilator],
                             cwd=bench, stdout=s, stderr=subprocess.STDOUT,
                             timeout=3600).returncode
    if brc != 0:
        return {"variant": name, "build_rc": brc, "verdict": "BUILD-FAILED"}
    with rlog.open("w") as s:
        rrc = subprocess.run(["./obj_dir/Vpp_top_sim", "--gsi-internal-only"],
                             cwd=bench, stdout=s, stderr=subprocess.STDOUT,
                             timeout=3600).returncode
    text = rlog.read_text()
    fails = [l for l in text.splitlines() if l.startswith("FAIL: ")]
    tally = [l for l in text.splitlines() if re.search(r"\d+ checks", l)]
    complete = "[build default," in text
    if name == "golden":
        verdict = "PASS" if (rrc == 0 and not fails and complete) else "GOLDEN-FAILED"
    elif expected is None:
        verdict = "SURVIVED" if (rrc == 0 and not fails and complete) else "KILLED"
    else:
        named = [l for l in fails if l.startswith("FAIL: " + expected)]
        verdict = ("KILLED-BY-NAMED-CHECK" if (rrc == 1 and named and complete)
                   else "NOT-KILLED-AS-REQUIRED")
    first_named = next((l for l in fails if expected and l.startswith("FAIL: " + expected)), None)
    shutil.rmtree(bench / "obj_dir", ignore_errors=True)
    return {"variant": name, "edits": [[e[0], e[1], e[2]] for e in edits],
            "build_rc": brc, "run_rc": rrc,
            "expected_named_check": expected, "verdict": verdict,
            "first_named_failure": first_named,
            "fail_lines": fails[:8], "fail_count": len(fails),
            "tally": tally[-2:]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--verilator", required=True)
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--only", default="")
    args = ap.parse_args()
    assert args.workers * args.jobs <= 8
    Path(args.out).mkdir(parents=True, exist_ok=True)
    defs = Path(args.scratch) / "_defs"
    export(Path(args.repo), args.rev, defs)
    variants = EXTRA[:1] + head_mutants(defs) + EXTRA[1:]
    sel = [v for v in variants if not args.only or v[0] in args.only.split(",")]
    results = []
    with cf.ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(run_variant, args, *v): v[0] for v in sel}
        for f in cf.as_completed(futs):
            r = f.result()
            print(json.dumps(r), flush=True)
            results.append(r)
    order = [v[0] for v in variants]
    results.sort(key=lambda r: order.index(r["variant"]))
    (Path(args.out) / "results.json").write_text(json.dumps(results, indent=2) + "\n")


if __name__ == "__main__":
    main()
