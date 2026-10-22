[A659] REVIEW READY

Commit: 2389506ac50467987c4714555851de2539a4e8f3 (milan-fpga, branch 632-764-media-phase, PR #770; not pushed; fourteen commits on 3fdaea3d, no rebase, no amend)
Processor head: 51f88c7e14e7e2527c09ff9a23b93dd6b857fd50 (branch 632-sinfo-notify-stored), unchanged this round; its pin adoption stays the prerequisite.
Assignment: https://github.com/kebag-logic/milan-fpga/pull/770#issuecomment-6316458183, with the owner decisions https://github.com/kebag-logic/milan-fpga/issues/632#issuecomment-6309219099 and https://github.com/kebag-logic/milan-fpga/issues/632#issuecomment-6309313685. The reviews cover rounds 3 and 4 together.

**Changed (R678-1-F1, the listener at the pin):**
- `KL_render_queue` (new) replaces `KL_render_setpoint` on the TDM listener path. At each PDU's header it divides d = avtp_timestamp - E_n exactly by Ps (thirds of a ns) and writes event k of the PDU into frame n + round(d / Ps) + k, for a PDU of any length. On domain event n each interface i reads frame n + K_i. Storage: 128 rows per stream at 48 kHz (derived from 2.126 ms plus the event latency), two inferred block-RAM banks, synchronous read, block-RAM style, no device primitive.
- `KL_media_if_latency_pkg`: `out_pipe_ns`, `out_lead_frames`, `out_lead_ok`. K_i is derived per interface: 2 on the 1x1 TDM8, 1 on the 8x8 TDM32. The datapath refuses at elaboration an out-lead that would straddle a frame start.
- `KL_aaf_rx_depacketizer`: the read side publishes tv and the timestamp, and holds the payload 16 cycles (the frame is known after 11).
- `milan_datapath`: the #386 prefill, rails and at-switch recentre and #387's render re-base are retired. #645's settle recentre stays, for the LOOP queues only. `RENDER_STAT` (0x8DC) is re-defined: lead, idle, converged, refused. `KL_i2s_playback` is unchanged.
- Docs: MEDIA_CLOCK_FOLLOWING.md (the listener's presentation at the timestamp), TIME_SYNC.md (listener render latency), REGISTER_MAP.md 0x8DC, TESTING.md, CHANGELOG.

**Item 2 (with clauses):**
- Supported range: a sample is written for every interface from 31.1 us to 2.656 ms ahead of its presentation time at arrival on the 1x1 (Milan v1.2 4.4.2.1; IEEE 1722-2016 4.4.4.9).
- Rules, each with its counter: late (the frame every interface has read) `late_o`; too early (past the queue) `early_o`. Both also count in `refused_o`, which `RENDER_STAT[31:16]` reads. Untimed (tv clear, or the payload before the frame is known) `untimed_o` (4.4.4.5). Gaps and overlaps go to `slips_o`.
- Stream start: silence until the first presentation time, with no prefill.
- gPTP step: E_n and the talkers' stamps move together, queued frames keep their rows, and nothing re-centres. A PDU placed across the two time bases is refused or slips, counted.
- Media-clock hold: queued frames are delayed by the hold, and later PDUs take over within the lead with one counted slip (10.8; Milan v1.2 7.6.1).

**Item 3 (at the pins, the slot-MSB decoder):** `make -C tb/verilator/media_phase render`, two interfaces of one domain a frame apart (K = 2 and 3): 13 checks, 0 failures. Every sample is at its presentation time inside +/-5 % of Ps (largest 833.5 / 874.2 ns, the planted phase itself) and at the nearest frame at every phase. Controls, each KILLED by its named check: the interface constant dropped, the queue read untimed, a frame off by one, the late rule removed (and the early rule). On the shipping datapath `milan_dp_render` puts the first event at +0.6 ns and every slot within 15.1 ns over 22 windows.

**Item 1 (re-graded):** render_queue (36 + 35 checks, 22 of 22 planted defects caught), milan_dp aclk (182), milan_dp_gm_steps (195; 2 refused, one slip, one offset), follow_ring (48, 19, 30; 16 of 16 controls), milan_dp_render (263, 71), milan_dp_mclk (55, 32, 49; 31 of 31).

**Item 4 (area):**
- Out of context, `KL_render_queue` with every tap:
  - 1x1: 2 RAMB18, 0 LUTRAM, 553 LUT, 228 FF;
  - 8x8: 6 RAMB36, 0 LUTRAM, 890 LUT, 387 FF.
- route-1x1 at bb9a9200 (the last RTL change): LUT +464, FF +422, SLICE +76 against +500/+600/+80; RAMB36 0; RAMB18 +2 (the budget); DSP 13; WNS +0.123 ns, WHS +0.036 ns; route complete. `pp_resource_gate.py check` exits 1 on RAMB18 alone.
- The stage's first route (6631b0b2) read LUT +582. bb9a9200 cuts the stage from 596 to 494 LUT in the datapath's view, its behaviour unchanged.

**Validation (exact commands, results):**
- Full sweep, `scripts/run_all_suites.sh`, four shards at 2389506a: 63 of 64 suites. Shard 0 has 14 of 15, `milan_dp` failing only the [NOTIFY] SET_STREAM_INFO steps 3 and 4 at the current processor pin. Shards 1 to 3: 331,469 / 262,062 / 1,540,265 checks, 0 failures.
- `make -C tb/verilator/milan_dp run ORDINARY_CASES="base crflic dynmap nxn nxndv nxn8 nxn4c nolpf prune ax1x1 aclk"` at 2389506a: rc 0, eleven legs, 11,248 checks, 0 failures; `render_mutants.py` 4 of 4. `run-notify`: 441 checks, 3 failures (those steps, at the pin).
- With the processor head's E_SINFO spliced into a scratch clone's submodule: `make notify` 441 checks, 0 failures; `gsi_mutants.py 9` caught at step 3.
- At bb9a9200:
  - `make -C tb/verilator/media_phase mutants MUTANT_JOBS=1`: 20 clean controls, then 38 of 38 caught;
  - `make -C tb/verilator/render_queue` and `mutants`: 24 of 24;
  - `make -C tb/verilator/milan_dp render-csr-controls`: 3 of 3;
  - follow_ring mutants: 16 of 16;
  - milan_dp_render, the four #632 mutants: 4 of 4;
  - gm_steps, the two stage controls: 2 of 2;
  - `python3 scripts/lint_rtl.py --check`: 89 <= 89;
  - `syn/yosys/run.sh` on the three changed tops: PASS;
  - `sw/builder/test_builder.py --require-elaboration --require-rv32`: all but the one recorded not-run gate.
- At 2389506a: the docs workflow's 49 gates pass.

**Acceptance criteria:**
- Item 1 met (above).
- Item 2 met, the clauses in MEDIA_CLOCK_FOLLOWING.md and TIME_SYNC.md.
- Item 3 met, all four required controls KILLED.
- Item 4: block RAM inside the budget and no LUTRAM. LUT, FF, slice, DSP and timing are within their bars; RAMB18 +2 as budgeted. No STOP condition reached.
- R678-1-F1 is done. #632 and #764 stay "Relates to" (the bench items follow after merge).

**Open risks/questions:**
- The route-1x1 record still reads RAMB18 25. The gate prints the budgeted +2 as a regression until the record is re-written by the accepted measurement; not done here.
- Four slices of headroom are left.
- Found and fixed this round:
  - The stage's first form indexed a PDU's events on 3 bits, so a PDU of more than eight events (not Milan's; the depacketizer bounds by data_len only) wrapped onto its first frames. Fixed in bb9a9200 and graded ([long]: 40 and 300 events, two planted defects).
  - milan_dp's base-leg I2S check stamped its PDU 0xAABBCCDD, which only the #386 law presented. 2389506a stamps it against the domain event.
- A step of this listener's PHC alone, its talker's time not following, follows from the law (a counted overlap or gap, or a refusal). It is analysed, not graded by its own case.
- The CSR reads late and too-early together. The per-rule counters are the stage's taps, read by the simulations.
