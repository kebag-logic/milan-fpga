#!/usr/bin/env python3
"""Reviewer probe of the connected #545 tail oracle (milan_dp gmstep leg).

Copies the scratch head's tb/verilator/milan_dp into a sibling directory,
adds one printf to check_slew_connection() reporting the oracle's counters
(tail samples, servo-high samples, alignment errors), and builds the leg
through its own `make gmstep-build` recipe against datapath variants:
  head        - unchanged datapath; the head must pass, tail samples > 0
  tail3       - release tail shortened 4 -> 3 stages; must FAIL coverage
  tail12      - release tail lengthened 4 -> 12 (over-coverage); records the
                verdict, since the oracle is one-sided by construction
  addend2     - two extra registers on the counter addend; must FAIL
Nothing tracked in the reviewed clone is touched.
"""
import concurrent.futures as cf
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

PKT = Path(os.environ.get("PKT", "$REVIEWS/545-r301-2-packet"))
TREE = PKT / "scratch/tree"
SRC_DIR = TREE / "tb/verilator/milan_dp"
PROBE = TREE / "tb/verilator/milan_dp_r301probe"
DP = TREE / "hdl/milan/milan_datapath.sv"
WORK = PKT / "scratch/connected_probe"

TAIL_DECL = "logic [3:0] gptp_slew_tail_r;"
TAIL_SHIFT = "{gptp_slew_tail_r[2:0], gptp_slew_active_w}"
ADJ_PORT = "    .adj_i                (phc_adj_ts_w),"
ADJ_DELAY = ("  logic [31:0] r301_adj_d1_r, r301_adj_d2_r;\n"
             "  always_ff @(posedge gtx_clk) begin : r301_addend_delay\n"
             "    r301_adj_d1_r <= phc_adj_ts_w;\n"
             "    r301_adj_d2_r <= r301_adj_d1_r;\n"
             "  end : r301_addend_delay\n")
COUNTER_OPEN = "  timestamp_counter #("


def variants(src: str) -> dict:
    for anchor in (TAIL_DECL, TAIL_SHIFT, ADJ_PORT):
        assert src.count(anchor) == 1, anchor
    # the counter instance that carries ADJ_PORT
    i = src.index(ADJ_PORT)
    j = src.rindex(COUNTER_OPEN, 0, i)
    add2 = src[:j] + ADJ_DELAY + src[j:i] + ADJ_PORT.replace("(phc_adj_ts_w)", "(r301_adj_d2_r)") \
        + src[i + len(ADJ_PORT):]
    return {
        "head": src,
        "tail3": src.replace(TAIL_DECL, "logic [2:0] gptp_slew_tail_r;")
                    .replace(TAIL_SHIFT, "{gptp_slew_tail_r[1:0], gptp_slew_active_w}"),
        "tail12": src.replace(TAIL_DECL, "logic [11:0] gptp_slew_tail_r;")
                     .replace(TAIL_SHIFT, "{gptp_slew_tail_r[10:0], gptp_slew_active_w}"),
        "addend2": add2,
    }


def prepare() -> None:
    if PROBE.exists():
        shutil.rmtree(PROBE)
    shutil.copytree(SRC_DIR, PROBE, ignore=shutil.ignore_patterns("obj_*"))
    h = PROBE / "sim_gmstep.cpp"
    text = h.read_text()
    anchor = '    check_.that("slew path: PHC advances witness the release tail", slew_tail_samples_ > 0);'
    assert text.count(anchor) == 1
    text = text.replace(anchor, '    printf("R301PROBE tail_samples=%u servo_high_samples=%u alignment_errors=%u falls=%u\\n",\n'
                        '           slew_tail_samples_, slew_high_samples_, slew_alignment_errors_, slew_falls_);\n' + anchor)
    h.write_text(text)


def run(name: str, text: str) -> str:
    d = WORK / name
    d.mkdir(parents=True, exist_ok=True)
    dp = d / "milan_datapath.sv"
    dp.write_text(text)
    mdir = d / "obj"
    b = subprocess.run(["make", "-s", "-C", str(PROBE), "gmstep-build", f"GMSTEP_MDIR={mdir}",
                        f"DP_SRC={dp}"], capture_output=True, text=True)
    (d / "build.log").write_text(b.stdout + b.stderr)
    exe = mdir / "Vmilan_dp_gmstep"
    if b.returncode or not exe.is_file():
        return f"== {name}: BUILD FAILED (see scratch)"
    r = subprocess.run([str(exe), str(mdir / "aemi.bin")], cwd=str(PROBE), capture_output=True, text=True)
    out = r.stdout + r.stderr
    (d / "run.log").write_text(out)
    keep = [l for l in out.splitlines() if "slew path" in l or "R301PROBE" in l or
            re.search(r"== gmstep: checks|RESULT", l)]
    return f"== {name}: rc={r.returncode}\n" + "\n".join(keep)


def main() -> int:
    prepare()
    vs = variants(DP.read_text())
    sel = sys.argv[1:] or list(vs)
    with cf.ThreadPoolExecutor(max_workers=len(sel)) as ex:
        for res in ex.map(lambda n: run(n, vs[n]), sel):
            print(res, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
