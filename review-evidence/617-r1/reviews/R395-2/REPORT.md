[R395] NEGATIVE - exact head 377d1ac3658feb8d544e6ed1005b186b67127f35

Round R395-2, external independent review of PR #618 for issue #617. Exact head
`377d1ac3658feb8d544e6ed1005b186b67127f35`, tree `1707f6897f5c1824e7ec4f1e6f40c9be62d4fc7d`,
source base `ce550952e47fbd92367f0d9b099345100f7f4215`, round-2 range `5546b976..377d1ac3`
(three commits). Lenses covered in this round: Conformance, RTL, Robustness, Tests, Docs.

## Verdict in one paragraph

The round-2 guard does what it was designed to do at a settled lock. The walk's snapshot
moved into the tick cycle, a close on that cycle is taken late under the #74 coincidence law, and the
counters key on close against snapshot. The aligner's marker, its delayed tick and its keep-off
put the lock target at least 256 cycles from the crossing at every lock phase. I re-derived this
analytically and by simulation, and the committed suite reproduces at head (junction 5,240 and
datapath 311 checks, 0 failures; 14 mutants and 5 clean controls, 19/19). The latency statement
is exact, the area figures reproduce exactly, and `[F1]` answers round-1 F2. The PR still claims
that an engagement landing on the crossing "may repeat and skip one frame, then clear, within 64
columns, net zero", and that every phase of the committed CRF sweep passes `[C]`. That claim is
false at the stated -50 ppm design point. With sub-cycle placement, 3 of 1,024 on-crossing
engagements drop two media ticks. The cause is a `KL_media_nco` terminal-count race that the
aligner's per-frame trim update reaches while the close dwells on the crossing. Those runs end
with 1 repeat and 2 skips, not net zero, and one slip lands inside the lock tail (F1, MAJOR).
The shipped keep-off constant in `milan_datapath` is also unprotected: a reviewer mutant that
halves it survives every committed leg (F2, MINOR). And the stated rate envelope is inaccurate:
"about +/-75 ppm" is really about 65 ppm, and the 64-column law's stated derivation is wrong
(F3, MINOR).

## Findings

### F1 - MAJOR - Conformance, RTL, Robustness, Tests, Docs - an on-crossing CRF engagement at -50 ppm can drop two media ticks and slip frames outside the engagement window, net non-zero

- **Where.**
  - `hdl/ieee1722/crf/KL_media_nco.sv:216`: `else if (32'(cnt_r) == end_w)`, with `end_w` derived from the registered `trim_r`.
  - `hdl/ieee1722/crf/KL_media_nco.sv:187`: the stated assumption that `servo_trim_i` "moves at most once per servo tick (about 1 ms)". The aligner updates it every frame.
  - The guard binding at `hdl/milan/milan_datapath.sv:5707-5724`.
  - The claims at:
    - `docs/design/TIME_SYNC.md:543-547`
    - `docs/reference/REGISTER_MAP.md:1954-1957,1965`
    - `hdl/ieee1722/aaf/KL_chan_map_capture.sv:92-97`
    - `CHANGELOG.md`
    - the PR body ("The one engagement that still moves a frame ... net zero, within 64 columns ... No lock phase slips").
  - The committed sweep at `tb/verilator/capture_coherence/sim_main.cpp:620-621` (+/-50 ppm, every 4 cycles).
- **Authority.**
  - The #617 ruling (issue comment 5875206178), item 2: "Every phase passes `[C]` with 0 torn columns and no tail slips".
  - The round-2 assignment (5875511547): a dense sweep "through the band (true plan and +/-50 ppm)".
  - TIME_SYNC.md adopts +/-50 ppm (Milan v1.2 7.4) as the design point.
- **Evidence.** This is the committed junction harness, unmodified in its checks. Two things are added: the engagement placed at every quarter cycle within -1..+2 cycles of the crossing, and 64 sub-step TDM phases (`scripts/probe_crossing/`, `receipts/probe-fine-*.log`).
  - At -50 ppm, 3 of 1,024 placements fail 9 committed checks. All three landed "+0 cycles from the crossing" (the close on the tick cycle), at sub-step phases 34-36/64:
    - `[C] CRF slips net zero`
    - `[C] CRF slips only inside the engagement's first columns`
    - `[C] slips while the CRF lock held got=1 exp=0`

    Each ends with 1 repeat, 2 skips, the last slip at column 166, and a tail spread of 70 cycles.
  - Frame trace (`receipts/probe-trace-m50-35.log`): with the -50 ppm drift against the 64 ppm pull, the net departure is about 14 ppm. So the close dwells one to two cycles before the tick for about 160 frames, with `err` at 253-256.
  - At frame 167 the close lands 2081 cycles after its tick, the counter's saturation value: a tick is missing. The unwrapper then mis-folds (`err` +254 to -753), and the loop walks the lock target about 1,000 cycles, re-crossing the walk.
  - Cycle trace (`receipts/probe-nco-overrun-trace.txt`), at cycle 495608:
    - `cnt_r` = 1041 while `trim_r` changes 3207 to 3194. That update is the aligner's, two cycles after the close.
    - `sum` drops from 48002 to 47989, below `DEN`, so `end_w` drops from 1041 to 1040.
    - The `==` compare is missed and `cnt_r` runs on to its 11-bit wrap. The media grid loses about two ticks (a 3,089-cycle period).
  - Root cause confirmed in a scratch copy. With only that compare changed to `>=` (`scripts/probe_crossing/nco-terminal-ge.diff`, diagnosis only, not a proposed design), the same 1,024 placements give 0 failures, and every slip nets zero by column 57 (`receipts/probe-ncofix-fine-m50.log`).
  - Scope at head, same probe:

    | Plan | Placements | Result |
    |---|---|---|
    | true plan | 1,024 | 0 failures |
    | -25 ppm | 1,024 | 0 failures |
    | -40 ppm | 1,024 | 0 failures |
    | -50 ppm | 1,024 | 9 failures |
    | -60 ppm | 1,024 | 98 failures |
    | +50 ppm | 1,280 | 0 failures |
    | +60 ppm | 1,280 | 0 failures |
    | +65 ppm | 1,280 | 0 failures |

    Only the pre-crossing side is exposed, where the trim update lands on the NCO's terminal count.
  - The committed +/-50 ppm sweeps place every 4 cycles and so never sample these phases. Their pass is not the "every phase" the ruling requires.
  - At a settled lock the race is unreachable: trim updates land at least 256 cycles from the tick. The race predates this PR in `KL_media_nco`, but this PR newly asserts the engagement guarantee and the complete sweep.
- **Impact.**
  - Rarely, a CRF selection or re-engagement against a slow source, landing within a cycle of the crossing, loses two media ticks. Every consumer of `media_tick_p` sees a two-sample hole: the capture walk, the talker's columns, and the tick-paced render feed.
  - The walk then slips frames, net non-zero, hundreds of columns after engagement, during the "lock".
  - `SLIP_TDM` stays exact, but the documented "one dup and one skip, once" reading is wrong for that case.
- **Required outcome.** Either:
  - the on-crossing engagement at the +/-50 ppm design point nets zero within the stated window at every phase, and no media tick is lost (fixed in the NCO's terminal compare, in the aligner's update timing, or elsewhere; the design choice is the author's); or
  - a recorded manager decision narrows the ruling, with the docs and the PR body corrected to state the exception and its effect (a dropped tick pair and a non-net-zero excursion).

  Per AGENTS.md section 7, moving it to an Issue alone does not resolve it.
- **Verification.**
  - A committed check that places the engagement at sub-cycle phases on the pre-crossing side at -50 ppm, or a direct NCO test of a trim change on the terminal cycle, fails at this head and passes after.
  - This probe (`scripts/probe_crossing/run_fine.sh -50 -1 2`) reports 0 failures.

### F2 - MINOR - Tests - the shipped keep-off constant is unprotected: halving it in `milan_datapath` survives every committed leg

- **Where.**
  - `hdl/milan/milan_datapath.sv:5707-5708` (`MGA_KEEPOFF_CYC_C`).
  - `tb/verilator/capture_coherence/coherence_wrap.sv:146` restates `LOCK_KEEPOFF_CYC_P (256)` as a literal.
  - `tb/verilator/capture_coherence/sim_dp.cpp:408`: the datapath leg's only placed band is the true plan, -20..+4.
- **Authority.**
  - The ruling's "a mutant that removes the new guard reproduces the band".
  - AGENTS.md section 6, Tests: "each new test can fail for the defect it claims to detect".
  - The docs name `MGA_KEEPOFF_CYC_C` = 256 as what clears the 149-cycle +/-50 ppm transient.
- **Evidence.**
  - Reviewer mutant RM5 (`scripts/rm5-keepoff128.diff`) sets `MGA_KEEPOFF_CYC_C` to at most 128. The whole datapath leg passes: `--band` 185/0 and `--quick` 126/0 (`receipts/rm5-dp-band.log`, `receipts/rm5-dp-quick.log`).
  - The value is defective. The same 128 in the junction wrapper fails the committed checks on the committed +/-50 ppm bands: 88 and 90 failures, with tail slips in 17/53 and 18/53 placements (`receipts/rm5-wrap128-band-*.log`).
  - The committed removal mutants (the default keep-off, the round-1 binding) are caught only because the true-plan transient (32 cycles) exceeds 8.
- **Impact.** The shipped guard value can regress to one that reopens the +/-50 ppm band while every gate stays green.
- **Required outcome.** A committed check fails when the datapath's keep-off falls below what clears the +/-50 ppm transient. Examples: the datapath leg runs a placed +/-50 ppm band, or the wrapper's keep-off is tied to and checked against the datapath's constant.
- **Verification.** RM5, added to the mutation arm or rerun by hand, is caught by a named check.

### F3 - MINOR - Docs, Robustness, Tests - the stated rate envelope and the 64-column law's derivation are inaccurate

- **Where.**
  - PR body, "Known limitations": "covers media clock sources within about +/-75 ppm of the local grid".
  - The #617 REVIEW READY comment 5879271133: "about +/-75 ppm".
  - `hdl/ieee1722/aaf/KL_chan_map_capture.sv:96` ("within a 50 ppm source").
  - `docs/design/TIME_SYNC.md:521` (+/-50 ppm "source rate error").
  - `tb/verilator/capture_coherence/coherence_bench.hpp:56-60` (`kEngageColumns` = 64, "0.07 cycles per frame ... two cycles clear").
- **Evidence.**
  - The engagement pull's authority is 256 x 4 / 16 = 64 ppm.
  - In the RTL at head, on-crossing engagements pass at +65 ppm and fail 796 checks at +70 ppm, with tail slips in 240 of 1,280 placements (`receipts/probe-fine-p70.log`).
  - An integer model of the bound loop (`scripts/model_guard.py`, `receipts/model-guard-50MHz-k256.txt`) crosses from 65 ppm, and the unpulled transient reaches 256 near 86 ppm.
  - The rate the aligner sees is the TDM frame against the undisciplined local axis clock. TIME_SYNC.md:128,274 itself assumes local oscillators up to +/-100 ppm, so a Milan-compliant +/-50 ppm source does not bound it.
  - The 64-column law is derived from a 0.07 cycle/frame pull. Against a +/-50 ppm drift the net pull is about 0.0146 cycle/frame, and the measured last slip reaches column 57 even with F1's race removed. The law holds with 7 columns of margin, not for the stated reason.
- **Impact.** Readers are told the transient guarantee holds to about 75 ppm of source error, when it ends near 65 ppm of relative rate. The bench's law rests on a derivation that does not hold at its own +/-50 ppm scenarios.
- **Required outcome.**
  - The envelope is stated as the relative rate at the aligner, with the actual limits (about 64-65 ppm for an on-crossing engagement, about 86 ppm for the transient) and what happens beyond them. Engagement-time net-zero slips are expected there; the settled lock is still guarded.
  - The `kEngageColumns` comment states a derivation that holds at +/-50 ppm.
- **Verification.** Text check against these receipts.

### Suggestions (non-blocking)

- **S1 (Docs).** The `KL_media_grid_align.sv` banner's raced-engagement sentence (lines 80-89) is qualified "by default" and remains true of the module. The PR need not edit it; I do not treat it as a stale statement. A one-line pointer to the `milan_datapath` instance binding (256 cycles, delayed tick) would save a reader the search.
- **S2 (Tests / CI).** Locally `capture_coherence` took 945 s (`receipts/head-capture_coherence-make.rc`, 4-job builds) under `run_all_suites.sh`'s 1,800 s per-suite guard. It is placed on hosted Verilator shard 1/5, which was still in progress at the time of writing. The manager should confirm the hosted duration against the 1,800 s guard.

## Lens results with evidence

| Lens | Result | Evidence (at 377d1ac3) |
|---|---|---|
| Conformance | UNCLEAN (F1) | Checked and passing: #617 acceptance 1-3 in simulation; the ruling's items 1, 3 and 4; the round-2 assignment items 2 and 3. Committed suite at head: junction 5,240/0, datapath 311/0, mutation 19/19 (`receipts/head-capture_coherence-make.log`); `chmap_capture` 318/0 + netlist 20/0 (`receipts/head-chmap_capture.log`). Latency re-derived: change = 6 + 26p + (3-p) x 260.42 cycles = 787.25/552.8/318.4/84.0. Measured minimum pair-0..3 ages -6/-32/-58/-84 at base, 776.. at 5546b976 and 781/520/260/0 at head, so +5 = LB_PAIRS_C + 1 for the read at the tick (+2 on the 8x8 product, `loopback_lane: false`). Ruling item 2 fails at -50 ppm (F1). |
| RTL | UNCLEAN (F1) | Read `KL_chan_map_capture.sv:966-1068,1119-1200`: the snapshot instant (idle tick in its own cycle; a queued tick at its walk's start), the late load on close-at-snapshot with nothing pending, counters on close against snapshot, and `tick_late_r`. `milan_datapath.sv:5700-5727`: the marker is the same `aafcap` event as `tdm_close_w`; tick delayed one cycle; `MGA_KEEPOFF_CYC_C` = min(DIV/4, 256). `KL_media_grid_align.sv` (unchanged): the split of `ref_keep_w` falls at the tst wrap, which is the walk's crossing. Area reproduced (`receipts/ooc-chmap.txt`): 1x1 TDM8 LUT 1292 -> 1263 -> 1265, FF 1048 -> 1384; 8x8 2103 -> 2132 LUT, FF 1931; RAM32M 8, no BRAM. The NCO terminal race is F1. |
| Robustness | UNCLEAN (F1, F3) | Edge cases:<br>- Engagement on the crossing: F1.<br>- Re-engagement and CRF loss: the watchdog re-engages from a fresh, kept-off reference.<br>- INTERNAL: `sel_i` = 0, so there is no trim and no race.<br>- Reset: all new state resets.<br>- Stream start: not in the tick path.<br>- I2S one-pair frame: the close is the slot-0 strobe; `[F1]`.<br>- 8x8 TDM32: the close is pair 3, the last kept.<br>- 100 MHz: the transient is 164.5 cycles, inside 256 (`receipts/model-peak-50-100MHz.txt`).<br>- Rate envelope: F3. |
| Tests | UNCLEAN (F1, F2, F3) | The committed mutants are each caught by their named check. `[F1]` catches the RM1 class. `media_grid_align` 45/0 with its 3 negative controls red (`receipts/head-media_grid_align.log`): the #74 coincidence law is intact, so no chatter regression. The +/-50 ppm sweep granularity misses F1. RM5 survives (F2). The `kEngageColumns` derivation is wrong (F3). |
| Docs | UNCLEAN (F1, F3) | TIME_SYNC.md "Talker capture handoff" and "The guarded crossing" state the latency, the guard and the costs; REGISTER_MAP.md SLIP_TDM; CHANNEL_MAP_64.md section 4; FPGA_DESIGN.md; TESTING.md; CHANGELOG.md. All are accurate except the engagement-exception claims (F1) and the envelope (F3). |

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN | #617 body, ruling 5875206178, round-2 assignment 5875511547, committed suite logs, latency derivation, fine CRF probe | R395-2 | 377d1ac3658feb8d544e6ed1005b186b67127f35 |
| RTL | UNCLEAN | `KL_chan_map_capture.sv`, `milan_datapath.sv:5650-5727`, `KL_media_grid_align.sv`, `KL_media_nco.sv:150-230`, OOC area, NCO cycle trace | R395-2 | 377d1ac3658feb8d544e6ed1005b186b67127f35 |
| Robustness | UNCLEAN | Edge cases in the table above, the loop model at 50 and 100 MHz, rate sweeps from -60 to +70 ppm | R395-2 | 377d1ac3658feb8d544e6ed1005b186b67127f35 |
| Tests | UNCLEAN | `tb/verilator/capture_coherence/*` (Makefile, wrapper, bench, `sim_main.cpp`, `sim_dp.cpp`, `mutants.py`), `chmap_capture` `[F1]`, `media_grid_align` wrapper, reviewer mutant RM5 | R395-2 | 377d1ac3658feb8d544e6ed1005b186b67127f35 |
| Docs | UNCLEAN | TIME_SYNC.md, REGISTER_MAP.md SLIP_TDM, CHANNEL_MAP_64.md, FPGA_DESIGN.md, TESTING.md, CHANGELOG.md, PR body, REVIEW READY comment | R395-2 | 377d1ac3658feb8d544e6ed1005b186b67127f35 |

## Prior public findings on this PR, resolved or retained at 377d1ac3

These were read after the independent pass above.

| Prior finding | Status at this head | Evidence |
|---|---|---|
| R394-1 F1 (MINOR) = R395-1 F1 (MAJOR): CRF locks sitting on the frame-close/snapshot crossing, repeat/skip with `SLIP_TDM` static | **RESOLVED at the lock**, by the ruling's fix route. | The committed placed sweeps pass at head (`receipts/head-capture_coherence-make.log`). Reviewer placements, 742 in all, show 0 failures and no tail slip; the only slips are single net-zero pairs at on-crossing engagement (`receipts/probe-band-*.log`):<br>- the true plan at every quarter cycle across -40..+40;<br>- -50 ppm at every cycle across -176..+32;<br>- +50 ppm at every cycle across -32..+176.<br>The counters now key on close against snapshot and are graded per walk (junction) and against the columns (datapath). The new F1 above is a different mechanism (the NCO terminal race at engagement), not a retention of this finding. |
| R395-1 F2 (MINOR): the one-pair frame not load-bearing | **RESOLVED** | `chmap_capture` `[F1]` elaborates lane B with `TDM_FRAME_PAIRS_P = 1` and drives pair 0 alone. The committed RM1-class mutant is caught by "F1: col 0 carries its own pair-0 frame (L)" (`receipts/head-capture_coherence-make.log`; 318/0 at head). |
| R395-1 F3 (MINOR) = R394-1 S1: sampled-mean latency table | **RESOLVED** | TIME_SYNC.md tables the exact change, re-derived above; the pair-3 sentence and row agree; the CHANGELOG states 1.68 to 15.75 us. |
| R394-1 S2 (optional per-pair "staged" bits) | Suggestion, not adopted in RTL | No coverage effect. |
| R395-1 S1: Arty blend note | Taken | TIME_SYNC.md: "On the Arty blend the I2S pair is pair 0. It waits for the TDM close: at most a frame." |
| R395-1 S2: stale `tdm_hold_r` | Taken | `tb/verilator/milan_dp/sim_nxn.cpp:7874-7878` |
| R395-1 S3: slot-0 counters and marker | Moot | Both now key on the frame close. |

## Real limits

- Tool identity (`receipts/tool-identity.txt`): simulation used Verilator 5.050 (the CI pin), from `$VALIDATION_TOOLS/verilator-v5.050-src`, because the assigned pinned-tool path does not exist on this host. Build parallelism was capped at 4 jobs per stream, 8 in total.
- The OOC used sv2v v0.0.13 (CI pins v0.0.12) and Yosys 0.66. It is an estimate, not the ledgered `ooc.sh`.
- F1's sub-cycle probes ran on the junction leg. It binds the aligner as `milan_datapath` does (marker, delayed tick, keep-off 256 at 50 MHz, read and compared); the datapath leg was not probed at sub-cycle phases.
- Not run by this reviewer:
  - `milan_dp`, `milan_dp_render` (the T30 residual -0.5339 ppm), `tdm`, `pair_fill`, `pp_shadow`;
  - the builder bank, lint, the Yosys `run.sh`, the xvlog gate, the Markdown gates;
  - the #386 recentre timings (682.7 / 486.9 ms).

  These are the manager's banks or the author's measurements, and are not re-derived here.
- Physical calibration: NOT RUN. Bench acceptance 4 is out of scope. Field skips are not hardware proof.
- Hosted run 36487875476 at this head, as of 2026-09-28T22:29Z:
  - Verilator shards 0, 2, 3 and 4 of 5: success.
  - Yosys shards 0-3, `rtl-fast`, `elaborate`, `yosys-elaboration`, `verilator-lint`, `docs-check`, `full-ci-gate`: pass.
  - Physical gPTP: skipped (a skipped context, not an executed one).
  - Verilator shard 1/5, which owns `capture_coherence`: still in progress after 46 min (a bounded wait expired; the job's own limit is 120 min).

## Pending manager duties

- Hosted acceptance at 377d1ac3: shard 1/5, including `capture_coherence`'s duration against the 1,800 s per-suite guard.
- The candidate merge build on live `dev` 7390b436.
- The native banks.
- A decision on F1's resolution route (fix in this lane, or narrow the ruling with a tracking Issue and corrected docs).
- After any new head, re-review of every lens this round could not clear.

## Restoration

The review clone is back at exact head bytes (`receipts/restore-verification.txt`):

- HEAD, tree and index hash match the pre-probe state; no worktree blob or mode mismatch.
- The four gitlinks are unchanged.
- `git status --porcelain --ignored` is empty.

Two stray items written into the clone during probing were removed before that check: a 0-byte synthesis-tool history file, and a mistaken copy of probe sources and a probe build directory.

R395-2 FINISHED
