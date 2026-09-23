#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Disposable probe: a grandmaster FAILOVER (the old grandmaster's Syncs stop
for longer than syncReceiptTimeout, then a new grandmaster is adopted through
the same parent) followed by a pair 50 us off.

Phase 18c of the engine suite proves a grandmaster identity change WITHOUT a
Sync lapse keeps the servo locked (50 us slews). This probe inserts one phase
right after 18c that differs only by the lapse, and prints how many step
pulses the 50 us pair produced. It edits a COPY of sim_main.cpp only.

Usage: probe_failover.py <exported tree>
"""

import sys
from pathlib import Path

ANCHOR_CALL = "    stay_locked_across_a_grandmaster_change();\n"
ANCHOR_DEF = "  // ---- 19: the parent degrades below us -> immediate takeover"

PROBE = r'''  // ---- R258 probe: a grandmaster FAILOVER, i.e. 18c plus a Sync lapse ----
  void r258_probe_failover_after_a_sync_lapse() {
    const uint64_t SRC5 = 0x00F1F1FFFE000009ull;
    const uint64_t GM_C = 0x00C0C0FFFE00000Cull;
    const uint64_t GM_D = 0x00D0D0FFFE00000Dull;
    const uint64_t T = 52000000000ull;
    const size_t s0 = steps_seen.size();
    const size_t a0 = adj_seen.size();
    printf("PROBE r258 failover: gm before %016llx, sync-ok before %u\n",
           static_cast<unsigned long long>(dut->pub_gm_id_o),
           (dut->pub_flags_o & FL_SYNCOK) ? 1u : 0u);
    // the old grandmaster still announces (its Announce watch is 3 s) but
    // its Syncs stop: the 375 ms syncReceiptTimeout fires first
    announce(50, 100, GM_C, 1, SRC5);
    const bool fell = wait_flags(FL_SYNCOK, 0, 900000ull);
    printf("PROBE r258 failover: sync-ok fell at the receipt timeout: %d\n",
           fell ? 1 : 0);
    // a new grandmaster is adopted through the same parent: a failover
    announce(51, 100, GM_D, 1, SRC5);
    printf("PROBE r258 failover: gm after %016llx, flags %02x\n",
           static_cast<unsigned long long>(dut->pub_gm_id_o),
           dut->pub_flags_o & 0xF);
    sync_pair(0x0603, T, T - static_cast<uint64_t>(pdm.d) - 50000ull, SRC5);
    printf("PROBE r258 failover +50 us: offset published %d ns, step pulses "
           "%zu, addend pulses %zu, sync-ok after %u\n",
           static_cast<int32_t>(dut->pub_offset_o), steps_seen.size() - s0,
           adj_seen.size() - a0, (dut->pub_flags_o & FL_SYNCOK) ? 1u : 0u);
    if (steps_seen.size() > s0)
      printf("PROBE r258 failover +50 us: step value %lld ns\n",
             static_cast<long long>(static_cast<int64_t>(steps_seen.back())));
    // keep the later phases' bookkeeping honest: mirror what the plane did
    servo_mirror(50000, steps_seen.size() > s0);
  }

'''


def main():
    root = Path(sys.argv[1])
    sim = root / "tb/verilator/engine/sim_main.cpp"
    text = sim.read_text(encoding="utf-8")
    assert text.count(ANCHOR_CALL) == 1 and text.count(ANCHOR_DEF) == 1
    text = text.replace(ANCHOR_CALL, ANCHOR_CALL +
                        "    r258_probe_failover_after_a_sync_lapse();\n")
    text = text.replace(ANCHOR_DEF, PROBE + ANCHOR_DEF)
    sim.write_text(text, encoding="utf-8")
    print(f"probe inserted into {sim}")


if __name__ == "__main__":
    main()
