# HANDOFF r1: [A814] gPTP in software on the #872 optimisation line (#884, #665 F6)

Status: **DONE** (19:45 CET). Head `c1e3055c`; every gate run passed (REPORT.md "Gate table").
TAKEN posted: #884 issuecomment-7062435030. REPORT posted: #884 issuecomment-7067459898 (body: REPORT-COMMENT.md, from REPORT.md).

Lane: `/data-2/milan/lanes/opt-gptp-sw`, branch `opt-gptp-sw-1` from `15168e14` (`origin/dev-soft-core-optimisation`).
Local commits only; nothing pushed. Scratch: `/data-2/milan/tmp/gptpsw-a814` (bin/, clones/, syn/, h/, logs/, gates/).
Final-gate clone: `clones/g2` at `eea4a361`.

## Commits (one-line subjects, no body, no trailers)

| # | Commit | What |
|---|---|---|
| 1 | `cccf1899` | The IEEE 802.1AS-2020 end station port in firmware (`sw/firmware/ctrl/gptp/gptp.[ch]`), its GoogleTest suite, RV32IM object arm, 25 planted defects |
| 2 | `5d5a4222` | The timestamp unit `KL_gptp_tsu`, its bench `tb/verilator/gptp_tsu`, 16 planted defects |
| 3 | `41ba6fc7` | Mailbox contract 2.5: gptp channel, TIMESTAMP event, gPTP publication; KL_mbx/CDC/evt, firmware mbx layer, host model, mbx bench rows |
| 4 | `0dfaa3c1` | The unit in the plane's place on the split (`GPTP_SW_EN_P`, `milan_soc.py --sw-gptp`), the publication decoded onto the plane's nets |
| 5 | `3cc407ae` | The adapter `gptp_mbx.[ch]`, no 64-bit divide on the hart, the closed-loop bench `tb/verilator/gptp_sw` |
| 6 | `36f6d5a8` | The harness carries the gptp channel: rules A and B, the provisional gptp family outside THE SHARE, the fixture re-recorded |
| 7 | `4493fc95` | Documentation: `docs/design/GPTP_SOFTWARE.md`, NFR-SCOUT-02/03, docs map, audit row |
| 8 | `eea4a361` | The tree's gates: idioms, module-length splits, port docs, naming, Yosys lists, census and rows-model rulings, regenerated references |
| 9 | `c1e3055c` | The fixture trim keeps the tick after each deadline (the escaped timer-late mutant), the fixture re-trimmed from the same run, rows unchanged |

## Changes, each with its place and reason

### The firmware port and its adapter

- `sw/firmware/ctrl/gptp/gptp.h:28` `struct gptp_hal` is the four-call HAL (send, adjust rate, step, time base). It keeps the port portable and testable on simulated PHCs.
- `gptp.h:170` `struct gptp_port` holds a port's whole state, with nothing global. Milan v1.2 8.3.4 runs one gPTP an interface, so a redundant entity is two instances.
- `sw/firmware/ctrl/gptp/gptp.c:51` `udiv64`/`sdiv64` divide by shift and subtract. The split image's object audit refuses libgcc's `__udivdi3`/`__divdi3` on RV32IM (MULDIV_HELPERS).
- `gptp.c:228` `become()` restarts the sync receipt timer on entering SLAVE. A stale timer aged a fresh grandmaster at once (mutant `slave-timer-stale`).
- `gptp.c:339` `pd_complete` applies neighborRateRatio to the delay, takes the median of three, and clears asCapable on the 5th lost response (Milan v1.2 4.2.6.2.4).
- `gptp.c:468` `servo_pair` is the PI servo. Gains are derived from the PHC clock and Sync interval, double pole 0.6. The integrator is seeded on the second pair, with the 20 µs and 100 µs step thresholds, the 200 ppm clamp and the #75 slew level.
- `sw/firmware/ctrl/gptp/gptp_mbx.c:116` binds the gptp channel to the loop. `gptp_mbx.c:74` writes every `GPTP_*` word, then `GPTP_STATE` with `GEN` moved, so the snapshot crosses whole.
- `sw/firmware/ctrl/test/ctrl_aecp_image.c:16` and `ctrl_srp_image.py:169` build `--with-gptp` images (`CTRL_IMAGE_GPTP`). The fixture's PHC is RAM words, not the CSR block (a few stores a Sync, noted in REPORT).

### Fabric

- `hdl/ieee8021as/gptp_tsu/KL_gptp_tsu.sv:165` is the ingress stamp point and `:113` the egress correction (426 / 3,770 ns). `:248` gates the seal. Both stamp points are the plane's, so the plane's ±11.2/±12.6 ns digital bound holds.
- `hdl/milan/mailbox/KL_mbx_evt.sv:86` adds the TIMESTAMP source: never coalesced, one record a credit.
- `KL_mbx_cdc.sv:152` adds two crossings: the GEN-committed publication snapshot and the credit-flowed record. Both are cdc_handshake.
- `hdl/milan/KL_ctrl_split.sv:56` `GPTP_P` opens the gptp tuple.
- `hdl/milan/milan_datapath.sv:80` `GPTP_SW_EN_P`. `:9339` `g_gptp_sw` builds the unit and decodes `i_ctl_gptp_pub` onto `gptp_pub_*`, so the consumers keep their RTL.
- `sw/litex/milan_soc.py:3692` `--sw-gptp`, owner "software". `:538` adds the split wrapper's five ports.
- `sw/mailbox/mailbox.yaml` contract 2.5: channel `gptp` (id 5), event TIMESTAMP (9), the GPTP_* publication (22 words). The generated outputs are checked by `gen_mailbox.py --check --crosscheck --selftest`.
- `syn/yosys/run.sh:247` adds a standalone Yosys top `KL_gptp_tsu` (PASS, 2,824 cells). The unit is added to both `GPTP_DP_SRCS`, which the source-list gate requires.

### The service-budget harness (the recorded rule)

- `tb/verilator/ctrl_service_budget/channel_gate.py:30` implements rule A: the defined load covers the channels the image opened, from its last `FILTER_EN` (`sim_main.cpp:247` prints `OPEN`). A log with none is refused.
- `channel_gate.py:44` implements rule B: an opened channel with no load frame is refused.
- `grade.py:742` uses channel_gate in the defined load.
- `scenario.py:99` adds the `gptp` family at 10 ms, PROVISIONAL (owner decides).
- `share.py:26` `EXCLUDED`: the gptp family does not enter THE SHARE. Without this the share would halve, 2 ms to 1 ms, which changes approved bounds; the first self-test run showed exactly that failure.
- `selftest.py:94` and `selftest_opened.py` grade the fixture at its recorded clocks (`oracle.json` `clocks`). The fixture was re-recorded on the split SoC at 100/100 MHz, because rule A needs a trace with a `FILTER_EN` write.
- `selftest_opened.py:35` `planted_probe`: the planted over-budget path now lands on the first 20 ms probe whose window holds it. On the split SoC BIND_RX's window is 1 ms.
- `selftest_opened.py` `fixture_kept`: the trim keeps each deadline's tick and the next. Mutant "a timer path starts one millisecond after its deadline" escaped on the re-recorded trace because the next tick was trimmed away. It is now caught by the `tmr_no_resp1` row (`c1e3055c`).
- `selftest_share.py:497`: the save loads are graded over the opened channels only.
- `rows_tiers.py:212` excludes `gptp/` from the served-channel scan, and `rows_grade.py:114` excludes TIMESTAMP. Only a `--with-gptp` image links the port, and no row's image does.
- `build.py:327` `ImageArgs` bundles flash map and gptp, keeping `firmware()` within 6 parameters. `ts_pads.py` holds the timestamp pads' C++. `refusal.py` holds `grade.Refusal`, so that channel_gate can raise it.
- `gptp_group.py:38` `hits`: the gptp probe end (messageType, sequenceId).
- Harness README "Markers and grading" records rules A/B and the gptp family.
- The 1x1/2if point was measured with a one-line scratch POINTS entry (`clones/w3`), not committed. Adding it to `run.POINTS` cascades into `shape_costs.BUILT`, the firmware's shape table and the flip check, which is out of scope.

### Census and gates

- `sw/mailbox/census_split.py:212` adds M rows for `o_ctl_ts_valid`, `o_ctl_ts_data`, `i_ctl_ts_take`, `i_ctl_gptp_pub` and `i_ctl_gptp_pub_p`.
- `census_split.py:243` `GPTP_SW_ONLY` rules the three gPTP inputs unread under the census's plane shapes: a read there is refused. TIMESTAMP is a mailbox-made event. The GPTP_* fields are carried whole on `pub_gptp_o`. A `GPTP_SW_EN_P` shape is owed (R2).
- `scripts/measure_test_evidence_readers.py:229` adds the disposition of `tsu_mutants.py`.
- Port docs on KL_gptp_tsu's `rec_*`. The record ports' docs say STAMP, not NS: the port carries a record, not a quantity (naming gate).

## New checks: planted defect -> failing words

`sw/firmware/ctrl/test/gptp_mutants.py` (25 of 25 killed, `receipts/fw/gptp_mutants.log`):

ascap-after-one "asCapable after one good exchange with a rate"; lost-clears-at-fourth "asCapable fell at the fourth lost response"; npd-threshold-exclusive "800 ns is at the threshold, inside it"; late-bound-exclusive "a response at the bound was refused"; nrr-inverted "neighborRateRatio"; delay-without-nrr "the delay ignores the neighbor's rate"; cease-one-late "Pdelay_Req still sent during the cease"; cease-survives-link-toggle "the link toggle did not end the cease"; bmca-inverted "10.3.5: priority1 100 is better than 248"; path-loop-kept "a path holding thisClock was used"; sync-timeout-500 "no Sync for 375 ms did not age the grandmaster"; sync-any-source "another port's Sync displaced the master's pending Sync"; linkup-threshold-lost "an offset over 20 us at link-up did not step"; step-sign "the step is not the offset, negated"; p-term-sign "local ahead: the trim must slow it"; trim-unclamped "the trim left the 200 ppm envelope"; slow-loop "the 24th pair's offset is not under 150 ns"; follow-up-origin-zero "preciseOriginTimestamp is not the Sync's egress stamp"; resp-t2-zero "requestReceiptTimestamp is not the ingress stamp"; announce-before-ascapable "Announce before asCapable"; sync-250ms "Milan v1.2 Table 4.1: Sync each 125 ms"; late-stamp-unpaired "a stamp read after its frame was never paired"; slave-timer-stale "not inside 100 ns of the grandmaster by 15 s"; own-frames-used "asCapable from its own responses"; link-loss-keeps-ascap "asCapable came back with the link before any exchange".

`tb/verilator/gptp_tsu/tsu_mutants.py` (16 of 16 killed, `receipts/tsu/tsu_mutants.log`):

stamp-at-beat-1 and ingress-latency-added "I1 the stamp is the first beat's PHC less INGRESS_LAT"; general-messages-timed "I3 general messages"; ethertype-ignored "I4 another EtherType at the gPTP address is not timed"; sdo-ignored "I4 majorSdoId 0"; half-tick-dropped and egress-latency-subtracted "E2 GMII: the launch's PHC less 426 ns"; mii-octet-term-dropped "E2 MII: the launch's PHC less 3770 ns"; delta-unchecked and abort-unchecked "E3 an aborted launch and a fragmented one are losses"; guard-ignored "G1 a launch 20 cycles after a PHC step is a loss"; envelope-ignored "G3 an addend past the 200 ppm envelope is a loss"; unsealed-accepted "E1 before the echo a launch is a counted loss"; generation-unchecked "S1 a record of generation 0"; no-reseal "S1 and the unit offers its seal again"; full-overwrites "F1 the ninth record past eight held is counted".

Harness self-test, new checks (`selftest_opened.py`), each a self-planted negative:

- the fixture's image opened its five channels, gptp unopened;
- an image that opens gptp carries its admitted burst;
- an unopened channel carries no defined load;
- an opened channel with no load frame is refused ("no load frame defines");
- a log with no FILTER_EN write is refused ("no FILTER_EN write");
- the image's last gate is the one read.

The existing share check ("the per-pass share is T_svc's 20 ms ...") failed when gptp entered the share (selftest4.log): it is the control for `share.EXCLUDED`.

Owed: the closed loop has no planted defects yet, and census `GPTP_SW_ONLY` has no plant (R2).

## Gate table (clean clone `g2` at `eea4a361` unless stated)

See REPORT.md "Gate table" (kept current there). Every gate run passed. Not run: the firmware gate's `--self-test`
shards, the hosted CI and act (no PR), and the full Yosys sweep.

## Scratch drivers (not committed)

- `bin/mutshard.py`: the harness self-test's mutants in 4 shards, through the same `selftest.checks()` and
  `selftest.mutated()` as `main()`. Copy: `receipts/harness/selftest/`.
- `bin/gptp_cost.py`: the gPTP cycles from the PASS lines' `mods=`. Copy: `receipts/harness/`.
- `bin/syn.sh`: synthesis only, by the train gate's recipe. Copy: `receipts/syn/`.
- `bin/index.py`: writes receipts/INDEX.md.

## Hunks other lanes will merge with

See REPORT.md "Merge surface".
