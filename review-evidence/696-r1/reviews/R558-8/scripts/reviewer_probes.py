#!/usr/bin/env python3
"""R558-8 disposable fault probes for KL_maap at the reviewed head.

Usage: python3 -I reviewer_probes.py <clone> <workdir> [--jobs N]

Each probe is an exact source replacement (anchor must occur once) applied
to a copy under <workdir>; no checkout file is edited. Unit probes rebuild
the MAAP unit harness, datapath probes the MAAP integration harness (a
milan_datapath.sv probe substitutes the copy in the derived source list).
A probe is CAUGHT when its build succeeds and its run exits 1 with at least
one [FAIL] line; ESCAPED when the run exits 0; BROKEN otherwise. Every
failing check name is reported.
"""
import concurrent.futures
import os
import subprocess
import sys
from pathlib import Path

KL = "hdl/ieee1722/maap/KL_maap.sv"
DP = "hdl/milan/milan_datapath.sv"

# (name, kind, file, anchor, replacement, intent)
PROBES = (
    ("u1_own_count_unlatched", "unit", KL,
     "requested_count = (tx_msg_r == MSG_DEFEND_C) ? tx_cnt_r : {8'd0, tx_own_cnt_r};",
     "requested_count = (tx_msg_r == MSG_DEFEND_C) ? tx_cnt_r : {8'd0, count_i};",
     "own requested_count follows count_i during a frame (latching unchecked?)"),
    ("u2_done_at_beat4", "unit", KL, "(rbeat_r >= 3'd5)", "(rbeat_r >= 3'd4)",
     "a PDU ending at beat 4 (no conflict_count) is accepted"),
    ("u3_beat5_one_byte", "unit", KL, ": (rbeat_r == 3'd5) ? 8'h03 : 8'h00;",
     ": (rbeat_r == 3'd5) ? 8'h01 : 8'h00;", "conflict_count low byte not required"),
    ("u4_port_edge_from_idle_only", "unit", KL,
     "else if (restart_w || port_operational_p) begin",
     "else if (restart_w || (port_operational_p && state_r == ANNOUNCE_S)) begin",
     "link return ignored while probing"),
    ("u5_echo_count_low_byte", "unit", KL, "tx_cnt_r        <= rx_cnt_r;",
     "tx_cnt_r        <= {8'd0, rx_cnt_r[7:0]};", "DEFEND count echo loses the high byte"),
    ("u6_seed_on_every_idle_enable", "unit", KL,
     "if (enable_i && !rng_seeded_r) begin",
     "if (enable_i && state_r == IDLE_S) begin",
     "generator reseeded at every Begin!"),
    ("u7_pending_kept_on_link_return", "unit", KL,
     "if (!enable_i || restart_w || port_operational_p)",
     "if (!enable_i || restart_w)", "pending DEFEND survives link return"),
    ("u8_conflict_counted_on_link", "unit", KL, "if (restart_w)\n              conflicts_o",
     "if (1'b1)\n              conflicts_o", "link return counted as a conflict"),
    ("u9_first_probe_from_running_generator", "unit", KL,
     "lfsr_r       <= enable_seed_w;\n        rng_seeded_r <= 1'b1;",
     "lfsr_r       <= lfsr_next_w;\n        rng_seeded_r <= 1'b1;",
     "generator not loaded with the seed (only first offset uses it)"),
    ("d1_port_tied_high", "dp", DP, ".port_operational_i (eff_link_w),",
     ".port_operational_i (1'b1),", "datapath ties PortOperational! high"),
    ("d2_clock_high_word", "dp", DP, ".realtime_ns_i     (ptp_now_w[31:0]),",
     ".realtime_ns_i     (ptp_now_w[63:32]),", "datapath feeds the PHC high word"),
    ("d3_clock_zero", "dp", DP, ".realtime_ns_i     (ptp_now_w[31:0]),",
     ".realtime_ns_i     (32'd0),", "datapath feeds no clock"),
)


def run(cmd, cwd=None, env=None):
    r = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, check=False)
    return r.returncode, r.stdout + r.stderr


def probe(clone: Path, work: Path, spec, jobs: int):
    name, kind, rel, anchor, repl, intent = spec
    d = work / name
    d.mkdir(parents=True, exist_ok=True)
    src = (clone / rel).read_text()
    if src.count(anchor) != 1:
        return name, intent, "BROKEN", "anchor count %d" % src.count(anchor), []
    mutated = d / Path(rel).name
    mutated.write_text(src.replace(anchor, repl))
    tb = clone / "tb/verilator/maap"
    env = dict(os.environ)
    if kind == "unit":
        rc, out = run(["make", "-s", "-C", str(tb), "build", f"MAAP_RTL={mutated}",
                       f"MDIR={d / 'obj'}", f"VERILATOR={env['VERILATOR']}",
                       f"VERILATOR_JOBS={jobs}"], env=env)
        exe = d / "obj" / "VKL_maap_sim"
    else:
        rc, srcs = run(["make", "-s", "--no-print-directory", "-C",
                        str(clone / "tb/verilator/milan_dp"), "print-srcs"],
                       env={**env, "MAKEFLAGS": ""})
        words = srcs.split()
        rel_dp = "../../../hdl/milan/milan_datapath.sv"
        if words.count(rel_dp) != 1:
            return name, intent, "BROKEN", "datapath source not found once in list", []
        words = [str(mutated) if w == rel_dp else w for w in words]
        rc, out = run(["make", "-s", "-C", str(tb), "-f", "integration.mk", "build",
                       f"DP_MDIR={d / 'obj'}", f"DP_SRCS={' '.join(words)}",
                       f"VERILATOR={env['VERILATOR']}", f"VERILATOR_JOBS={jobs}"], env=env)
        exe = d / "obj" / "maap_integration"
    (d / "build.log").write_text(out)
    if rc:
        return name, intent, "BROKEN", "build rc %d" % rc, []
    rc, out = run([str(exe)], cwd=d / "obj")
    (d / "run.log").write_text(out)
    fails = [l.strip() for l in out.splitlines() if "[FAIL]" in l]
    verdict = "CAUGHT" if rc == 1 and fails else "ESCAPED" if rc == 0 else "BROKEN"
    return name, intent, verdict, "rc %d" % rc, fails


def main():
    clone, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    jobs = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 4
    work.mkdir(parents=True, exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as ex:
        results = list(ex.map(lambda s: probe(clone, work, s, 2), PROBES))
    for name, intent, verdict, note, fails in results:
        print(f"[{verdict}] {name} ({note}): {intent}")
        for f in fails:
            print(f"    {f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
