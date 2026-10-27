#!/bin/sh
# Disposable behavioural probe of the sync receipt ageing rule (#89).
# Copies a tree's engine harness into <workdir>, appends one probe phase
# right after phase 39 (which leaves the plane a slave of GMS with usable
# Sync), builds it against the tree's own RTL and image, and runs the
# shipping pass. Only the PROBE lines are evidence; the harness's own tally
# after the probe is irrelevant (the probe moves state later phases expect).
# Usage: probe_reaging.sh <tree> <workdir>
set -eu
TREE=$(cd "$1" && pwd)
W=$2
mkdir -p "$W"
W=$(cd "$W" && pwd)
rm -rf "$W/tb"
cp -r "$TREE/tb" "$W/tb"
E="$W/tb/verilator/engine"
python3 -I - "$E/sim_main.cpp" <<'EOF'
import sys
p = sys.argv[1]
s = open(p).read()
call = "    age_a_grandmaster_whose_sync_fails();\n"
assert s.count(call) == 1
s = s.replace(call, call + "    probe_reaging();\n    probe_parked_sync();\n    return;\n")
anchor = "  //! #82: every commit of the whole run that names thisClock, whatever\n"
assert s.count(anchor) == 1
probe = r'''
  // PROBE. 802.1AS-2011 10.3.11 with Cor1: the port's information is aged
  // whenever currentTime >= syncReceiptTimeoutTime && gmPresent, and only a
  // received Sync moves syncReceiptTimeoutTime. Scenario per round: the
  // grandmaster's Sync dies (ageing), ONE usable pair is heard as master,
  // Sync dies again for 500 ms (> 375 ms after that pair), then the
  // grandmaster announces. Clause expectation: that Announce is aged at
  // once, so no commit names GMS. Control round: the Announce comes 125 ms
  // after the lone pair (inside its 375 ms), so re-election is expected.
  int probe_round(bool late, int round) {
    for (int k = 0; k < 4; k++) s39_interval(SyncShape::stopped, 250000, false);
    const int aged_master = (dut->pub_flags_o & FL_AMGM) ? 1 : 0;
    // the lone pair's Follow_Up lands about 2000 cycles into its interval;
    // heard as master it writes no addend, so take the cycle from here
    const uint64_t pair = cyc + 2000;
    s39_interval(SyncShape::usable, 250000, false);
    const int master_after_pair = (dut->pub_flags_o & FL_AMGM) ? 1 : 0;
    if (late)
      for (int k = 0; k < 4; k++) s39_interval(SyncShape::stopped, 250000, false);
    const size_t c0 = commit_snaps.size();
    const uint64_t ann_cyc = cyc;
    s39_announce();
    const int elected_now = ((dut->pub_flags_o & 3) == FL_PRESENT &&
                             dut->pub_gm_id_o == GMS) ? 1 : 0;
    run_svc(1000000);                     // 500 ms more, Sync still dead
    int gms = 0, self = 0, changes = 0;
    uint64_t prev = OUR_CID, gm_cyc = 0, self_cyc = 0;
    for (size_t k = c0; k < commit_snaps.size(); k++) {
      if (commit_snaps[k].gm == GMS) { gms++; if (!gm_cyc) gm_cyc = commit_snaps[k].cyc; }
      if (commit_snaps[k].gm == OUR_CID && (commit_snaps[k].flags & FL_AMGM)) {
        self++; if (!self_cyc) self_cyc = commit_snaps[k].cyc; }
      if (commit_snaps[k].gm != prev) { changes++; prev = commit_snaps[k].gm; }
    }
    printf("PROBE round %d detail: grandmaster changes=%d gm_commit_ms_after_announce=%.1f "
           "retakeover_ms_after_gm_commit=%.1f\n", round, changes,
           gm_cyc ? (double)(gm_cyc - ann_cyc) / 2000.0 : -1.0,
           (gm_cyc && self_cyc) ? (double)(self_cyc - gm_cyc) / 2000.0 : -1.0);
    printf("PROBE round %d %s: aged_master=%d master_after_pair=%d "
           "announce_ms_after_pair=%.1f elected_by_announce=%d "
           "commits_naming_gm=%d retakeovers=%d master_at_end=%d\n",
           round, late ? "late-announce" : "control-announce", aged_master,
           master_after_pair, (double)(ann_cyc - pair) / 2000.0, elected_now,
           gms, self, (dut->pub_flags_o & FL_AMGM) ? 1 : 0);
    return elected_now;
  }
  // PROBE 2. followUpReceiptTimeout is 125 ms (Milan v1.2 Table 4.2). A
  // Sync parked just before the sync receipt timeout makes this plane
  // grandmaster; BECOME stops the Follow_Up watch. That Sync's Follow_Up
  // then comes 200 ms after it, later than 125 ms, so it is not usable and
  // must not clear the aged state: the next Announce should not elect GMS.
  void probe_parked_sync() {
    recover_from_the_aged_port("probe2");
    const uint64_t p0 = cyc;
    s39_interval(SyncShape::usable, 4000, false);      // last usable pair
    const uint64_t pair = p0 + 2000;
    run_svc(680000 - (cyc - p0));                      // to ~340 ms after it
    const uint64_t local = phc() + 150;
    const uint16_t seq = s39_sync_seq++;
    Frame f = ptp(0x0, seq, 0, 0x0208, 10, SRCS);
    f.ts(0);
    const uint64_t sync_cyc = cyc;
    send_frame(f.b, local);
    run(1000);
    const bool master = wait_flags(FL_AMGM, FL_AMGM, 200000ull);
    const uint64_t master_cyc = cyc;
    run_svc(400000 - (cyc - sync_cyc));                // 200 ms after the Sync
    const uint64_t fu_cyc = cyc;
    Frame g = follow_up(seq, 0, local - static_cast<uint64_t>(pdm.d), SRCS);
    send_frame(g.b, local + (fu_cyc - sync_cyc) * 500);
    run(1000);
    run_svc(200000);                                   // 100 ms
    const size_t c0 = commit_snaps.size();
    s39_announce();
    const int elected = ((dut->pub_flags_o & 3) == FL_PRESENT &&
                         dut->pub_gm_id_o == GMS) ? 1 : 0;
    printf("PROBE parked: sync_ms_after_pair=%.1f master=%d takeover_ms_after_sync=%.1f "
           "follow_up_ms_after_sync=%.1f elected_by_next_announce=%d "
           "commits_naming_gm=%d\n",
           (double)(sync_cyc - pair) / 2000.0, master ? 1 : 0,
           (double)(master_cyc - sync_cyc) / 2000.0,
           (double)(fu_cyc - sync_cyc) / 2000.0, elected,
           a_commit_since_names(c0, GMS) ? 1 : 0);
  }
  void probe_reaging() {
    printf("PROBE start: slave=%d gm_is_GMS=%d\n",
           (dut->pub_flags_o & 3) == FL_PRESENT ? 1 : 0,
           dut->pub_gm_id_o == GMS ? 1 : 0);
    int late = 0;
    for (int r = 1; r <= 3; r++) late += probe_round(true, r);
    // recover fully, then the control
    recover_from_the_aged_port("probe");
    probe_round(false, 4);
    printf("PROBE summary: late Announces that re-elected the aged "
           "grandmaster: %d of 3\n", late);
  }

'''
s = s.replace(anchor, probe + anchor)
open(p, "w").write(s)
EOF
cd "$E"
GEN="$TREE/hdl/ucode/gen_gptp_ucode.py"
python3 -I "$GEN" --clk-hz 2000000 --cease-ms 3000 -o gptp_ucode.hex >/dev/null
verilator --cc --exe --build -j 4 --top-module KL_gptp_engine \
  -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
  -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
  -GUCODE_HEX_P='"gptp_ucode.hex"' -GCLK_HZ_P=2000000 \
  -CFLAGS "-std=c++17 -O2 -I$E -Wall -Wextra" \
  "$TREE/hdl/ucpu/gptp_ucpu_pkg.sv" "$TREE/hdl/ucpu/KL_gptp_ucpu.sv" \
  "$TREE/hdl/wire/KL_gptp_rx_parser.sv" "$TREE/hdl/wire/KL_gptp_tx_slot.sv" \
  "$TREE/hdl/common/KL_gptp_timer.sv" "$TREE/hdl/top/KL_gptp_engine.sv" \
  sim_main.cpp -o Vengine_probe >"$W/build.log" 2>&1
./obj_dir/Vengine_probe >"$W/probe.log" 2>&1 || true
grep '^PROBE' "$W/probe.log"
