[R394] NEGATIVE - exact head 5546b976161bdfd0611040160df44806a0b95d15

# R394-1 internal cleared-context review: issue #617 / PR #618

- Head `5546b976161bdfd0611040160df44806a0b95d15`, tree `628e40ce5857d0a487839a72ff392069b33392e3`, three commits on dev `ce550952e47fbd92367f0d9b099345100f7f4215`.
- Reconstructed from AGENTS.md, CONTRIBUTING.md, the #617 body, the assignment comment 5872575286, the TAKEN and REVIEW READY comments, the PR body, the diff and history `ce550952..5546b976`, and the public evidence tree `c30997b9:review-evidence/617-r1`.
- Prior public review findings on PR #618: **none**. At the time of writing the PR had 0 reviews, 0 inline comments and two review-start notices (R394-1, R395-1). No other reviewer's report was read.
- Five lenses applied. One MINOR finding is open under `Tests` and `Docs`. That makes the verdict NEGATIVE.

## Summary

The frame-atomic handoff is correct, and it fixes #617.

- **RTL.** STAGE is written by each pair strobe. FRAME is published in one edge by the strobe of pair `TDM_FRAME_PAIRS_P-1`. WALK is loaded on the pre-walk's last cycle and held for the whole walk. Every AAF column therefore carries one TDM frame.
- **Harness evidence.** Re-run at the head: junction leg 456/0, datapath leg 118/0, committed mutation arm 8/8.
- **Base reproduction.** The same harness against the `ce550952` RTL fails: junction 47/456, datapath 7/118, INT-true 66.1% torn in exactly the four #451 states. The failure, torn and tally lines are identical to the author's published base logs.
- **My mutants.** I wrote four, all killed. RM4 tears only when the last pair's strobe lands exactly on the snapshot cycle.
- **CRF sweep.** I swept 313 CRF lock phases (261 on the true plan at 4-cycle steps, 52 at ±50 ppm). None tears a column.
- **Resources.** Reproduced exactly from the RTL.
- **Unchanged.** The render path, ports, processor and firmware are untouched.

What is open is honesty about a residual. Under CRF, the crossing that decides a column is now the frame close against the walk snapshot. The aligner's keep-off protects the slot-0 marker against the tick, not this crossing. A lock landing within its dither of the crossing repeats and skips whole frames continuously while locked.

- This is pre-existing and reduced. At base, each pair had its own such band, and 180 of 261 phases also tore.
- The PR body discloses it.
- The authoritative docs this PR writes do not. The committed suite's 16-phase CRF grid steps over the band, while its header says a lock lands in every region the INTERNAL sweep crosses.
- At the band, the suite's own `[C] slips while the CRF lock held` check fails. That is F1.

## Findings

### F1 - MINOR - lenses: Tests, Docs

**Location:** `tb/verilator/capture_coherence/sim_main.cpp:31-32,47,424`; `docs/design/TIME_SYNC.md:453-494` (row `:467`); `docs/reference/REGISTER_MAP.md:1833-1836,1940`.

**Title:** the residual CRF-lock repeat/skip band at the frame-close / walk-snapshot crossing is missing from the authoritative docs, and the committed CRF grid structurally misses it.

**Authority / evidence:**

- AGENTS.md section 5 requires updating authoritative documentation when behavior changes. Section 6 (Tests) says tests must not merely reproduce implementation assumptions. Section 6 (Docs) requires changed contracts to be reflected in authoritative docs.
- The change moves the TDM data crossing from four per-pair crossings (each pair strobe against its slot's inject) to one crossing. That crossing is the frame close against the snapshot, which I measured at up to `LB_PAIRS_C+1` = 5 axis cycles after the tick on 1x1.
- `KL_media_grid_align`'s keep-off guards the slot-0 marker against the tick (`REGISTER_MAP.md:1924-1930`). It does not guard this crossing, which lies about 781 cycles (3 pair periods) after the marker.
- Reviewer sweep `receipts/r394-crf-sweep-head-true.summary.txt`. The true 391/1591 plan, CRF, 261 start delays 0..4160 in steps of 16 (4 axis cycles), 2000 columns each, running the committed checks unchanged:
  - Delays 4080 and 4096 fail the committed `[C] slips while the CRF lock held`, with 61 and 31 tail slips (about 1000 tail columns).
  - All four pairs slip together, with 0 torn columns. The lock phase is tick 1037-1041 cycles after the close.
  - Delays 4112 and 4128 chatter 20-29 repeat/skip pairs before the tail.
- ±50 ppm (`r394-crf-sweep-head-m50.summary.txt`, `-p50`): 14 of 26 and 13 of 26 phases fail the same check. The lock spread is 39 cycles, so the band is at least 40 cycles wide, roughly 4% or more of lock phases. Both sweeps hit their window edge, so this is a lower bound.
- Base comparison (`r394-crf-sweep-base-true.summary.txt`, same 261 phases): 8 phases with tail slips (2 per pair), 180 phases with torn columns. So the head is a strict improvement, and the residual is pre-existing in class.
- **Committed grid.** `sim_main.cpp:424` starts the 16 CRF-true locks 260 steps (about 65 cycles) apart. Its nearest phases, 1018 (`CRF-true-00`) and 43 (`CRF-true-15`), bracket the band. The ±50 ppm locks are 1041 steps apart and also miss it. Meanwhile `sim_main.cpp:31-32` says the offsets are chosen "so a lock lands in every region the INTERNAL sweep crosses", and `:47` says "a CRF lock held its phase slip-free". The PR body states "None of the 32 simulated CRF phases hit it", so the gap is known and deliberate, but it is not represented in the suite.
- **Docs.** The new "Talker capture handoff" section states "CRF holds the phase" (`TIME_SYNC.md:467`) and does not mention the unguarded crossing. `REGISTER_MAP.md:1833-1836`, edited by this PR, says the counters count "every slip at each junction ... the TDM frame bank". Its reading table (`:1940`) grades `static`/`static` as "one grid".
- In the band, the marker sits about 260 cycles from the tick, one per tick. By construction, `SLIP_TDM` therefore stays static while the talker repeats and skips 3-6% of frames. This is derived from the counter law at `KL_chan_map_capture.sv:594-627`; the counter was not read in the probe.
- The limitation lives only in the PR body. No public Issue tracks it.

**Impact:**

- A CRF engagement that lands in the band emits continuous whole-frame repeat/skip. That is about 1% of lock phases on the true plan and at least about 4% at ±50 ppm.
- The durable documentation and `SLIP_TDM` tell a reader "one grid, slip-free". Acceptance 4's bench run, or a later field report, would be misread.
- The committed CRF `[C]` check passes because of phase selection, not because the property holds at every lock phase.

**Required outcome:**

1. The authoritative docs record the residual as a known limitation of the frame-atomic handoff under CRF. At minimum, the TIME_SYNC.md Talker capture handoff section, with a caveat or pointer where the `SLIP_TDM` reading table grades `static`/`static`. They must state:
   - the crossing (frame close against walk snapshot) is not covered by the keep-off;
   - the effect: whole-frame repeat/skip while locked, never a torn column, with `SLIP_TDM` static;
   - the measured band width;
   - that it is pre-existing and reduced relative to the per-pair law.
2. The capture_coherence suite represents the band honestly. Either it runs a CRF scenario inside the band and records the known behavior (information, or an explicitly labeled expected-limitation check with a pointer to the tracking Issue), or its header comments stop claiming full-region CRF coverage and state which band is excluded and why.
3. The residual is tracked by a public Issue. Filing it is a manager duty; it is not asked of this lane's code.

This finding does not ask for an RTL change in this PR. Whether to fix the crossing here (for example, by keying the keep-off on the frame close) or to track it is a maintainer decision.

**Verification:** re-read the corrected sections. Re-run `scripts/r394_crf_phase_probe.py` at the new head. The band behavior should be unchanged unless the RTL changes, and the documented width should match the probe.

### S1 - SUGGESTION - lens: Docs

**Location:** `docs/design/TIME_SYNC.md:474-482`.

The per-pair change is the difference of means over a 1.02-beat window. That window includes a slip cluster, so the means carry up to about ±10 cycles of window bias, for example head pair 3 at 525.8 against a [-5, 1036] range centre of 515.5.

The structural shifts, taken from the measured min/max ranges in `receipts/head-junction-leg.log` against `base-ce550952-junction-leg.log`, are +782, +547, +313 and +79 cycles. That is +15.64, +10.94, +6.26 and +1.58 us.

`:482` explains pair 3's change as "the read moving to slot 0's instant". That move is about 79 cycles, not the tabled 99.1. Consider tabling the structural shift, or noting the bias. The "+2 to +16 us" order of magnitude and the "what atomicity requires" argument stand.

### S2 - SUGGESTION - lens: Robustness

**Location:** `hdl/ieee1722/aaf/KL_chan_map_capture.sv:547-566`.

The close publishes whatever STAGE holds for pairs `0..TDM_FRAME_PAIRS_P-2`. Every front end restarts at slot 0 and re-stages all pairs before the next close:

- the master at `fpos 0`;
- the slave at an armed fsync start of line (`sol`);
- after reset, all banks are zero.

So this holds on every path I found. A front end that dropped a mid-frame pair (the CDC FIFO `!cap_full_w` write gate) would publish that pair's previous-frame sample. Per-pair "staged since last close" bits would make that case visible if it is ever reachable. This is optional.

## Lens results (clean-lens lines carry their artifact)

```text
[R394] PASS Conformance — hdl/ieee1722/aaf/KL_chan_map_capture.sv:518-566,1013-1027,1052-1053 @5546b976; receipts/head-junction-leg.log, head-datapath-leg.log, base-ce550952-*.log — #617 acceptance 1-3 against IEEE 1722-2016 7.3.5 (an AAF-PCM sample event is one sample per channel at one instant; the talker's events are the crossbar walks): 0 torn columns at head in every committed scenario and in 313 reviewer CRF phases; the defect reproduces at ce550952 (47/456, 7/118, 66.1% torn in the #451 states 0,0,0 / -1,-1,-1 / 0,0,-1 / 0,-1,-1); "no added sample" graded per walk by [W] "older than the newest frame closed by the tick" (committed late-publish mutant killed by it); render path untouched (r394-scope-check.txt); acceptance 4 is out of scope by the assignment.
[R394] PASS RTL — KL_chan_map_capture.sv:311-317,436-438,518-566,594-627,1013-1027,1079-1153; milan_datapath.sv:842-845,1208-1223,1260-1274,5675 @5546b976 — edges traced by hand: a close strobe in the snapshot cycle lands in FRAME at the same edge WALK samples the old FRAME, so the walk takes the previous whole frame; a close mid-walk changes FRAME only; the walk reads WALK only (CM_STEP_S, :1124-1131); a queued tick restarts the pre-walk and re-snapshots; reset zeroes STAGE/FRAME/WALK; the FSM is unchanged; the guard :520-524 fires for 0, N/2+1 (r394-guard-probe.txt; fatal without -Wno-fatal); CMAP_TDM_FRAME_PAIRS_C = min(AIF_PAIRS_C,4) is 1 (I2S), 2 (TDM4), 4 (TDM8), 4 (TDM16/32, close on the last kept pair), 4 (blend, close on TDM pair 2; TDM pair 3 already unreachable); the #74 marker and counters are unchanged, and the harness wrapper's marker binding matches the datapath (:5675); no port changed; OOC reproduced: 1x1 LUT 1292->1263, FF 1048->1384 (+336 = 7x48: STAGE 0..2 + WALK 0..3; STAGE 3 is never read), BRAM 0; 8x8 product shape (loop lane off) LUT 2062->2103, FF 1595->1931 (receipts/r394-ooc-summary.txt, ooc/*.stat.txt).
[R394] PASS Robustness — KL_chan_map_capture.sv:547-566,1013-1027; KL_tdm_capture_master.sv:291-363; KL_tdm_capture.sv:136-180; KL_pair_blend.sv:103-116 @5546b976; receipts/r394-mutants-quick.log, r394-crf-sweep-*.summary.txt — stream start/reset (the front ends start at slot 0; banks zero until the first whole frame), fsync restart mid-frame (re-staged before the next close), mid-walk close (RM3 killed; chmap_capture [F] col 3), close coincident with the snapshot cycle (RM4 killed: 3/4 torn columns in the ±1000 ppm sweeps, 25 in CRF+50-0), CRF lock at every phase at 4-cycle resolution: 0 torn; the residual whole-frame repeat/skip band is continuity, not atomicity, and is pre-existing (base: 8 per-pair bands and 180/261 torn), reduced by this change and outside #617 acceptance; its documentation, tests and tracking are F1 and a manager duty.
[R394] NEGATIVE Tests — F1 open (tb/verilator/capture_coherence/sim_main.cpp:31-32,47,424). Otherwise examined: re-ran capture_coherence (456/0, 118/0, mutants 8/8), chmap_capture (254/0 + 20/0) at head; base reproduction identical to the published author logs (r394-base-crosscheck.txt); four reviewer mutants all killed by [A]/[W]; the chmap_capture arm changes deliver whole frames without dropping any prior expectation.
[R394] NEGATIVE Docs — F1 open (docs/design/TIME_SYNC.md:453-494, docs/reference/REGISTER_MAP.md:1833-1836,1940); S1 optional. Otherwise examined and accurate: CHANNEL_MAP_64.md sections 4/7, FPGA_DESIGN.md row, TESTING.md row (six mutants as named), CHANGELOG.md, the TIME_SYNC.md rows (frame complete, publish, read at LB_PAIRS_C+3 = 7 on 1x1, age range -5..1036, per-pair (3-p) x 5.208 us), MODULE_MATRIX/README-tests regeneration (gate evidence is the manager's).
```

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #617 body + assignment; KL_chan_map_capture.sv:518-566,1013-1027,1052-1053; head and base harness logs; IEEE 1722-2016 7.3.5 sample-event semantics | R394-1 | 5546b976161bdfd0611040160df44806a0b95d15 |
| RTL | CLEAN | KL_chan_map_capture.sv (whole module, changed regions traced edge by edge); milan_datapath.sv:842-845,1208-1223,1260-1274,5675; front ends and blend; guard probe; OOC 1x1 and 8x8 head vs base | R394-1 | 5546b976161bdfd0611040160df44806a0b95d15 |
| Robustness | CLEAN | reset/start/restart paths; RM1-RM4; 313-phase CRF sweeps head vs base; shape derivations | R394-1 | 5546b976161bdfd0611040160df44806a0b95d15 |
| Tests | UNCLEAN (F1) | capture_coherence sim_main.cpp, coherence_bench.hpp, coherence_wrap.sv, sim_dp.cpp, mutants.py, Makefile; chmap_capture diff; re-runs | R394-1 | 5546b976161bdfd0611040160df44806a0b95d15 |
| Docs | UNCLEAN (F1) | TIME_SYNC.md, CHANNEL_MAP_64.md, REGISTER_MAP.md, FPGA_DESIGN.md, TESTING.md, CHANGELOG.md, PR body | R394-1 | 5546b976161bdfd0611040160df44806a0b95d15 |

## Evidence I ran (receipts listed in MANIFEST.sha256)

The simulator was 5.050. The path named in the assignment, `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator`, does not exist. I used the byte-identical 5.050 wrapper at `$VALIDATION_STORAGE/372-manager-r2/pinned-tool-bin/verilator`; its identity is in `receipts/tool-identity.txt`.

All runs used a scratch copy of the head tree. Its 952 tracked files are byte-identical to the clone (`r394-clone-integrity.txt`). The submodule directories were made git-listable in scratch only.

| Run | Result |
|---|---|
| `make run` (junction leg) | `capture_coherence: checks: 456 failures: 0`, rc 0 |
| `make dp` | `capture_coherence_dp: checks: 118 failures: 0`, rc 0 |
| `python3 mutants.py` | 8 checks, 8 PASS, rc 0 |
| `make -C tb/verilator/chmap_capture` | 254 checks, 0 failures; netlist pin 20/0; rc 0 |
| Base RTL + head harness (`r394-base-probe-tree.txt`) | junction 47/456 FAIL, INT-true 66.1% torn; datapath 7/118 FAIL; identical to the published author logs |
| `scripts/r394_mutants.py` (quick) | RM1 late snapshot, RM2 stale closing pair, RM3 mid-walk refresh, RM4 close on the snapshot cycle: 4/4 killed |
| `scripts/r394_crf_phase_probe.py` + `r394_sweep_summary.py` | head true plan 2/261 phases fail `[C]` tail slips, 0 torn; base 8/261 slip, 180/261 torn; head ±50 ppm band at least 40 cycles, 0 torn |
| `scripts/r394_ooc_capture.sh` | reproduces every PR area figure |
| Elaboration guard | errors for 0 / N/2+1, passes 1..N/2 |

## Limits

- Not run by me: `milan_dp`, `milan_dp_render`, `tdm`, `media_grid_align`, `pair_fill`, `pp_shadow`, the builder bank, lint, the Markdown/code-quality gates, Yosys `run.sh`, xvlog, act and hosted CI. These are the manager's; their published evidence reports rc 0.
- The render path is judged unchanged from the diff (no render file touched), not by re-running `milan_dp_render`.
- The drift-level simulation covers the 1x1 TDM8 shape at a 50 MHz axis clock only. The 8x8 walk length is covered only by the deterministic chmap_capture `[F]` arm and by RTL reading.
- The CRF band width at ±50 ppm is a lower bound; both sweeps reached their window edge. The `SLIP_TDM` stasis in the band is derived from the counter law, not read from the probe.
- No physical calibration or hardware run was done. Acceptance 4 (the bench re-run) is NOT RUN. Simulation passes and skipped field checks are not hardware proof.
- Hosted exact-head checks were only partly finished when I snapshotted them (`receipts/hosted-checks-snapshot.txt`); the manager owns hosted and act acceptance.
- The home-directory prefix is redacted to `$HOME` in the receipts.

## Pending manager duties

- Decide F1's route: document and test the residual in this PR (the required outcome), and file a public Issue for the unguarded close/snapshot crossing under CRF with this packet's probe as evidence. Decide whether any RTL fix belongs here or there.
- Final current-dev candidate validation: source base `ce550952`, live dev `7390b43627032c71c470e2aa8d0845eb5b740663`, with the builder and native banks at the merge turn.
- Hosted and act acceptance at the exact head, including the Verilator shards that were still in progress at my snapshot.
- Acceptance 4: the #451 bench re-run on the next image.
- Re-review of the corrected head for Tests and Docs. Re-cover any lens whose scope a new commit touches.

R394-1 FINISHED
