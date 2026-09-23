#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Failing arms for PR #107 correction round 1 (issue #106), author-side.

Usage: arms.py <repo> <rev> <scratch> <verilator-bin-dir> <out.txt> [ARM ...]

Each arm is planted into a fresh `git archive <rev>` export under <scratch>
(never the working checkout). A plant whose pattern does not occur exactly
once is refused. The four SRP suites run in that export under the given
simulator; the tally and every FAIL line are recorded. ARM "none" runs the
unmutated export.

X1/R1, X7, R8 and X2/R4 are the reviewers' own plants, copied verbatim from
R270-1 scripts/mutation_probes.py and R271-1 scripts/03_mutate.py. Y1 and Y2
are two further gate mutants of the same two classes.
"""
import concurrent.futures as cf
import hashlib
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

SUITES = ["srp_decoder", "srp_encoder", "srp_stream_fsms", "srp_top"]
DEC = "hdl/srp/KL_srp_decoder.sv"
CLEAR = "            la_done_r  <= 4'd0;          // a new MRPDU: every type may LeaveAll once\n"

ARMS = {
    "none": [],
    # X1-class. R270 X1 == R271 R1: any VectorHeader of the type closes the
    # gate, so a flagged vector after an unflagged one of its type is lost
    "X1/R1": [(DEC,
               "              if (la_first_w) begin\n"
               "                la_done_r[la_lane_w] <= 1'b1;\n",
               "              la_done_r[la_lane_w] <= 1'b1;\n"
               "              if (la_first_w) begin\n")],
    # X1-class (own): the lane fires only at a message's first VectorHeader
    # (MSRP), so a flagged vector behind an unflagged one in its message is lost
    "Y2": [(DEC,
            "  assign la_first_w = (vhdr1_r[7:5] == SRP_LEAVEALL_EV_C) && !la_done_r[la_lane_w];\n",
            "  assign la_first_w = (vhdr1_r[7:5] == SRP_LEAVEALL_EV_C) && !la_done_r[la_lane_w]\n"
            "                    && (!app_msrp_r || (listlen_cnt_r == 16'd1));\n")],
    # X7-class. R270 X7: re-armed only by a clean dual EndMark (at pdu_malformed_o <= 0)
    "X7": [(DEC, CLEAR, ""),
           (DEC, "              pdu_malformed_o <= 1'b0;\n",
            "              pdu_malformed_o <= 1'b0;\n              la_done_r       <= 4'd0;\n")],
    # X7-class. R271 R8: the same, planted at pdu_ok_o <= 1
    "R8": [(DEC, CLEAR, "\n"),
           (DEC, "              pdu_ok_o        <= 1'b1;\n",
            "              pdu_ok_o        <= 1'b1;\n              la_done_r       <= 4'd0;\n")],
    # X7-class (own): re-armed at a new MRPDU only when it is MSRP
    "Y1": [(DEC, CLEAR, "            if (mrp_msrp_i) la_done_r <= 4'd0;\n")],
    # R270 X2 == R271 R4 (the S1 suggestion): the Domain participant takes every MSRP lane
    "X2/R4": [("hdl/srp/KL_srp_top.sv",
               ".leaveall_tick_i     (dec_la_msrp_w[SRP_LA_DOMAIN_C] || p_la_msrp_r),",
               ".leaveall_tick_i     ((|dec_la_msrp_w) || p_la_msrp_r),")],
}


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def export(repo: str, rev: str, tree: Path):
    if tree.exists():
        shutil.rmtree(tree)
    tree.mkdir(parents=True)
    arch = subprocess.run(["git", "-C", repo, "archive", rev], check=True,
                          capture_output=True).stdout
    subprocess.run(["tar", "-x", "-C", str(tree)], input=arch, check=True)


def plant(tree: Path, path: str, old: str, new: str) -> str:
    f = tree / path
    s = f.read_text()
    n = s.count(old)
    if n != 1:
        raise SystemExit("refused: pattern occurs %d times in %s: %r" % (n, path, old[:70]))
    before = sha(f)
    f.write_text(s.replace(old, new, 1))
    return "%s %s -> %s" % (path, before, sha(f))


def run_suite(tree: Path, vbin: str, suite: str):
    d = tree / "tb" / suite
    env = dict(os.environ, PATH=vbin + ":" + os.environ.get("PATH", "/usr/bin:/bin"))
    p = subprocess.run(["make"], cwd=d, capture_output=True, text=True, env=env)
    log = p.stdout + p.stderr
    (tree / ("%s.run.log" % suite)).write_text(log)
    m = re.findall(r"(\d+) checks: (\d+) PASS, (\d+) FAIL", log)
    fails = [ln.strip() for ln in log.splitlines() if ln.startswith("FAIL:")]
    got = [ln.strip() for ln in log.splitlines() if ln.strip().startswith(("got :", "want:"))]
    tally = ("%s/%s FAIL" % (m[-1][2], m[-1][0])) if m else "NO-TALLY rc=%d" % p.returncode
    return suite, tally, fails, got


def main():
    repo, rev, scratch, vbin, out = sys.argv[1:6]
    arms = sys.argv[6:] or list(ARMS)
    full = subprocess.run(["git", "-C", repo, "rev-parse", rev], check=True,
                          capture_output=True, text=True).stdout.strip()
    ver = subprocess.run([vbin + "/verilator", "--version"], capture_output=True,
                         text=True).stdout.strip()
    lines = ["rev %s (%s)" % (full, rev), "simulator %s" % ver, ""]
    for arm in arms:
        tree = Path(scratch) / ("arm-%s-%s" % (full[:8], arm.replace("/", "_")))
        export(repo, full, tree)
        planted = [plant(tree, *p) for p in ARMS[arm]]
        with cf.ThreadPoolExecutor(max_workers=4) as ex:
            res = list(ex.map(lambda s: run_suite(tree, vbin, s), SUITES))
        killed = any(not t.startswith("0/") for _, t, _, _ in res)
        verdict = "baseline" if arm == "none" else ("KILLED" if killed else "SURVIVED")
        lines.append("%-6s %-8s %s" % (arm, verdict,
                     "  ".join("%s=%s" % (s, t) for s, t, _, _ in res)))
        print(lines[-1], flush=True)
        for p in planted:
            lines.append("         plant: " + p)
        for s, _, fails, got in res:
            for ln in fails:
                lines.append("         %s: %s" % (s, ln))
            for ln in got:
                lines.append("           %s" % ln)
    Path(out).write_text("\n".join(lines) + "\n")
    print(Path(out).read_text(), end="")


if __name__ == "__main__":
    main()
