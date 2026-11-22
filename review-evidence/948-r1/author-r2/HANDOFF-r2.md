# HANDOFF, lane 948 round 2 (PR #959 corrections)

Status: round 2 DONE (REVIEW READY issuecomment-7075385669 at e8252323); round 2b DONE (REVIEW READY
issuecomment-7080201967, last line `REVIEW READY 64e55a59e09339114926c2600056c3ad8b33b9b4`). Head `64e55a59`, tree
clean, not pushed.

Base of this round: `4ceba3d4` (round 1 head, pushed by the manager as `948-rx-fanout`, PR #959, base `dev-soft-core`).
Lane: `pf-948-1`, head `e8252323`, tree clean. Not pushed (the manager pushes and edits the PR with `PR-BODY.md`).

## Commits this round

| Commit | What |
|---|---|
| `a9ed2a6d` | conformant stimulus: harness data_len equal to the format's frame size (sim_lockstep fsh, sim_main_nx formats, sim_ctxfmt, sim_nxn FMT_LO spf 6) |
| `ce61b2a2` | failing tests: [FO11]-[FO13], sim_depkt (DT1-DT3), sim_nxn [FAN] STOP/START, fan_stop_plant.py + `fan-stop-plants` |
| `b670b961` | RTL: monitor frame-size verdict (+ reference), depacketizer hold-only tail keep, write-side whole-payload check, S1 no-reset note; fanout_mutants +7, depkt_mutants (7) |
| `f89a3593` | docs: walkthrough diagram/rows, meter table row, FPGA_DESIGN rows, TESTING row (R1 fixed), milan_dp README, register reference, evidence dispositions, inventory |
| `6ab8b355` | [FO12] sizes: every remainder 1..7 in frames of >= 13 beats (the first sizes were 9-10-beat frames, lost before the enqueue: see "new scope") |
| `29ffa248` | milan_dp root harness (`sim_main.cpp`): the PDU sized at the declared format's frame size (the 8-channel ax1x1 shape sent 48 octets; found by the milan_dp run at f89a3593, 11 failures) |
| `77777e5b` | check_cpp_idiom: one name per declaration in sim_depkt/sim_fanout, `-Wall -Wextra` in the depkt recipe |
| `e8252323` | wording: the depacketizer tests name the defect by its issue (no review label in source text) |

## Findings answered

| ID | Severity | What | State |
|---|---|---|---|
| R878-1 F1 | MINOR Docs | DATAPLANE_WALKTHROUGH.md:157 diagram, MEDIA_CLOCK_FOLLOWING.md:444 names | fixed f89a3593 |
| R878-1 F2 | MAJOR | non-multiple-of-8 data_len loses its hold-only last beat, no tlast (pre-existing) | fixed b670b961: (a) frame-size verdict per input, (b) tail kept to the tlast beat; also frames short of their payload dropped whole and counted |
| R877-1 F1 | MINOR | no test fails when one input's 5.3.8.7 STOP discards the shared stream for the others | [FAN] STOP/START legs; both plants caught by name, on 4ceba3d4's RTL and at the head |
| R877-1 R1 | residue | TESTING.md:706 sentence break | fixed f89a3593 |
| R877-1 S1 | suggestion | why fmem_r/qa_r/qb_r/rq_msk_r/idxq_r have no reset | comment b670b961 |

## Evidence (receipts/INDEX.md, 120 files)

- Failing first on 4ceba3d4's RTL: fanout 91/489 fail (FO11-13 only); sim_depkt 2842/5150 at both leads; [FAN] STOP
  legs pass on the clean base (4061/0) and fail by name on both plants.
- Head: avtp_rxmon suite at e8252323, every leg and arm PASS (fanout 489, depkt 369 x2, fanout_mutants 19/19,
  depkt_mutants 7/7); milan_dp 14142/0 (29ffa248); milan_dp_mclk 173/0; aaf_audio_loop 10; seven more suites
  548206/0 (f89a3593); twin gate + fan-stop-plants PASS; gates at e8252323 (lint, xvlog, Yosys, docs 104/104,
  tsn_fuzz AAF with the generator 164/fresh).
- Routes at 6ab8b355 (hdl/sw/configs/pinned processors identical to the head), three directives each, all six meet
  #818: best 8x8 AltSpreadLogic_high +0.327/+0.102, 1x1 AltSpreadLogic_high +0.391/+0.102 (receipts/fit/SUMMARY.txt).

## New scope (reported in REVIEW READY; for the manager to file)

- Frames of 10 beats or fewer (<= 80 octets) are accepted and counted but never delivered: the enqueue pulse lands
  after their tlast. A 1-channel 48 kHz Base stream (24 octets, 62-octet frames) is reachable (the inputs advertise
  Milan 6.4's family) and renders nothing. Predates #948 (measured on 4ceba3d4's RTL; at 15168e14 the commit waited
  for the later accept pulse). Probe: receipts/probe/.

## Notes for the next round

- `capture_coherence`'s mutation arm starts one datapath build per CPU in its affinity: at 8 CPUs it exceeded a 12 GB
  unit (OOM-killed); pinned to 4 it peaks near 3 GB (r2/tools/suites2.sh).
- Never edit a script a running unit is executing (bash reads it by offset); copy to a new name instead.

## Scratch

`/data-2/milan/tmp/948-a810/r2/` (clones c2-*, ff/, head/, probe/, sweep/, twin/, final/, tools/), Vivado work in
`/data-2/milan/tmp/948-a810/viv/work/r2{8x8,1x1}`, chain logs `viv/q2/`. Not output.

## Round 2b (manager ruling 2026-11-22: the short-frame defect is fixed in this PR)

Ruling: frames of 10 beats or fewer (counted, never delivered) are fixed here; measure at 15168e14, 4ceba3d4 and the
head; every advertised frame size delivered with its own tlast and tag, off-format still discarded and counted; tests
failing at e8252323 per size class with every remainder and a plant re-breaking the short path; re-run suites, twin,
datapath shards, Yosys, docs; re-route (RTL changed).

Measured (probe_minframe2.cpp, each revision's own wrap and RTL; receipts/probe/minframe2-table.txt):
- 15168e14 (true base): the shortest delivered frame is 98 octets (13 beats); 2-channel 48 kHz (86) and 1-channel (62)
  never delivered.
- 4ceba3d4 and e8252323: 82 octets (11 beats); round 1 made 2-channel deliverable; 1-channel still not.
- Cause: the monitor's enqueue pulse lands exactly 3 cycles after the tap's eighth beat (parser input register,
  registered match, registered pulse); a frame whose tlast comes sooner was dropped at its tlast.

Fix (`d24a15c8`): the store's write side runs 3 cycles (ENQ_LAT_C) behind the tap; the tap's own beat count names each
pulse's frame (taw_r/tq_r/te_r); the verdict is taken at the stored eighth beat (same-cycle pulse included).

| Commit | What |
|---|---|
| `0b4517c3` | failing tests: [FO14] (8-10 beats, every remainder, 1-channel 48 kHz, tagged/untagged, back to back, off-size discarded), sim_depkt [DT4] (pulse at 3 and 1 cycles), sim_nxn [FAN] inputs 6/7 at one channel (62/66-octet frames), [FO8] cut frame = DEPKT drop |
| `d24a15c8` | RTL: three-cycle write-side lag + tap-side attribution; depkt_mutants +4 (11), fanout_mutants +2 and one re-anchored (21) |
| `64e55a59` | docs: walkthrough, FPGA_DESIGN, TESTING, milan_dp README, dispositions, inventory |

Results so far (receipts/round2b/):
- failing first at 0b4517c3 (e8252323's RTL): fanout 236/1205 fail (FO14 234, FO8 2); sim_depkt 3077/5750 at both
  leads (DT4 192/960 whole, 1-channel PDU no frame); obj_nxn8 6/4073 fail (the 1-channel rounds)
- head 64e55a59: avtp_rxmon suite PASS (fanout 1205, depkt 374 x2, fanout_mutants 21/21, depkt_mutants 11/11);
  milan_dp 14148/0 then render_mutants 6/6 alone (the sweep's 7200 s clock stopped the suite inside it, rc=124);
  milan_dp_mclk 173/0; eight more suites 548216/0; twin gate + fan-stop-plants PASS; gates (lint, xvlog, Yosys,
  docs 104/104, tsn_fuzz AAF 164/fresh); probe: every length delivered
- routes at the head (viv/tools/chain_r3.sh, logs viv/q3/, receipts/round2b/fit/): all six meet #818; best 8x8
  ExtraPostPlacementOpt +0.339/+0.060, 1x1 AltSpreadLogic_high +0.139/+0.102; depacketizer +80 FF and +29..+80
  LUT against round 2; no setup path in the receive modules
- REVIEW-READY.md and PR-BODY.md updated in place to the head; REVIEW READY posted once (issuecomment-7080201967)
