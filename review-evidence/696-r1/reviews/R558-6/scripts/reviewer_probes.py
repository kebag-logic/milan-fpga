#!/usr/bin/env python3
"""Reviewer-planted KL_maap probes, outside the committed mutant table.

Usage: reviewer_probes.py <repo-root> <work-dir> [jobs]

Each probe is an exact, once-only source replacement applied to a scratch copy
(no checkout file is edited) and run through the committed driver's run_case():
a probe is CAUGHT when its build succeeds and the harness exits 1 with any
[FAIL] line (failure name "" matches every "[FAIL] " line). A probe that builds
and passes is an ESCAPE: no committed check observes that defect. Datapath
probes run the real-CSR integration harness.
"""
import concurrent.futures as cf
import multiprocessing
import contextlib
import io
import sys
from pathlib import Path

root, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
jobs = int(sys.argv[3]) if len(sys.argv) > 3 else 8
sys.path.insert(0, str(root / "tb/verilator/maap"))
import mutants as m  # noqa: E402

FIRST_DRAW = ("rand_offset(rng_seeded_r ? lfsr_next_w[15:0]\n"
              "                                                                    : enable_seed_w[15:0], count_i)")
#: (name, anchor, replacement, datapath?)  the claim each probe tests is in REPORT.md
PROBES = (
    ("p1_beat5_keep_low_byte_only", "(rbeat_r == 3'd5) ? 8'h03", "(rbeat_r == 3'd5) ? 8'h01", False),
    ("p2_link_return_keeps_pending", "if (!enable_i || restart_w || port_operational_p)",
     "if (!enable_i || restart_w)", False),
    ("p3_restart_keeps_pending", "if (!enable_i || restart_w || port_operational_p)",
     "if (!enable_i || port_operational_p)", False),
    ("p4_seed_end_unchecked", "(seed_offset_i < POOL_SIZE_C)\n                         && (seed_end_w <= {1'b0, POOL_SIZE_C})",
     "(seed_offset_i < POOL_SIZE_C)", False),
    ("p5_link_return_counts_conflict", "            if (restart_w)\n              conflicts_o",
     "            if (1'b1)\n              conflicts_o", False),
    ("p6_requested_count_follows_live_count", "{8'd0, tx_own_cnt_r}", "{8'd0, count_i}", False),
    ("p7_first_offset_ignores_seed_unit", FIRST_DRAW, "rand_offset(lfsr_next_w[15:0], count_i)", False),
    ("p7_first_offset_ignores_seed_datapath", FIRST_DRAW, "rand_offset(lfsr_next_w[15:0], count_i)", True),
    ("p8_echo_count_low_byte", "tx_cnt_r        <= rx_cnt_r;", "tx_cnt_r        <= {8'd0, rx_cnt_r[7:0]};", False),
    ("p9_seed_only_mac_high_bits", "station_mac_i[31:0] + realtime_ns_i", "station_mac_i[47:16] + realtime_ns_i", False),
)

source = m.RTL.read_text()
cases, bad = [], []
for name, anchor, repl, dp in PROBES:
    if source.count(anchor) != 1:
        bad.append(name)
    else:
        cases.append((name, source.replace(anchor, repl), dp))
work.mkdir(parents=True, exist_ok=True)


def one(case):
    """Run one probe through the committed run_case in its own process."""
    name, src, dp = case
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        caught = m.run_case(work, name, src, "", dp)
    return name, caught, buf.getvalue()


with cf.ProcessPoolExecutor(max_workers=jobs,
                            mp_context=multiprocessing.get_context("fork")) as ex:
    for name, caught, out in ex.map(one, cases):
        fails = [line for line in out.splitlines() if line.startswith("[FAIL] ")]
        print(f"PROBE {name}: {'CAUGHT' if caught else 'ESCAPED'}")
        for line in fails[:8]:
            print("   ", line)
        if not caught:
            print("\n".join("    | " + x for x in out.splitlines()[-6:]))
for name in bad:
    print(f"PROBE {name}: ANCHOR-NOT-UNIQUE")
sys.exit(0)
