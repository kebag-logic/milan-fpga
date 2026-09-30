#!/usr/bin/env python3
"""Reviewer probes for PR #135 round 3 (disposable; never touches the clone).

Each probe is a literal string substitution in hdl/maap/KL_pp_maap.sv of a
scratch copy of the exact head tree; the unified diff is saved as a patch and
tb/maap is built and run. A probe counts as KILLED only when the simulation
finishes with a tally, rc != 0 and at least one FAIL line.

Also runs the head tb/maap bench against the round-1 RTL (b03d36f) to measure
how many of U29's 20 one-cycle falls that RTL absorbs.

usage: own_probes.py --clone <exact-head clone> --out <packet dir>
env:   PATH must resolve `verilator` to the pinned (capped) wrapper.
"""
import argparse
import difflib
import re
import shutil
import subprocess
from pathlib import Path

RTL = "hdl/maap/KL_pp_maap.sv"
HEAD = "921fff59d6e1243284e477f7a368173018420d35"
ROUND1 = "b03d36f2c763061e3c9f1dcc19e4f7aee0f1a745"

PROBES = {
    # a one-cycle fall first seen in W_POST is absorbed (rel_pend only)
    "r401-3-post-ignores-own-fall": [(
        "          if (!eng_w || rel_pend_r) begin\n",
        "          if (rel_pend_r) begin\n")],
    # the latch keeps the claim through the drain (pstate not dropped)
    "r401-3-latch-keeps-claim": [(
        "        pstate_r   <= P_INITIAL;\n        rel_pend_r <= 1'b1;\n",
        "        rel_pend_r <= 1'b1;\n")],
    # the TX-state latch honoured in DEFEND only: a mid-walk PROBE absorbs it
    "r401-3-latch-defend-only": [(
        "      if (!eng_w && (w_st_r inside {W_ALLOC, W_GWAIT, W_WRITE, W_COMMIT,\n"
        "                                    W_LANE})) begin\n",
        "      if (!eng_w && (pstate_r == P_DEFEND)\n"
        "          && (w_st_r inside {W_ALLOC, W_GWAIT, W_WRITE, W_COMMIT,\n"
        "                             W_LANE})) begin\n")],
    # the TX-state latch skipped while an sDefend frame is being sent
    "r401-3-latch-skips-sdefend": [(
        "      if (!eng_w && (w_st_r inside {W_ALLOC, W_GWAIT, W_WRITE, W_COMMIT,\n"
        "                                    W_LANE})) begin\n",
        "      if (!eng_w && (send_msg_r != MSG_DEFEND_C)\n"
        "          && (w_st_r inside {W_ALLOC, W_GWAIT, W_WRITE, W_COMMIT,\n"
        "                             W_LANE})) begin\n")],
    # W_IVAL honours a fall only for the announce draw (PROBE entry absorbs)
    "r401-3-ival-announce-only": [(
        "        W_IVAL: begin\n          if (!eng_w) begin\n",
        "        W_IVAL: begin\n          if (!eng_w && ival_ann_r) begin\n")],
}

TALLY = re.compile(r"^(\d+) checks: \d+ PASS, (\d+) FAIL", re.M)


def sh(cmd, cwd=None, log=None):
    if log is None:
        return subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True).stdout
    with open(log, "w") as f:
        return subprocess.run(cmd, cwd=cwd, stdout=f, stderr=subprocess.STDOUT).returncode


def fresh_tree(clone: Path, dst: Path, rev: str) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    dst.mkdir(parents=True)
    arc = subprocess.run(["git", "-C", str(clone), "archive", rev], check=True, capture_output=True).stdout
    subprocess.run(["tar", "-x", "-C", str(dst)], input=arc, check=True)


def run_maap(tree: Path, log: Path):
    rc = sh(["make", "-C", str(tree / "tb/maap"), "run"], log=log)
    text = log.read_text()
    t = TALLY.findall(text)
    fails = [l for l in text.splitlines() if l.startswith("FAIL:")]
    return rc, (tuple(map(int, t[-1])) if t else None), fails, text


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--clone", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    scratch = a.out / "scratch" / "probes"
    mdir = a.out / "mutations"
    rdir = a.out / "receipts" / "own-probes"
    mdir.mkdir(parents=True, exist_ok=True)
    rdir.mkdir(parents=True, exist_ok=True)
    base_src = sh(["git", "-C", str(a.clone), "show", f"{HEAD}:{RTL}"])
    summary = []
    for name, subs in PROBES.items():
        src = base_src
        for old, new in subs:
            if src.count(old) != 1:
                raise SystemExit(f"{name}: anchor not unique ({src.count(old)})")
            src = src.replace(old, new)
        patch = "".join(difflib.unified_diff(base_src.splitlines(True), src.splitlines(True),
                                             f"a/{RTL}", f"b/{RTL}"))
        (mdir / f"{name}.patch").write_text(patch)
        tree = scratch / name
        fresh_tree(a.clone, tree, HEAD)
        (tree / RTL).write_text(src)
        rc, tally, fails, text = run_maap(tree, rdir / f"{name}-maap.log")
        u29 = [l for l in text.splitlines() if l.startswith("  U29:") and "ABSORBED" in l]
        verdict = "KILLED" if (rc != 0 and tally and tally[1] > 0 and fails) else "SURVIVED"
        named = sorted({re.match(r"FAIL: (U\d+\w?):", l).group(1) for l in fails
                        if re.match(r"FAIL: (U\d+\w?):", l)})
        line = (f"{name}: rc={rc} tally={tally} fails={len(fails)} suites={','.join(named)} "
                f"U29-absorbed={len(u29)} {verdict}")
        print(line, flush=True)
        for l in u29:
            print("   ", l.strip(), flush=True)
        summary.append(line)
        shutil.rmtree(tree)
    # U29 against the round-1 RTL (only KL_pp_maap.sv replaced)
    tree = scratch / "round1-rtl"
    fresh_tree(a.clone, tree, HEAD)
    (tree / RTL).write_text(sh(["git", "-C", str(a.clone), "show", f"{ROUND1}:{RTL}"]))
    rc, tally, fails, text = run_maap(tree, rdir / "round1-rtl-head-bench-maap.log")
    u29 = [l for l in text.splitlines() if l.startswith("  U29:")]
    absorbed = sum("ABSORBED" in l for l in u29)
    line = (f"round-1 RTL {ROUND1[:8]} under the head bench: rc={rc} tally={tally} "
            f"U29 lines={len(u29)} absorbed={absorbed}")
    print(line, flush=True)
    for l in fails:
        if l.startswith("FAIL: U29"):
            print("   ", l, flush=True)
    summary.append(line)
    shutil.rmtree(tree)
    (rdir / "summary.txt").write_text("\n".join(summary) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
