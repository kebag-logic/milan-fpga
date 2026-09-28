[R394] NEGATIVE - exact head 377d1ac3658feb8d544e6ed1005b186b67127f35

# R394-2 internal cleared-context review: issue #617 / PR #618, round 2

- **Head:** `377d1ac3658feb8d544e6ed1005b186b67127f35`, tree `1707f6897f5c1824e7ec4f1e6f40c9be62d4fc7d`. Six commits on dev `ce550952e47fbd92367f0d9b099345100f7f4215`; round 2 is `5546b976..377d1ac3` (three commits).
- **Reconstructed from:**
  - AGENTS.md, CONTRIBUTING.md and docs/README.md;
  - the #617 body; assignment 5872575286, ruling 5875206178 and round-2 assignment 5875511547; the TAKEN and REVIEW READY comments;
  - the PR body;
  - `git diff ce550952..377d1ac3` and `5546b976..377d1ac3`;
  - my own round-1 packet (read-only input);
  - executable evidence I re-ran myself.
- **Other reviewers' reports:** none was read before the verdict and ledger below were written. Prior public findings are resolved in their own section, which was written after that.
- **Lenses:** all five applied.
- **Verdict:** two MINOR findings are open, both under `Docs`, so the verdict is NEGATIVE. `Conformance`, `RTL`, `Robustness` and `Tests` are covered clean at this head.

## Summary

The round-2 guard is correct, and it does what the ruling asked. I re-derived it by hand and checked it with my own phase probes and mutants. No lock phase inside the Milan v1.2 7.4 ±50 ppm source bound places the frame close on the walk snapshot after engagement.

- **Committed suites reproduce exactly at the head** (scratch copy of the head tree, Verilator 5.050):

  | Run | Result |
  |---|---|
  | `capture_coherence` junction leg | 5,240 checks, 0 failures |
  | Datapath leg | 311 / 0 |
  | Committed mutation arm, via its own functions | 19 / 19 |
  | `chmap_capture` | 318 / 0, netlist 20 / 0 |
  | `media_grid_align` | 45 / 0; its three negative controls are red as required |

- **Placed engagements.** 260 junction and 21 datapath engagements were placed. Exactly one, placed on the crossing (`CRF-band-true+0`), shows slips: one repeat and one skip.
- **Between the committed sweep's steps.** My quarter-cycle placements (44 engagements: +50 ppm from -1 to +4 cycles of the crossing, -50 ppm from -4 to +1.5) show no slip. The only exception is an engagement landing exactly on the crossing: one repeat and one skip, inside 64 columns.
- **Area.** Reproduced exactly: 1x1 LUT 1263 -> 1265, 8x8 2103 -> 2132, FF unchanged, BRAM 0.
- **Latency.** The per-pair table is exact for the shape it describes.

What is open is two statements the change made untrue:

- **F1.** The aligner module's banner still says a raced engagement starts inside the root's 1/64-sample settle band. At the root's new 256-cycle keep-off it does not.
- **F2.** The PR body's "about ±75 ppm" guarantee is falsified by measurement. At +70 and ±75 ppm, engagements a few cycles from the crossing slip after the first 64 columns, and at 75 ppm also in the lock tail. At +65 ppm the same placements pass.

## Findings

### F1 - MINOR - lens: Docs

**Location:** `hdl/ieee1722/crf/KL_media_grid_align.sv:79-83` (the LOCK TARGET banner paragraph).

**Title:** the module banner's raced-engagement claim about the root is false since this PR.

**Authority / evidence:**

- AGENTS.md section 5 requires authoritative documentation to be updated when behavior changes. The section 6 `Docs` lens asks that changed contracts be reflected.
- The banner reads: "a raced one is pulled at most the keep-off, 1/128 sample by default - half the root's 1/64-sample settle band, so a raced engagement starts inside it."
- "The root's settle band" is `milan_datapath` `SRC_SETTLE_ERR_C` = `DIV_C/64`: 16 cycles at 50 MHz, 32 at 100 MHz (`milan_datapath.sv:6060`, the #386 block).
- This PR overrides the root's instance to `MGA_KEEPOFF_CYC_C` = 256 cycles (`milan_datapath.sv:5706-5717`). The root is the only product instance of this module.
- A raced engagement in the product therefore starts 256 cycles off: 16 times the band at 50 MHz. That is not "inside it".
- The PR's own probe measures the consequence: the #386 recentre falls to its 32,768-tick ceiling, 682.7 ms, against 486.9 ms for an unpulled engagement.
- The REVIEW READY comment acknowledges that the sentence "no longer holds for this instance" and leaves the module file unedited. The datapath banner and TIME_SYNC.md describe the instance, but the module that owns the lock target still states the opposite, about the root by name.

**Impact:** a cold reader of the lock-target authority, for example someone assessing #386 recentre timing or reusing the aligner, concludes that the product's raced engagements start inside the settle band and do not delay the recentre. That is the reverse of the measured behavior.

**Required outcome:**

- The banner no longer asserts that a raced engagement starts inside the root's settle band.
- It either scopes the claim to the module default, or states that `milan_datapath` overrides the keep-off to `MGA_KEEPOFF_CYC_C` and what that costs (pointer to TIME_SYNC.md "The guarded crossing").
- This is a comment-only change. No RTL change is asked.

**Verification:** re-read `KL_media_grid_align.sv:72-89` at the new head against `milan_datapath.sv` `MGA_KEEPOFF_CYC_C` and TIME_SYNC.md:551-556.

### F2 - MINOR - lens: Docs

**Location:** the PR #618 body, "Open risks", line "The keep-off guarantee covers media clock sources within about +/-75 ppm of the local grid". The same claim appears in the REVIEW READY comment 5879271133 ("about +/-75 ppm").

**Title:** the published robustness envelope is falsified by measurement; the true bound is about 65 ppm.

**Authority / evidence:**

- AGENTS.md section 6 `Docs` says "The PR and Issue contain enough evidence for another cold reviewer". A stated guarantee that the executable harness refutes is incorrect evidence.
- **Measured at this head.** I ran the committed junction harness unchanged except for its scenario list (`scripts/r394_probe.py`). Engagements were placed on the side where the source's rate pushes the close toward the crossing, 9,000 columns each:

  | Source | Placements | Result | Receipt |
  |---|---|---|---|
  | +75 ppm | +8, +16 | fail `[C] CRF slips only inside the engagement's first columns`; +16 also fails `[C] CRF slips net zero` and `[V] the CRF lock held its phase` | `receipts/sum-75.txt` |
  | -75 ppm | -8, -16, 0 | fail the same law; at 0 also `[C] slips while the CRF lock held got=1` | `receipts/sum-75.txt` |
  | +70 ppm | +2, +4 | fail `[C] CRF slips only inside the engagement's first columns` | `receipts/sum-threshold.txt` |
  | +55, +60, +65 ppm | 0 to +40 in 2-cycle steps | all pass | `receipts/sum-threshold.txt` |

- **Why.** The PR's stated reason for 256 is that it clears the 149-cycle transient of an *unpulled* engagement (`milan_datapath.sv:5670-5677`, TIME_SYNC.md:516-521). That transient is not the binding constraint.
  - A *pulled* engagement starts up to 256 cycles from its target.
  - Its proportional term holds the phase `4 x |rate|` cycles from the target, per the datapath comment ("4 cycles of phase per ppm").
  - At 50 ppm that is 200 cycles, so a pulled close sits about 56 cycles from the crossing until the integrator walks it home. Measured: -50 ppm pulled engagements approach to 53-61 cycles (`receipts/sum-head-junction.txt`).
  - Above 64 ppm the equilibrium exceeds the keep-off, and a close engaging near the crossing is carried across it.
- Within Milan v1.2 7.4's ±50 ppm, the in-tree claims hold, and I confirmed them (Robustness below). This finding is the published envelope, not the design.

**Impact:** a maintainer or a later lane sizing the guard, or accepting a source outside the ±50 ppm tolerance, relies on a 75 ppm margin that does not exist. Engagements near the crossing then repeat and skip frames long after the first 64 columns, and at 75 ppm in the settled lock.

**Required outcome:**

- The PR body, which is the durable review object, states the envelope that the harness supports: about ±65 ppm, or "the Milan ±50 ppm bound, with margin measured to 65 ppm".
- It names the binding constraint: the pulled engagement's `4 x |rate|` proportional equilibrium must stay under the keep-off.
- Adding that constraint to TIME_SYNC.md's guarded-crossing table is recommended but not required (S3).

**Verification:** re-read the PR body. Optionally re-run `scripts/r394_probe.py <suite> p70 +70 9000 off:0:40:8`: two failures reproduce at this RTL.

## Suggestions (optional; they do not affect coverage)

- **S1 - Tests.** The queued-tick snapshot path added in round 2 has no check that can fail:
  - Code: `tick_late_r`, `KL_chan_map_capture.sv:810,971,1195-1198`; documented in TIME_SYNC.md:463 ("a tick queued behind an overrunning walk snapshots when that walk starts").
  - My mutants RM7 (path removed) and RM8 (`tdm_snap_w = tick_i`, so the walk bank reloads under a running walk) both survive `capture_coherence --quick` (494 / 0) and `chmap_capture` (318 / 0) (`receipts/RM7_*`, `RM8_*`).
  - The path is unreachable inside the documented walk budget, so this is optional.
  - Suggested check: a `chmap_capture` arm that drives a tick mid-walk with a close between it and the walk end, and grades that walk's frame and the counters.
- **S2 - Tests.** The committed arm's guard legs run only the true-plan band. A keep-off between what the true plan needs and what ±50 ppm needs survives the arm:
  - My RM5, keep-off 128: `--band` gives 1,302 / 0.
  - The full suite kills RM5: 181 failures, all in the ±50 ppm placed sweeps and the CRF+50-0 lock (`receipts/rm5-*.log`). So the ±50 sweeps are load-bearing, but only the full run shows it.
  - A ±50 band leg in `mutants.py` would make the arm enforce that.
- **S3 - Docs.**
  - State the pulled-engagement margin (`256 - 4 x |rate|` cycles; 56 at 50 ppm) beside the 149-cycle transient in TIME_SYNC.md:516-521 and `milan_datapath.sv:5670-5677`.
  - Scope the per-pair latency table (TIME_SYNC.md:477-488) to the 1x1 TDM8 shape at 50 MHz with the TDM pairs in slots 0-3. At 100 MHz the pair period is 520.8 cycles. A TDM pair mapped to talker t's slots had its `ce550952` read 104·t cycles later, so its change differs by that amount.

## Judgments the round asked for

1. **The guard.**
   - **Snapshot and counters.** `tdm_snap_w` (`:971`) fires in the tick's own cycle when the walk is idle and nothing is queued. When a close lands on that cycle with nothing pending (`tdm_snap_take_w`, `:1055`), the walk bank loads one cycle late (`:1057-1068`), which is before the slot walk's first read, `LB_PAIRS_C+1` cycles on. That matches the counters' 2'b11 law exactly (`:1010-1039`):
     - with a frame pending, the snapshot takes the bank as it stood, and the close pends;
     - with none pending, the walk takes the closing frame, and pend stays 0.
   - **Where the aligner splits.** The aligner sees `media_tick_p` one cycle late (`milan_datapath.sv:5709-5724`), so its `tst_next_w` restarts on the cycle after the snapshot:
     - a close at T (this walk's) captures `P-1` and is clamped to `KEEP_HI`, which moves it earlier;
     - a close at T+1 (the next walk's) captures 0 and is clamped to `KEEP_LO`, which moves it later.
     So the split sits exactly on the walk's crossing, and no engagement is pulled across it. My RM6 moves the split one cycle late, and the committed band leg kills it (`[C] CRF slips net zero` at +2/+3).
   - **Keep-off.** `MGA_KEEPOFF_CYC_C` = min(`DIV_C/4`, 256) is 256 at 50 and 100 MHz, and the module's `2K < DIV_C` guard holds at every clock. The lock target lies in [256, `DIV_C`-256] measured from the crossing.
   - **Proof inside ±50 ppm.** Distance from the crossing never falls below the smaller of two bounds:
     - the engagement's own starting distance less one cycle, for pulled engagements, whose net rate at engagement is at least 64 - 50 = 14 ppm away from the crossing;
     - 256 - max(149, 4·50) = 56 cycles, for every other engagement (unpulled transient, or the pulled proportional equilibrium).

     Measured across 260 + 21 + 44 placed engagements, the only slips are single repeat/skip pairs at an engagement exactly on the crossing.
   - **Edge cases**, checked by RTL reading and runs:
     - *Engagement exactly on the crossing:* one repeat and one skip, net zero, inside 64 columns.
     - *Re-engagement, feed timeout, CRF re-selection, INTERNAL→CRF:* each is a fresh engagement under the same analysis. A re-engagement from a settled lock keeps its phase bit for bit.
     - *Reset:* every new register resets: `tick_late_r`, `tdm_snap_late_r`, `media_tick_q_r`.
     - *Stream start:* the counters gate on the first close.
     - *CRF loss/holdover:* the aligner keys on the selection, not on CRF lock, so it keeps following the frame.
     - *INTERNAL:* the aligner is disengaged, and the free-running passage is counted once per beat (INT-true: one repeat, counters exact walk by walk).
     - *I2S one-pair shape:* the close is the slot-0 strobe for both the crossbar and the aligner (same `aafcap` signals, `:1217-1273`, `:5722`).
     - *8x8:* the late load fits the 2-cycle pre-walk.
     - *Blend:* the crossbar and the aligner both close on `aafcap` slot 3.
2. **SLIP_TDM.** It now keys on the close against `tdm_snap_w`, the walk's own instant.
   - `[C] walks whose repeat or skip the junction counters did not count` is 0 in every scenario of both legs.
   - The committed "round-1 counter law" mutant is killed.
   - The #74 coincidence law is preserved: `media_grid_align` [G9] passes, and its MGA_MUT_COIN negative control is red.
   - No false alarm at a slip-free lock: every CRF tail counts nothing.
3. **Sweeps and mutants.**
   - The sweeps are as stated: 65 / 65 / 53 / 53 / 13 engagements, with window coverage graded by `[V]`.
   - The CRF law (net zero, only inside the first 64 columns, no tail slip) held at every placement within ±50 ppm, including my quarter-cycle placements.
   - The `kEngageColumns` comment's 0.07 cycles/frame is the true plan's rate. At ±50 ppm the rate-toward side departs at about 0.015 cycles/frame, and the coincidence law's one-cycle hysteresis is what keeps it clean. Measured, not assumed.
   - The committed arm has 14 mutants on 5 legs, each killed by its named check; the guard removals in the wrapper and in `milan_datapath` and the RM1 class (`chmap` [F1]) are among them.
   - My guard mutants:

     | Mutant | Result |
     |---|---|
     | RM5, keep-off 128 | killed by the full suite |
     | RM6, split one cycle late | killed by the band leg |
     | RM7 / RM8, queued-tick path | survive (S1) |
     | RB1, whole round-1 binding against the head crossbar | 17 of 65 band phases slip |

4. **Latency.**
   - **Base read point.** At `ce550952` pair p is read at tick + (`LB_PAIRS_C`+2) + 26p.
   - **Frame atomicity.** Pair p's frame closes (3-p)·260.42 cycles after pair p. The round-1 snapshot read closes by tick + 5, so atomicity costs 781.25 + 6 - 5 = 782.25, then 547.83, 313.42 and 79.0 cycles.
   - **Guard.** The round-2 read at the tick cycle adds `LB_PAIRS_C`+1 = 5 cycles, giving 787.25 / 552.83 / 318.42 / 84.0 cycles, or 15.745 / 11.057 / 6.368 / 1.680 µs at 20 ns per cycle. This matches TIME_SYNC.md:479-482.
   - **Cross-check.** The minimum-age columns (-6/-32/-58/-84 at base, 781/520/260/0 at the head) match my head junction log.
   - **Cost.** That is all round 2 costs in latency. Scope: S3.
5. **Declared costs.**
   - **Keep-off pull.** Captures within 256 cycles of the tick get pulled: 512 of 1041 phases at 50 MHz, about 49%, at up to 64 ppm (u = 4·256 LSB of 1/16 ppm).
   - **#386 recentre.** It falls back to its 32,768-tick ceiling, 682.7 ms. That is bounded and stated in TIME_SYNC.md:553-555 and the PR body. It is acceptable, but the module banner contradicts it (F1).
   - **CI time.** `capture_coherence` wall time here was 168 s for the junction leg, 106 s for the datapath leg, and 133 s for the arm on 7 threads (15 min of CPU). The suite is inside the 1,800 s per-suite guard in `run_all_suites.sh` and the 120-min Verilator job. It sits on hosted shard 1/5, which was still pending at my snapshot.
   - **sv2v.** Local v0.0.13 (my area figures) against the CI pin v0.0.12. Hosted Yosys shards 0-3/4 passed at this head.
6. **Unchanged surfaces and docs.**
   - **Render path and channel-map semantics:** no render file changed, and `resolve_ch` is unchanged.
   - **Area:** reproduced as in the Summary. `milan_datapath` gains exactly one register (`media_tick_q_r`).
   - **Docs checked:** TIME_SYNC.md, REGISTER_MAP.md `SLIP_TDM` text and reading table, CHANNEL_MAP_64.md, FPGA_DESIGN.md, TESTING.md (14 mutants listed, matching `mutants.py`) and CHANGELOG.md are accurate, apart from F1, F2 and S3.

## Lens results (clean lenses carry their artifact)

```text
[R394] PASS Conformance — hdl/ieee1722/aaf/KL_chan_map_capture.sv:971,1010-1068 @377d1ac3; receipts/head-junction-full.log, head-dp-leg.log, sum-head-junction.txt — #617 acceptance 1-3 and ruling 5875206178 items 1-4 against IEEE 1722-2016 7.3.5 (one event = one instant): 0 torn columns in every INTERNAL scenario and all 281 placed/unplaced CRF engagements; crossing guarded; dense sweep with no tail slip; guard-removal mutants killed; suite header/TIME_SYNC/REGISTER_MAP state it; R395-1 F2 answered by chmap [F1] (RM1-class mutant killed); latency table exact (787.25/552.83/318.42/84.0 re-derived); Milan v1.2 7.4 ±50 ppm envelope holds.
[R394] PASS RTL — KL_chan_map_capture.sv:810,971,1010-1068,1190-1198; milan_datapath.sv:5706-5724 @377d1ac3; receipts/ooc/*.stat.txt, r394-ooc-summary.txt — snapshot/late-load/counter 2'b11 law traced edge by edge and consistent; aligner split on the walk's crossing by the one-cycle tick delay; keep-off min(DIV/4,256) legal at every clock (2K<DIV guard); every new register reset; close and aligner marker are the same aafcap signals on solo/I2S/blend/wide shapes; area reproduced (1x1 LUT 1263->1265, 8x8 2103->2132, FF unchanged, BRAM 0; datapath +1 FF).
[R394] PASS Robustness — KL_chan_map_capture.sv:971,1055-1068,1195-1198; KL_media_grid_align.sv:176-186,253-268 @377d1ac3; receipts/sum-quarter.txt, sum-head-junction.txt, rm6-band-run.log — engagement on/near the crossing at quarter-cycle placement ±50 ppm (one net-zero repeat/skip only exactly on it), pulled-engagement approach floor 53-61 cycles at 50 ppm, re-engagement/timeout/re-selection (fresh engagement, same analysis), reset, stream start, CRF loss/holdover, INTERNAL, I2S one-pair, 8x8 pre-walk, blend; the >64 ppm behaviour is outside the Milan bound and is recorded as F2 (Docs), not as a design defect.
[R394] PASS Tests — tb/verilator/capture_coherence/{sim_main.cpp,coherence_bench.hpp,coherence_wrap.sv,sim_dp.cpp,mutants.py,Makefile}, tb/verilator/chmap_capture/sim_main.cpp @377d1ac3; receipts/head-*.log, head-mutation-arm.log, r394-mutants2*.log — junction 5240/0, dp 311/0, arm 19/19, chmap 318/0 + 20/0, media_grid_align 45/0 + 3 red controls; header coverage statements match the scenario code exactly; reviewer mutants RM5/RM6 killed, RB1 reproduces the band (17/65); RM7/RM8 survive on a path unreachable within the walk budget (S1, optional); arm leaves the ±50 sweeps' role to the full run (S2, optional).
[R394] NEGATIVE Docs — F1 (hdl/ieee1722/crf/KL_media_grid_align.sv:79-83) and F2 (PR #618 body "Open risks", ±75 ppm) open. Otherwise examined and accurate: TIME_SYNC.md:176-178,453-562; REGISTER_MAP.md:1829-1968; CHANNEL_MAP_64.md:330-340; FPGA_DESIGN.md:258,292; TESTING.md:490; CHANGELOG.md:37-55; milan_datapath.sv:5650-5717 and KL_chan_map_capture.sv:75-105,960-1068 comments.
```

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #617 acceptance, rulings 5875206178 / 5875511547; KL_chan_map_capture.sv:971,1010-1068; junction and datapath logs; latency re-derivation; IEEE 1722-2016 7.3.5; Milan v1.2 7.4 ±50 ppm | R394-2 | 377d1ac3658feb8d544e6ed1005b186b67127f35 |
| RTL | CLEAN | KL_chan_map_capture.sv (round-2 regions, edge by edge); milan_datapath.sv:5650-5724, 1205-1273; KL_media_grid_align.sv whole module; OOC 1x1/8x8, round 1 vs head | R394-2 | 377d1ac3658feb8d544e6ed1005b186b67127f35 |
| Robustness | CLEAN | 44 quarter-cycle ±50 ppm placements; 260 + 21 committed placements; threshold probes at 55-75 ppm; RM6; reset/start/re-engagement/shape analysis | R394-2 | 377d1ac3658feb8d544e6ed1005b186b67127f35 |
| Tests | CLEAN | capture_coherence (all files), chmap_capture diff and run, media_grid_align run, committed arm 19/19, RM5-RM8 and RB1 | R394-2 | 377d1ac3658feb8d544e6ed1005b186b67127f35 |
| Docs | UNCLEAN (F1, F2) | TIME_SYNC.md, REGISTER_MAP.md, CHANNEL_MAP_64.md, FPGA_DESIGN.md, TESTING.md, CHANGELOG.md, module banners, PR body, REVIEW READY comment | R394-2 | 377d1ac3658feb8d544e6ed1005b186b67127f35 |

Note on banking. F1 is a comment in `hdl/`. A later commit that answers it touches the `RTL` lens's files but not their logic. Whether that un-covers `RTL` is the manager's call under AGENTS.md section 7. A comment-only diff re-read under `Docs` is enough for this reviewer. F2 needs no commit.

## Prior public review findings at this head

I wrote this section after the verdict and ledger above. It covers the two round-1 reports on this PR: my R394-1 (comment 5875199285) and the external R395-1 (comment 5875505042). No other review report exists on the PR. Nothing here changes the verdict or the ledger.

| Prior finding | Status at 377d1ac3 | Evidence |
|---|---|---|
| R394-1 F1 (MINOR, Tests/Docs): residual CRF band at the close/snapshot crossing was undocumented, and the committed grid missed it | **RESOLVED**, by a fix rather than documentation, per ruling 5875206178. The crossing is guarded; the sweep through it is dense and committed; the suite header, TIME_SYNC.md and REGISTER_MAP.md state it | Judgments 1 and 3; `head-junction-full.log` (65 + 65 + 53 + 53 placed, one net-zero pair exactly on the crossing); `sum-quarter.txt`; `rb1-band-run.log` (band 17/65 without the guard) |
| R394-1 S1 (Docs): the latency table carried sampled-mean bias | **TAKEN.** The exact table is TIME_SYNC.md:477-488, re-derived in Judgment 4 | TIME_SYNC.md:477-498 |
| R394-1 S2 (Robustness): per-pair "staged since last close" visibility for a front end that drops a mid-frame pair | **NOT TAKEN, still optional.** The round-2 assignment filed it under the slot-0 counter notes instead. No front end I found drops a mid-frame pair (R394-1), so it does not affect coverage | `KL_chan_map_capture.sv:561-580` unchanged in that respect |
| R395-1 F1 (MAJOR, RTL/Robustness/Tests/Docs): CRF locks could sit on the crossing, and SLIP_TDM was blind to it | **RESOLVED.** The aligner keys on the close, with the tick one cycle late and a 256-cycle keep-off. SLIP_TDM keys on the close against the snapshot and is graded walk by walk. The dense sweeps run at 1-cycle steps (true plan), 4-cycle steps (±50 ppm; my quarter-cycle placements fill the gaps) and 2-cycle steps (datapath). Docs updated. Within ±50 ppm no lock slips | Judgments 1-3; `head-dp-leg.log` (DP-band 13 placements, 0 slips); `head-mutation-arm.log` (guard-removal mutants killed in the wrapper and in `milan_datapath`) |
| R395-1 F2 (MINOR, Tests/Robustness): the one-pair frame was not load-bearing | **RESOLVED.** `chmap_capture` [F1] drives pair 0 alone on lane B's one-pair frame; the RM1-class mutant ("closes on the bucket's last pair whatever the frame length") is killed by `F1: col 0 carries its own pair-0 frame (L)` | `head-chmap_capture.log`, `head-mutation-arm.log` |
| R395-1 F3 (MINOR, Docs): sampled means stated as the latency change | **RESOLVED.** The table is deterministic; the pair-3 sentence ("the read moving to the tick", 84 cycles) agrees with its row; the CHANGELOG says 1.68 to 15.75 µs; "+2 to +16 us" no longer appears in the PR body, CHANGELOG or TIME_SYNC.md | Judgment 4; CHANGELOG.md:44 |
| R395-1 S1 (Docs): Arty blend I2S pair latency note | **TAKEN** | TIME_SYNC.md:502-504 |
| R395-1 S2 (Docs): stale `tdm_hold_r` name | **TAKEN** | `tb/verilator/milan_dp/sim_nxn.cpp:7874-7878` |
| R395-1 S3 (Tests): the counters and marker were slot-0 based | **TAKEN / superseded.** Neither keys on slot 0 now, and the suite header says so | `sim_main.cpp:83-89`, `media_grid_align_wrap.sv:75-81` |

Round 2 opened no prior finding. F1 and F2 of this report are new: they are statements that round 2 itself made untrue or published.

## Evidence I ran (receipts listed in MANIFEST.sha256)

**Setup.**

- **Simulator:** 5.050. The assignment's path `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` does not exist. I used `$VALIDATION_STORAGE/372-manager-r2/pinned-tool-bin/verilator`, whose wrapper hash matches the one my round-1 packet recorded (`receipts/tool-identity.txt`).
- **Tree:** every run used a scratch copy of the head tree (`receipts/r394-scratch-tree.txt`).
- **Clone:** never built or edited. `receipts/r394-clone-integrity.txt` shows HEAD, tree and index at the exact head, a clean worktree with nothing ignored, and all four gitlinks equal to `HEAD`'s.

| Run | Result | Receipt |
|---|---|---|
| `capture_coherence` junction leg, full | 5,240 checks, 0 failures, rc 0 | `head-junction-full.log`, `sum-head-junction.txt` |
| `capture_coherence` datapath leg | 311 / 0, rc 0 | `head-dp-leg.log` |
| Committed mutation arm, its own `clean_control`/`grade_mutant`, 7 threads (`scripts/r394_run_arm.py`) | 19 / 19 PASS | `head-mutation-arm.log` |
| `chmap_capture` (`make run`) | 318 / 0; netlist 20 / 0 | `head-chmap_capture.log` |
| `media_grid_align` | 45 / 0; 3 negative controls red | `head-media_grid_align.log` |
| Quarter-cycle placements, ±50 ppm (`scripts/r394_probe.py`) | 44 engagements; only exactly-on-crossing ones repeat/skip once; 0 failures | `probe-head-[pm]50-quarter.log`, `sum-quarter.txt` |
| ±75 ppm, 34 placements each | 3 + 4 check failures near the crossing | `probe-head-[pm]75.log`, `sum-75.txt` |
| +55/+60/+65/+70 ppm, 0..+40 in 2-cycle steps | pass / pass / pass / 2 failures | `probe-head-p5*.log`, `p6*.log`, `p70.log`, `sum-threshold.txt` |
| Reviewer mutants (`scripts/r394_mutants2.py`) | RM5 killed (full 181 failures; `--band` 1302/0); RM6 killed; RM7, RM8 survive; RB1 17/65 band phases slip | `r394-mutants2*.log`, `rm5-*.log`, `rm6-band-run.log`, `RM7_*`, `RM8_*`, `rb1-band-run.log`, `sum-rb1.txt` |
| OOC area, round 1 vs head (`scripts/r394_ooc_capture.sh`, Yosys 0.66, sv2v v0.0.13) | 1x1 LUT 1263 -> 1265, FF 1384; 8x8 lane-off 2103 -> 2132, FF 1931; RAM32M 8, no BRAM | `r394-ooc-summary.txt`, `ooc/*.stat.txt` |
| Hosted checks at 377d1ac3 (snapshot) | 18 pass (Verilator shards 0, 2, 3; Yosys 0-3; elaborate; docs-check; rtl-fast; full-ci-gate; lint and others); Verilator shards 1/5 (owns `capture_coherence`) and 4/5 (`milan_dp`) **pending**; physical gPTP skipped (a skipped context, not a pass) | `hosted-checks.txt` |

## Limits

- **Not run by me:**
  - `milan_dp`, `milan_dp_render`, `tdm`, `pair_fill` and `pp_shadow`;
  - the builder bank, lint, xvlog and Yosys `run.sh`;
  - the Markdown and code-quality gates;
  - act and any host runner.

  These are the manager's; the published evidence reports rc 0. The render path is judged unchanged from the diff.
- **Drift-level coverage.** Simulation covers the 1x1 TDM8 shape at 50 MHz only. The I2S one-pair, blend and 8x8 shapes are covered by RTL reading and the deterministic `chmap_capture` arms, not by a drift sweep.
- **Source model.** The harness models the source's rate error as seen whole by the aligner, because the NCO is not mirrored from an MMCM servo. In the product the NCO mirrors the MMCM command, so the aligner sees about the -10.64 ppm plan. The ±50/±65/±75 ppm results are therefore a harness envelope and a stress bound, not a product measurement.
- **#386 timings.** The 682.7 ms / 486.9 ms #386 figures are the author's probe. I confirmed only that the ceiling is 32,768 ticks = 682.7 ms and that the loop's slow mode makes a fully pulled engagement plausibly reach it.
- **Hosted status.** Verilator shards 1/5 and 4/5 were pending at my snapshot. The hosted `capture_coherence` wall time against the 1,800 s per-suite guard is therefore unobserved.
- **No hardware.** No physical calibration or hardware run was done. Acceptance 4, the #451 bench re-run, is NOT RUN. Simulation passes and skipped field contexts are not hardware proof.
- **Redaction.** The home-directory prefix is redacted to `$HOME` in receipts.

## Pending manager duties

- Route F1 (a comment edit in `KL_media_grid_align.sv`) and F2 (a PR body correction). Then request a Docs re-review at the resulting head, and decide under section 7 whether the comment-only `hdl/` diff un-covers `RTL`.
- Hosted acceptance at the exact head: Verilator shard 1/5 (`capture_coherence`, including its wall time against the 1,800 s guard) and shard 4/5 (`milan_dp`). Also the act replica.
- The builder and native banks are already published. Final current-dev candidate validation happens at the merge turn: source base `ce550952`, live dev `7390b43627032c71c470e2aa8d0845eb5b740663`.
- Acceptance 4, the #451 bench re-run on the next image, remains open. The PR says "Relates to #617".
- Optional: S1-S3.

R394-2 FINISHED
