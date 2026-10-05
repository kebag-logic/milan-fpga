# HANDOFF: #656 milan_dp_gptp audio sample-order failures (executor A536)

Status: DONE, REVIEW READY at head `d0e29f6dda6f04f3ace1dbb395f57379e58cacaf` (not pushed).
Every local acceptance item is met. The hosted-nightly half of acceptance item 3 needs a push
and a hosted run, which this lane may not do.

- Lane: branch `656-dp-gptp-order` from dev `c0280fc008ef9c5c1650402a58bab3e47a92127b`.
  Head `d0e29f6dda6f04f3ace1dbb395f57379e58cacaf` (two commits, not pushed).
- Assignment: issue #656 comment 5985174558. TAKEN: issuecomment-5985191870.
  REVIEW READY: issuecomment-5986261146.
- Inputs read: #656 body; R470-1 (PR #655 comment 5982983632, item 5); hosted nightly run
  37184411090 in full (Physical gPTP job 111383314493 log and its `physical-gptp-logs`
  artifact, `milan_dp_gptp.log` and the preflight logs).
- Tool: pinned Verilator 5.050 (`Verilator 5.050 2026-07-01 rev v5.050`), put first on PATH
  for every run here (host default is 5.052).

## Answer in one paragraph

The three failures are a **bench timing defect**, not a datapath defect. The first bad
merge is `bbf704ec` (PR #634); the first bad commit inside it is `d676ecfd4`, whose A2-a
line (`mga_sel_w = int_clk_selected_r | follow_sel_r`, owner decision #629 D4) engages the
grid aligner at INTERNAL. In this leg the aligner then holds the media NCO, which drains the
loopback queue, on the modeled TDM FSYNC: plan A, 782/1591 of the axis clock, 10.64 ppm under
48 kHz. The bench's peer talker was paced on the axis clock at exactly 48 kHz. So the queue
gains 0.51 events/s and, once its two spare events are used, drops the oldest event (counted
on `lb_skip`, `SLIP_LB`) every 1.958 s: five gaps in 17 s, 2 + 2 in the peer-loss and
recovery windows and 1 after the reset. Before `d676ecfd4` the NCO free-ran on the axis
clock, exactly the talker's rate, and the 10.64 ppm slip sat at the TDM junction, which this
leg does not grade. The checker is right: those were real, honestly counted slips between
two clocks. The bench's assumption was wrong. The fix paces the peer talker on the modeled
audio clock (a peer that follows the DUT's INTERNAL media clock), so "no duplicates or gaps"
is again the correct expectation and grades the datapath. No RTL, port, register or
parameter change.

## 1. Reproduction

Hosted nightly 37184411090 at dev `241f9184` (5.050): `milan_dp_gptp` 139 checks / 3
failures, physical simulation 4639.98 s, driver 4734.86 s:

```text
AUDIO arm=peer loss, real fourth missed Pdelay deadline=4.749977 s
AUDIO result rx=37595 tx=37595 samples=225570 bad_payload=0 bad_order=2
  [FAIL] audio sample order, no duplicates or gaps got=2 exp=0
AUDIO arm=recovery transition deadline=3.000000 s
AUDIO result rx=20402 tx=20401 samples=122406 bad_payload=0 bad_order=2
  [FAIL] audio sample order, no duplicates or gaps got=2 exp=0
  [FAIL] all monitored audio sample ordering errors got=5 exp=0
```

Local, dev `c0280fc0`, pinned 5.050, `make -C tb/verilator/milan_dp_gptp`: rc 2,
`== ax1x1gptp physical: checks: 139   failures: 3 ==`, the same three FAIL lines,
simulation 3268.83 s, total 3297 s. The suite stops at the failing physical leg, so the 40
accounting checks do not run (as in the nightly). The 275-line simulation transcript
(`ax1x1gptp PHYSICAL` .. `RESULT`) is byte-identical to the nightly artifact's: sha256
`aef5c121e480eb0c646d846c0c961be32704e98554d0d1f199a1c46fb7894a82`.

## 2. Bisect table

Range `1269cdaf..241f9184` has four first-parent merges. Only `bbf704ec` (PR #634) touches
a simulation input: `git diff bbf704ec 241f9184 -- hdl tb configs sw avdecc gptp-processor
protocol-processor third_party` is empty (the other three change docs, `syn/ooc`, CI scoping
scripts and one workflow). All points carry the same gitlinks (gptp `5dce647a`, processor
`631eeb34`, verilog-axis `48ff7a7e`).

A single run takes about 55 minutes here (simulation alone 3,231-3,321 s for 16.99
simulated seconds, plus build; about 65 minutes with the accounting controls), over the
40-minute limit. **So this bisect runs on the first-parent merges only**, as the assignment
directs. The first bad commit inside the first bad merge is named by mechanism (section 3),
then confirmed, not bisected, by a run of that commit and of its parent, and by reverting
its one gating line on today's tree (section 4).

All runs: `make -C tb/verilator/milan_dp_gptp` in a detached worktree of the point, the
three submodules cloned at that point's gitlinks, pinned 5.050. "Sim" is the harness's own
`wall_clock_seconds`; "total" includes build, image generation and (when the physical leg
passes) the 40 accounting checks. Up to nine runs shared the 16-CPU host with other lanes.

| Point | Commit | What it is | Verdict | Sim | Total |
|---|---|---|---|---|---|
| dev | `c0280fc0` | lane base, reproduction | BAD: physical 139 / 3, rc 2 | 3268.83 s | 3297 s |
| m0 | `1269cdaf` | good end (parent of `bbf704ec`) | GOOD: physical 139 / 0; accounting 6 / 0, 20 / 0, 14 / 0; rc 0 | 3320.81 s | 3945 s |
| m1 | `bbf704ec` | Merge PR #634 (#629 lane M2) | BAD: physical 139 / 3, rc 2 | 3300.10 s | 3327 s |
| m2 | `54643724` | Merge PR #644 (docs only), bisect midpoint | BAD: physical 139 / 3, rc 2 | 3285.35 s | 3308 s |
| m3 | `5fabb46e` | Merge PR #646 (docs only) | not run: between two bad points, not a bisect step; simulation inputs identical to m1 | - | - |
| m4 | `241f9184` | Merge PR #638 (syn/ooc, CI scope) | BAD: physical 139 / 3 (hosted nightly 37184411090, 5.050) | 4639.98 s (hosted) | 4734.86 s (hosted) |

Binary bisect: good `1269cdaf`, bad `241f9184` -> midpoint `54643724` BAD -> `bbf704ec` BAD
-> **first bad merge `bbf704ec`**.

The simulation transcript is byte-identical (sha256 `aef5c121...`) at dev, m1, m2, the trace
run (less its `TRACE` lines) and the nightly artifact at m4. The binaries' own sha256 differ
by build path and are not compared.

## 3. First bad merge and first bad commit

- **First bad merge: `bbf704ec`** (Merge PR #634, "Follow one selected AAF or CRF media
  clock, and align the grid at INTERNAL (#629, lane M2)"), by the bisect above.
- **First bad commit inside it: `d676ecfd4afc48069f0fe06c26e3469c353ac6fd`**, by mechanism.
  It is the only commit of the 31 in `1269cdaf..2bc5adc0` that changes the grid aligner's
  select: from `.sel_i (crf_clk_selected_r)` and `assign mnco_servo_en_w =
  crf_clk_selected_r` to `wire mga_sel_w = int_clk_selected_r | follow_sel_r` driving both
  (A2-a, `hdl/milan/milan_datapath.sv:5905`, `:5924`, `:5932` at dev). This leg retains
  INTERNAL, so from this commit on the aligner is engaged in this leg; before it, it was
  not (trace, section 4).
- Confirmation pair (same pins at both: gptp `5dce647a`, processor `b2db3a97`, axis
  `48ff7a7e`):

| Point | Commit | Verdict | Sim | Total |
|---|---|---|---|---|
| parent | `0b074298` | GOOD: physical 139 / 0; accounting 6 / 0, 20 / 0, 14 / 0; rc 0 | 3219.70 s | 3852 s |
| first bad | `d676ecfd` | BAD: physical 139 / 3 (2 + 2 per window, 5 cumulative); rc 2 | 3223.97 s | 3248 s |

So the commit named by mechanism is also the commit where the verdict flips, on identical
pins. This pair is a confirmation of that commit, not a bisect of the 31.

## 4. Mechanism (with trace excerpt)

**The clocks.** The leg's audio clock is plan A, 782/1591 of the 50 MHz axis clock
(24,575,738.53 Hz), so its TDM FSYNC (audio / 512) is 47,999.489 Hz, 10.64 ppm under
48 kHz. The peer's AAF PDUs were paced on the axis clock, one per 6,250 cycles: exactly
48 kHz. The difference is 0.5107 samples/s, one sample per 1.95815 s.

**The path.** RX AAF -> depacketizer tap -> `KL_chan_map_capture` LOOP queue (8 events per
pair: one 6-event PDU plus 2 of margin; drop-oldest on a full push counted on
`lb_skip_cnt_o`, repeat on an empty tick counted on `lb_dup_cnt_o`) -> popped one event per
`media_tick_p` -> packetizer -> MAC TX, where the harness grades `index == last + 1`.

**Why it changed.** `media_tick_p` is `KL_media_nco`. Before `d676ecfd4`, at INTERNAL its
servo was off and it free-ran on the axis clock at exactly 48 kHz: fill rate = drain rate.
Since A2-a the aligner holds it on the FSYNC grid (-10.64 ppm), so the queue fills faster
than it drains and drops one event per pair every 1.958 s.

**Trace** (dev `c0280fc0` plus print-only instrumentation of `sim_ax1x1gptp.cpp` in a
scratch copy, `instrument.py` in this directory; it prints, every 50 ms and at every
ordering error, the DUT's public `lb_dup_cnt_w`/`lb_skip_cnt_w` (`SLIP_LB`), the TDM
junction pair, `mga_engaged_w`, `mga_err_w`, `mnco_servo_trim_w` and `mnco_servo_en_w`; its
check results are identical to the uninstrumented run, 139 / 3):

```text
TRACE STATE t=0.05 lb_dup=0 lb_skip=0 tdm_dup=0 tdm_skip=0 mga_eng=1 mga_err=-105 trim=519 nco_en=1
TRACE STATE t=2.00 lb_dup=0 lb_skip=0 tdm_dup=0 tdm_skip=0 mga_eng=1 mga_err=0 trim=-170 nco_en=1
TRACE STATE t=4.50 lb_dup=0 lb_skip=0 tdm_dup=0 tdm_skip=0 mga_eng=1 mga_err=0 trim=-170 nco_en=1
TRACE ORDER t=4.513547 cyc=225677362 last=216645 index=216647 step=2 lb_dup=0 lb_skip=4 tdm_dup=0 tdm_skip=0 mga_eng=1 mga_err=0 trim=-170 nco_en=1
TRACE ORDER t=6.471693 cyc=323584654 last=310635 index=310637 step=2 lb_dup=0 lb_skip=8 ...
TRACE ORDER t=8.429839 cyc=421491946 last=404625 index=404627 step=2 lb_dup=0 lb_skip=12 ...
TRACE ORDER t=10.387985 cyc=519399237 last=498615 index=498617 step=2 lb_dup=0 lb_skip=16 ...
TRACE ORDER t=15.283986 cyc=764199276 last=216603 index=216605 step=2 lb_dup=0 lb_skip=4 ...
```

Reading:

- The aligner is engaged at INTERNAL from boot. Its trim settles at -170 (1/16 ppm per LSB,
  so -10.6 ppm, the plan A offset). The TDM junction stays slip-free, which is A2-a's purpose.
- Every error is a GAP of one sample (step 2) on the edge where `lb_skip` moves by 4: one
  dropped-oldest event on each of the four loopback pairs. All eight channels skip the same
  sample, so the payload check stays clean.
- The gaps are exactly 1.958146 s apart: 4.51 and 6.47 fall in the peer-loss window (2),
  8.43 and 10.39 in the recovery window (2). The reset at about 10.75 s re-primes the queue
  and the DUT's counters (`lb_skip` restarts at 4), so the next gap is at 15.28 s. That falls
  in the closing transmit-flag phase, counted only cumulatively: 5.
- The gPTP transitions (Sync loss, peer loss, recovery, reset) play no part. The windows
  are simply where the clock beat lands.

**Before (`1269cdaf`, same instrumentation; a probe, stopped by hand at 4.0 simulated
seconds once two increments had shown, so it has no verdict):**

```text
TRACE STATE t=0.05 lb_dup=0 lb_skip=0 tdm_dup=0 tdm_skip=0 mga_eng=0 mga_err=0 trim=0 nco_en=0
TRACE STATE t=1.95 lb_dup=0 lb_skip=0 tdm_dup=1 tdm_skip=0 mga_eng=0 mga_err=0 trim=0 nco_en=0
TRACE STATE t=3.90 lb_dup=0 lb_skip=0 tdm_dup=2 tdm_skip=0 mga_eng=0 mga_err=0 trim=0 nco_en=0
```

The aligner was off at INTERNAL and the loopback queue was slip-free. The same 1.958 s beat
was at the TDM junction instead, as a repeat (the free-running grid outran the FSYNC). This
leg does not grade that junction (its TDM input is silent). A2-a moved the slip from there to
the loopback queue, which this leg does grade.

**Causal confirmation on today's tree** (scratch copies; the planted line is exactly the
`tdm8render` mutant "#629's A2-a removed": `wire mga_sel_w = follow_sel_r;`):

| RTL \ peer talker paced on | axis clock (harness at `c0280fc0`) | audio clock (harness at `c24722ac`) |
|---|---|---|
| A2-a present (dev) | FAIL 139 / 3 (dev run) | **PASS 139 / 0, 40 / 0 (the fix)** |
| A2-a removed (planted) | PASS 139 / 0, 40 / 0 (3231.06 s sim, rc 0) | FAIL 139 / 5, 8 ordering errors (3266.61 s sim, rc 2) |

The order checks pass exactly when the talker's clock equals the packet grid's clock.

**DUT or bench?** The bench (timing). The checker grades correctly: each failure is a real
sample slip, and the DUT counts every one of them on `SLIP_LB`. That slip is the documented
behaviour of a listener whose media clock is INTERNAL against a talker on another clock
(the LOOP QUEUE banner, `hdl/ieee1722/aaf/KL_chan_map_capture.sv:173-224`: "SLIP, HONEST AND
BOUNDED"). A2-a (#629 D4, an owner decision) moved it from the TDM junction to the loopback
queue. The bench's model was wrong: its peer was on the axis clock, which matched the DUT's
media clock only while the INTERNAL grid free-ran on that same clock.

Two authoritative statements agree:

- `docs/reference/REGISTER_MAP.md`, the `SLIP_LB`/`SLIP_TDM` reading table. The row
  "climbing | static" reads "our own front end is aligned but the upstream talker's clock is
  not this media clock: look at the peer's clock source". That is this trace exactly (`lb_skip`
  climbing, TDM pair static). The table's preamble also says its rates "assume the upstream
  talker runs at the physical grid's rate, the disciplined peer `obj_aclk` models".
- The same suite's `obj_aclk` ring phases (`tb/verilator/milan_dp/sim_aclk.cpp:816-852`,
  #390) already model "the upstream talker ... on the PHYSICAL grid - the AAF feed at 12500 +
  52/391 cycles per PDU, the cadence a peer disciplined to the same CRF produces". At this
  leg's 50 MHz that is 6,250 + 52/782 cycles: exactly the fix's 3,072 audio edges per PDU.

## 5. Fix or options

**Fixed (test defect).** Commit `c24722ac` (`tb/verilator/milan_dp/sim_ax1x1gptp.cpp`):
the peer talker sends one six-sample PDU per `kAafAudioEdges = 6 * 512` rising edges of the
modeled audio clock (`audio_edges`, which the harness already counts), instead of one per
`kHz * 6 / 48000` axis cycles. That models a peer following the DUT's INTERNAL media clock,
the configuration in which zero duplicates or gaps is the correct expectation. The check
code, the windows, every timer and the 139 checks are unchanged. The PTP reservation guard
and the catch-up schedule (`next_audio_edge` advances by a fixed step, never from the send
time) are as before. Commit `d0e29f6d` documents the model in
`tb/verilator/milan_dp/README.md` (a model-table row and one paragraph).

Options considered and not taken:

- Grade the slip instead (expect `bad_order` = the DUT's `SLIP_LB` skips, about 0.51/s).
  Rejected: it turns the zero-glitch check into a rate check and stops grading the datapath
  ordering under gPTP transitions.
- Select the peer's AAF stream as the DUT's clock source (follow it). Not possible in this
  leg: it models no MMCM actuation ("MMCM DRP/phase actuation" is in its omissions), so the
  audio clock cannot follow. That is `tb/verilator/milan_dp_mclk`'s job.
- Model the DUT's audio clock at exactly 48 kHz. Rejected: the leg deliberately models plan
  A (782/1591), and two checks grade that ratio.
- Revert A2-a. Rejected: an owner decision (#629 D4), and the RTL is correct.

## 6. New checks and planted controls

No check is added or removed: the leg stays at 139 physical + 40 accounting checks, as
acceptance item 3 requires. The corrected check is the existing pair "audio sample order, no
duplicates or gaps" / "all monitored audio sample ordering errors" under the corrected
talker model. Its planted controls:

| Control | What is planted | Expected | Result |
|---|---|---|---|
| C1, DUT side | Fix head `c24722ac` + `wire mga_sel_w = follow_sel_r;` (A2-a removed, scratch copy): the INTERNAL grid free-runs on the axis clock, 10.64 ppm faster than the talker | the corrected order checks fail | **FAIL, physical 139 / 5**: acquisition 1, peer loss 3, recovery 1, reset reacquisition 1, cumulative 8; rc 2; sim 3266.61 s |
| C2, bench side | The talker back on the axis clock (the pacing of `c0280fc0`), dev RTL | the corrected order checks fail | **FAIL, 139 / 3**: this is the dev reproduction (the harness at `c0280fc0` differs from the fix only in the pacing, its comment and one variable name) |

The C1 errors are inferred to be repeats (the queue starved at a tick): the fill now runs
slower than the drain. That run was not instrumented, so the step is not printed.

Reproduce C1 (from a clean worktree at the head):

```sh
sed -i 's/^  wire        mga_sel_w = int_clk_selected_r | follow_sel_r;$/  wire        mga_sel_w = follow_sel_r;/' hdl/milan/milan_datapath.sv
make -C tb/verilator/milan_dp_gptp VERILATOR_JOBS=4   # expect rc 2, physical 139 / 5
```

## 7. Gate table

All at pinned 5.050 where a simulator is involved. Logs are listed in section 8.

| Gate | Where | Result |
|---|---|---|
| `make -C tb/verilator/milan_dp_gptp` (physical + accounting) | fix commit `c24722ac` (worktree) | **rc 0: physical 139 / 0; setup abort 6 / 0; no-TX 20 / 0; no-Pdelay 14 / 0**; sim 3262.60 s, total 3893 s |
| `env -u SUITE_TIMEOUT VERILATOR_JOBS=4 scripts/run_all_suites.sh <out> --physical-gptp` + `suite_tally.py <out> --quiet --expect-suite-root tb/verilator --physical-gptp` (the hosted job's two commands) | **exact head `d0e29f6d`** (worktree) | **driver rc 0, tally rc 0: `PASS milan_dp_gptp`, checks 179, in-suite failures 0** (physical 139 / 0, every `AUDIO result` `bad_order=0`; setup abort 6 / 0; no-TX 20 / 0; no-Pdelay 14 / 0); sim 3227.80 s; driver 3968.59 s of its 5400 s deadline; all eight preflight self-tests PASS |
| `sw/builder/test_builder.py` (builder bank; runs `test_sim_clock`, which reads this harness) | head, lane clone | rc 0, "ALL GATES PASS EXCEPT 1 NOT RUN" (gate 11: needs a Vivado build tree not on this host, unrelated), 1134 s |
| `sw/builder/test_clock_contract.py` | head | rc 0 |
| `scripts/check_cpp_idiom.py` + `--selftest` | head | rc 0, rc 0 |
| `scripts/measure_naming.py --check` + `--selftest` | head / working tree | rc 0, rc 0 |
| `scripts/measure_test_evidence.py --check` + `--selftest` | head | rc 0, rc 0 |
| `scripts/check_hygiene.py --check` + `--selftest` | working tree / head | rc 0, rc 0 |
| `scripts/docs_check.py` | head | rc 0 |
| `scripts/check_doc_style.py` + `--selftest` | head | rc 0, rc 0 |
| `scripts/check_em_dash.py --base c0280fc0` + `--selftest` (pinned markdown lock) | head | rc 0: 0 findings over 10 added lines, arms 339/339; selftest rc 0 |
| `scripts/gen_toc.py --check`, `--verify-anchors` (pinned markdown lock) | head / working tree | rc 0, rc 0 |
| `scripts/check_doc_paths.py`, `check_todo_ownership.py`, `check_feature_status.py` | working tree / head | rc 0 each |
| `scripts/ci_scope.py <changed files>` | head | `true` (RTL/tooling relevant: `rtl-fast` applies on push) |
| Compiler warnings in the harness build | fix run vs dev run | 65 vs 65 lines mentioning "warning", none in `sim_ax1x1gptp.cpp` |

Not run, and why:

- `milan_dp` default sweep: it never builds `sim_ax1x1gptp.cpp` (only the `ax1x1gptp`
  recipe does, `tb/verilator/milan_dp/Makefile:496`), and the README edit is prose.
- `lint_rtl`, `xvlog_gate`, Yosys, synthesis and area: no RTL, port, register or parameter
  change.
- `act_ci.py` and hosted CI: nothing is pushed.
- Hosted nightly at the fix: needs a push and a manual dispatch of the Physical gPTP job, or
  the first nightly after merge (acceptance item 3, second half).

## 8. Notes, limits, links to #645 / #647

- **#645 (loopback ring slips once 15 to 45 s after an AAF source locks, bench).** Same
  component and counter (the LOOP queue, `SLIP_LB`), different case. #645 is a followed and
  locked source, where rates match and a slip is undeclared. Here the source is INTERNAL
  against an unfollowed talker, where a steady 0.51/s slip is the declared behaviour. This
  issue's mechanism does not explain #645. It does show the queue's margin: 2 events over one
  PDU and no recentre, so a 2-sample phase displacement at lock would produce exactly #645's
  one-slip signature. That is a hypothesis for A531's lane, not tested here.
- **#647 (render latency shift after an INTERNAL aligner pull-in).** A different path (the
  render setpoint), the same root decision (A2-a). No overlap with this fix. This lane
  changes no RTL, so nothing here touches A531's files (`sim_ax1x1gptp.cpp` and the
  `milan_dp` README are this leg's own).
- **Bench and release gate (#396).** At INTERNAL the DUT now slips against any talker not on
  its plan clock, about 0.51/s per 10 ppm of difference, counted on `SLIP_LB`, on the
  loopback path. A zero-glitch run through the loopback lane must therefore either have the
  DUT follow the talker or have the talker follow the DUT. This is the documented A2-a
  consequence. Before A2-a the same slip was at the TDM junction.
- **Residual fragility (not new, now visible).** `verify_abort.py` pins the no-TX control's
  20 ms window at exactly 160 RX PDUs. At the new pacing a PDU is 6,250.0665 axis cycles (6,250 + 52/782), so a
  20 ms window holds 160 PDUs unless its phase falls in the last 10.6 of those cycles (about 0.17 %
  of phases). The model is deterministic and every 20 ms window here counted 160 (normal
  run, no-TX, stop-TX, no-Pdelay).
- **Stale counts, not touched (out of scope).** `tb/verilator/milan_dp/README.md:297` (at this head) and
  `tb/verilator/milan_dp_gptp/README.md:7,9` still say 137 physical checks / 177 total. The
  leg counts 139 physical checks, 179 with accounting, at dev and at this head. That predates this lane, so it is left for the
  manager's residue list.
- **Simulation only.** No hardware, bench or flashing.
- **Logs (this directory, `logs/`, sha256 in `logs/SHA256SUMS`, every file under 200 KB).**
  `<point>.log` for each run in sections 2-7: `dev-c0280fc0`, `m0-1269cdaf`, `m1-bbf704ec`,
  `m2-54643724`, `c-0b074298`, `c-d676ecfd`, `trace-dev`, `trace-m0`, `fix1-c24722ac`,
  `ctl-fix-noA2a`, `ctl-dev-noA2a`, `head-driver` (plus `head-driver-milan_dp_gptp.log`, the
  driver's own suite log). `controls/` holds the accounting controls' DUT transcripts at
  the fix and at the head. `gates/` holds every gate in section 7 (`wt-*` = working tree
  before the README commit, `head-*` = head). `nightly-37184411090-milan_dp_gptp.log` is the
  hosted artifact. Build lines in the logs carry the local simulator's include path.
- **Scratch.** Worktrees were under `$VALIDATION_STORAGE/656-a536/pts/`, one per point. Each was
  removed (build included) once its verdict was recorded, and the lane clone's worktree list is
  back to the lane alone. Helper scripts copied here: `mkpoint.sh` (detached worktree +
  submodule clones at the gitlinks), `runpoint.sh` (one timed run with the pinned simulator),
  `instrument.py` (the print-only trace patch).
