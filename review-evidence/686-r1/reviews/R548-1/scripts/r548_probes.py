#!/usr/bin/env python3
"""Reviewer fault probes for KL_maap (#686, round R548-1).

Each probe is an exact source replacement (anchor must occur once) applied to a
scratch copy of hdl/ieee1722/maap/KL_maap.sv; the checkout is never edited. The
harness tb/verilator/maap/sim_main.cpp is built against the copy through the
suite Makefile's MAAP_RTL/MDIR overrides. A probe is KILLED when the build
succeeds and the harness exits 1; SURVIVED when it exits 0 with 0 failures.

usage: r548_probes.py <repo> <workdir>   (env VERILATOR, VERILATOR_JOBS)
"""
import os
import subprocess
import sys
from pathlib import Path

PROBES = (
    # the defend path must not rewrite a frame already on the wire
    ("defend_while_busy", "&& (state_r == ANNOUNCE_S) && !tx_busy_r;",
     "&& (state_r == ANNOUNCE_S);"),
    # compare_MAC direction inverted (B.3.6.4: TRUE when the station is lower)
    ("compare_mac_inverted",
     "octet_rev(station_mac_i) < octet_rev(rx_src_r);",
     "octet_rev(station_mac_i) > octet_rev(rx_src_r);"),
    # Restart! does not re-run init_maap_probe_count
    ("restart_keeps_probe_count",
     "            offset_r     <= rand_offset(lfsr_r, count_i);\n"
     "            probe_left_r <= 3'(PROBE_SENDS_C);\n",
     "            offset_r     <= rand_offset(lfsr_r, count_i);\n"),
    # Restart! keeps the old range (generate_address not called)
    ("restart_same_offset",
     "            offset_r     <= rand_offset(lfsr_r, count_i);\n",
     "            offset_r     <= offset_r;\n"),
    # a PDU outside the 91:E0:F0:00 pool judged as a conflict
    ("conflict_ignores_pool", "conflict_w = rx_pool_r && ", "conflict_w = 1'b1 && "),
    # this station's own empty range (count_i 0) treated as conflicting
    ("own_empty_range_conflicts", "&& (count_i != 8'd0)", ""),
    # DEFEND judged on its requested_* fields
    ("defend_judged_on_requested", "rx_defend_w = (rx_msg_r == {2'b00, MSG_DEFEND_C});",
     "rx_defend_w = 1'b0;"),
    # rProbe! in DEFEND state re-addresses instead of defending
    ("probe_in_announce_restarts",
     "(((rx_msg_r == {2'b00, MSG_PROBE_C}) && (state_r == PROBE_S)) ||",
     "(((rx_msg_r == {2'b00, MSG_PROBE_C})) ||"),
    # rDefend! ignored while probing
    ("defend_ignored_while_probing",
     "                    (rx_msg_r == {2'b00, MSG_DEFEND_C}) ||\n",
     "                    ((rx_msg_r == {2'b00, MSG_DEFEND_C}) && (state_r == ANNOUNCE_S)) ||\n"),
    # five PROBEs (count compare off by one)
    ("five_probes", "if (probe_left_r <= 3'd1) begin", "if (probe_left_r == 3'd0) begin"),
    # truncated PDUs accepted (beat gate dropped)
    ("truncated_pdu_accepted", "(rbeat_r >= 3'd5) && enable_i", "enable_i"),
    # DEFEND's conflict_start reports our offset regardless of the overlap
    ("conf_start_our_offset",
     "conf_start_w = (rx_start_r > offset_r) ? rx_start_r : offset_r;",
     "conf_start_w = offset_r;"),
    # announce timer loads the probe draw (announce cadence wrong)
    ("announce_reload_probe_draw",
     "              timer_ms_r <= announce_iv_w;\n",
     "              timer_ms_r <= probe_iv_w;\n"),
    # source MAC latched from the wrong lanes (DEFEND DA)
    ("src_mac_lanes_swapped",
     "rx_src_r[47:32] <= {lane(rx_tdata_i, 3'd6), lane(rx_tdata_i, 3'd7)};",
     "rx_src_r[47:32] <= {lane(rx_tdata_i, 3'd7), lane(rx_tdata_i, 3'd6)};"),
)


def main() -> int:
    repo, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    work.mkdir(parents=True, exist_ok=True)
    tb = repo / "tb/verilator/maap"
    source = (repo / "hdl/ieee1722/maap/KL_maap.sv").read_text()
    survived = 0
    for name, anchor, repl in PROBES:
        if source.count(anchor) != 1:
            print(f"[ANCHOR] {name}: anchor count {source.count(anchor)}", flush=True)
            survived += 1
            continue
        rtl = work / f"{name}.sv"
        rtl.write_text(source.replace(anchor, repl))
        mdir = work / f"obj_{name}"
        b = subprocess.run(["make", "-s", "-C", str(tb), "build", f"MAAP_RTL={rtl}",
                            f"MDIR={mdir}", f"VERILATOR={os.environ['VERILATOR']}",
                            f"VERILATOR_JOBS={os.environ.get('VERILATOR_JOBS', '4')}"],
                           capture_output=True, text=True, check=False)
        if b.returncode:
            print(f"[BUILDFAIL] {name}\n{b.stdout[-1500:]}{b.stderr[-1500:]}", flush=True)
            continue
        r = subprocess.run([str(mdir / "VKL_maap_sim")], capture_output=True, text=True,
                           check=False)
        out = r.stdout + r.stderr
        fails = [l.strip() for l in out.splitlines() if "[FAIL]" in l]
        tally = [l for l in out.splitlines() if l.startswith("KL_maap:")]
        if r.returncode == 0 and " 0 failures" in out:
            survived += 1
            print(f"[SURVIVED] {name}: {tally}", flush=True)
        else:
            print(f"[KILLED] {name}: rc={r.returncode} {tally}", flush=True)
            for l in fails[:6]:
                print(f"    {l}", flush=True)
    print(f"== r548 probes: {len(PROBES)} probes, {survived} survived ==")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
