#!/usr/bin/env python3
"""extra_plants.py TREE WORK - reviewer probe for PR #685 (#665 lane FC), R522-1.

Defects the PR's own campaign (tb/verilator/mbx/mutants.py) does not plant,
each in a fresh copy of the extracted head tree TREE under WORK. For each arm:
the PR's suite through the Wishbone host (`make run-wb`), then the reviewer's
differential probe (run_diff_probe.sh, N=3000). Prints, per arm, whether the
suite and the probe each reddened. Arm "probe-control" plants one of the PR's
own defects (rx-own-any-unicast) to show the probe can fail.
VERILATOR must name the pinned Verilator 5.050.
"""
import concurrent.futures as cf
import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RX = "hdl/milan/mailbox/KL_mbx_rx.sv"
ARMS = (
    ("mismatch-not-saturating", RX,
     "if (mis_w && mismatch_r != 16'hFFFF) mismatch_r <= mismatch_r + 16'd1;",
     "if (mis_w) mismatch_r <= mismatch_r + 16'd1;"),
    ("mismatch-flag-not-cleared", RX,
     "        hit_r      <= 1'b0;\n        mis_r      <= 1'b0;\n        msg_r      <= '0;",
     "        hit_r      <= 1'b0;\n        msg_r      <= '0;"),
    ("own-tuple-on-index-without-interface", RX,
     "(MBX_TUPLE_DST_TBL_C[j] == MBX_DST_OWN_C && own_if_w && dst_r == own_mac_w)",
     "(MBX_TUPLE_DST_TBL_C[j] == MBX_DST_OWN_C && dst_r == own_mac_w)"),
    ("aecp-response-term-reads-target", "hdl/milan/mailbox/KL_mbx_pkg.sv",
     "MBX_CH_AECP_T1_OFFSET_C = 32'd26;", "MBX_CH_AECP_T1_OFFSET_C = 32'd18;"),
    ("probe-control", RX,
     "(MBX_TUPLE_DST_TBL_C[j] == MBX_DST_OWN_C && own_if_w && dst_r == own_mac_w)",
     "(MBX_TUPLE_DST_TBL_C[j] == MBX_DST_OWN_C && !dst_r[40])"),
)


def run(arm, tree: Path, work: Path):
    name, path, old, new = arm
    copy = work / name
    if copy.exists():
        shutil.rmtree(copy)
    shutil.copytree(tree, copy, symlinks=True)
    f = copy / path
    text = f.read_text()
    if text.count(old) != 1:
        return name, "NOT PLANTED", "", ""
    f.write_text(text.replace(old, new))
    mbx = copy / "tb/verilator/mbx"
    for d in ("obj_wb", "obj_axil", "obj_cosim", "obj_fw", "obj_if2"):
        shutil.rmtree(mbx / d, ignore_errors=True)
    suite = subprocess.run(["make", f"VERILATOR={os.environ['VERILATOR']}", "run-wb"], cwd=mbx,
                           capture_output=True, text=True)
    fails = [l for l in suite.stdout.splitlines() if l.startswith("[FAIL]")]
    s = f"suite rc {suite.returncode}, {len(fails)} failing check(s)" + (f"; first: {fails[0]}" if fails else "")
    env = dict(os.environ, N="3000", SEED="99")
    probe = subprocess.run([str(HERE / "run_diff_probe.sh"), str(copy), str(work / (name + "-probe")), "0"],
                           capture_output=True, text=True, env=env)
    lines = [l for l in probe.stdout.splitlines() if l.startswith(("[FAIL]", "differential", "RESULT"))]
    p = f"probe rc {probe.returncode}: " + " | ".join(lines[:3] + lines[-1:])
    return name, "planted", s, p


def main() -> int:
    tree, work = Path(sys.argv[1]), Path(sys.argv[2])
    work.mkdir(parents=True, exist_ok=True)
    with cf.ThreadPoolExecutor(max_workers=3) as ex:
        for name, state, s, p in ex.map(lambda a: run(a, tree, work), ARMS):
            print(f"== {name}: {state}\n   {s}\n   {p}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
