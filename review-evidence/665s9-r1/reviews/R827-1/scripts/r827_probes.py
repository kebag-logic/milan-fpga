#!/usr/bin/env python3
"""r827_probes.py REPO WORK [--jobs N]: reviewer-planted RTL defects for the #870 timing cuts.

Each probe copies REPO/hdl/milan/mailbox to WORK/<probe>/rtl, applies ONE
substitution that must occur exactly once, builds the mailbox suite against
the copy with the suite Makefile's own verilator recipe (`make print-vflags`),
runs it through the named adapter, and records the exit status and every
[FAIL] line. A probe is CAUGHT when the run exits non-zero with at least one
[FAIL] line; the expected check is reported beside what actually failed.
The repository tree is never written. Exit 0 always; the table is the result.
"""
from __future__ import annotations

import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

RTL_FILES = ("KL_mbx_pkg.sv", "KL_mbx_ring.sv", "KL_mbx_rx.sv", "KL_mbx_tx.sv", "KL_mbx_evt.sv", "KL_mbx.sv",
             "KL_mbx_wb.sv", "KL_mbx_axil.sv")

# (name, file, old, new, host, expected check prefix, why)
PROBES = [
    ("control-unmodified", "KL_mbx_rx.sv", "", "", 0, "(none: must PASS)",
     "positive control through the Wishbone adapter"),
    ("control-unmodified-axil", "KL_mbx_rx.sv", "", "", 1, "(none: must PASS)",
     "positive control through the AXI4-Lite adapter"),
    ("p1-byte-taken-in-verdict-cycle", "KL_mbx_rx.sv",
     "assign rx_ready_o = (st_r == RECV_S) && (q_cnt_r < 3'(QD_C));",
     "assign rx_ready_o = (st_r == RECV_S || st_r == VRD_S) && (q_cnt_r < 3'(QD_C));", 0, "V0",
     "the next frame's first byte taken in the verdict's acting cycle, before the clean-up"),
    ("p3-cleanup-at-the-verdict-not-the-act", "KL_mbx_rx.sv",
     "if ((act_w && !accept_w) || st_r == HDR1_S) begin",
     "if (fin_ready_w || st_r == HDR1_S) begin", 0, "V0",
     "the frame state cleared when the verdict is taken, so the header is written from cleared state"),
    ("p15-port-address-only-zeroed", "KL_mbx_rx.sv",
     "      wr_addr_o <= waddr_w;\n",
     "      wr_addr_o <= wen_w ? waddr_w : '0;\n", 0, "W0",
     "only the port address carries the write decision again (the word does not)"),
    ("p16-port-word-only-zeroed", "KL_mbx_rx.sv",
     "      wr_data_o <= wdata_w;\n",
     "      wr_data_o <= wen_w ? wdata_w : '0;\n", 1, "W0",
     "only the port word carries the write decision again, through AXI4-Lite"),
    ("p12-head-published-from-unregistered-port", "KL_mbx_rx.sv",
     "        head_pub_r[c] <= head_r[c];\n",
     "        head_pub_r[c] <= (commit_w && ch_r == MBX_CH_W_C'(c)) ? head_r[c] + 16'd2 + 16'(widx_r)"
     " : head_r[c];\n", 0, "H0",
     "the published head moved in the commit cycle itself, two cycles before the last header word lands"),
    ("p17-verdict-reads-live-bucket", "KL_mbx_rx.sv",
     "  assign rate_w      = act_w && vd_rate_r;\n  assign accept_w    = act_w && vd_acc_r;\n",
     "  assign rate_w      = act_w && vd_rate_r && (tokens_r[ch_r] == 8'd0);\n"
     "  assign accept_w    = act_w && (vd_acc_r || (vd_rate_r && tokens_r[ch_r] != 8'd0));\n", 0,
     "V0 (or none: equivalent unless a refill lands between FIN and VRD)",
     "the rate verdict re-read in the acting cycle; differs only if a refill tick falls in that one cycle"),
    ("p18-verdict-not-gated-by-fin", "KL_mbx_rx.sv",
     "    end else if (fin_ready_w) begin\n      vd_drop_r <= hit_r && rule_pass_w && bad_w;",
     "    end else begin\n      vd_drop_r <= hit_r && rule_pass_w && bad_w;", 0,
     "(none expected: equivalent, values in VRD_S are the FIN cycle's sample either way)",
     "verdict registers sampled every cycle (equivalence probe, not a defect)"),
    ("p19-and-or-drops-eid-valid", "KL_mbx.sv",
     "rd_bnd_reg_w != 2'd2 && bnd_eid_vld_w;",
     "rd_bnd_reg_w != 2'd2;", 0, "R1 / bound-talker read-back",
     "an unwritten BOUND_EID word answered from the read-back memory instead of 0"),
    ("p20-register-read-offset-every-cycle", "KL_mbx.sv",
     "      if (reg_rd_w) rd_off_r <= off_w;\n",
     "      rd_off_r <= off_w;\n", 1, "R0 / noise",
     "the registered offset follows the port every cycle, so the noise between requests reaches the answer"),
]


def recipe(tb: Path) -> list[str]:
    out = subprocess.run(["make", "-s", "--no-print-directory", "print-vflags"], cwd=tb, capture_output=True,
                         text=True, check=True).stdout
    return [w for w in out.splitlines() if w]


def run(repo: Path, work: Path, probe: tuple) -> dict:
    name, path, old, new, host, expect, why = probe
    tb = repo / "tb/verilator/mbx"
    copy = work / name / "rtl"
    copy.mkdir(parents=True, exist_ok=True)
    for f in RTL_FILES:
        (copy / f).write_bytes((repo / "hdl/milan/mailbox" / f).read_bytes())
    if old:
        text = (copy / path).read_text()
        if text.count(old) != 1:
            return {"probe": name, "result": f"FIXTURE: occurs {text.count(old)} times", "expect": expect}
        (copy / path).write_text(text.replace(old, new))
    argv = recipe(tb) + [f"-GHOST_P={host}", "--Mdir", str(work / name / "obj"), "-j", "4",
                         *[str(copy / f) for f in RTL_FILES], "tb_mbx_top.sv", "sim_main.cpp", "-o", "Vmbx"]
    built = subprocess.run(argv, cwd=tb, capture_output=True, text=True, check=False)
    if built.returncode != 0:
        (work / name / "build.log").write_text(built.stdout + built.stderr)
        return {"probe": name, "result": "BUILD FAILED", "expect": expect}
    ran = subprocess.run([str(work / name / "obj" / "Vmbx"), str(host)], capture_output=True, text=True,
                         check=False, timeout=3000)
    (work / name / "run.log").write_text(ran.stdout + ran.stderr)
    fails = [ln.strip() for ln in ran.stdout.splitlines() if "[FAIL]" in ln]
    tail = [ln for ln in ran.stdout.splitlines() if ln.startswith("RESULT")]
    return {"probe": name, "host": host, "why": why, "expect": expect, "rc": ran.returncode,
            "result": tail[-1] if tail else "no RESULT line", "fails": fails[:12], "n_fail": len(fails)}


def main() -> int:
    repo, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    jobs = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 3
    with ThreadPoolExecutor(jobs) as ex:
        rows = list(ex.map(lambda p: run(repo, work, p), PROBES))
    print(json.dumps(rows, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
