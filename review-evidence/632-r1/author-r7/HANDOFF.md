# A659: milan-fpga #632 + #764 (phase-align the recovered media clock to the followed CRF)

## Round 7c (session 14, 2026-10-23 09:56 CEST onward) -- test-only fix of the gmstep boot-GM control

**Status: REVIEW READY at `c2c996fa` (not pushed), posted https://github.com/kebag-logic/milan-fpga/issues/632#issuecomment-6368300512 (text: `public-review-ready-r7c.txt`).** Every gate the round names passes. Assignment: the [A10] ruling
https://github.com/kebag-logic/milan-fpga/pull/770#issuecomment-6360257772 (ruling (c): the detector is right, no RTL
change; ruling (a): the fix is test-only and goes in this PR). Base `d835ba12` (confirmed HEAD; not pushed).
Receipts under `receipts/round7/` (this round's directories carry `r7c` or the head).

Items: (1) fix the control "the grandmaster change stops the talker for good", keyed on the leg's own GM A -> GM B
event; the driver prints the failing check names for every control; prove it planted alone at the head and on a
clean dev `e5b480a3` clone with only the test fix; add one clean-leg check recording the boot own-identity -> GM A
pulse; (2) gmstep-mutants, `ctrl_boundary.py`, the full sweep, lint and the docs gates where their inputs changed,
`check-baseline`; (3) PR body and HANDOFF.

Commit on `d835ba12`: `c2c996fa` "Key the gmstep talker-stop control on the GM A to GM B event and record the boot
grandmaster's detector pulse with a control that must fail it" (test and docs only;
`git diff --stat d835ba12 c2c996fa -- hdl syn configs` is empty, so no RTL change and the resource record stands).

### Changes (file:line at `c2c996fa`; clause)

| File:line | Change | Clause |
|---|---|---|
| `tb/verilator/milan_dp_gm_steps/gmstep_mutants.py:203-217` | the control "the grandmaster change stops the talker for good" latches `gm_stop_r` on `gm_recentre_p_r && (\|aaf_stream_en_raw_w)` (`:213`): keyed on the leg's own GM A -> GM B event, the first detector pulse while the talker's gate is open; comment gives the reason | ruling (a), issuecomment-6360257772 |
| `gmstep_mutants.py:89-93` | `GM_DETECT_EXEMPT` (the detector's 0 -> id exemption line) and `THIS_CLOCK` (the leg's thisClock) | IEEE 802.1AS-2020 9.6.2.2, 10.2.4.13 |
| `gmstep_mutants.py:263-271` | new `--all` control "the detector exempts this station's own boot identity" | ruling (c) |
| `gmstep_mutants.py:106`, `:109-112`, `:300` | `Leg.probes`; the gmstep leg's `gmstep_probes.vlt`; the freshness check counts it as an input | -- |
| `gmstep_mutants.py:360-374`, `:406-421` | the failed check names printed for every control outcome and for a failing clean leg | ruling item 1 |
| `gmstep_mutants.py:23-25` | docstring names the new control | -- |
| `tb/verilator/milan_dp/gmstep_probes.vlt:1-7` | `public_flat_rd` on `milan_datapath`'s `gm_recentre_p_r` and `gm_recentre_q_r` (the repository's probe-file pattern, as `ax1x1gptp_probes.vlt`) | -- |
| `tb/verilator/milan_dp/Makefile:430-431`, `:439` | the gmstep recipe reads the probe file | -- |
| `tb/verilator/milan_dp/sim_gmstep.cpp:74-77` | banner: GM A is a grandmaster change since FPGA-gPTP #82; the baseline records the pulse | FPGA-gPTP #82 |
| `sim_gmstep.cpp:114-117` | `kThisClock` (the generator's default MAC 02:A1:B2:C3:D4:E5, as `sim_gptp.cpp:53`) | -- |
| `sim_gmstep.cpp:278-284`, `:395-400`, `:559-566` | `GmPulse`; every detector pulse from reset with the identity it left and the one it names (kept across `acquire()`'s trace reset) | -- |
| `sim_gmstep.cpp:974-990` | `GMDET:` lines and the check "boot grandmaster: the detector pulsed once, at this station's own identity -> GM A, and the baseline talker streams after it" | IEEE 802.1AS-2020 9.6.2.2, 10.2.4.13 |
| `tb/verilator/milan_dp/README.md:1057`, `:1059`, `:1064-1071`, `:1126`, `:1134`, `:1139`, `:1143`, `:1454` | the phase table, the boot-grandmaster paragraph, the control table (keyed control, new row), twenty-one controls, eighteen tabulated | -- |
| `docs/testing/TESTING.md:278` | sixteen gmstep controls | -- |
| `docs/design/GM_LOSS_RECOVERY.md:253`, `:271-279`, `:291-295` | 21 controls; the stop's key and the boot pulse; the new control | IEEE 802.1AS-2020 |
| `CHANGELOG.md:112-116` | five lines | -- |

### New checks (planted mutant -> failing words)

| Check | Planted mutant | Failing words |
|---|---|---|
| clean leg: "boot grandmaster: the detector pulsed once, at this station's own identity -> GM A, and the baseline talker streams after it" | `gmstep_mutants.py` control "the detector exempts this station's own boot identity": `(gm_recentre_q_r != 64'd0)` -> `... && (gm_recentre_q_r != 64'h02A1B2FFFEC3D4E5)` | `[FAIL] boot grandmaster: the detector pulsed once, at this station's own identity -> GM A, and the baseline talker streams after it` (exactly one failed check, at the head and on dev + the fix) |
| the repaired control (meaning unchanged) | `gm_stop_r` on `gm_recentre_p_r && (\|aaf_stream_en_raw_w)` gating the talker | `[FAIL] licence: the talker never pauses beyond four of its intervals` (12 failed checks; "baseline: the talker streams" passes) |
| driver output | -- | every control outcome now ends `    it broke N check(s): ...` |

### Gate table (round 7c)

| Gate | Command | Head | Result | Receipt |
|---|---|---|---|---|
| the fixed control, planted alone | `scripts/round7b/gm_stop_probe.py <out>` | tree = `c2c996fa`'s test files; dev `e5b480a3` + the fix | caught at both; the same 12 failed checks; the baseline streams | `round7/gmstep_fix_c2c996fa/` |
| the new control, planted alone | `gm_stop_probe.py <out> "the detector exempts this station's own boot identity"` | same | caught at both; 1 failed check, the new one | same |
| clean gmstep leg | `make -C tb/verilator/milan_dp gmstep-build GMSTEP_MDIR=<scratch>`; the binary | tree | 196 checks, 0 failures | same |
| gmstep-mutants | `scripts/round7/campaign.sh gmstep-c2c996fa c2c996faa tb/verilator/milan_dp_gm_steps gmstep-mutants VERILATOR_JOBS=2` | `c2c996fa` | **exit 0, 23 checks, 23 PASS** (08:13 -> 09:40 UTC) | `round7/gmstep_mutants_c2c996fa/` |
| campaign audit | `scripts/round7/campaign_audit.py` | receipts | gmstep 21/21 recorded | `round7/campaign_audit_c2c996fa/` |
| firmware boundary gate | `scripts/round7b/firmware_gates.sh <clone> <out> boundary` | `c2c996fa` | rc 0, 1,440 s, "ctrl_boundary: PASS" | `round7/firmware_boundary_c2c996fa/` |
| docs gates | `scripts/round7b/docs_run.sh c2c996faa` | `c2c996fa` | 44 steps, 42 rc 0, 2 skipped by rule; LiteX leg 1, md312 5/5, no-git pair rc 0 | `round7/docs_steps_c2c996fa/` |
| lint | `python3 scripts/lint_rtl.py --check` | `c2c996fa` | PASS 89 <= 89 | `round7/gmstep_fix_c2c996fa/lint_c2c996fa.log` |
| resource record | `python3 syn/ooc/pp_resource_gate.py check-baseline` | `c2c996fa` | "baseline PASS: 3 endpoints" | `round7/gmstep_fix_c2c996fa/check_baseline_c2c996fa.log` |
| full sweep | `scripts/round7/sweep.sh <clone> <out> 0 1 2 3` | `c2c996fa` | 63 of 64 suites pass, 2,190,061 checks, 0 in-suite failures: shard 0 15/15 (54,917 checks; `milan_dp` whole, the notify leg among it), shard 1 16/16 (331,530), shard 2 16 of 17 (262,031; `capture_coherence` stopped by the runner's 2,400 s wall clock, result unknown, not a failure), shard 3 16/16 (1,541,583). `capture_coherence` was then run again alone, the suite's own target as the runner invokes it on the same two CPUs: exit 0 in 2,402 s, 20,832 and 447 checks, 0 failures, its campaign 35 of 35, the runner's tally verdict clean. 09:40 to 15:19 UTC | `round7/sweep_c2c996fa/`, `round7/capture_coherence_rerun_c2c996fa/` |
| not re-run (inputs unchanged) | Vivado bank, Yosys, tdm8render-mutants, the pull-in, the builder bank, the firmware set's other seven | -- | round 7b's at `5282b8b6` / `d835ba12` stand: `c2c996fa` changes no `hdl`, `syn`, `configs`, `milan_dp_render`, `sw` or firmware file | -- |

Progress (kept current):
- 07:57 UTC HEAD `d835ba12` confirmed, origin `https://github.com/kebag-logic/milan-fpga.git`.
- Design (test-only; `git diff --stat d835ba12 HEAD -- hdl syn configs` is empty):
  - the control's planted stop latches on `gm_recentre_p_r && (|aaf_stream_en_raw_w)`: the first detector pulse while
    the talker's gate is open. The leg opens the gate in its media phase, after acquisition, so the boot
    own-identity -> GM A pulse cannot latch it and the GM A -> GM B pulse does; no pulse count, so a boot sequence
    with more or fewer pulses before the talker opens leaves it keyed on the same event. The control's meaning (a
    grandmaster change stops a streaming talker for good) and its named check are unchanged.
  - the driver prints "it broke N check(s): ..." for every control and for a failing clean leg, not only for a catch.
  - the clean leg records the adopted behaviour: `tb/verilator/milan_dp/gmstep_probes.vlt` opens `gm_recentre_p_r`
    and `gm_recentre_q_r` read only (the repository's probe-file pattern), `sim_gmstep.cpp` logs every pulse with
    the identity it left and the one it names, and the baseline checks "boot grandmaster: the detector pulsed once,
    at this station's own identity -> GM A, and the baseline talker streams after it".
  - a new `--all` control, "the detector exempts this station's own boot identity" (ruling (c)'s rejected
    behaviour), must fail that check and must not break "baseline: the talker streams". 21 controls + 2 clean legs =
    23 driver checks.
- 08:06 UTC clean leg at the edited tree: 196 checks, 0 failures; `GMDET: pulse at cycle 6001430, 02a1b2fffec3d4e5 ->
  00aaccfffe010203`.
- 08:10 UTC the fixed control planted alone (`scripts/round7b/gm_stop_probe.py`, the driver's own plant/build/run, whole
  leg): **caught** at the edited tree and on a clean dev `e5b480a3` clone with only the test fix applied
  (`$VALIDATION_STORAGE/scratch/632-a659/r7c/dev-e5b480a3`, patch archived): "baseline: the talker streams" ok, the boot
  record ok, 12 failed checks with "licence: the talker never pauses beyond four of its intervals" among them
  (TALKER: 0 PDUs over 825871 cycles). The same 12 on both.
- 08:15 UTC the new control planted alone: caught at both, exactly 1 failed check, the new one; the baseline streams.
- Commit `c2c996fa` (8 files: the harness, the probe file, the recipe line, the driver, the milan_dp README, TESTING,
  GM_LOSS_RECOVERY, CHANGELOG). `docs_check.py`, `check_doc_style.py`, `DOC_MAP.gen.py --check`,
  `measure_test_evidence.py --check` rc 0 on the tree before the commit.
- At `c2c996fa`: lint PASS 89 <= 89; `pp_resource_gate.py check-baseline` "baseline PASS: 3 endpoints".
- 08:13 UTC started at `c2c996fa`, each in its own clean clone: gmstep-mutants (`scripts/round7/campaign.sh`), the
  firmware boundary gate (`scripts/round7b/firmware_gates.sh <clone> <out> boundary`), the docs replica
  (`scripts/round7b/docs_run.sh`). The full sweep follows the two Verilator jobs.
- `ci/image/tool-inventory.json` hashes `gmstep_mutants.py`, but it is already stale at `d835ba12` and on dev (46 of
  378 inputs differ; the image build regenerates it, and it needs the pinned shfmt this host does not have), so it is
  left as dev keeps it.
- 08:37 UTC firmware boundary gate (`ctrl_boundary.py --require-rv32 --selftest`, LiteX interpreter) rc 0, 1,440 s:
  "ctrl_boundary: PASS" (3,193 compiled sources of 3,440 recorded invocations). Receipts `round7/firmware_boundary_c2c996fa/`.
- 08:55 UTC docs replica at `c2c996fa`: 44 steps, 42 rc 0, 2 skipped by rule; leg 1 with LiteX all but gate 11; markdown
  5/5 on 3.12.3; the no-git pair rc 0. Receipts `round7/docs_steps_c2c996fa/`.
- **09:40 UTC gmstep-mutants (`--all`) at `c2c996fa`: exit 0, 23 checks, 23 PASS, 0 FAIL** (both clean legs; 21
  controls; the fixed control caught on its named check, 12 checks broken; the new control caught, 1 check broken).
  The clean leg: 196 checks, 0 failures. Receipts `round7/gmstep_mutants_c2c996fa/`. Campaign audit (R678-3 script):
  gmstep 21/21 recorded; tdm8 20/20, 3/3, 3/3 and the pull-in 19 logs PASS from round 7b (inputs unchanged).
- 09:41 UTC the full sweep (`scripts/round7/sweep.sh <clone> <out> 0 1 2 3`) started alone in its own clean clone.
- Full sweep at `c2c996fa`, 09:40 to 14:38 UTC, nothing else of this lane running beside it: shard 0 15/15 (54,917
  checks, `milan_dp` whole with the notify leg), shard 1 16/16 (331,530), shard 2 16 of 17 (262,031, 0 in-suite failures;
  `capture_coherence` TIMEOUT at the runner's 2,400 s wall clock, result unknown), shard 3 16/16 (1,541,583). 63 of 64
  suites, 2,190,061 checks, 0 failures. Receipts `round7/sweep_c2c996fa/`.
- 14:39 to 15:19 UTC `capture_coherence` again alone (`scripts/round7/cc_rerun.sh`, the runner's invocation on the
  shard's two CPUs, no wall clock): exit 0 in 2,402 s, 20,832 + 447 checks, 0 failures, campaign 35/35, tally verdict 0.
  It needs about the whole 2,400 s budget on two CPUs uncontended, so it times out in this sweep layout every round
  (rounds 1 and 6 too); a hosted runner with more CPUs is the suite's real budget. Receipts
  `round7/capture_coherence_rerun_c2c996fa/`.
- For the manager: `receipts/round7/cc-rerun-c2c996fa/` was not written by this session. It appeared at 13:03-13:12
  UTC from another checkout (`lanes/632-cc` in its log), with a 300 KB log carrying host paths. It is left untouched
  and is not cited here; the index lists it because it is generated from the files present.
- 15:20 UTC receipts collected (host paths stripped, logs over 200 KB by sha256), indexes regenerated (round 7: 499 files); PR-BODY.md Round 7c (status, item 4 row, `#### Round 7c`, validation, the round 7c gate table, DoD); REVIEW READY posted (URL above). Stopped.

## Round 7b (session 13, 2026-10-23 06:33 CEST onward) -- owner accepted the area; re-record, then item 4 in full

**Status: STOP at `d835ba12` (not pushed): gmstep-mutants (`--all`) exits 2, 21 of 22, at the head; dev
`e5b480a3`'s own tree fails the same control the same way (pre-existing, from the fourth pin adoption). Posted
https://github.com/kebag-logic/milan-fpga/issues/632#issuecomment-6360215816 (text: `public-stop-r7b.txt`). Stopped
there, as the STOP condition requires.**
Assignment: the [A10] comment
https://github.com/kebag-logic/milan-fpga/pull/770#issuecomment-6357449062 (owner decision of 2026-10-23 06:32,
option (a): this PR's +500 LUT, +376 FF, +107 slices and +2 RAMB18 on route-1x1 accepted against #771's record; it
extends the block-RAM exception #632 issuecomment-6309313685; Mark II #640 recovers the area). Base `5282b8b6`
(confirmed HEAD; not pushed). Receipts under `receipts/round7/` (this round's directories carry `r7b` or the head;
index regenerated, 306 files).

Items: (1) re-record route-1x1, ooc-1x1, ooc-8x8 with the recipe at the head, citing both exceptions, per-shape
figures, `check` exit 0 against the new record; (2) item 4 of issuecomment-6351804497 at the head: the full sweep,
Yosys, the firmware gate set, the docs gates under make 4.3, lint, the builder bank, tdm8render-mutants (31),
tdm8render-pullin (18 + history), gmstep-mutants (22); (3) PR body and HANDOFF Round 7 section.
STOP if any gate or campaign fails, or if the re-recorded route differs from round 7's in LUT, FF or slices.

Commits on `5282b8b6` (oldest first):

| Commit | Subject |
|---|---|
| `17280d2d` | Re-record route-1x1, ooc-1x1 and ooc-8x8 at the media phase merge under the owner's block-RAM exception and its LUT, FF and slice extension |
| `d835ba12` | Document the eleventh resource record, the media phase alignment on dev e5b480a3 under two owner exceptions, with 15 slices left |

| Item | Outcome |
|---|---|
| 1 re-record | Done. The bank at `5282b8b6` reproduces round 7 in every field (figures, input digests, identity, all sub-block scopes) at all three endpoints, so the route-difference STOP is not met. `record --write` x3, the notes cite both exceptions; `check` exit 0 at all three against the new record; `check-baseline` exit 0 |
| 2 gates | lint, Yosys, the docs gates under make 4.3, the builder bank, the firmware set's seven commands before its boundary gate, tdm8render-mutants 31/31, the pull-in 19/19: all pass at `d835ba12`. **gmstep-mutants exit 2 (21/22): STOP.** Not run after the STOP: the firmware boundary gate (`ctrl_boundary.py`) and the full sweep |
| 3 PR body / HANDOFF | Round 7 section updated with the exception citation, the re-recorded figures, the gate table and the STOP |

### Changes (file:line at `d835ba12`; clause)

| File:line | Change | Clause |
|---|---|---|
| `syn/ooc/pp_resource_baseline.json` (route-1x1 record, `:451` note; ooc-1x1 `:919`; ooc-8x8 `:1377`) | the three records written by `record --write` from this round's bank; the notes name the measured head, the merge, both pins, the preceding record as dev's design, the deltas and both owner decisions | owner decisions #632 issuecomment-6309313685, PR #770 issuecomment-6357449062 |
| `docs/design/AREA_BUDGET.md:13`, `:117-120` | the record line and the re-record history name this record and both exceptions | -- |
| `AREA_BUDGET.md:130-147` | headroom table (51,259 LUT 80.85 %, 13,219 over NFR-RES-01; 53,208 FF; 15,835 slices, 15 free; 87.5 tiles; 13 DSP; +0.236 / +0.028 ns); 15 slices left and the next growth needs its own owner decision; the critical path; the #771 image added to the history | NFR-RES-01 |
| `AREA_BUDGET.md:158-164` | datapath 42,764 LUTs (67.5 %), wrapper 23,776; the wrapper at most 10,557 LUTs, 13,219 to remove (56 %) | NFR-RES-01 |
| `AREA_BUDGET.md:398`, `:438`, `:509-513` | the comparison-record history; at +0.236 ns the +0.030 ns floor binds first after a 0.206 ns fall; the eleventh-record paragraph | -- |
| `docs/design/MARK_II_AREA_PLAN.md:56`, `:660-661` | the gate-comparison row; the record history | -- |
| `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:10-13`, `:20`, `:40-138` | the current-record pointer, the contents entry, the new section (exceptions, endpoint and difference tables, per-block attribution, corners, worst paths, digests, runs) | -- |
| `docs/findings/README.md:25` | the current-record pointer (stale since #708) | -- |
| `CHANGELOG.md:109-111` | three lines: the re-baseline, the growth, 15 slices left | -- |

### New checks

None: this round adds no behaviour and no test. Its probes (`scripts/round7b/gm_stop_probe.py`,
`gm_change_probe.py`) are disposable diagnostics outside the tree.

### Gate table (round 7b)

| Gate | Command | Head | Result | Receipt |
|---|---|---|---|---|
| route-1x1, ooc-1x1, rtl-8x8, ooc-8x8 | `scripts/round7/vivado_bank.sh 5282b8b6 5282b8b6` (recipe, `--single-thread-synthesis`, `--integrated-clock`) | `5282b8b6` | rc 0 x4; 41.9, 12.6, 1.2, 24.7 min; peaks 8,406 / 5,141 / 4,311 / 6,137 MB; against #771's record route exit 1 (SLICE +107, RAMB18 +2), ooc x2 exit 0; every printed record equal to round 7's | `round7/vivado_bank_5282b8b6_r7b/` |
| re-record | `pp_resource_gate.py record <dir> --endpoint <e> --write` x3; `set_notes.py`; `check` x3; `check-baseline`; `--selftest` | tree -> `17280d2d` | rc 0 each; PASS, every delta 0; "baseline PASS: 3 endpoints" | same |
| lint | `python3 scripts/lint_rtl.py --check` | `d835ba12` | PASS 89 <= 89 | `round7/lint_d835ba12/` |
| Yosys | `syn/yosys/run.sh` | `d835ba12` | rc 0, 21.4 min: 60/60 tops, tied-input PASS, tap-purity PASS | `round7/yosys_d835ba12/` |
| docs gates | `scripts/round7b/docs_run.sh` (make 4.3, CPython 3.12.3) | `d835ba12` | 44 steps: 42 rc 0, 2 skipped by rule; leg 1 with LiteX all but gate 11; markdown 5/5 on 3.12.3; no-git pair rc 0 | `round7/docs_steps_d835ba12/` |
| builder bank | `scripts/round7/builder_run.sh` | `d835ba12` | rc 0, all gates but gate 11 (not run) | `round7/builder_bank_d835ba12/` |
| firmware set (seven of eight) | `scripts/round7b/firmware_gates.sh <clone> <out> nb` | `d835ba12` | all rc 0 (above) | `round7/firmware_gates_d835ba12/` |
| firmware boundary gate | `ctrl_boundary.py --require-rv32 --selftest` (LiteX interpreter) | -- | not run: STOP first (it builds Verilator models, so it was queued after the campaigns) | -- |
| tdm8render-mutants | `scripts/round7/campaign.sh tdm8m-d835ba12 ... tdm8render-mutants VERILATOR_JOBS=2` | `d835ba12` | exit 0, 31/31 (113 min) | `round7/tdm8render_mutants_d835ba12/` |
| tdm8render-pullin | `scripts/round7b/pullin_legs.sh` | `d835ba12` | 19/19 exit 0; 18 x 28 checks, history 272; 0 failures | `round7/pullin_d835ba12/` |
| gmstep-mutants | `scripts/round7/campaign.sh gmstep-d835ba12 ... gmstep-mutants VERILATOR_JOBS=2` | `d835ba12` | **exit 2: 22 checks, 21 PASS, 1 FAIL** ("the grandmaster change stops the talker for good": failed, but not the named check) | `round7/gmstep_mutants_d835ba12/` |
| the failing control, probed | `gm_stop_probe.py` at the head and on dev; `gm_change_probe.py` at the head | `d835ba12`, `e5b480a3` | the same 14 failed checks on both; the boot GM sequence 0 -> thisClock -> GM A pulses the detector at acquisition | `round7/gmstep_stop_probe_d835ba12/` |
| campaign audit (R678-3 script) | `scripts/round7/campaign_audit.py` | receipts | tdm8 20/20, 3/3, 3/3; gmstep 19/20 (the failing control); pull-in 19 logs PASS | `round7/campaign_audit_d835ba12/` |
| full sweep | `scripts/round7/sweep.sh` | -- | not run: STOP first | -- |

### The STOP and the options (for the manager)

The control (dev's, `tb/verilator/milan_dp_gm_steps/gmstep_mutants.py:195-203`, since `0e3eef5b`) latches
`gm_stop_r` on the datapath's GM-change detector `gm_recentre_p_r` (`hdl/milan/milan_datapath.sv:7701-7711`) and
names "licence: the talker never pauses beyond four of its intervals". FPGA-gPTP `55680bff` (#82, adopted by #771)
publishes this station's own identity before a peer is elected, so the first peer GM publication is a non-zero to
non-zero change and the detector pulses at acquisition, not only at the leg's GM A -> GM B event. The mutant then stops
the talker before the baseline; 14 checks fail, the named one is never reached. Dev `e5b480a3` fails it identically.
Options: (a) a test-only change in this PR that keeps the control's meaning: the planted stop takes effect at the leg's
grandmaster event after the baseline (for example on the detector's second pulse), so the named pause check is the one
that fails; (b) the same fix on dev in its own Issue first, then a merge of dev here; (c) a ruling that the detector
should not pulse on the boot self-identity -> first peer change (an RTL behaviour change; in this PR its only reader is
`KL_i2s_playback`'s re-centre, on dev it also drives the #387 render re-base). Recommendation: (b) if dev's own
campaign must be green first, else (a); (c) is a behaviour question for the owner. Then the boundary gate, gmstep
and the full sweep at the new head.

Next round (whichever option): `ctrl_boundary.py --require-rv32 --selftest` under the LiteX interpreter
(`scripts/round7b/firmware_gates.sh <clone> <out> boundary`), `gmstep-mutants` and the full sweep
(`scripts/round7/sweep.sh <clone> <out> 0 1 2 3`) at the new head. A test-only or merge change leaves the RTL, so the
resource record, Yosys and the tdm8 campaign stay valid unless the change touches their inputs (state that with a
`git diff --stat` against `d835ba12`). The scratch measurement directory is `r7/viv-5282b8b6/` on the build host.

Progress (kept current):
- 04:35 UTC: HEAD `5282b8b6` confirmed, origin `https://github.com/kebag-logic/milan-fpga.git`; the Vivado bank
  (`scripts/round7/vivado_bank.sh 5282b8b6 5282b8b6`, recipe unchanged, clean clone, one run at a time under the
  exclusive lock) started at MemAvailable 60 GB. `5282b8b6`'s synthesis inputs equal `dc9cda7d`'s (it changes
  `CHANGELOG.md`, the design page and the milan_dp README only).
- 05:17 UTC: route-1x1 rc 0, 41.9 min, Vivado peak 8,406 MB. Gate exit 1 against #771's record, the same lines as
  round 7 (SLICE +107, RAMB18 +2). **Reproduces round 7 exactly**: the printed record's figures, input digest
  (`e67f9619...`), identity and all 51 sub-block scopes equal round 7's `dc9cda7d` candidate record, so the STOP test
  (LUT, FF or slices differ) is not met. `record --write` rc 0; `check` against the new record rc 0 (PASS, every delta
  0). Corners, worst paths and hierarchy rows equal round 7's (`scripts/round7b/route_facts.py`).
- Correction to round 7's wording: dev `e5b480a3` differs from the record's `d664cf54` in comment lines of three files
  (`KL_gptp_shadow.sv`, `KL_pp_shadow.sv`, `milan_datapath.sv`: the AS_PATH count notes), not one block of one file.
  The conclusion (the record measures dev's own design) stands.
- The DSP -1 is `crf_tx`'s (its free-running divider held one: 1 DSP in the pre-#632 reference route, 0 now).
- 05:30 UTC ooc-1x1 rc 0 (12.6 min), 05:31 rtl-8x8 rc 0 (1.2 min), 05:56 ooc-8x8 rc 0 (24.7 min): both `check` exit 0
  against #771's record, every figure equal; each printed record equals round 7's in figures, digest, identity and
  scopes. Bank done, lock released.
- `record --write` for all three (rc 0), the three `measured` notes through `scripts/round7b/set_notes.py` (json
  `indent=1`, the gate's own layout: a load/dump of the old file reproduced it byte for byte), then `check` rc 0 at all
  three against the new record and `check-baseline` rc 0 ("baseline PASS: 3 endpoints"); `--selftest` rc 0.
- Docs (#771's pattern): AREA_BUDGET (record line, history, headroom table, critical path, allocation figures, the
  WNS floor sentence, the eleventh-record paragraph), MARK_II (gate-comparison row, record history), the #234 findings
  page (top, contents, new section with the tables, attribution, corners, paths, digests, run table), findings README
  (current-record pointer, stale since #708), CHANGELOG (three lines). `docs_check.py`, `check_doc_style.py`,
  `DOC_MAP.gen.py --check` rc 0 on the tree; no em dash or non-ASCII in added lines.
- Commits `17280d2d` (the record) and `d835ba12` (the docs). Head **`d835ba12`**.
- 05:57 UTC at `d835ba12`, each in its own clean clone (`scripts/round7b/launch_group1.sh`): tdm8render-mutants and
  gmstep-mutants (the two Verilator builds), the firmware gate set without its boundary gate (C/C++; the boundary
  gate builds Verilator models, so it runs between the campaigns and the sweep), full Yosys, lint. Lint rc 0, PASS
  89 <= 89.
- 05:58 UTC: the pull-in legs (`scripts/round7b/pullin_legs.sh`, own clone at `d835ba12`) on the campaign's clean
  ship binary, copied after both campaign builds with its three runtime files (sha256 of both copies equal,
  `binary_provenance.sha256`); the mutants build in a temporary directory, so the campaign clone's `obj_tdm8r` is the
  clean build. The docs replica (`scripts/round7b/docs_run.sh`: its clone's tsn-c-stack origin set to the
  `.gitmodules` URL first; the no-git pair on a `git archive` export without submodules, as the job checks out) and
  the builder bank (`scripts/round7/builder_run.sh`) started too; neither builds a Verilator model.
- The clean-clone builds were quick (the ship model built in about 2 minutes), so both campaigns were in their mutant
  phases by 06:00 UTC.
- 06:18 UTC Yosys (`syn/yosys/run.sh`, full serial gate) rc 0, 21.4 min: 60 of 60 tops PASS (`milan_datapath`
  1,778,837 cells, `KL_render_queue` 655,590, `KL_pp_shadow` 1,241,733), tied-input gate PASS (29 tied, 2 justified,
  0 unjustified), tap-purity PASS.
- 06:28 UTC builder bank rc 0, 28 min: all gates pass but gate 11 (not run: the Arty calibration tree is not here).
- The cgroup's MemoryCurrent sat at the 12 GB cap during the route: page cache (anon peaked near 7 GB, no OOM event).
  From 06:30 UTC the poll writes `memory.reclaim` whenever MemoryCurrent passes 8 GB (`scripts/round7b/poll.sh`).
- 06:47 UTC docs replica done at `d835ba12` (48 min): 44 steps, 42 rc 0, 2 skipped by rule (gate 42, the no-git
  step's `rm -rf .git`); leg 0 all but gate 1b's `MAKEFLAGS += -e` arm (make 4.3); leg 1 under CI's interpreter 16
  LiteX arms not run, and with the LiteX interpreter all but gate 11; the five markdown gates rc 0 on CPython 3.12.3;
  the no-git `docs_check.py` and `check_feature_status.py` rc 0 on a `git archive` export.
- 07:01 UTC pull-in legs done: 19 of 19 exit 0 (18 phases x 28 checks, history 272), 0 failures, 62.7 min.
- 07:23 UTC firmware set without its boundary gate done, all rc 0: `fw_rv32_selftest` 7 s, `tally_selftest --mutants`
  52 s, `test_ctrl_firmware --require-rv32 --self-test --lwsrp --jobs 4` PASS 3,079 s, shards PASS, `test_ctrl_nvm
  --require-rv32 --self-test --jobs 4` 1,796 s (saved-state store: 435 tests, 109 planted defects reddened),
  `fw_coverage --selftest` 29 of 29, `fw_coverage --check --jobs 4` 234 s.
- **07:27 UTC gmstep-mutants (`--all`) exit 2: 22 checks, 21 PASS, 1 FAIL.** The control "the grandmaster change stops
  the talker for good" fails the leg, but not its named check ("licence: the talker never pauses beyond four of its
  intervals"). **STOP condition met** ("STOP if any gate or campaign fails").
  Diagnosis (receipts `round7/gmstep_stop_probe_d835ba12/`):
  - `scripts/round7b/gm_stop_probe.py` (the driver's own plant/build/run on a disposable copy): 14 checks fail,
    "baseline: the talker streams" among them; the named check is never reached because the talker never sends.
  - The same probe on a clean clone of dev `e5b480a3`: the same 14 checks, the same verdict. **Pre-existing on dev**,
    not this PR's; the control dates from 2026-10-10 (`0e3eef5b`), the cause from the fourth pin adoption.
  - `scripts/round7b/gm_change_probe.py` (a display on the detector's input and pulse, clean leg): the published GM goes
    0 -> `02a1b2fffec3d4e5` (this station's own identity: FPGA-gPTP #82's boot grandmaster, adopted by #771) ->
    `00aaccfffe010203` (GM A, at acquisition). The detector `gm_recentre_p_r` exempts only 0 -> id, so it pulses at
    acquisition; the control's `gm_stop_r` latches there and the talker is stopped before the baseline.
  - Round 6 (`2700584e`, gPTP `e4869fd0`) passed 22/22: the old pin published 0 until the peer GM.
  - In this PR the detector's only reader is `KL_i2s_playback`'s re-centre (the render stage takes none since #632);
    on dev it also feeds the #387 render re-base, so dev's render stage re-bases at acquisition too.
- Per the STOP: the in-flight tdm8render-mutants campaign is let finish (as round 7 let its bank finish); nothing new
  starts: the firmware boundary gate (`ctrl_boundary.py`) and the full sweep are not run.
- 07:50 UTC tdm8render-mutants exit 0, 31/31 (113 min). Campaign audit: tdm8 20/20, 3/3, 3/3; gmstep 19/20; pull-in
  19 logs PASS. Receipts collected, host paths stripped (including the docs receipts' bare home field), the round 7
  index regenerated (306 files, none over 200 KB).
- 07:53 UTC STOP posted (URL above); PR-BODY.md carries the Round 7b part, the STOP status and the gate table.

## Round 7 (session 12, 2026-10-22 23:34 CEST onward) -- merge dev `e5b480a3` (fourth pin adoption), notify passes, resource re-record

**Status: STOP at `5282b8b6` (item 3's condition: route-1x1 slices +107 against #771's record, tolerance +80).
Posted https://github.com/kebag-logic/milan-fpga/issues/632#issuecomment-6353806286 (text: `public-stop-r7.txt`).
Stopped there, as the STOP condition requires.**
Assignment: the [A10] comment
https://github.com/kebag-logic/milan-fpga/pull/770#issuecomment-6351804497. Base `d40e2ee8` (confirmed HEAD and the
pushed PR head); `origin/dev` fetched at `e5b480a3` (confirmed; merge base `e26f1816`, four merges since: #767, #769,
#768, #772). Receipts under `receipts/round7/`.

Commits on `d40e2ee8` (oldest first):

| Commit | Subject |
|---|---|
| `dc9cda7d` | Merge dev e5b480a3, the fourth pin adoption (#771), into the media phase lane |
| `5282b8b6` | State that processor pin 93fb0b2d carries the stored-offset gate, so the SET_STREAM_INFO notify case passes, and give the CRF restart term both lock edges in the test plan |

| Item | Outcome |
|---|---|
| 1 merge | `dc9cda7d`, merge commit; submodules `93fb0b2d` / `55680bff`; 7 files, 12 hunks, resolved below; builder bank exit 0 at the merge (the census rows match the RTL) |
| 2 `[NOTIFY]` | passes at the merge: 461 checks, 0 failures (all eight steps); `gsi_mutants.py` 11/11 (#632 rows 3 of 461 each); "fails at the current pin" statements removed: design page `:1739-1744`, milan_dp README `:696-706`, CHANGELOG `:80`, PR body |
| 3 resource gate | route-1x1 exit 1: SLICE +107 (> 80) and RAMB18 +2 (excepted); LUT +500 (= tolerance, ok), FF +376, DSP -1, WNS +0.236; ooc-1x1 / ooc-8x8 exit 0, every figure equal to the record. **STOP**; nothing re-recorded |
| 4 gates | builder bank (merge), lint 89 <= 89 and the docs workflow's gate steps under make 4.3 (head) run; the full sweep, Yosys, the firmware gate set and the three campaigns not run (STOP first). The merge touched the campaigns' inputs (datapath RTL and both pins: `git diff --stat d40e2ee8 dc9cda7d -- hdl protocol-processor gptp-processor` is non-empty), so all three must be re-run in the next round |

### Changes (file:line at `5282b8b6`; clause)

| File:line | Change | Clause |
|---|---|---|
| merge `dc9cda7d` | the resolution table below | -- |
| `docs/design/MEDIA_CLOCK_FOLLOWING.md:1739-1744` | processor pin `93fb0b2d` carries the gate (processor PR #199, adopted by #771), so all eight steps pass; the readback-gate defect is `gsi_mutants.py`'s | Milan v1.2 5.4.2.9, 5.4.5.2 |
| `docs/design/MEDIA_CLOCK_FOLLOWING.md:2145` | the switch-row control's "as the CRF term is" -> "as the CRF term takes its raw lock edges" (found in the merge: #761 made the CRF term both edges) | IEEE 1722-2016 4.4.4.3 |
| `tb/verilator/milan_dp/README.md:696-706` | measured at processor pin `93fb0b2d`: clean leg 461/461; the #632 rows 3 of 461; the two "until a pin carries the fix" lines removed | -- |
| `CHANGELOG.md:80` | "That gate is the processor's; pin `93fb0b2d` carries it." | -- |

### New checks

None this round: the merge adds no behaviour of this PR's, and the round's checks are re-runs (notify, `gsi_mutants.py`,
the three Vivado endpoints, the builder bank, lint, the docs gates).

### Gate table (round 7)

| Gate | Command | Head | Result | Receipt |
|---|---|---|---|---|
| notify leg | `scripts/round7/notify.sh` (`make ci-prepare build-notify exec-notify`) | `dc9cda7d` | 461 checks, 0 failures, exit 0 | `round7/notify_dc9cda7d/` |
| gsi campaign | `scripts/round7/gsi.sh` (`python3 gsi_mutants.py`, all 11) | `dc9cda7d` | exit 0; 12 PASS (clean + 11 caught) | `round7/gsi_mutants_dc9cda7d/` |
| route-1x1, ooc-1x1, rtl-8x8, ooc-8x8 + gate | `scripts/round7/vivado_bank.sh dc9cda7d dc9cda7d` | `dc9cda7d` | route exit 1 (SLICE, RAMB18), 41.5 min, peak 8,413 MB; ooc-1x1 exit 0, 12.2 min, 5,141 MB; rtl-8x8 1.2 min, 4,315 MB; ooc-8x8 exit 0, 26.1 min, 6,138 MB | `round7/vivado_bank_dc9cda7d/` |
| builder bank | `scripts/round7/builder_run.sh` | `dc9cda7d` | exit 0, all but gate 11 (not run) | `round7/builder_bank_dc9cda7d/` |
| lint | `python3 scripts/lint_rtl.py --check` | `5282b8b6` | 89 <= 89 | `round7/lint_5282b8b6/` |
| docs workflow gate steps | `scripts/round7/docs_steps.py` (make 4.3, CPython 3.12.3); `docs_steps_md312.py` (the markdown gates on 3.12.3); the no-git pair on a `git archive` export | `5282b8b6` | 44 steps: 40 rc 0 at once; the two builder legs first refused on the scratch clone's tsn-c-stack origin (a lane path; `scripts/ci_case_receipts.py` requires the GitHub URL), then rc 0 after `remote set-url` in the clone: leg 0 all but gate 1b's `MAKEFLAGS += -e` arm (make 4.3 cannot express it), leg 1 with the LiteX interpreter all but gate 11; markdown gates 5/5 on 3.12.3; no-git `docs_check.py` and `check_feature_status.py` rc 0; gate 42 and the no-git step skipped by rule | `round7/docs_steps_5282b8b6/` |
| full sweep, Yosys, firmware gate set, tdm8render-mutants, tdm8render-pullin, gmstep-mutants | -- | -- | not run: STOP first | -- |

Progress (kept current):
- 23:34 CEST: HEAD `d40e2ee8`, origin `https://github.com/kebag-logic/milan-fpga.git`, dev `e5b480a3` confirmed.
- 23:40 CEST: `git merge --no-ff --no-commit origin/dev`: the seven predicted files conflict (12 hunks, resolved below);
  committed as `dc9cda7d` ("Merge dev e5b480a3, the fourth pin adoption (#771), into the media phase lane"), parents
  `d40e2ee8` and `e5b480a3`. `git submodule update --init --recursive`: protocol-processor `93fb0b2d`, gptp-processor
  `55680bff` (each `rev-parse --show-toplevel` its own directory, origins the processor and FPGA-gPTP repositories,
  status clean); it also initialised `external` at its gitlink `efeb541a`.
- 23:42 CEST (21:42 UTC): the Vivado bank (`scripts/round7/vivado_bank.sh dc9cda7d dc9cda7d`) started in a clean clone:
  route-1x1, then ooc-1x1, rtl-8x8 and ooc-8x8, one Vivado run at a time under the exclusive lock, MemAvailable 60 GB.
- The lane's local `dev` branch moved to `e5b480a3` (a local ref only) so the docs replica's em-dash gate, which fetches
  `dev` from the clone's origin, judges this PR's added lines against the live dev tip.

- 00:24 CEST (22:24 UTC): route-1x1 done, rc 0, 41.5 min, Vivado peak 8,413 MB. Gate exit 1: SLICE +107 (tolerance
  +80) and RAMB18 +2 (excepted). **STOP condition of item 3 hit** (the slice delta exceeds its tolerance). The record
  is not re-written. The bank continues to ooc-1x1 and ooc-8x8 so the report carries all three endpoints.
- 00:28 CEST: the notify leg at the merge (`scripts/round7/notify.sh`, clean clone at `dc9cda7d`, processor
  `93fb0b2d`): 461 checks, 0 failures, exit 0; all eight SET_STREAM_INFO steps `[ok]`. `gsi_mutants.py` (all 11)
  started on that clean build; the builder bank started at the merge in its own clean clone.
- 00:36 CEST: ooc-1x1 done, rc 0: identical to the record (exit 0, 23,828 LUT / 20,000 FF, 16/3 RAM, 8 DSP).
- 00:37 CEST: rtl-8x8 rc 0 (1.2 min); 01:03 CEST ooc-8x8 rc 0, identical to the record (exit 0). Bank done; the lock
  released. gsi campaign exit 0 (12 PASS); builder bank exit 0.
- 01:05 CEST: `5282b8b6` (item 2's docs); lint 89 <= 89; the docs replica at `5282b8b6` (results in the gate table).
- 01:39 CEST: receipts collected (`receipts/round7/`), host paths stripped; the STOP posted (URL above). The PR body
  (`PR-BODY.md`) carries the Round 7 section, the STOP status and every "fails at the current pin" statement removed.

### Next round (for the manager)

- Under option (a): re-record the three endpoints with `pp_resource_gate.py record <dir> --endpoint <e> --write` from
  this round's measurement directories (inputs reproduce at any head whose RTL equals `dc9cda7d`'s), cite the slice
  exception and #632 issuecomment-6309313685 in the records' notes and in AREA_BUDGET / the #234 findings page /
  MARK_II_AREA_PLAN (the #771 pattern), `check-baseline`; then item 4 in full: the sweep (four shards), Yosys, the
  firmware gate set, and the three campaigns (their inputs changed at the merge).
- Under option (b): any RTL trim re-runs the Vivado bank, the media_phase campaign (the servo's terms) or the
  `media_phase ofs` cases and `milan_dp` notify/nxn (the rounder), then the same item 4.
- The scratch measurement directories are `r7/viv-dc9cda7d/` (route, ooc-1x1, rtl-8x8, ooc-8x8) on the build host.

### Resources (item 3): route-1x1 against #771's record, the STOP

`pp_resource_gate.py check` against `syn/ooc/pp_resource_baseline.json` as dev `e5b480a3` carries it (#771's record,
measured at `8de4b80b`/`d664cf54`). dev `e5b480a3`'s synthesis inputs differ from `d664cf54`'s by one comment block
in `milan_datapath.sv` (the AS_PATH count note), so the record is dev's own route and these deltas are this PR's share
on the current dev.

| Figure | Record (#771) | Merge `dc9cda7d` | Delta | Tolerance | Verdict |
|---|---:|---:|---:|---:|---|
| LUT | 50,759 | 51,259 | +500 | 500 | ok (at the tolerance) |
| FF | 52,832 | 53,208 | +376 | 600 | ok |
| SLICE | 15,728 | 15,835 | **+107** | 80 | **REGRESSION**; 15 of 15,850 left |
| RAMB36 / RAMB18 | 74 / 25 | 74 / 27 | 0 / +2 | 0 / 0 | RAMB18 REGRESSION, excepted (owner, #632 issuecomment-6309313685) |
| DSP | 14 | 13 | -1 | 0 | ok, below |
| WNS / WHS | +0.291 / +0.036 | +0.236 / +0.028 | -0.055 / -0.008 | 0.25 | ok; route complete, no unrouted net |

Logic LUTs 46,857 -> 47,483 (+626), LUTRAM 3,898 -> 3,772 (-126); BRAM tiles 86.5 -> 87.5. Worst setup path: the
SoC's `milansoc_write_w_buffer_level0_reg[0]` -> `storage_13_dat1_reg[6]`, 10 ns clock, 13 levels, 9.471 ns (7.717 ns
routing), outside the datapath.

Per instance, post-place, against the record's own route report (the #771 lane's `m1` run, 50,759 LUTs; LUT / FF):
`milan_datapath` +516 / +379, of which `g_mmcm_servo.mmcm_servo` +380 / +200 (the phase loop; `u_tick_cdc` +59 of
it), `g_pres_crf.pres_round` +130 / +159 (new: the CRF row's Equation (14) rounder), `render_queue` +345 / +170 against
the retired `render_setpoint` -381 / -137 (net -36 / +33), `crf_tx` -59 / -141 (its free-running divider retired),
`media_domain_event` +6 / +79, `chan_map_capture` -19 / +64, `crf_rx` 0 / +33, `aaf_rx_depkt` -5 / +20; blocks this
PR does not change move by up to about 100 (`csr` +102, `ts_counter` +76, `g_gptp_plane.u_gptp_shadow` -79,
`aaf_latency_tap_bank` -58, `chan_map_render` +32). Outside the datapath: top -66, `KL_gptp_gmii_launch` +25, the CPU
+41.

Why round 6 read +72 slices and -26 LUTs: it compared with #708's record (49,613 LUTs at `435af429`), which was not
dev's own route at this lane's base `e26f1816` (dev's changes between them merged within tolerance without
re-recording). Against dev's own route the PR's share is about 500 LUTs larger than that comparison showed.

### Merge resolution (`dc9cda7d`; every conflicted hunk)

Seven files conflicted, as the assignment named; 22 files changed on both sides, the other 15 merged clean and were
read too (below). Each hunk was resolved from the three versions (diff3), never one side wholesale.

| File | Hunk | Ours (`d40e2ee8`) | Theirs (dev `e5b480a3`) | Resolution |
|---|---|---|---|---|
| `CHANGELOG.md` | Contents | adds the "media clock phase" entry | adds the "pins 93fb0b2d and 55680bff" entry | both, this PR's first (it lands after #771) |
| `CHANGELOG.md` | sections | adds `## Unreleased - media clock phase` | adds `## Unreleased - pins 93fb0b2d and 55680bff` (#771) | both sections whole, this PR's first |
| `docs/design/MEDIA_CLOCK_FOLLOWING.md` | test-plan rows (switch, loss) | switch row: "never more than one #645 settle recentre per switch (until #632: one #386 recentre)"; loss row unchanged | switch row unchanged; loss row: "none on the AAF return, one on the CRF return (#761)" and the per-edge control | ours for the switch row, theirs for the loss row |
| `docs/integration/BAREMETAL_FIRMWARE.md` | PHC-net census rows | `cfg_ptp_cmd_load` 4 / `eff_ptp_adjust_w` 2 (#632 retired the re-base reader); the `KL_render_queue` `flush_i` pin; the old `mcr_restart_p_w` row | the #387 rows (5/3, `media_rebase_p_w`, `render_recentre_p_w`) and the #761 `mcr_restart_p_w` row (`tkd_crflk_q_r ^ crf_locked_w`, both AAF terms, "Either edge ... (#761)") | ours' first two rows (the retired readers stay retired), theirs' `mcr_restart_p_w` row |
| `docs/reference/MILAN_COMPLIANCE_MATRIX.md` | 4.4.4.3 and 4.4.4.5/.9 rows | 4.4.4.3 ends "the render queue takes no re-base since #632"; 4.4.4.5 states the presentation at the pins | 4.4.4.3 gains "Since #761 the selected CRF's return ... with a mutant per edge"; 4.4.4.5 unchanged | ours with theirs' #761 sentence inserted; ours for 4.4.4.5 |
| `docs/testing/TESTING.md` | campaign rows (#658, gmstep, media phase) | gmstep row (the render queue, its flush, the five controls); the new #632/#764 media phase row; #658 row unchanged | #658 row becomes "#658 power-on audio maps and #637 map records, the 63 planted controls ... `DYNMAP_MUTANT_JOBS=4`"; gmstep row unchanged | theirs' #658/#637 row, ours' gmstep row, ours' media phase row |
| `docs/testing/TESTING.md` | suite rows (`milan_dp_mclk`, `tdm8render`) | `milan_dp_mclk` unchanged; `tdm8render` row rewritten for the presentation law | `milan_dp_mclk` "eighteen named mutants ... either edge of the selected CRF's lock dropped from the restart request (#761)"; `tdm8render` unchanged | theirs' `milan_dp_mclk` row, ours' `tdm8render` row |
| `sw/builder/test_builder.py` | gate 1b's printed fact list | "admits no media reader of adjtime or settime: the render presentation stage is emptied by a bind wipe alone ... restart takes only selected CRF disruption and" | "admits media_rebase_p_w ... restart takes only selected CRF lock edges and" | ours' census sentence with theirs' "selected CRF lock edges" (the #761 wording, which the clean-merged `direct_initializer` message and mutant row at `:11379`, `:15935` also carry) |
| `tb/verilator/milan_dp_mclk/README.md` | leg B row | "never more than one #645 settle recentre per switch; each switch kind over 0.8 s gaps" | "its lock loss and return, each one request and one `mr` toggle per output (#761)" | both: theirs' #761 clause after "lock loss and return", ours' settle-recentre and 0.8 s wording |

Clean-merged files changed on both sides, read for meaning: `hdl/milan/milan_datapath.sv` (dev's
`mcr_restart_p_w` = `(crf_clk_selected_r & ((tkd_crflk_q_r ^ crf_locked_w) | crf_mr_toggle_p_w)) | aafm_disrupt_p_w |
aafm_mr_toggle_p_w`, the lane's banner beside it; no retired net is referenced anywhere outside docs and the stale CI
image inventory), `hdl/ieee1722/crf/KL_crf_rx.sv` (dev's #765 subtype move into `w_fmt_ok` and #762 timeout count;
the lane's `ts_p_o` stays on `w_acc_run_w`, which still requires `w_fmt_ok`), `tb/verilator/milan_dp/Makefile` (dev's
maprec8/maprec4 legs build from the lane's source list, `RQ_SRC` included), `sim_nxn.cpp`, `sim_main.cpp`,
`stream_counters.hpp`, the milan_dp README, `gmstep_mutants.py` (dev's two `^` anchors; the lane's controls),
`sim_mclk.cpp`/`mclk_mutants.py` (dev's crfloss mode and mutants 17/18 on the merged RTL line),
`scripts/measure_test_evidence_readers.py` (union of both dispositions), REGISTER_MAP, README, GM_LOSS_RECOVERY,
TIME_SYNC, MARK_II_AREA_PLAN. Anchor checks at the merge: all 63 `dynmap_mutants.py` patterns and all
`gsi_mutants.py` patterns (datapath, processor top and the microcode generator at `93fb0b2d`, mutant 9's
`READ_ST ... SEL_PTOFF` anchor included) occur exactly once (`scratch r7/anchor_check.py`).

## Round 6 (session 11, 2026-10-22 15:02 CEST onward) -- per-event late rule, full campaigns, retired render law out of the pages

**Status: REVIEW READY at `d40e2ee8`, posted https://github.com/kebag-logic/milan-fpga/issues/632#issuecomment-6351779402 (text: `public-review-ready-r6.txt`; gate table below). Stopped there, as assigned.** Assignment: the [A10] comment
https://github.com/kebag-logic/milan-fpga/pull/770#issuecomment-6341411985 answering R677-3
(issuecomment-6341403630) and R678-3 (issuecomment-6339307135). Base `ee5ece60` (confirmed HEAD). Receipts under
`receipts/round6/`.

Commits on `ee5ece60` (oldest first):

| Commit | Subject |
|---|---|
| `f98d00dd` | Judge every event of a PDU stamped behind the latest domain event on its own frame, presenting the ones still ahead and refusing only the ones past |
| `05e32929` | Grade PDUs stamped behind the latest event on both queue shapes, to the late reach and past it, with the whole-PDU refusal and the short reach planted |
| `1d61e5c4` | Grade a map write in a closed epoch on two streams, where the other stream keeps the crossbar live, and plant the ungated commit there |
| `2362f1db` | State the per-event late rule and the late reach, retire the render re-base from the time and recovery pages, and correct the queue's figures and campaign counts |
| `0ffcd7f0` | Name the former offset bindings by behaviour in three test comments |
| `2700584e` | Keep the arrival-placed and untimed-read controls placing what they did, through the late reach's bias |
| `d40e2ee8` | Say a refused PDU's other events are presented, outside the supported range too |

| Item | Outcome |
|---|---|
| 1 R677-3-F1 per-event late rule | RTL `f98d00dd`: the divider takes d + LATE x Ps (LATE 504 frames from MAX_EV_P 504, the depacketizer FIFO's longest PDU); per-event judgement for every d from 504 frames behind; beyond, late in every event (exact). Six texts + model agree. `[behind]` on both shapes; whole-PDU drop planted on both shapes, killed; also the short reach and the double-counted refusal. Area: route +4 slices vs round 5 (8 left of 80; the fix used 4 of 12) -- no STOP |
| 2 R678-3-F3 / R677-3-F3 campaigns | tdm8render-mutants 31/31 (exit 0), pull-in 18 phases + history all pass, gmstep-mutants 22/22 (exit 0), follow_ring 16/16, render_mutants 6/6, CSR controls; audit 20/20, 3/3, 3/3, 20/20. T26: two-stream form in the multi leg; `ungated commit` killed by it. PR body's local-bar line backed by these receipts |
| 3 R678-3-F1 retired render law | TIME_SYNC (step policy bullet; `tu`/holdover vs queue accounting; pending-decision passage replaced), GM_LOSS_RECOVERY (actual controls; 20-control inventory; table row), MEDIA_CLOCK_FOLLOWING (bind measurement marked pre-#632), compliance 4.4.4.3 |
| 4 R678-3-F2 / R677-3-F2 figures | OOC figures re-measured this round with provenance (531/236, 883/402; round 4's 553/228, 890/387 named); 26 queue defects (design page, TESTING, evidence reader); follow_ring sixteen (TESTING x2); "once an event lies past the queue"; CHANGELOG media_phase forty |
| 5 R678-3-R1 residue | `0ffcd7f0`, R678-3's exact wording for all three |

Progress (kept current):
- `f98d00dd` RTL: the divider takes d + LATE_C x Ps (LATE_C = 504 frames, 10.5 ms, from `MAX_EV_P` = 504, the longest PDU
  the depacketizer's 2048-byte FIFO passes); F0 taken LATE_C lower; frame numbers 10 bits, quotient 10 bits (13 cycles
  < PAY_LEAD 16). A PDU stamped behind the latest event is judged per event; one more than the reach behind is late in
  every event (exact: its last event is at or before n <= R). The datapath binds `MAX_EV_P` from the FIFO depth.
  OOC (scratch, before commit): 1x1 531 LUT / 236 FF (was 553/228), 8x8 883/402 (was 890/387), RAM unchanged.
- `05e32929` render_queue: `[behind]` phase (the probe's three PDUs; 250 and 500 frames behind with their tails ahead;
  a 504-event PDU late, presented and early at once; at the reach; past it), refusal counts declared per PDU (S3),
  refused_o once per PDU with both, the `[wrap]` self-check (the phase moved past the 2^32 crossing: kWrapAt 3200), a
  504-event early PDU in `[long]` (keeps the hold control live at 10-bit frame numbers); 4 new mutants (whole-PDU drop x2
  shapes, short reach, double-counted refusal). 39/0, 38/0, 28/28.
- `1d61e5c4` milan_dp_render: two-stream T26 in the multi leg (stream 1's loss holds the epoch closed, stream 0 live, a
  map write re-seeds slot 0): clean 79/0; `ungated commit` re-pointed there: killed by T26 (833 nonzero slots).
- `2362f1db` docs; `0ffcd7f0` residue; `2700584e` media_phase `render_read_untimed` and milan_dp `render_mutants` patterns
  kept meaning through the bias.
- Probe (reviewer's patch on `ee5ece60`: 32/20 mismatched beats; same PDUs on `0ffcd7f0`: 0/0, 41 and 40 checks pass).
- media_phase render 13/0 + 5 controls killed at `2700584e`.
- route-1x1 started 13:37 UTC at `0ffcd7f0` (RTL = `2700584e`).
- route-1x1 done 14:13 UTC: LUT 49,587 (-26 vs record; -335 vs round 5), FF 52,742 (+389; +46), SLICE 15,797 (+72; +4,
  8 left), RAMB18 27 (+2 budgeted, the gate's only REGRESSION line, exit 1), DSP 13, WNS 0.163, WHS 0.017, complete.
  Per-instance: stage +272 LUT at synthesis, csr -424 (unchanged RTL): cross-hierarchy attribution; datapath at synth
  -42 LUT/+48 FF vs round 5. Stage alone, clocked OOC (20 ns, AreaOptimized_high), old 538/228 vs new 527/236.
  Receipts `round6/route_1x1_0ffcd7f0/`, `ooc_2700584e/`, `ooc_clocked_old_new/`.
- Yosys changed tops at `2700584e`: queue 655,590 cells, depacketizer 60,880, datapath 1,770,851; PASS, tied-input,
  tap-purity (`round6/yosys_changed_tops_2700584e/`). Docs gates 49/49 at `2700584e` (scratch `docs_2700584e`).
- 14:14 UTC campaigns started in their own clean clones at `2700584e` (`scripts/round6/campaign.sh`):
  `tdm8render-mutants`, `gmstep-mutants`. 14:46 UTC the 19 pull-in legs (`scripts/round6/pullin_legs.sh`: the
  Makefile's recipe, 4 at a time) on the clean ship binary the tdm8 campaign's `tdm8render-build` made at the head,
  copied (sha256 recorded), so no third Verilator build runs.

### Changes (file:line at `2700584e`; clause)

| File:line | Change | Clause |
|---|---|---|
| `hdl/ieee1722/aaf/KL_render_queue.sv:188` | `MAX_EV_P` (504): the longest PDU walked | -- |
| `KL_render_queue.sv:295-316` | `LATE_C` = 3 x ceil((MAX_EV_P - 1) / 3) = 504 frames; `BIAS_L` = LATE_C x Ps (10,500,000 ns, whole ns); QW_C over LATE_C + QMAX_C (10 bits); `DMAX_C`/`FW_C` (10 bits) hold the walk's differences from -(LATE_C + K + 2) to QMAX_C + 9; `g_chk_wrap` on DMAX_C; `g_chk_max_ev` `:359` | IEEE 1722-2016 4.4.4.9, 7.5 |
| `KL_render_queue.sv:445-446` | `db_w` = ts - E_n + LATE_C x Ps (32-bit wrap; window [-2^31 - reach, 2^31 - reach)); late-whole only when db < 0 (past the reach) | 4.4.4.9 |
| `KL_render_queue.sv:788` | the header's frame `n_now - LATE_C`; F0 = n - LATE_C + round(N / Ps) | 7.5 |
| `KL_render_queue.sv:30-45`, `:75-96`, `:247`, `:917-919` | banner (signed d, the reach; the rules per event; refused once per PDU with either, a long PDU can have both); `refused_o` port note; counter comment | -- |
| `hdl/milan/milan_datapath.sv:6550-6560` | `DPKT_FIFO_BYTES_C` (2048, bound to the depacketizer), `RENDER_MAX_EV_C` = 2 x ceil((2048 - 38) / 8) = 504 | -- |
| `milan_datapath.sv:6940-6952`, `:7009` | the stage comment states the per-event rule and the counts (R677-3-F1); `.MAX_EV_P` | -- |
| `tb/verilator/render_queue/sim_main.cpp:343`, `:366` | model reads the difference in the stage's window; refused once per PDU with either | -- |
| `sim_main.cpp:484` | `[behind]` phase (7 PDUs) | -- |
| `sim_main.cpp:307`, `:64`, `:564` | declared refusal counts (S3); `kWrapAt` 3200 and the `[wrap]` self-check | -- |
| `tb/verilator/render_queue/mutants.py` | 4 new controls; the 31-bit and refused patterns re-pointed | -- |
| `tb/verilator/milan_dp_render/sim_tdm8_render.cpp:3946` | two-stream T26 in the multi leg's M5; ship T26 comment states why it is kept | -- |
| `tb/verilator/milan_dp_render/tdm8_render_mutants.py` | `ungated commit` on the multi leg, named check the two-stream T26 | -- |
| `tb/verilator/media_phase/phase_mutants.py`, `tb/verilator/milan_dp/render_mutants.py` | `render_read_untimed` (+LATE_C), `each PDU placed by its arrival` (+BIAS_L): same placement as before | -- |
| docs | MEDIA_CLOCK_FOLLOWING (law: signed d and the reach, 13 cycles; rule table per event; the FIFO bound; OOC figures with provenance; proof table 26; bind measurement marked pre-#632); TIME_SYNC (step policy, `tu`/holdover vs queue accounting, the listener rows, the pending-decision passage replaced); GM_LOSS_RECOVERY (actual controls, 20-control inventory, table row); REGISTER_MAP `RENDER_STAT[31:16]`; compliance matrix 4.4.4.3; TESTING (follow_ring 16, render_queue 26, the row); CHANGELOG (rules, forty); `scripts/measure_test_evidence_readers.py` (twenty-six) | -- |

### New checks (planted defect -> failing words)

| Suite | Defect | Named check that fails |
|---|---|---|
| `render_queue` (both shapes) | a PDU stamped behind the latest event refused whole (the former rule) | `[behind] every event presented to every interface is the frame the law names` |
| `render_queue` | the late reach short of the longest PDU (LATE_C halved) | same |
| `render_queue` | a PDU with both a late and a too-early event counted twice in refused_o | `[refused] PDUs with a late or too-early event counted once each in refused_o` |
| `render_queue` (harness guard) | the `[wrap]` phase starting after the 2^32 crossing | `[wrap] the phase starts before its frame instants cross 2^32 ns, so its PDUs straddle the wrap` |
| `milan_dp_render` multi | `ungated commit: a closed epoch admits frames anyway` | `T26 MAP WRITE IN A CLOSED EPOCH: the re-seeded crossbar value never reaches a slot, though the other rendered stream still feeds it` (833 nonzero slots) |

### Design notes

- Why a bias and not a signed divider: d + LATE x Ps keeps the unsigned long division as it was (one quotient bit per
  cycle), with the bias whole ns because LATE is a multiple of three (Ps = 62,500/3 ns). The header's frame register
  starts LATE lower, so the final add is unchanged. The late-whole test is the biased sum's sign.
- Why 504: exactness needs LATE >= MAX_EV - 1 (a PDU further behind than LATE has its last event at or before n <= R).
  MAX_EV is the depacketizer's bound: `DROP_OVERSIZE_FRAME` on a 2048-byte frame FIFO, 38 header bytes, so at most
  ceil(2010/8) = 252 payload beats, 504 one-channel samples (the walk counts a zero-padded tail sample as one).
- Frame numbers: FW = clog2(DMAX + 1) + 1 = 10 bits (DMAX = LATE + K_max + 2 = 508 at 1x1); quotient 10 bits; the
  frame is known QW + 3 = 13 cycles after the header (PAY_LEAD 16).
- The half-wrap window moves by the reach: d in [-2^31 - 10.5 ms, 2^31 - 10.5 ms); a timestamp 2.137-2.147 s ahead
  counts late instead of early (refused either way). Documented (banner, design page, PR limitation); keeping the
  split at 2^31 would cost a second 32-bit compare.
- `refused_o` counts once per PDU with a late or an early event: only a PDU longer than the queue can have both
  (the [behind] 504-event PDU at -200 does; it counts once in each of late_o, early_o, refused_o). The counter comment
  "never both" was wrong for long PDUs before this round too; corrected and graded.
- The `[wrap]` phase had silently stopped straddling 2^32 when the refusal phases grew (the 31-bit control survived);
  kWrapAt moved to 3200 and the phase now checks it starts before the crossing.
- `[long]` gains a 504-event PDU starting 10 events inside the queue: with 10-bit frame numbers the 300-event PDU no
  longer passes half the wrap, so the past-the-queue hold control needed a PDU that does.
- T26: since #632 a bind fall flushes the stage for its stream (`flush_i` = bind fall) and a reset empties it, so on
  the one-stream shape a closed epoch always coincides with a silent queue for the rendered stream; only a second
  rendered stream keeps the crossbar live while the epoch is closed (freshness waits for the lost stream). Chosen over
  renaming the check: the reviewer's own suggestion (a non-zero value reaching the crossbar while closed).
- Area: the in-context per-instance numbers swap between the stage and the CSR block between routes (synthesis: stage
  +272, csr -424 with csr unchanged); the datapath total at synthesis moves -42 LUT/+48 FF, and the stage alone (same
  script, both RTLs, clocked) -11 LUT/+8 FF. The gate's totals: LUT -26, FF +389, SLICE +72 vs record.
- The pull-in legs ran on the tdm8 campaign's clean ship binary (same head, same recipe, sha256 recorded) to keep to two
  concurrent Verilator builds; the Makefile target would have rebuilt it first.
- `ps` output in this environment is filtered by a command proxy: monitor through the cgroup's `cgroup.procs`
  (`$VALIDATION_STORAGE/scratch/632-a659/r6/procs.sh`). An apparent loss of the campaign processes at 14:53 UTC was that.

### Gate table (round 6)

| Gate | Command | Head | Result | Receipt |
|---|---|---|---|---|
| full sweep | `scripts/round6/sweep.sh <clone> <out> 0 1 2 3` | `d40e2ee8` | Shard 0: 14 of 15, 47,447 checks, `milan_dp` failing only the notify leg's CRF-output steps 3 and 4 at the current pin (three checks; its pool ran base, notify, crflic, dynmap, nxn and nxndv, all others 0 failures, then started no later leg, so every leg is also run on its own, below). Shard 1: 16/16, 331,526 checks (`render_queue` 39/0, 38/0, 28 of 28; `media_phase`, `follow_ring`, `milan_dp_mclk`). Shard 2: 16 of 17 passed, 262,027 checks, 0 in-suite failures; `capture_coherence` was stopped by the runner's 2,400 s wall clock mid-campaign (exit 92, result unknown: the host was loaded by other work), so it was run again uncontended, the suite's own target as the runner invokes it on the same two CPUs: exit 0 in 2,312 s, 20,832 and 447 checks, 0 failures, its campaign 35 of 35, the runner's tally verdict clean. Shard 3: 16/16, 1,540,273 checks (`milan_dp_render`: ship 263, multi 79, leg defects 5 of 5). 18:26 to 22:52 CEST | `sweep_d40e2ee8/` |
| tdm8render-mutants | `scripts/round6/campaign.sh tdm8m ... tdm8render-mutants` | `2700584e` | exit 0, 31/31 (16:14-17:49 CEST) | `tdm8render_mutants_2700584e/` |
| tdm8render-pullin | `scripts/round6/pullin_legs.sh` (the Makefile recipe on the campaign's clean binary) | `2700584e` | 19 legs exit 0; 18 x 28 checks, history 272; 0 failures | `pullin_2700584e/` |
| gmstep-mutants | `campaign.sh gmstep ... gmstep-mutants` | `2700584e` | exit 0, 22/22 | `gmstep_mutants_2700584e/` |
| campaign audit (R678-3 script) | `scripts/round6/campaign_audit_r6.py` | receipts | 20/20, 3/3, 3/3, 20/20, 19 pull-in logs PASS | `campaign_audit/` |
| follow_ring mutants | `campaign.sh frmut ... mutants SWEEP_JOBS=1` | `d40e2ee8` | exit 0, 16/16 | `follow_ring_mutants_d40e2ee8/` |
| milan_dp legs, render controls, notify | `scripts/round6/dplegs.sh` | `d40e2ee8` | 11 legs 0 failures; render_mutants 6/6; CSR controls exit 0; notify 459/3 (CRF 3/4, ruled) | `milan_dp_legs_d40e2ee8/` |
| render_queue | `make -C tb/verilator/render_queue` | `0ffcd7f0` | 39/0, 38/0, 28/28 | `render_queue_0ffcd7f0/` |
| reviewer's F1 probe | patch on `ee5ece60`; `probe_r6.py` on `0ffcd7f0` | both | 32/20 mismatched; 0/0 | `f1_probe/` |
| media_phase render + 5 controls | `make render`; `phase_mutants.py --only <5>` | `2700584e` | 13/0; 6/6 | `media_phase_render_2700584e/` |
| T26 multi clean (head) | the campaign's clean multi binary | `2700584e` | 79/0; 120 pops, 0 nonzero | `tdm8render_multi_clean_2700584e/` |
| route-1x1 | `scripts/round6/route.sh` + gate | `0ffcd7f0` | above; exit 1 on RAMB18 alone | `route_1x1_0ffcd7f0/` |
| OOC stage | `run_ooc.sh` | `2700584e` | 531/236, 883/402, no LUTRAM | `ooc_2700584e/` |
| OOC clocked old/new | `ooc_clocked_old_new/run.sh` | `ee5ece60` vs `2700584e` | 538/228 vs 527/236 | `ooc_clocked_old_new/` |
| Yosys changed tops | `syn/yosys/run.sh --top KL_render_queue --top KL_aaf_rx_depacketizer --top milan_datapath` | `2700584e` | PASS 655,590 / 60,880 / 1,770,851 | `yosys_changed_tops_2700584e/` |
| lint | `python3 scripts/lint_rtl.py --check` | `d40e2ee8` | 89 <= 89 | `lint_d40e2ee8/` |
| docs gates (49) | `scripts/docs_gates.sh` | `d40e2ee8` | 49/49 | `docs_gates_d40e2ee8/` |
| builder bank | `scripts/round6/builder_run.sh` | `d40e2ee8` | exit 0, all but gate 11 (not run) | `builder_bank_d40e2ee8/` |
| capture_coherence re-run (the sweep's wall clock stopped it under host load) | `scripts/round6/cc_rerun.sh` (`make -C tb/verilator/capture_coherence` on the sweep's 2 CPUs, no wall clock; `suite_tally.py --verdict`) | `d40e2ee8` | exit 0, 2,312 s, 20,832 + 447 checks, 0 failures, campaign 35/35 | `capture_coherence_rerun_d40e2ee8/` |

## Round 5 (session 10, 2026-10-22 05:07 CEST onward) -- AAF talkers apply the offset as set; only CRF rounds

**Status: REVIEW READY at `ee5ece60`, posted https://github.com/kebag-logic/milan-fpga/issues/632#issuecomment-6338815326 (text: `public-review-ready-r5.txt`; gate table below). Stopped there, as assigned.** Assignment: the [A10] ruling
https://github.com/kebag-logic/milan-fpga/pull/770#issuecomment-6320617745 (AAF talkers apply the presentation time
offset exactly as set; only the CRF output keeps IEEE 1722-2016 10.7 Eq. (14)), with the owner decision
https://github.com/kebag-logic/milan-fpga/pull/770#issuecomment-6320453361 (render queue sized for the 2 ms default;
state the supported range). Base `2389506a` (confirmed: HEAD and the pushed PR head; dev at `d77a8afd`, not merged,
no rebase). Receipts under `receipts/round5/`.

Commits on `2389506a` (oldest first):

| Commit | Subject |
|---|---|
| `133ef20f` | Stamp each AAF talker's presentation offset as set and read it back so, the Equation 14 rounder serving the CRF output's row alone |
| `ac3bb11a` | Grade every AAF timestamp as its frame instant plus its offset as set and the CRF output's by Equation 14 over the ruled offsets, with the AAF rows rounded and read back rounded planted |
| `950bffec` | Give the CRF rounder's tied readback row its reason |
| `5b502a05` | Say the domain's outputs stamp one grid's instants each plus its own offset, the CRF output's alone in whole periods |
| `d5b516f6` | Grade every output's stamp as a domain event's instant plus the offset GET_STREAM_INFO reads, the AAF row as set and the CRF row applied, and the four SET_STREAM_INFO steps on both outputs |
| `ee5ece60` | Document AAF offsets stamped as set and the CRF output's alone rounded, GET_STREAM_INFO's split, and the listener's supported range per shape |

The last RTL change is `5b502a05` (comment-only after `133ef20f`/`950bffec`); route, lint and Yosys are at the RTL
head. The two earlier routes (at `133ef20f`, `950bffec`) were stopped 12 and 4 minutes in, each for a comment fix the
gates asked for; no figure was taken from them.

### Outcome per ruling item

| Ruling item | Outcome |
|---|---|
| AAF talkers' row = the stored value as set | done: `aecp_pres_offset` straight into the packetizer (`milan_datapath.sv:1447`) |
| `KL_mtt_round` serves the CRF output only (remove from AAF or identity mode, whichever costs less, with the area) | removed from the AAF path: one row, the CRF output's (`g_pres_crf`, `:3454`); no instance at a shape without a CRF output. Area below: removal is the cheaper (an identity mode keeps the AAF rows' output registers) |
| GSI word 3: AAF row as set, CRF row as applied; document the 5.4.2.10.2 split | done (`:5005`, `:5258`); MEDIA_CLOCK_FOLLOWING, TIME_SYNC, compliance matrix |
| Re-grade 0, 1, 20,833, 20,834, 62,500, 2,000,000, 2,010,000, 0xFFFFFFFF; AAF = pin instant + offset as set; CRF = Eq. 14 | `media_phase ofs`: eleven cases, every value on AAF rows and on the CRF row (plus 4,294,958,333/4 on CRF), every AAF stamp exact to the ns; on the datapath, nxn legs grade every stamp exact against the domain events |
| Keep the round-3 33-bit carry for CRF | kept; its four planted drops still caught (H case) |
| Four-step notify keeps its expected column; step 4 a plain change | AAF output 0: pushes 0,1,0,1, GET reads each as set (passes even at the pin). The old table moved to the CRF output, where stored and readback differ (see D10) |
| Docs: non-idempotent write-back for CRF only | done |
| Owner: state the supported range exactly; 7.4.77.1 limit | MEDIA_CLOCK_FOLLOWING "The supported range": 31,119 ns to 2,656,119 ns (1x1), 25,942 ns to 2,650,942 ns (8x8) ahead at arrival; offset mapping; too-early rule; talker accepts 0..0x7FFFFFFF; buffer_length 2,126,000 ns declared, backed |
| Route-1x1 again, LUT/FF/slices/timing against the same record; record not edited | done, below |

### D10: the processor-gate control had nothing left to catch on an AAF row (found while re-grading, fixed)

`gsi_mutants.py` mutant 9 (the processor's SET_STREAM_INFO gate comparing with GET_STREAM_INFO's word, the gate
before #632) was caught at the AAF output's step 3. With AAF rows read back as set, the readback IS the stored value
on an AAF output, so that mutant became equivalent there (and the pinned processor passes the AAF steps). The only
output whose readback differs from the stored value is the CRF output, so `[NOTIFY]` now runs the same four steps on
it (the old table, GET reading 2,020,834 then 2,041,667), and mutant 9 names `CRF step 3`. Consequence: at the
processor pin `2cbed0a9` the notify leg fails CRF steps 3 and 4 (3 checks of 459), exactly the round-4 state moved to
the CRF row; with the processor head's E_SINFO spliced, 459/0. Processor PR #199 is MERGED at `51f88c7e`
(checked); milan-fpga dev still pins `2cbed0a9`, so the adoption is still the prerequisite.

### Changes (file:line at `ee5ece60`; clause)

| File:line | Change | Clause |
|---|---|---|
| `hdl/milan/milan_datapath.sv:1447` | AAF talkers stamp `aecp_pres_offset` (as set) | Milan v1.2 5.4.2.9 |
| `milan_datapath.sv:1693-1694` | `pres_crf_ns_w`, `pres_crf_c_w` replace the 16-row applied vectors | -- |
| `milan_datapath.sv:3423-3474` | banner (as set for AAF; Eq. 14 for CRF; the GSI split; write-back CRF only); `g_pres_crf` `KL_mtt_round #(N_P=1)` on row `CRF_TUID_C`, readback row tied 0 with its reason; `g_pres_no_crf` passes the row through | 10.7 Eq. 14, 10.4.13.1; 5.4.2.10.2 |
| `milan_datapath.sv:5003-5005`, `:5250-5260` | `gsi_crf_out_w`; word 3 = CRF row through the rounder's readback, an AAF row from `aecp_pres_offset` | 5.4.2.10.2 |
| `milan_datapath.sv:6399-6401` | `KL_crf_tx` transit from `pres_crf_ns_w`/`pres_crf_c_w` (33 bits) | 10.7, 10.4.13.1 |
| `milan_datapath.sv:1414-1418`, `:6106-6116` | comments: outputs stamp one grid's instants, each plus its own offset | 4.3.5 |
| `hdl/ieee1722/crf/KL_mtt_round.sv:12-70` | banner: the CRF output's row only; not the AAF talkers'; write-back CRF only | 10.7 Eq. 14 |
| `KL_crf_tx.sv:30-35`, `:133-137`, `:410-412`; `KL_media_domain_event.sv:26-31` | comments only | 4.3.5 |
| `sw/litex/milan_soc.py:638` | source-list note | -- |
| docs | MEDIA_CLOCK_FOLLOWING (offset bullets, 10.8/4.3.5 consequence stated, supported range table, 7.4.77.1, proof table), TIME_SYNC rows, compliance 4.3.5/10.8 row, TESTING rows, CHANGELOG, milan_dp README gsi table | -- |

### New checks (planted defect -> failing words)

| Suite | Defect | Named check that fails |
|---|---|---|
| `media_phase ofs` (`phase_mutants.py`) | `aaf_rows_rounded`: round 2's binding, every AAF row through a rounder into the talkers | `[ofs A] every AAF timestamp is a frame instant plus its row as set, to the ns` |
| same | `aaf_readback_rounded`: GET reads the AAF rows rounded | `[ofs A] GET_STREAM_INFO reads every AAF row as set` |
| same | `crf_rounding_bypassed` (re-pointed): the CRF row stamped as set | `[ofs B] every CRF timestamp, all 64 bits, is a frame instant plus the CRF row rounded by Equation 14` (the run's first failure is the readback one) |
| same | `mtt_carry_dropped`, `mtt_reset_carry_dropped`, `readback_saturation_dropped`, `crf_carry_dropped`, `crf_row_raw` (re-pointed to the H/A/B cases) | `[ofs H] the CRF row reads back as applied ... all 33 bits`; `[ofs A] in reset the CRF row reads its factory value ...`; `[ofs H] GET_STREAM_INFO reads the CRF row as applied, 0xFFFFFFFF past 32 bits`; `[ofs H] every CRF timestamp, all 64 bits ...`; `[ofs B] every CRF timing point is a frame instant plus the CRF row as read back` |
| `milan_dp` notify (`gsi_mutants.py` 10, new, dp) | GET reads the CRF output's row as set | `[NOTIFY] SET_STREAM_INFO CRF step 2: GET_STREAM_INFO reads the offset applied, whole periods` |
| same (11, new, dp) | GET reads every output's row rounded (round 4's binding: one rounder over all rows) | `[NOTIFY] SET_STREAM_INFO step 2: GET_STREAM_INFO reads the offset as set` |
| same (9, re-pointed, uc) | the processor gate compares with GET's word | `[NOTIFY] SET_STREAM_INFO CRF step 3: 2,010,000 ns again modifies nothing` |
| `milan_dp` nxn (scratch driver `scripts/round5/nxn_plant.py`, receipts) | the CRF output stamps its row as set | `#632 every CRF timestamp, all 64 bits, is a domain media event's instant plus its offset applied` |
| same | the AAF talkers stamp their rows rounded | `#632 every AAF timestamp is a domain media event's instant plus its offset as set, to the ns` |

### Design notes

- The exact datapath check: `grade_output_timestamps` records every `dom_ns_w` value (a public timestamp tap, never an
  expected value) during its drain and window; an AAF stamp less its row as GET reads it must be the low 32 bits of
  one of them, a CRF stamp (64 bits) less its applied row one of them. The domain grid is required live while graded.
  nxn: AAF 8 on/0 off, CRF 2 on/0 off per call, ~910 events.
- `sim_ofs.cpp`'s phase check now asserts the AAF phase against the CRF timing points is (row as set - CRF applied)
  modulo Ps to 2 ns (max 0.33 ns): the documented 4.3.5 consequence of a non-period AAF offset, measured.
- Spec text published, not re-litigated: IEEE 1722-2016 10.8 Eq. (15) ("shall not exceed +/-5.0 %") and 4.3.5 hold
  for AAF offsets of whole periods; with any other offset a CRF-following AAF stream sits the offset's fraction off
  the timing points (2,010,000 ns: 0.48 Ps, past Eq. (16)'s 25 % too). The ruling takes 5.4.2.9's as-set over that;
  the docs and the compliance row say so. Raised in the REVIEW READY's open questions.
- No bench arrival-lead measurement exists in this lane; the supported range is stated at arrival from the depth and
  the derived event latencies, with the offset mapping through the transit as a symbol.
- Processor PR #199's harness face (`gsi_ptoff_applied`) models the integrator rounding every Stream Output's GSI(3).
  After this round only the CRF output's is rounded. Its gate test stays valid (it needs one row whose readback
  differs from the stored value) but its description of the integrator is now true of the CRF output alone. That
  clone is closed to this lane; recorded for the manager.
- The builder accepts `buffer_length_ns` above 2,126,000 while the queue's depth is fixed by 2.126 ms: no shipped
  config does, documented; a builder check would be new work (for the manager).

### Resources and timing (route-1x1 against the unchanged record; `receipts/round5/route_1x1_5b502a05/`)

| Figure | Record | Round 4 (`bb9a9200`) | Round 5 (`5b502a05`) | Round 5 vs round 4 | Bar |
|---|---|---|---|---|---|
| LUT | 49,613 | 50,077 (+464) | 49,922 (+309) | -155 | +500 |
| FF | 52,353 | 52,775 (+422) | 52,696 (+343) | -79 | +600 |
| SLICE | 15,725 | 15,801 (+76) | 15,793 (+68) | -8 (12 left) | +80 |
| RAMB36 / RAMB18 | 74 / 25 | 74 / 27 | 74 / 27 | 0 | RAMB18 +2 budgeted; gate exit 1 on it alone |
| DSP | 14 | 13 | 13 | 0 | -- |
| WNS / WHS | 0.215 / 0.036 ns | 0.123 / 0.036 | 0.108 / 0.015 | -0.015 / -0.021 | met; route complete |

Worst setup path: the CPU's DMA write bridge (100 MHz, 20 levels), outside this change. Per instance (post-place):
`pres_round` 149 LUT/193 FF -> `g_pres_crf.pres_round` 131/159; `milan_datapath` 41,375/41,632 -> 41,412/41,553
(untouched blocks move by up to 150: `crf_rx` +134, `pp_shadow` -143, `avtp_rx_parser` -65). Vivado OOC of
`KL_mtt_round` (AreaOptimized_high, `receipts/round5/ooc_mtt_5b502a05/`): N_P=2 (round 4's 1x1) 215 LUT/193 FF,
N_P=9 (round 4's 8x8) 386/427, N_P=1 (now) 182/159: -33/-34 at 1x1, -204/-268 at 8x8 in the rounder; the AAF rows'
readback became a mux on the rows as set in the datapath. Yosys `milan_datapath` 1,771,134 -> 1,770,334 cells.

### Gate table (round 5)

| Gate | Command | Head | Result | Receipt |
|---|---|---|---|---|
| route-1x1 | `scripts/round5/route.sh` then `pp_resource_gate.py check` | `5b502a05` | above; exit 1 on RAMB18 alone | `route_1x1_5b502a05/` |
| OOC rounder | `ooc_mtt_5b502a05/run_ooc.sh` | `5b502a05` | N_P 1/2/9: 182/159, 215/193, 386/427 | `ooc_mtt_5b502a05/` |
| lint | `python3 scripts/lint_rtl.py --check` | `5b502a05` | 89 <= 89 | `lint_5b502a05/` |
| Yosys changed tops | `syn/yosys/run.sh --top KL_mtt_round --top KL_crf_tx --top milan_datapath` (sv2v v0.0.12) | `d5b516f6` (RTL = `5b502a05`) | PASS 1,215 / 2,687 / 1,770,334 cells; tied-input, tap-purity PASS | `yosys_changed_tops_d5b516f6/` |
| media_phase ofs + 8 offset mutants | `make ofs`; `phase_mutants.py --jobs 1 --only <8>` | `133ef20f` + the ofs change (= `ac3bb11a`) | 93/0; 9/0 (clean + 8 caught) | `media_phase_pre/` |
| media_phase pins, render, blend, det; crf_tx | `make pins render blend det`; `make -C ../crf_tx` | `950bffec` (RTL comments differ) | 11/0, 13/0, 24/0, det 0 failures; 129/0 | `media_phase_pre/` |
| milan_dp every leg | `legs.sh` (build-/exec- each) | `d5b516f6` | base 236, crflic 416, dynmap 162, nxn 2,009, nxndv 2,011, nxn8 3,817, nxn4c 2,009, nolpf 236, prune 33, ax1x1 233, aclk 182: 0 failures; render_mutants 4/4 + 2 clean | `milan_dp_legs_d5b516f6/` |
| milan_dp notify at the pin | `./obj_notify/Vmilan_dp_notify` | `d5b516f6` | 459 checks, 3 failures: CRF steps 3, 4 (D10) | same |
| notify + gsi_mutants with the processor's E_SINFO spliced | scratch clone; `make notify-build`; `gsi_mutants.py 1..11` | `d5b516f6` | 459/0 (ROM `f9954a76...`); 11/11 caught | `notify_fix_d5b516f6/` |
| nxn planted defects | `scripts/round5/nxn_plant.py` x2 | `d5b516f6` | both caught by their named checks (2009 checks, 1 failure each) | `nxn_plants_d5b516f6/` |
| docs gates (49) | `scripts/docs_gates.sh` | `ee5ece60` | 49/49 | `docs_gates_ee5ece60/` |
| C++/Python/SV idiom, port contracts | `check_cpp_idiom.py`, `check_py_idiom.py`, `check_sv_idiom.py`, `check_port_contracts.py` | `ee5ece60` | pass (inside the 49) | same |
| full sweep | `scripts/round5/sweep.sh <clone> <out> 0 1 2 3` | `ee5ece60` | 63/64 suites: shard 0 14/15, 47,447 checks (`milan_dp` failing only the CRF notify steps 3/4 at the pin, 3 checks; its pool then started none of nxn8, nxn4c, nolpf, prune, ax1x1, aclk, all run one by one above; its prefix cases gptp 182, gptp-lat 182, counters pass); shard 1 16/16, 331,516 (`media_phase` ofs 93/0); shard 2 17/17, 262,062; shard 3 16/16, 1,540,265. 05:41 to 10:01 UTC | `sweep_ee5ece60/` |
| media_phase campaign (all 40) | `phase_mutants.py --jobs 2 --only <chunk>` x6 | `ee5ece60` | 40 of 40 caught, every clean case passes (two mutants first cut off by the 595 s command timeout, re-run alone: caught) | `media_phase_mutants_ee5ece60/` |

## Round 4 (session 9, 2026-10-21 14:52 onward) -- the listener presents each sample at its presentation time

**Status: REVIEW READY at `2389506a`, posted https://github.com/kebag-logic/milan-fpga/issues/632#issuecomment-6331675159 (gate table below). Stopped there, as assigned.** Assignment: https://github.com/kebag-logic/milan-fpga/pull/770#issuecomment-6316458183, owner
decisions https://github.com/kebag-logic/milan-fpga/issues/632#issuecomment-6309219099 and
https://github.com/kebag-logic/milan-fpga/issues/632#issuecomment-6309313685. Base `3fdaea3d` (fetched: the remote
branch head is `3fdaea3d`; dev has moved to `d77a8afd`, not merged, no rebase). Receipts under `receipts/round4/`.

Progress (kept current):
- `111538670` RTL: `KL_render_queue` (new), depacketizer header timestamp + payload lead, latency package out-lead
  functions, datapath swap (the #386 stage and its #386/#387 render re-centre triggers retired; the #645 settle
  recentre kept for the LOOP queues), source lists.
- `ae26a827b` media_phase `render` case: two render interfaces a frame apart (out-leads 2 and 3), 13 checks pass;
  five planted controls (B's constant dropped, untimed read, frame off by one, late rule, early rule) KILLED. The
  slot-MSB decoder is now `slot_msb_decoder.hpp`, shared with `sim_pins.cpp` (pins case and its three mutants re-run:
  clean pass, all killed).
- `25fae69f0` unit suite `tb/verilator/render_queue` (replaces `render_setpoint`): 33 + 32 checks on two shapes, 18
  planted defects all caught by their named checks.
- Early STOP check (Vivado OOC, `receipts/round4/ooc_*`): 1x1 = 2 RAMB18, 0 LUTRAM, 594 LUT, 231 FF; 8x8 = 6 RAMB36,
  0 LUTRAM, 945 LUT, 395 FF. Under the 2-RAMB18-per-stream budget; no LUTRAM.
- `4b2df8ea` RTL: `PAY_LEAD_P` -> `PAY_LEAD_CYC_P` (depacketizer, queue), queue port `hdr_ts_i` -> `hdr_ts_ns_i`
  (naming ratchet); the depacketizer's lead gate reads its count alone (`lead_ok_w`, a false combinational loop
  through `pop_w` that lint counted as a new UNOPTFLAT); explicit 64-bit operands in `out_pipe_ns` (two new
  WIDTHEXPAND); the queue's STEP note corrected and a HOLD note added. Unit and pin harnesses under the C++ and
  Python idiom ratchets (split `plan()`/`phases()`, one declarator per line, a named enum).
- `7d7ffc09` milan_dp_render rework (pins: T6 FIRST EVENT/PRESENTATION, [LAW] x18, [CRF], T31, [PULLIN]); the
  `[LAW]` phases' drain gap is now the lead's PDU slots + 4 (the first phase saw the previous phase's 92-frame tail);
  M4 waits the lead out before its window.
- `504ae8b3` milan_dp aclk: the presentation instrument at the queue output (PT stamped on the domain grid, K = 2,
  free time across commanded steps), [RENDER-INT/CRF/ARRIVE/STEP/SETTIME/REFUSE/LIVE], RENDER_STAT's new fields;
  render_mutants (4) and render_csr_controls (3) re-planted; observation fixtures re-frozen.
- `1ab53ffc` gmstep: samples name {seq, event}; the step refuses the PDUs stamped across the two steps (2 at feed
  delay 0), one slip, one offset (3945 cycles) before and after; controls re-planted (flush on GM identity / step;
  refusals uncounted; a gap uncounted).
- `baa9ea69` builder census: `cfg_ptp_cmd_load` 4, `eff_ptp_adjust_w` 2, no media re-base; the queue's `flush_i`
  pinned to the bind wipe; mutants moved.
- `43f06d17` follow_ring: wrapper binds `KL_media_domain_event` + `KL_render_queue`; glue piece "settle arming
  edges"; presentation graded at nearest frame (Ps/2 + 2 clk_i) after and across each settle; mutants remapped,
  SETTLE-FLUSH added; trace table columns.
- `e6756e6f` milan_dp_mclk: the 0.8 s row no longer counts a recentre (the #386 one retired; #645's waits 8 LOCKED
  windows); the sweep's "never more than one" counts #645's settle.
- `6631b0b2` docs.
- route-1x1 at `6631b0b2`: LUT 50195 (+582 over 49613, bar +500) -> MATERIAL REGRESSION; FF +539, RAMB18 +2
  (budgeted), WNS +0.179, WHS +0.033. Receipt `receipts/round4/route_1x1_6631b0b2/`. Synth-vs-place diff against
  round 3's route: +275 at synthesis, +462 after place; unchanged blocks move +-100 (pp +106/+150, crf_tx +82,
  gptp_shadow -160): the total is placement/synthesis-noisy. Worst path now inside pp (33 levels, routing-bound).
- `2d786e8b` the LUT cut below (queue + datapath + tests + docs). At it: render_queue 34 + 33 checks pass, 20 of 20
  planted defects caught (two new: a step keeping its quotient bit with the remainder unreduced; a too-early PDU
  missing from `refused_o`; "last quotient bit dropped" now names `[round]`, since the rounding is a separate carry
  the defect misplaces only floor-odd phases); media_phase render 13/13 (same figures), its five controls killed;
  milan_dp aclk 182/0; lint 89 <= 89; Yosys `KL_render_queue` PASS; docs gates 49/49. route-1x1 started 17:49 UTC on
  clone `r4/clone-route-2d786e8b`.
- route-1x1 at `2d786e8b`: LUT 50065 (+452), FF 52780 (+427), SLICE 15780 (+55), RAMB36 74, RAMB18 27 (+2, the
  owner's budget; the gate prints REGRESSION for it), DSP 13, WNS +0.069 (worst path inside pp: u_d3 -> event_router,
  50 MHz), WHS +0.030, route complete. Gate exit 1 on RAMB18 alone. Receipt `receipts/round4/route_1x1_2d786e8b/`.
- Found while drafting (Robustness): the walker's event index `k_r` was 3 bits, so a PDU of more than eight events
  (non-Milan; the depacketizer bounds a PDU by `data_len` only) wrapped its later events onto its first frames. The
  old FIFO stage had no such limit. `bb9a9200`: `f0_r` itself is the walk's frame (F0, +1 per event; the next header
  only comes after the last payload beat, the depacketizer's read order), and once an event is past the queue the
  PDU's later events are refused with it (`far_in_w`, the existing `pdu_early_r`), so a long PDU's frame numbers never
  wrap into the window. Unit `[long]` phase: 40 stereo events (the last ten past the queue), 300 mono (120 on past,
  frame numbers past their wrap); two planted defects (the 3-bit index restored; the hold removed -> counted late).
  Cost: OOC 494 LUT/164 FF vs 495/167 (a first form with its own register and compares cost +29 LUT, rejected).
  At `bb9a9200`: unit 36 + 35 checks, 22 of 22 defects caught; media_phase render 13/13 and its five controls; lint
  89; Yosys queue PASS; docs 49/49. OOC receipts `receipts/round4/ooc_bb9a9200/` (all taps, AreaOptimized_high): 1x1
  2 RAMB18, 0 LUTRAM, 553 LUT, 228 FF; 8x8 6 RAMB36, 0 LUTRAM, 890 LUT, 387 FF. route-1x1 started 18:36 UTC.
- LUT cut: OOC experiments in scratch `r4/ooc_exp/` (queue alone,
  1x1, synth only): v0 596 LUT/197 FF (with the datapath's refused adder); no divider 442; long division with a
  3-operand tri 567. Kept: long division of 3d against the constant Ps (16-bit remainder), the rounding by a remainder
  compare in an extra cycle (QW_C + 3 <= PAY_LEAD 16), write data muxed by the bank bit (b1 = !b0), the flush mask
  as the banks' synchronous read reset (invalid words are all zero), one `refused_o` counter in the queue (the
  datapath adder gone), frame numbers RW_C + 2 bits (bound QMAX + 9 < 2 x ROWS, `g_chk_wrap`): 495 LUT/167 FF.
  Queue + crossbar together: round-3 stage 1003 LUT, `6631b0b2` 1073, reworked 981. Rejected: event-counted
  observer (+14 LUT), registered output (-12 LUT, +50 FF).
- route-1x1 at `bb9a9200` (FINAL for RTL): LUT 50077 (+464), FF 52775 (+422), SLICE 15801 (+76, 4 left), RAMB36 74,
  RAMB18 27 (+2 budgeted; the gate's only REGRESSION line), DSP 13, WNS +0.123 (pp path), WHS +0.036, complete.
  Receipt `receipts/round4/route_1x1_bb9a9200/`.
- Campaigns at `bb9a9200` (receipts `*_bb9a9200/`): milan_dp aclk 182/0, render_mutants 4/4, CSR controls 3/3;
  gm_steps leg 195/0 + the two stage controls (refusals uncounted; gap) caught; follow_ring mutants 16/16;
  milan_dp_render #632 subset 10/10 (clean law-only/pullin/serial-only, 3 leg defects, 4 #632 mutants); media_phase
  mutants 58/0 (20 clean + 38 caught, 2,744 s, jobs 1); builder all-but-1-not-run (gate 11, Arty tree); Yosys
  changed tops PASS (queue 652,454 cells; depacketizer 60,880; datapath 1,771,134), tied-input, tap-purity.
- Sweep at `bb9a9200`, shard 0: 14/15, `milan_dp` FAIL: the notify steps 3/4 (pin, known) and a NEW one, base leg
  "I2S left sample from payload" (I2S words all zero). Cause: `mkaaf` stamps 0xAABBCCDD with tv=1; the #386 law
  presented any PDU, the stage refuses it (late/early). The pool then started none of the 9 later legs. Sweep stopped
  in shard 1; every other leg run one by one at `bb9a9200` (all 0 failures: crflic 416, dynmap 162, nxn 1988, nxndv
  1990, nxn8 3784, nxn4c 1988, nolpf 236, prune 33, ax1x1 233). `2389506a`: the I2S check's PDU is stamped
  83,333 ns past `dom_ns_w` (four periods, inside 31.1 us..2.656 ms): base 236/0. Docs gates 49/49 at `2389506a`.
- Full sweep restarted at `2389506a` 22:06 UTC (clone `r4/clone-sweep-2389506`, out `r4/sweep-2389506`); after it,
  `tools/chain_n.sh`: `make run ORDINARY_CASES=...` + `run-notify` at the pin in that clone, then notify + `gsi_mutants.py
  9` with the processor head's E_SINFO spliced into a scratch clone's submodule.
- Sweep at `2389506a` (receipt `receipts/round4/sweep_2389506/`): shard 0 14/15, 45,397 checks (milan_dp: the three
  notify steps at the pin; pool stopped after nxn); shard 1 16/16, 331,469; shard 2 17/17, 262,062; shard 3 16/16,
  1,540,265. milan_dp_render ship 263, multi 71: first event +0.6 ns, every slot within 15.1 ns over 22 windows.
- `tools/chain_n.sh` at `2389506a` (receipt `milan_dp_and_notify_2389506/`): `make run ORDINARY_CASES=...` rc 0, 11 legs
  0 failures (11,248 checks), render_mutants 4/4; `run-notify` 441/3 at the pin; with the processor head's E_SINFO
  spliced into a scratch clone's submodule (ROM `f9954a76...`): notify 441/0, `gsi_mutants.py 9` caught at step 3.
  The lane's submodule untouched (pin `2cbed0a9`, status empty).
- receipts/round4/INDEX.md (447 files) and receipts/INDEX.md regenerated.

### Gate table (round 4)

| Gate | Command | Head | Result | Receipt |
|---|---|---|---|---|
| full sweep | `scripts/round4/sweep.sh <clone> <out> 0 1 2 3` | `2389506a` | 63/64 suites; only milan_dp's notify steps at the pin | `sweep_2389506/` |
| milan_dp every leg + notify | `make run ORDINARY_CASES="base crflic dynmap nxn nxndv nxn8 nxn4c nolpf prune ax1x1 aclk"`; `make run-notify` | `2389506a` | rc 0, 11,248 checks, 0 failures; notify 441/3 (pin) | `milan_dp_and_notify_2389506/` |
| notify with the processor fix | splice + `make notify`; `gsi_mutants.py 9` | `2389506a` | 441/0; caught at step 3 | same |
| route-1x1 | `scripts/round4/route.sh` then `pp_resource_gate.py check` | `bb9a9200` | LUT +464, FF +422, SLICE +76, RAMB18 +2 (budgeted; exit 1 on it alone), DSP 13, WNS +0.123, WHS +0.036 | `route_1x1_bb9a9200/` |
| OOC queue | `ooc_bb9a9200/run_ooc.sh` | `bb9a9200` | 1x1 2 RAMB18/0 LUTRAM/553/228; 8x8 6 RAMB36/0 LUTRAM/890/387 | `ooc_bb9a9200/` |
| render_queue + mutants | `make run odd`; `make mutants` | `bb9a9200` | 36, 35; 24/24 | `render_queue_bb9a9200/` |
| media_phase render + 5 controls; full campaign | `make render`; `phase_mutants.py --only ...`; `make mutants MUTANT_JOBS=1` | `bb9a9200` | 13/0; 5/5; 58/0 (20 clean + 38) | `media_phase_render_bb9a9200/`, `media_phase_mutants_bb9a9200/` |
| milan_dp aclk, render_mutants, CSR controls | `make aclk`; `render_mutants.py`; `make render-csr-controls` | `bb9a9200` | 182/0; 4/4; 3/3 | `milan_dp_bb9a9200/` |
| gm_steps leg + 2 stage controls | `make -C ../milan_dp gmstep`; `gm_subset.py` | `bb9a9200` | 195/0; 2/2 | `gm_steps_bb9a9200/` |
| follow_ring controls | `fr_subset.py --jobs 1` (all) | `bb9a9200` | 16/16 | `follow_ring_controls_bb9a9200/` |
| milan_dp_render #632 subset | `tdm8_subset.py` | `bb9a9200` | 10/10 | `milan_dp_render_632_bb9a9200/` |
| Yosys changed tops | `syn/yosys/run.sh --top KL_render_queue --top KL_aaf_rx_depacketizer --top milan_datapath` | `bb9a9200` | PASS, tied-input, tap-purity | `yosys_changed_tops_bb9a9200/` |
| lint | `python3 scripts/lint_rtl.py --check` | `bb9a9200` | 89 <= 89 | `lint_bb9a9200/` |
| docs gates (49) | `scripts/docs_gates.sh` | `2389506a` | 49/49 | `docs_gates_2389506/` |
| builder | `scripts/round4/builder_run.sh` | `bb9a9200` | all but gate 11 (Arty tree, not run) | `builder_bank_bb9a9200/` |

### Changes (file:line at `bb9a9200`; clause)

| File:line | Change | Clause |
|---|---|---|
| `hdl/ieee1722/aaf/KL_render_queue.sv:153` (new, banner `:1-133`) | the presentation stage: `d_w` `:410` (32-bit wrap), the exact divider (long division of 3d, thirds of ns, rounded from the remainder) in `pdu_frame` `:724`, rows `:247` (128 at 48 kHz, derived), frame numbers RW_C + 2 bits bounded by `g_chk_wrap` `:319`, the banks' read reset `:363`, the invalidation write `:587`, the schedule `:638` (each interface reads n + K_i, then the consumed frame's rows are written zero), the walk's frame per event and the past-the-queue hold `:464`, late/early/untimed classification and counters `:870` (`refused_o` `:883`), slips `:536`, `:864`; STEP `:102`, HOLD `:111` | IEEE 1722-2016 4.4.4.5, 4.4.4.9, 7.5; Milan v1.2 4.4.2.1 |
| `hdl/ieee1722/crf/KL_media_if_latency_pkg.sv:149`, `:163`, `:171` | `out_pipe_ns`, `out_lead_frames`, `out_lead_ok` | 10.8, 4.3.5 |
| `hdl/ieee1722/aaf/KL_aaf_rx_depacketizer.sv:74`, `:347`, `:364` | header tv/timestamp on the read side, `PAY_LEAD_CYC_P` hold of the payload | 4.4.4.5, 4.4.4.9 |
| `hdl/milan/milan_datapath.sv:6951-6990` | the stage replaces `KL_render_setpoint`; out-lead derived, its guard `:6951`; `RENDER_STAT` mapping `:6978` from `refused_o` `:6976`; the #386/#387 render re-base glue retired, `g_src_edges` `:6711` kept for the #645 settle | -- |
| `sw/builder/test_builder.py` (gate 1b) | census: `cfg_ptp_cmd_load` 4, `eff_ptp_adjust_w` 2, no media re-base; the queue's `flush_i` pinned to the bind wipe; mutants moved | -- |
| docs | MEDIA_CLOCK_FOLLOWING.md "The listener: each sample at its presentation time (#632)" (the divider, the rules for a PDU of any length); TIME_SYNC.md "Listener render latency"; REGISTER_MAP.md 0x8DC "render presentation state" (`[31:16]` = `refused_o`); TESTING.md rows; CHANGELOG | -- |

### New checks (planted defect -> failing words)

| Suite | Defect | Named check that fails |
|---|---|---|
| `media_phase` `render` | B's constant dropped; the queue read untimed; a frame off by one; late rule removed; early rule removed | `[render B]/[render A] every sample's slot-MSB pin instant, less its slot offset, is its presentation time inside +/-5 % of Ps` (and the late/early count checks) |
| `render_queue` | 22 defects (rounding, last quotient bit, unreduced remainder, carry, bank, scrub, read frame, untimed, payload-before-frame, late/early per event, slips, lead_o, refused_o, ticks, pops, converged, pad lane, the 3-bit event index, the past-the-queue hold, ...) | each its `[<phase>]` check; 24/24 (2 clean + 22) at `bb9a9200` |
| `milan_dp` aclk (`render_mutants.py`) | each PDU placed by its arrival; tv ignored; a PHC step resets the stage; a source change flushes it | `RENDER-ARRIVE-INT: every event presented at its presentation time (late)`; `RENDER-REFUSE: no refused PDU presented`; `RENDER-STEP-INT: every event presented once, in order`; `RENDER-LIVE-CRF: every event presented once, in order` |
| `milan_dp` (`render_csr_controls.py`) | lead field tied zero; bit 9 selector; stage absent | `RENDER-CSR: queued mirrors taps`; `RENDER-CSR: bit 9 preserves talker rejection`; absent passes |
| `milan_dp_gm_steps` | GM identity empties the stage; the step empties it; refusals uncounted; a gap uncounted | `render: every PDU not presented was refused by the stage and counted once` (x3); `render: the refused PDUs' frames are one counted slip` |
| `follow_ring` | SETTLE-FLUSH (new); NO-ARM, HIGH-ARM, NO-SETTLE, EARLY, LB-WITHHELD remapped | `[B8] the presentation stage presented every PDU across the settle recentre`; `[PULLIN] exactly one settle recentre from the transient to the hold's end` (x3); `[B8] the settle recentre came 8 servo windows after LOCKED`; `[B8] the loopback ring is centred after the settle recentre (margin in (5, 6] ticks)` |
| `milan_dp_render` (`tdm8_render_mutants.py`) | the render out-lead one frame long (serial, and at every [LAW] phase); the domain event's instant not back-dated; the settle recentre never pulses | `T6 FIRST EVENT: ...in the frame its timestamp names, inside +/-5 % of Ps` (and one more); `T30 INTERNAL LAW +0 PRESENTATION: every event's slot-MSB pin instant...`; `T6 PRESENTATION: every event's slot-MSB pin instant, less its slot offset...`; `T647 PULLIN +1562: one settle recentre for the LOOP queues after the hold` (subset run at `bb9a9200`: 10/10, `scripts/round4/tdm8_subset.py`) |

### Design notes / gains

- No fill exists to re-centre: a gPTP step, a settime, a source change and an aligner pull-in move no queued sample
  (graded in aclk, gm_steps, follow_ring, milan_dp_render). A step whose talkers' time does not follow (our PHC
  alone) shifts later PDUs by the step and is counted as an overlap or gap; refused when it reaches past the queue.
- A frame-grid hold (serial clock stopped) delays the frames already queued by the hold for up to the lead
  (~2 ms), then later PDUs take over with one counted slip: `follow_ring` pullin's "before" window must stop a lead
  before the hold for this reason (found by its first run: 54.6 us = the 52 us hold + the marker phase).
- The 32-bit wire timestamp wraps every 4.29 s: harness PT records are kept in 64-bit ns (follow_ring's first run
  graded 2^32 errors before that fix); the domain instant read signed (a settime to zero back-dates below zero).


## Round 3b (session 8, 2026-10-21 12:23 to 14:48) -- option (b) committed in the processor

**Status: REVIEW READY** posted on #632 with both heads: https://github.com/kebag-logic/milan-fpga/issues/632#issuecomment-6316365497 (text: `public-review-ready-r3b.txt`; URL also in
`public-review-ready-r3b.posted.txt`). Every item of the round 3b assignment done; every gate it touches rc 0.

Ruling: https://github.com/kebag-logic/milan-fpga/pull/770#issuecomment-6312625146 ([A10], option (b); the STOP
condition "more than the one gather change" waived for these five words; R677-2's four-step case stays as
specified). Scope of this round, and only this: (1) the processor commit with its test and planted defects, (2) the
milan_dp re-measure with the committed processor head applied uncommitted to the submodule, (3) docs/receipts in
milan-fpga. The listener render queue was NOT started (next round). TAKEN not re-posted. Nothing pushed.

**Heads.** milan-fpga `3fdaea3d2adee05c41629363bffbf32cff5b0656` on `32fb8fc2` (one docs commit). Processor `51f88c7e14e7e2527c09ff9a23b93dd6b857fd50` on
branch `632-sinfo-notify-stored` at processor main `08023123` (origin checked: the protocol-processor repository, the
same URL as the milan-fpga submodule's; branch base verified `08023123` before committing). The milan-fpga submodule
is at its pin `2cbed0a9`, status clean, after the measurement.

### Processor commits (on `08023123`, oldest first)

| Commit | Subject |
|---|---|
| `175a5a15` | Compare SET_STREAM_INFO's offset with the stored row once a controller set it and with the integrator's factory word before, so the push follows the offset as set (milan-fpga #632) |
| `0b097464` | Re-record tb/aecp_cmds' decode sweep against the ROM with SET_STREAM_INFO's stored-row compare |
| `51f88c7e` | Measure D3S5's SET_STREAM_INFO latency on a row already set, the arm its timed SET takes, since E_SINFO's two arms reach the store a cycle apart |

`0b097464` exists because `make check`'s AECP command gate refused `175a5a15` alone: `tb/aecp_cmds/decode.json`
records the ROM digest its sweep ran on. Re-recorded through its own target (`make -C tb/aecp_cmds record`, 617,916
trials, 176 checks pass): the digest line alone moved. No amend.

### D9: D3S5's premise took the never-set arm's latency (found by the sweep at `0b097464`, fixed)

`tb/pp_top` D3S5 places an NVM WRITE's done on the store's accepting cycle of a SET_STREAM_INFO, using the latency
of an earlier SET measured on the same row. With option (b) that earlier SET ran on a row never set (the GSI(3)
arm) and the timed SET on a set row (the stored arm), which reaches the store one cycle later: "D3S5 premise: the
change accepted at 315227, the WRITE's done at 315228" (the only failure of the first build; `make run` then ran
none of pp_top's six later builds). `51f88c7e` sets the row first and measures on the arm the timed SET takes; the
premise is graded as before (`primed` added to it). The D3 control graded by D3S5 (`clear_wins_same_edge`) is still
killed, and the other eleven D3 controls graded by section S were re-run at the head (gate table). Receipts of the
superseded run: `receipts/round3/processor_0b097464_superseded/`. The E_SINFO block and the ROM are identical at
`0b097464` and `51f88c7e` (`hdl/` unchanged), so the milan-fpga measurement holds for the head.

### milan-fpga commit (on `32fb8fc2`)

| Commit | Subject |
|---|---|
| `3fdaea3d` | Record that SET_STREAM_INFO's push compares with the stored offset once set and with the factory offset in force before, as the processor gate ruled for #632 |

`docs/design/MEDIA_CLOCK_FOLLOWING.md:1694-1705`: the design doc said only "a processor whose gate reads the offset
as set"; the ruled form compares with GET_STREAM_INFO's word on an output never set, so the doc now states both
arms, the SET of 0 on a never-set output, and the factory-row residue. Docs gates 49/49 at `3fdaea3d`.

### Changes (file:line at the processor head; clause)

| File:line | Change | Clause |
|---|---|---|
| `hdl/aecp/ucode/gen_ucode.py:2434-2466` | E_SINFO: `READ_ST RGN_DYNV + SEL_PTOFF`, COMPARE, `BR_STATUS` -> the unset arm; set arm `READ_ST RGN_DYN + SEL_PTOFF` (the anchor of milan-fpga's mutant 9, kept byte-exact), `BRANCH`; unset arm `GATHER_EXT GSI(3)`; skip target `E_SINFO + 17`; three asserts on the branch targets and END. 13 -> 18 words of a 32-word slot; ROM words 1859..1873 alone differ from main's | Milan v1.2 5.4.5.2, 5.4.2.9, 5.4.2.10.2; IEEE 1722.1-2021 7.5.2 |
| `tb/pp_top/sim_main.cpp:1286-1299`, `:2018-2021` | `gsi_ptoff_applied`: the face answers a Stream Output's GSI(3) as milan-fpga's integrator does (row rounded up to whole 48 kHz periods once set, factory 2,000,000 ns before); off everywhere but NS | 5.4.2.10.2; IEEE 1722-2016 10.7 Eq. (14) |
| `tb/pp_top/notify_phases.hpp:1131-1201`, `:2349-2352` | section NS, run by `run_pushes` after NP on its own model | 5.4.5.2 |
| `tb/pp_top/notify_mutants.py:228-243` | two planted defects | -- |
| `tb/pp_top/README.md:69-73`, `:2484`, `:2661-2698`, `:2997-3003`, `:3029-3036` | D3S5's measurement, NS in the run list, section NS (with the residue), the mutation record (137 controls; four rows' counts moved) | -- |
| `tb/pp_top/d3_phases.hpp:640-682` (`51f88c7e`) | D3S5 sets the row first and measures the latency on the arm its timed SET takes (`primed` in the premise) | -- |
| `docs/architecture/06_aecp_engine.md:522`, `09_verification.md:184`, `:318` | the chain names the compare and the residue; NS on both arms of the A/B row; the 8.4 evidence row | -- |
| `tb/aecp_cmds/decode.json` | the ROM digest (`0b097464`) | -- |

### New checks (planted mutant, failing words)

pp_top section NS (`--notify-only`): A and B registered (NS0); NS0b premise (no row set, GET 2,000,000 on both);
NS1 output 1 SET 2,000,000 on a never-set row: nothing; NS2 output 0 SET 0 on a never-set row: one push, byte-exact;
NS3 2,010,000: one push, NS3b GET reads 2,020,834 (premise); NS4 2,010,000 again: nothing; NS5 2,020,834: one push.
20 checks. The ruled four: identical SET pushes nothing (NS4), changed SET pushes once (NS3, NS5), SET 0 on a
never-set row pushes once (NS2), first SET equal to the factory value pushes nothing (NS1).

| Mutant | Planted | Failing words (all named checks fail, nothing else) |
|---|---|---|
| `stream_info_compare_applied` (the planted defect: the GSI(3) compare restored) | set arm's stored read -> `GATHER_EXT GSI(3)` | "NS4 ... again: an unchanged offset pushes nothing (Milan 5.4.5.2), got 1 at the other controller and 0 at the requester"; "NS5 ..., the value GET read, a change: exactly one unsolicited response of this command at the other registered controller, got 0" |
| `stream_info_unset_arm_dropped` (the never-set arm control) | the unset arm's `BR_STATUS` a NOP: option (a) | "NS1 ... on a row never set: an unchanged offset pushes nothing (Milan 5.4.5.2), got 1 at the other controller"; "NS2 ... on a row never set: exactly one unsolicited response of this command at the other registered controller, got 0" |

Moved by NS (re-measured, README updated): `enq_dropped_stream_info` 1 -> 4 (NP3, NS2, NS3, NS5),
`stream_info_get_body` 1 -> 4 (same), `requester_not_excluded` 12 -> 15, `entry_seq_not_advanced` 13 -> 15. The
other eighteen `--notify-only` controls fail exactly their recorded checks.

### The consumer re-measure (milan-fpga, `receipts/round3/notify_sinfo_pp_0b097464/`)

The processor head is 50 commits past the pin. Its gen_ucode.py diff does not apply at the pin with three lines of
context (a later comment differs), and with one line its third hunk lands on another `])` 33 lines away (it would
have put the asserts in the wrong block). So `scripts/round3b/splice_sinfo.py` replaced the pin's E_SINFO block (and
nothing else) with the head's, each found exactly once; `submodule_applied.diff` is exactly the committed hunk. The
ROM it emits is `f9954a76...`, byte-identical to round 3's option (b) ROM, words 1859..1873 alone differing from the
pin's `518b900c...`, and those words equal the processor head's own ROM.

| Measure (lane `32fb8fc2`, submodule pin + head's E_SINFO, uncommitted) | Result |
|---|---|
| `make notify` (the timed leg, 1x1) | rc 0, 441 checks, 0 failures; pushes 0, 1, 0, 1 at steps 1..4; GET 2,000,000 / 2,020,834 / 2,020,834 / 2,041,667 |
| `python3 gsi_mutants.py 9` (the planted control) | rc 0: clean leg PASS; mutant caught at "[NOTIFY] SET_STREAM_INFO step 3: 2,010,000 ns again modifies nothing" (3 failures of 441) |
| never-set probe (disposable, scratch clone at `32fb8fc2`, `scripts/round3b/sinfo_never_set_probe.py`) | rc 0, 444 checks, 0 failures: SET 0 on the CRF output's never-set row pushes once; GET then 0; SET 2,000,000 back pushes once |
| submodule after | `2cbed0a9`, status empty; milan_dp's ignored `ucode.hex` regenerated from the pin (`518b900c...`) |

The docs commit `3fdaea3d` touches no simulated input, so the measurement at `32fb8fc2` stands at the head.

### The residue (recorded by ruling, not a finding)

Before a row's first SET the compare reads the integrator's GSI(3), the offset as applied: a factory row that is
not whole periods compares with its applied value, so a SET of exactly that factory value would push. No shipping
configuration has such a row (every factory row is 2 ms, whole periods). Recorded in the processor README section
NS, 06's chain, the milan-fpga design doc, PP-PR-BODY.md and PR-BODY.md.

### Resources

No gateware structure changes this round: milan-fpga's commit is docs only, and the processor change is ROM content
(the 2048-word ROM keeps its size; five more words placed in E_SINFO's existing 32-word slot). Route not re-run; the
round 3 route at `62ee1a8c` stands. The pin adoption that brings the new ROM is a later round's.

### Gate table (round 3b)

| Gate | Command | Head | Result | Receipt |
|---|---|---|---|---|
| processor docs gates | `make check` | `51f88c7e` (and `0b097464`) | rc 0: lint, wavedrom, links, matrix, req-tags (231 tags), modmatrix, params, aecpcmd (selftest 231 of 231; 31 commands), ids, figures, stale. At `175a5a15` alone: aecpcmd refused (decode.json's ROM digest), fixed by `0b097464` | `receipts/round3/processor_51f88c7e/make_check.log` |
| processor HDL lint | `./scripts/lint_hdl.sh` | `51f88c7e` | rc 0 | `processor_51f88c7e/lint_hdl.log` |
| processor suites | `REQ_TAG_LOG=... ./scripts/run_suites.sh` (CI's step) | `51f88c7e` | rc 0: every suite PASS, 1,030,329 checks, 0 failing; `pp_top` 10,741 over its seven builds; `ucpu` 447; `aecp_cmds` 176; `aecp_notify` 131. At `0b097464`: `pp_top` failed D3S5's premise (D9) | `processor_51f88c7e/suites.txt`; `processor_0b097464_superseded/` |
| processor traceability, executed half | `python3 scripts/check-req-tags.py --suites ... --evidence ...` | `51f88c7e` | rc 0: 231 evidence lines, 14 suites | `processor_51f88c7e/req_tags_executed.log` |
| notify controls (`--notify-only`) | `notify_mutants.py --jobs 1 --only` the 22 | `51f88c7e` (and `0b097464`) | rc 0: goldens PASS, 22 of 22 KILLED by their named checks; the two new ones fail NS4+NS5 and NS1+NS2 | `processor_51f88c7e/campaigns/notify.*` |
| D3 controls graded by section S | `d3_mutants.py --jobs 1 --only` the 12 | `51f88c7e` | rc 0: goldens PASS, 12 of 12 KILLED, each failing exactly its recorded count (3, 2, 1, 18, 14, 2, 5, 2, 2, 1, 2, 1) | `processor_51f88c7e/campaigns/d3.*` |
| AECP command decode controls (CI) | `python3 -B tb/aecp_cmds/mutants.py --jobs 1` | `51f88c7e` | rc 0: 17 of 17 detected by their named failures; golden and restored PASS | `processor_51f88c7e/campaigns/aecp_cmds.*` |
| AECP dispatch controls (CI) | `aecp_dispatch_mutants.py --jobs 1` | `51f88c7e` | rc 0: the four controls (aecp-dispatch, aecp-line, d3, line-guards) PASS, then 69 of 69 planted defects KILLED by their named checks; 73 checks, 0 failures | `processor_51f88c7e/campaigns/aecp_dispatch.*` |
| AECP deadline and hazard controls (CI) | `aecp_mutants.py --jobs 1` | `51f88c7e` | rc 0: six controls (pp_top budget, d3, deadline, hazards, timer-defaults; ucpu) PASS, then 61 of 61 planted defects KILLED; 67 checks, 0 failures | `processor_51f88c7e/campaigns/aecp.*` |
| ucode generator | `python3 hdl/aecp/ucode/gen_ucode.py` (also inside every suite's build) | `51f88c7e` | 2048 words, 92 programs; ROM differs from main's at 1859..1873 alone | `notify_sinfo_pp_0b097464/digests.sha256` |
| milan_dp notify leg, the processor head's E_SINFO applied | `make -C tb/verilator/milan_dp notify` | lane `32fb8fc2` + processor `0b097464` = `51f88c7e` E_SINFO | rc 0: 441 checks, 0 failures | `receipts/round3/notify_sinfo_pp_0b097464/` |
| its planted control | `python3 gsi_mutants.py 9` | same | rc 0: clean PASS; caught at step 3 (3 of 441) | same |
| never-set probe (disposable) | `make notify` with the probe, scratch clone | same | rc 0: 444 checks, 0 failures; SET 0 pushes once | same |
| milan-fpga docs gates (49) | `scripts/docs_gates.sh` (round-3 runner) | `3fdaea3d` | 49 of 49 rc 0 | `receipts/round3/docs-gates-3fdaea3d/` |

Not run this round, with reason: the milan-fpga sweep, media_phase, route, Yosys, lint and builder (no input changed
since `32fb8fc2`: `3fdaea3d` is one design document); the processor's SRP, MAAP and ADP campaigns, Yosys and
elaboration guards (no input changed: the processor change is ROM content and tb/pp_top); the full D3 campaign's
other 98 controls (graded by sections the change does not touch; the D3S5 setup change is equivalent for them).

### Environment notes (round 3b)

- One exploratory run of all 22 `--notify-only` mutants (before the receipts) used `--jobs 3`, three builds at once,
  against the two-build cap; memory stayed under 1 GB. Every receipt run used `--jobs 1` beside at most one other
  build. A first slot-2 launch at the head would have run tb/aecp_cmds' `make mutants` at its default four jobs; it
  was stopped seconds in (during the notify golden) and relaunched with `--jobs 1`.
- The probe of round 3 anchored on the call before `28510858`; the round 3b copy anchors on the timed-leg call.
- Processor gates ran in clean clones at the head under scratch; no build product in either checkout.

## Round 3 (session 7, 2026-10-21 04:36 to 12:40) -- STOP on the processor gate (STOP condition 2)

STOP posted: https://github.com/kebag-logic/milan-fpga/issues/632#issuecomment-6313646784 (text: `public-stop-r3.txt`),
head `32fb8fc2`, no processor commit. TAKEN not re-posted. Not pushed.

Assignment: https://github.com/kebag-logic/milan-fpga/pull/770#issuecomment-6306591168, answering R678-2
(issuecomment-6306376430) and R677-2 (issuecomment-6306520485). Base `2ff30f0d`, new commits on it (no rebase, no
amend). Processor clone `$LANES/632-pp` (private path), branch `632-sinfo-notify-stored` at processor main
`08023123` (origin checked: the same repository URL as the milan-fpga submodule's). **No processor commit**: see the
STOP below. The milan-fpga submodule stays at its pin `2cbed0a9`, clean (`git -C protocol-processor status` empty);
the processor change was applied to it uncommitted only for the milan_dp measurements, then restored.

### The STOP: the one-read processor fix does not meet the ruled case

The ruling's fix is one word in E_SINFO: `READ_ST rd=6, RGN_DYN + SEL_PTOFF` in place of `GATHER_EXT rd=6, GSI(3)`
(option (a), `receipts/round3/notify_sinfo/option_a.diff`). Measured on the real datapath and processor (the
committed `milan_dp` `[NOTIFY]` case, the notify leg, 1x1), with the microcode applied uncommitted to the
submodule at its pin:

| Processor | step 1 (2,000,000, held) | step 2 (2,010,000) | step 3 (2,010,000 again) | step 4 (2,020,834) | never-set CRF row: SET 0 (probe) | leg |
|---|---|---|---|---|---|---|
| pin `2cbed0a9` (GSI(3) gate) | 0 | 1 | **1** (exp 0) | **0** (exp 1) | 1 | 444 checks, 3 failures |
| option (a): the one read, as ruled | **1** (exp 0) | 1 | 0 | 1 | **0** (exp 1) | 444 checks, 2 failures |
| option (b): stored row once a controller set it, the integrator's word before | 0 | 1 | 0 | 1 | 1 | 444 checks, 0 failures |

Cause: the processor's dynamic store reads a row no controller has written as 0 with its valid bit clear
(`KL_aecp_dyn_state.sv`, `ptoff_r` reset 0, `ptoff_v_r` 0; the integrator serves the factory 2 ms meanwhile). In
the notify leg no SET has touched output 0 before `[NOTIFY]`, so option (a) compares 2,000,000 with 0 and pushes
at step 1, and a SET of 0 on a never-set row compares 0 with 0 and pushes nothing although the offset in force
moves from 2 ms to 0 (a missed 5.4.5.2 notification the base and the pin both send). Option (b) is the store's own
idiom for this, as E_SCFG does for #178 (`RGN_DYNV` valid read, COMPARE, BR_STATUS; the stored row if set, else the
integrator's GSI(3)): five more words (`option_b.diff`), the gather kept on the never-set arm. Its residue: before
the first SET a factory row that is not whole periods compares with its applied value (no shipping config has one;
every factory row is 2 ms). Decision needed: (a) as ruled, with R677-2's step 1 re-specified and the never-set SET
0 recorded as a follow-up, or (b). Either way the processor PR, its test and its planted defect follow the ruling.

Measured with option (b) uncommitted at `fe3ff999` (`receipts/round3/notify_sinfo/`): notify leg 441 checks, 0
failures; `gsi_mutants.py 9` (the planted control restoring the applied-readback compare) caught at "[NOTIFY]
SET_STREAM_INFO step 3" (3 failures of 441). At the pin: the clean leg fails steps 3 and 4 and the control reports
its pattern absent (0 PASS, 2 FAIL), as designed. Recorded: the committed case fails at the current pin.

### Round 3 commits (on `2ff30f0d`, oldest first)

| Commit | Subject |
|---|---|
| `81f09d06f` | Carry each rounded offset's bit 32 into the CRF output's 64-bit timestamp, and read a row past 32 bits back through GET_STREAM_INFO as 0xFFFFFFFF |
| `f36177f9b` | Grade every offset row on all 33 bits and every CRF timestamp on 64 at the 2^32 boundary, in reset and at run time, and the detector after a hold onto the fold, each with a planted defect |
| `fe3ff9999` | Grade SET_STREAM_INFO's push against the offset as set in four steps on the wire, with the microcode gate's applied-readback compare planted |
| `45633bd1c` | Drop review labels from the #632 source comments |
| `d790dd442` | Document the offsets' carry past 2^32 and GET_STREAM_INFO's saturated word, the SET echo against the applied readback, the push judged on the value set, and the listener out of this PR (#632) |
| `cf85a578b` | Document the rounder's readback row without a unit and hold the #632 changelog and render-latency lines to the style limits |
| `aea19ce73` | Record media_phase's default target at 553 s and its thirty-three-mutant campaign at 1,396 s on two jobs |
| `62ee1a8cc` | Write each rounded row's low word and carry as two indexed writes, its reset value from an elaboration table, since Yosys drops an indexed concatenation target and kept no cell of the rounder |
| `28510858b` | Run the SET_STREAM_INFO push case on the timed leg alone, the one leg whose output 0 still holds its factory offset when the section starts |
| `32fb8fc26` | Record that milan_dp's pool starts no leg after the notify leg while the processor pin's SET_STREAM_INFO gate reads the applied word |

**Head: `32fb8fc26acf7dedc507512d7a455898a26afd84`** (not pushed; no rebase, no amend). Processor: no commit.

### D8: the case's premise held on one leg only (found by the sweep, fixed)

`fe3ff999` ran the four steps in every `[NOTIFY]` (the timed leg and the nxn legs). The nxn legs' whole-model walk
leaves output 0 at 750,000 ns (#67) before `[NOTIFY]`, so step 1's "the offset held" was false there and its push
was right: the sweep's N=4 leg failed step 1 (`receipts/round3/sweep_62ee1a8c/shard0/milan_dp_failures_extract.txt`).
`28510858` runs the case on the timed leg alone, R677-2's leg, where nothing sets the row first. The same sweep
showed that `sim_pool.py` starts no leg after a failure, so at this pin the designed notify failure hides seven later
legs; `32fb8fc2` documents it, and the legs were run on their own at the head (gate table).

### D7: the rounder synthesized to nothing in Yosys (found this round, fixed)

`81f09d06` wrote each row as `{ofs_c_o[row_r], ofs_ns_o[32*row_r +: 32]} <= dv_quot_r[32:0];` (and the reset loop
likewise). Verilator and Vivado take it (the route at `81f09d06` kept `pres_round` at 149 LUT / 193 FF), but Yosys
0.66 through sv2v v0.0.12 drops a concatenation target with an indexed part: every output undriven, and
`KL_mtt_round` synthesized to **0 cells** (round 2: 1,084). `syn/yosys/run.sh` still printed `[PASS] KL_mtt_round
cells=0` (`receipts/round3/yosys_small_tops_aea19ce7_zero_cells/`). Fix `62ee1a8c`: two indexed writes, the reset
values from an elaboration-time table `RESET_RND_C`; Yosys 1,215 cells. The three mutants anchored on those lines
were re-anchored and re-killed (`receipts/round3/media_phase_ofs_62ee1a8c/`). Follow-up for the manager (new work,
not this lane's): the Yosys gate accepts a top whose synthesis kept zero cells; a floor (cells > 0, or a per-top
recorded minimum) would have caught this.

### Outcome per item

| Item | Status |
|---|---|
| R678-2-F1 (MAJOR) CRF carry | done: `81f09d06` (portable form `62ee1a8c`, D7), graded `f36177f9` |
| R677-2-F1 (MAJOR) processor gate | **STOP** (above); milan_dp case and planted control committed (`fe3ff999`, on the timed leg alone `28510858`), measured with every form at `fe3ff999` and form (b) again at `32fb8fc2`; docs scoped (`d790dd44`, `32fb8fc2`); follow-up recorded below |
| R677-2-F2 (MINOR) hold restarts the reference | done: `f36177f9` (`det afterhold`, `hold_keeps_ref`) |
| R677-2-F3 (MINOR) PR body figures | done in PR-BODY.md (404 LUTs and 8 slices; twenty-eight, now thirty-three) |
| R677-2-R1, R678-2-R1 comment labels | done: `45633bd1` and the files of `81f09d06`/`f36177f9`/`fe3ff999` (no `R67x-n-Fn` left in any source comment) |
| R677-2-R2 datapath fold comment | done (`81f09d06`, the R677-2 wording) |
| R677-2-R3..R5, R678-2-R2 listener scope | done: design doc, TIME_SYNC, CHANGELOG (`d790dd44`, `cf85a578`), PR body |
| S1..S4 (optional) | not taken: S2's guard would restrict factory rows, which the carry now serves in full |

### Changes (file:line at `cf85a578`; clause)

| File:line | Change | Clause |
|---|---|---|
| `hdl/ieee1722/crf/KL_mtt_round.sv:99` | `ofs_c_o`: each row's bit 32 | IEEE 1722-2016 10.7 Eq. (14), 10.4.13.1 Eq. (13) |
| `KL_mtt_round.sv:101-103`, `:217-219` | `rb_row_i`/`rb_ns_o`: GET_STREAM_INFO's readback of a row, saturated at 0xFFFFFFFF past 32 bits | Milan v1.2 5.4.2.10.2 |
| `KL_mtt_round.sv:129-138`, `:177`, `:210` | `g_carry` guard (33 bits hold the largest rounding); `round_c` 33 bits; reset and conversion load the carry | 10.7 Eq. (14) |
| `hdl/ieee1722/crf/KL_crf_tx.sv:160`, `:401` | `transit_c_i` (defaulted 0), added into the 64-bit sum at `ROUND_MTT_P = 0`; `:308` unused with the converter | 10.4.13.1 Eq. (13), 10.7 Eq. (14) |
| `hdl/milan/milan_datapath.sv:3452-3475`, `:5001`, `:5255`, `:6395` | carry vector, readback index, GSI word 3 from `rb_ns_o`, CRF output's carry | 5.4.2.10.2, 10.4.13.1 |
| `milan_datapath.sv:3418-3420`, `:3429-3444` | R677-2-R2 fold comment; the SET echo against the readback, the gate on the value set | 5.4.2.9, 5.4.2.10.2, 5.4.5.2 |

No top-level port, no register-map change. Module ports added: `KL_mtt_round` `ofs_c_o`, `rb_row_i`, `rb_ns_o`;
`KL_crf_tx` `transit_c_i` (defaulted, so every other instance is unchanged).

### New checks (planted mutant, failing words)

media_phase campaign, 28 -> 33 mutants:

| Mutant | Harness / case | Required failing check |
|---|---|---|
| mtt_carry_dropped | ofs | `[ofs C] every row reads back as applied, rounded up to whole periods, all 33 bits` |
| mtt_reset_carry_dropped | ofs | `[ofs A] in reset every row reads its factory value rounded up to whole periods, all 33 bits` |
| readback_saturation_dropped | ofs | `[ofs C] GET_STREAM_INFO reads every row as applied, 0xFFFFFFFF past 32 bits` |
| crf_carry_dropped (the planted truncation) | ofs | `[ofs C] every CRF timestamp, all 64 bits, is a frame instant plus the CRF row rounded by Equation 14` |
| hold_keeps_ref (R677-2-F2) | det afterhold | `[det afterhold] after a hold, samples either side of +/-Ps/2 read the half-period phase` |
| offset_rounding_bypassed (anchor follows the 33-bit load) | ofs | unchanged |

`ofs` cases: A, B (CRF row 4,294,958,333, the largest that rounds under 2^32), C (run time: CRF 4,294,958,334, the
first past it; talker 3 0xFFFFFFFF), D (CRF 0xFFFFFFFF), E (factory rows at the boundary, graded in reset), F (run
time: CRF back to 2 ms, the carry clears). The old grader's 32-bit cast and its skip of CRF rows past 2^31 are gone;
the AAF phase against the CRF is graded on 64 bits for AAF rows under 2^31. 46 checks.

`det afterhold`: settle on +/-100 ns, an mr hold mid-window, then +/-10,416 ns: theta -31,250, committed correction
-32,768/256 (the slew limit), settled low. With `hold_keeps_ref`: theta 0.

milan_dp `[NOTIFY]` (N6), `sim_nxn.cpp:1445`: four steps from A counted at B, with SUCCESS, none to A, the push's
latency = the value set (5.4.5.1) and GET's applied value per step. Planted control: `gsi_mutants.py` mutant 9
("uc" kind, `UC_SINFO_STORED` -> `UC_SINFO_APPLIED`), the clean build run with the mutated ROM.

### Resources and route (round 3)

The carry moves the CRF offset by one bit, so route-1x1 was re-run at `81f09d06`, and again at `62ee1a8c` after D7's
rewrite, each on a clean clone under the round-1 recipe (`receipts/round3/route_81f09d06/`,
`receipts/round3/route_62ee1a8c/`, `scripts/round3/route.sh`, Vivado under the exclusive lock only). The two routes
give the same figures and the same per-block utilization:

| Figure | Record | Round 2 `f1643214` | Round 3 `81f09d06` = `62ee1a8c` | Delta to record | Tolerance |
|---|---:|---:|---:|---:|---|
| LUT | 49,613 | 49,709 | 49,733 | +120 | +500 |
| FF | 52,353 | 52,760 | 52,765 | +412 | +600 |
| SLICE | 15,725 | 15,797 | 15,804 | +79 | +80 |
| RAMB36 / RAMB18 | 74 / 25 | 74 / 25 | 74 / 25 | 0 | +0 |
| DSP | 14 | 13 | 13 | -1 | +0 (re-baseline recommended) |
| WNS / WHS | +0.215 / +0.036 | +0.305 / +0.036 | +0.282 / +0.016 | | floor +0.030 / 0 |

Route complete, gate exit 0 (`RESULT: PASS`), 42 and 39 minutes. Worst setup path: the Ethernet MAC's TX CRC counter
into `KL_gptp_gmii_launch`, outside the lane. The STOP-condition-1 measure (the carry's own cost)
against the round-2 route, per block (`hier_delta_vs_f1643214.txt`): `pres_round` +1 LUT / +3 FF, `crf_tx` +1 / +1,
the datapath's own logic (GSI word 3 from `rb_ns_o`) +8 / +1: about +10 LUT, no RAMB, against the 64-LUT bar. The
rest of the movement is placement in unchanged RTL (`csr` +59, `pp_shadow` -37, the top +17). Headroom left: LUT 380,
FF 188, **SLICE 1**.

### Gate table (round 3)

| Gate | Command | Head | Result | Receipt |
|---|---|---|---|---|
| full sweep, four shards in sequence, one runner, builds capped at two | `scripts/round3/sweep.sh` -> `scripts/run_all_suites.sh <out> --shard i/4` (pinned Verilator 5.050, CPython 3.12.13, tsn-gen `deca300`) | `62ee1a8c` | shard 0 14/15, 45,415 checks, `milan_dp` FAIL (7: the 3 designed pin failures in the timed leg, 4 of D8's premise in the N=4 leg; 7 legs not started); shard 1 16/16, 331,638; shard 2 17/17, 262,057 (`capture_coherence` 20,832 / dp 447 / campaign 35 of 35); shard 3 16/16, 1,540,268; 0 failures outside `milan_dp` | `receipts/round3/sweep_62ee1a8c/` |
| milan_dp, every leg | `scripts/round3/mdp_run.sh`: `make run ORDINARY_CASES="base crflic dynmap nxn nxndv nxn8 nxn4c nolpf prune ax1x1 aclk"`, then `make run-notify` | `32fb8fc2` | rc 0: 14 tallies, 11,629 checks, 0 failures, 2,415 s; notify leg rc 2: 441 checks, 3 failures (steps 3, 4 at the pin, by design) | `receipts/round3/milan_dp_32fb8fc2/` |
| notify leg and planted control with the gate fix (form (b), uncommitted in the submodule) | `make notify`; `python3 gsi_mutants.py 9` | `fe3ff999`, `32fb8fc2` | 441 checks, 0 failures; control caught at step 3 (3 of 441); at the pin the control reports its anchor absent | `receipts/round3/notify_sinfo/` |
| the three processor forms against the case and the never-set probe | one build, three ROMs | `fe3ff999` | pin 3 failures, (a) 2, (b) 0 (table above) | `receipts/round3/notify_sinfo/` |
| media_phase default target | `make -C tb/verilator/media_phase` | `cf85a578` (`ofs` again at `62ee1a8c`; suite in the sweep at `62ee1a8c`) | rc 0: 27 tallies, 326 checks, 553 s at three case jobs, five builds | `receipts/round3/media_phase_default_cf85a578/`, `media_phase_ofs_62ee1a8c/` |
| media_phase mutants | `make -C tb/verilator/media_phase mutants MUTANT_JOBS=2` | `cf85a578`; the six `ofs` mutants again at `62ee1a8c` | rc 0: 19 clean, 33/33 killed, 52 checks, 1,396 s | `receipts/round3/media_phase_mutants_cf85a578/`, `media_phase_ofs_62ee1a8c/` |
| route-1x1 resource gate | `scripts/round3/route.sh` (round-1 recipe, clean clone), `pp_resource_gate.py check --endpoint route-1x1` | `81f09d06`, `62ee1a8c` | exit 0 both: LUT +120, FF +412, SLICE +79, RAMB +0, DSP -1, WNS +0.282, WHS +0.016 | `receipts/round3/route_81f09d06/`, `route_62ee1a8c/` |
| Yosys, the changed tops | `syn/yosys/run.sh --top KL_crf_tx --top KL_mtt_round --top KL_aaf_capture_i2s --top milan_datapath` (sv2v v0.0.12, CI's pin) | `32fb8fc2` | rc 0, 4/4 PASS (`KL_mtt_round` 1,215 cells; `milan_datapath` 1,712,703), tied-input and tap-purity PASS. At `aea19ce7`: `KL_mtt_round` 0 cells (D7) | `receipts/round3/yosys_changed_tops_32fb8fc2/`, `yosys_small_tops*/` |
| lint | `python3 scripts/lint_rtl.py --check` | `32fb8fc2` | PASS 89 <= 89 | `receipts/round3/lint_32fb8fc2/` |
| docs gates (49) | `scripts/docs_gates.sh` | `32fb8fc2` (and `62ee1a8c`) | 49/49 rc 0. At `d790dd44`: 47/49 (doc style, naming), fixed in `cf85a578` | `receipts/round3/docs-gates-*/` |
| builder bank | `sw/builder/test_builder.py --require-elaboration --require-rv32` | `32fb8fc2` | rc 0, all gates pass except gate 11 not run (needs the separate Arty build tree), as round 2 | `receipts/round3/builder_bank_32fb8fc2/` |
| crf_tx | `make -C tb/verilator/crf_tx` | working tree before `81f09d06`; in the sweep at `62ee1a8c` | 129/129 | sweep receipts |
| comment audit (R678-2-R1) | `git diff e26f1816..HEAD` added source lines, review labels | `62ee1a8c` (no source comment since) | 0 matches | `receipts/round3/comment_audit.txt` |

Superseded this round: the sweep at `aea19ce7`, cancelled with TERM after D7 was found (`CANCELLED: TERM`).

### Environment notes (round 3)

- The round-2 `bin/python3` symlink pointed at a deleted interpreter; round 3 uses a wrapper that execs the round-2
  CPython 3.12.13 venv (a symlink to a venv's python loses its site-packages, so the image generator found no YAML).
- sv2v: CI pins v0.0.12; the host's default is v0.0.13, so the Yosys runs put v0.0.12 first on PATH.
- The Vivado route ran inside this unit's 12 GB cap (peak about 8.8 GB); no Verilator build beside it except one
  small harness. `memory.events` shows reclaim at the cap and no OOM kill.

### Follow-up recorded (not implemented, by ruling)

An applied value that changes without a SET (a media clock rate change with the same row as set) changes what
GET_STREAM_INFO reads and what every output stamps, with no SET_STREAM_INFO behind it: IEEE 1722.1-2021 7.5.2's
change in normal operation, for which an unsolicited notification would be due. Out of #770's scope; a new Issue.

## Round 2 (session 6, 2026-10-20 21:50 to 2026-10-21 04:10) -- STOP posted on F1

**Status: STOP at `2ff30f0d` on R678-1-F1 (the decision below); every other round 2 item done and every gate
green.** Not pushed; dev `78ca9bdf` not merged. TAKEN not re-posted. STOP:
https://github.com/kebag-logic/milan-fpga/issues/632#issuecomment-6306168406 (text: `public-stop.txt`).

### Round 2 commits (on `f1fda3f1`, oldest first)

| Commit | Subject |
|---|---|
| `b23e9e31e` | Aggregate the phase circularly against a tracking reference, settle only with every sample of four full windows in band, and drop a correction whose hold lands on its own snapshot edge |
| `1c58fd9d6` | Apply every stream output's presentation offset in whole media clock periods by the CRF transmitter's Equation 14 rule, and read the applied rows back through GET_STREAM_INFO |
| `920e7e93b` | Grade the detector's fold boundary, settled flag, range guard and snapshot holds alone, engagements at the fold and a local PHC step in the loop, and four AAF offsets against the CRF timing points, with a planted defect for each |
| `07f774252` | Close the I2S blend's frame on its I2S pair, the last of the frame to arrive, back-dated by the I2S front end's latency, and present each I2S pair on its own strobe instead of the next |
| `07c7eeaf4` | Grade the in-tree I2S and TDM8 blend at both interfaces' pins through the capture crossbar's frame bank, with the old closing pair and the late I2S pop planted |
| `133d1a1e0` | Convert the offset rows round and round with one divider and no per-row copy, name the rounder's ports for their unit, and hold the new harnesses to the C++ rules |
| `dd2563439` | Document the tracking fold, the every-sample settle, the snapshot hold, offsets in whole periods, the blend's I2S close and the listener decision with its measured cost, and record media_phase's fresh timing (#632, #764) |
| `61c2b468e` | Record the media_phase campaign's measured 837 s at four jobs |
| `814695e3a` | Name the factory-row loop for its row, so the fold's own default binding stays the one the builder's binding controls plant |
| `44508dd89` | Round every output's offset in one multiplier-free rounder, the CRF output stamping its applied row with its own converter no longer elaborated, and plant its raw row |
| `f16432140` | Unwrap each phase sample with one compare and one whole period on the reference's side, the same representative the difference form chose, in about half its logic |
| `2ff30f0dc` | Record the campaign's 751 s at the head and the route-1x1 headroom the listener decision is measured against |

### Outcome per item

| Item | Ruling | Status |
|---|---|---|
| R678-1-F1 | listener presents each sample at the pin at its presentation time | **STOP: decision needed** (below). Not implemented: every form of it exceeds the route-1x1 gate the same ruling holds, and it replaces the #386 render law six suites grade |
| R678-1-F2 | AAF offsets in whole periods, Eq. 14's rule; readback applied | done: `1c58fd9d`, `920e7e93`, `133d1a1e`; one multiplier-free rounder for every row with the CRF output on it (`44508dd8`) |
| R678-1-F3 | circular aggregation; settled needs every sample in band; detector and closed-loop cases | done: `b23e9e31`, `920e7e93`; cheaper identical unwrap `f1643214` |
| R678-1-F4 | a hold on the snapshot edge drops the correction | done: `b23e9e31`, `920e7e93` |
| R677-1-F1 | in-tree blend gets its constants, graded at its pins | done: `07f77425`, `07c7eeaf`; found D6 on the way |
| R677-1-F2 | PHC step hold case and mutant | done: `920e7e93` |
| R677-1-F3 | settled-flag and fold-range checks and mutants | done: `920e7e93` |
| R677-1-F4 | media_phase budget basis | done in the docs commit (fresh timing below) |
| R677-1-F5, R678-1-R1 | stale divider texts; PR body reviewer lines | done (docs commit; PR-BODY.md) |

### F1: the decision needed (published with STOP)

Measured before designing (`receipts/round2/ooc_render_setpoint/`): presenting at the timestamp holds each sample for
the offset less its arrival lead, about 1.9 ms at 2 ms, about 96 events: 128 rows per 8-channel stream where the
stage keeps 32. Vivado OOC of `KL_render_setpoint` at the 1x1 parameters: depth 5 = 456 LUT (128 LUTRAM), depth 7 =
1,006 LUT (512 LUTRAM). +550 LUT for storage alone against 469 LUT and 20 SLICE of route-1x1 headroom
(round-1 head: +31 LUT, +60 SLICE of +500/+80). Block RAM: two or three RAMB18 (the parity-split rows need a write
port each) against a RAMB tolerance of 0. The depacketizer frame FIFO is 2,048 bytes (`FIFO_DEPTH_BYTES`), about 8
PDUs of the shipping stream, under the 14 a 2 ms hold needs. Every option replaces the #386 fill law graded by
`render_setpoint`, `milan_dp` (render law, settle recentre, aclk), `follow_ring`, `milan_dp_gm_steps`,
`milan_dp_render`. One pop per stream cannot land two interfaces whose post-grid delays differ by a frame on one
presentation time without a per-interface frame delay; the Arty DAC path (`KL_i2s_playback`) has its own fill law and
elastic FIFO, fed by the raw render tap by default. Options for the decision: (a) a timestamp-snapped setpoint queue
in LUTRAM (+~550 LUT storage + logic) or BRAM (+2..3 RAMB18), (b) a presentation gate at a deepened depacketizer FIFO
(+1 RAMB36; delays the loopback ring and the DAC tap too). Either needs the route-1x1 record re-written by an accepted
growth decision, the supported offset range (queue depth), and the late/early PDU policy.

### Defects found this round

- **D6, the I2S pair one pop late (found by the blend grade with sample values at the pins).** `KL_aaf_capture_i2s`
  (and the flat golden `aaf_talker_i2s` it was split from) copied `cdc_pair_fifo`'s registered `rdata_o` on the pop
  edge, so every strobe carried the PREVIOUS pair: the I2S data lagged its strobe by a frame. With the round-1 blend
  close on the TDM pair the banked I2S pair was two periods older than the stamp (R677's probe counted strobes, not
  samples, so it saw one). The TDM front ends alias `rdata_o`; both I2S front ends now do too (`07f77425`). Affects
  the I2S-only and blend shapes (Arty, retired); the AX7101 shapes have no I2S capture.
- **The detector's arithmetic mean across the fold (R678-1-F3)**, reproduced on `f1fda3f1` by the new det cases
  (`receipts/round2/det_vs_f1fda3f1/`): balanced, 129:127, 160:96 and jittered half-period samples read theta 0 / 244 /
  7,812 / 10,678 units instead of about 31,250; meanin settled; snap on the edge committed 3000/256 for mr, the term
  disabled and not-LOCKED (broken history, PHC step and slew squash the rate commit and so passed).

### Changes (file:line at the docs commit; clause)

| File:line | Change | Clause |
|---|---|---|
| `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:482` | `PH_UW_C` (unwrapped sample width) | 10.8 |
| `KL_mmcm_drp_servo.sv:521` | `g_refold_guard`: one re-fold brings the window phase into 16 bits | 10.8 |
| `KL_mmcm_drp_servo.sv:740-747` | tracking reference `ph_ref_r`/`ph_ref_v_r`, `ph_allin_r` | 10.8 Eq. 15 |
| `KL_mmcm_drp_servo.sv:778-806` | per-sample band, tracking unwrap, window re-fold, settled needs every sample | 10.8 Eq. 15 |
| `KL_mmcm_drp_servo.sv:856-895` | reference update per counted window, seeded by an era's first sample, cleared by a hold | 10.8 |
| `KL_mmcm_drp_servo.sv:1017` | snapshot reads `ph_hold_w` on its own edge (R678-1-F4) | 10.8 |
| `hdl/ieee1722/crf/KL_mtt_round.sv` (new) | every output row rounded up to whole periods, KL_crf_tx's Eq. 14 rule, one round-robin divider, no multiplier (pass 2's numerator is pass 1's less its remainder) | 10.7 Eq. 14, 4.3.5, 10.8 Eq. 15 |
| `hdl/ieee1722/crf/KL_crf_tx.sv` | `ROUND_MTT_P` (default 1, its converter); 0 takes the rounded row, no converter elaborated (the datapath's instance) | 10.7 Eq. 14 |
| `KL_mmcm_drp_servo.sv:787-797` (at `f1643214`) | the unwrap as one compare and one period on the reference's side (identical mapping, receipts/round2/unwrap_equivalence) | 10.8 |
| `hdl/milan/milan_datapath.sv:3439-3462` | `pres_round` over the ACMP_SRC_C rows; `aecp_pres_applied_w` | 4.3.5 |
| `milan_datapath.sv:1447`, `:5238` | talkers stamp the applied rows; GET_STREAM_INFO reads them | 4.3.5; IEEE 1722.1 GET_STREAM_INFO |
| `hdl/ieee1722/crf/KL_media_if_latency_pkg.sv:98-113` | `close_pair()` (TDM only), `close_slot()`, `close_is_i2s()` | 4.3.5, 10.8 |
| `hdl/ieee1722/aaf/KL_chan_map_capture.sv:386`, `:643`, `:661` | `TDM_CLOSE_SLOT_P`: the frame closes on its last pair to arrive | 4.3.5 |
| `milan_datapath.sv:1246`, `:1260`, `:6106-6125` | the blend closes on its I2S pair, back-dated by the I2S front end's latency | 4.3.5, 10.8 |
| `hdl/ieee1722/aaf/KL_aaf_capture_i2s.sv:153`, `aaf_talker_i2s.sv:178` | pair data alias the FIFO's registered read (D6) | 4.3.5 |
| `milan_datapath.sv:6307`, `sw/builder/endstation_builder.py:4748`, `sw/builder/test_builder.py:21628` | R677-1-F5 stale divider texts, as written | -- |
| `sw/litex/milan_soc.py`, `syn/yosys/run.sh`, `syn/yosys/ooc.sh`, `tb/verilator/milan_dp/Makefile` | source lists: `KL_mtt_round.sv` | -- |

No top-level port, no register-map layout change (MCSRV_STAT[9]'s meaning tightened, read only). Module parameter
added: `KL_chan_map_capture.TDM_CLOSE_SLOT_P` (defaulted to the old behaviour). `close_pair()` lost its blend
argument (callers updated).

### New checks (planted mutant, failing words)

media_phase campaign, 28 mutants (17 kept; `fold_not_centred` retargeted because the window re-fold now gives the
short way, so its observable is the per-sample band):

| Mutant | Harness / case | Required failing check |
|---|---|---|
| tracking_fold_removed | det balanced | `[det balanced] the window phase reads the half-period phase` |
| window_refold_removed | det cross | `[det cross] past +Ps/2 the window phase re-folds to the short way` |
| settled_on_mean_only | det meanin | `[det meanin] settled never asserts with every sample outside the band` |
| snapshot_hold_ignored | det snap | `[det snap] mr on the closing edge` |
| settled_is_engaged (R677 P2) | det inband | `[det inband] settled first reads 1 at the close of the fourth full in-band window` |
| fold_range_guard_removed (R677 P3) | det range | `[det range] a timestamp 2^25 ns from the domain event is not sampled` |
| fold_not_centred (retargeted) | det inband | same as settled_is_engaged |
| step_hold_removed (R677 P1) | phcstep | `[phcstep] the phase term let go at the PHC step` |
| offset_rounding_bypassed | ofs | `[ofs A] every AAF output stamps whole periods from the CRF timing points` |
| blend_closed_on_tdm_pair | blend | `[blend 0] the I2S pair of every banked frame started at its pins inside +/-5 % of Ps` |
| i2s_pair_one_pop_late | blend | same |
| crf_row_raw (ofs_wrap) | ofs | `[ofs A] every CRF timing point is a frame instant plus the CRF row as read back` |

capture_coherence: three anchors moved to the renamed close-rule text (same mutants, same expected checks).
milan_dp nxn: `#632 GET_STREAM_INFO reads the offset applied, whole periods` (2,010,000 ns set, 2,020,834 read) on
an AAF row and the CRF row, then the existing #403 timestamp grade at those offsets.

### Area work this round (receipts/round2/ooc_blocks/)

Vivado OOC per block, LUT / FF / DSP:

| Block | f1fda3f1 | this round |
|---|---|---|
| `KL_mmcm_drp_servo` | 1,233 / 1,006 / 0 | 1,384 / 1,026 / 0 with the difference-form unwrap (`b23e9e31`); 1,342 / 1,026 / 0 with the sign-selected unwrap (`f1643214`, identical mapping: `receipts/round2/unwrap_equivalence/`, 558 M pairs, 0 mismatches) |
| `KL_mtt_round` (new) | -- | 122 / 155 / **1** with multiplies (`1c58fd9d`), 182 / 190 / 0 multiplier-free (`44508dd8`): pass 1's numerator is shifted adds of DEN, pass 2's is pass 1's less its remainder |
| `KL_crf_tx` | 404 / 298 / 1 (its own converter) | 246 / 169 / 0 at `ROUND_MTT_P = 0` (the datapath's instance): the CRF row comes rounded from `KL_mtt_round` |

The first rounder would have added a DSP against a DSP tolerance of 0; the routed `KL_crf_tx` held one DSP for its
own x 62,500. One multiplier-free rounder for every row and `KL_crf_tx` at `ROUND_MTT_P = 0` gives the image one DSP
fewer. Expected route movement against the round-1 head: about +130 LUT, +80 FF, -1 DSP; slices the open risk
(+60 of +80 used at round 1).

### Resources and route (round 2)

route-1x1 at `f1643214` on a clean clone under the round-1 recipe (`receipts/round2/route_f1643214/`):

| Figure | Record | Round 1 `a6ae20f9` | Round 2 `f1643214` | Delta | Tolerance |
|---|---:|---:|---:|---:|---|
| LUT | 49,613 | 49,644 | 49,709 | +96 | +500 |
| FF | 52,353 | 52,641 | 52,760 | +407 | +600 |
| SLICE | 15,725 | 15,785 | 15,797 | +72 | +80 |
| RAMB36 / RAMB18 | 74 / 25 | 74 / 25 | 74 / 25 | 0 | +0 |
| DSP | 14 | 14 | 13 | -1 | +0 (re-baseline recommended) |
| WNS / WHS | +0.215 / +0.036 | +0.276 / +0.032 | +0.305 / +0.036 | | floor +0.030 / 0 |

Route complete, gate exit 0, 40 minutes. Per block against the reference route (`hier_delta_vs_ref.txt`): servo
+382 LUT / +200 FF, `pres_round` (KL_mtt_round) +148 / +190, `crf_tx` -109 / -142, domain event +6 / +79,
crossbar -15 / +64, crf_rx +24 / +33; outside the lane the gPTP shadow -209 LUT (placement). Worst setup path: the
SoC's write-beat counter into a RAMB18 enable, outside the lane.

### Gate table (round 2)

| Gate | Command | Head | Result | Receipt |
|---|---|---|---|---|
| full sweep, four shards, two runners on two clean clones | `scripts/run_all_suites.sh <out> --shard i/4` (pinned Verilator 5.050, CPython 3.12.13, tsn-gen `deca300`) | `2ff30f0d` | 64/64 suites, 2,187,770 checks, 0 failures: shard 0 15/15 53,842 (tsn_fuzz 164 + 677 pass), shard 1 16/16 331,603 (media_phase 291 checks, ~533 s), shard 2 17/17 262,057 (capture_coherence inside its 2,400 s window, campaign 35/35), shard 3 16/16 1,540,268 | `receipts/round2/sweep_2ff30f0d/` |
| media_phase mutants | `make -C tb/verilator/media_phase mutants MUTANT_JOBS=4` | `f1643214` (`2ff30f0d`: a Makefile comment and a doc paragraph) | rc 0: 18 clean, 28/28 killed, 46 checks, 751 s | `receipts/round2/media_phase_mutants/` |
| media_phase suite timing (R677-1-F4) | `make` at the default CASE_JOBS | working tree before `dd256343` | rc 0, 578 s with five builds | `receipts/round2/media_phase_suite/` |
| route-1x1 resource gate | round-1 recipe on a clean clone, `pp_resource_gate.py check --endpoint route-1x1` | `f1643214` (no RTL or build input changed since) | exit 0: LUT +96, FF +407, SLICE +72, RAMB +0, DSP -1, WNS +0.305, WHS +0.036, route complete | `receipts/round2/route_f1643214/` |
| lint | `python3 scripts/lint_rtl.py --check` | `2ff30f0d` | PASS 89 <= 89 | `receipts/round2/lint/` |
| docs gates (49) | `scripts/docs_gates.sh` | `2ff30f0d` | 49/49 rc 0 | `receipts/round2/docs-gates/` |
| Yosys | `syn/yosys/run.sh` (all tops); `--top` the six changed tops | `dd256343`; `f1643214` | 60/60 PASS, tap-purity PASS; the six changed tops PASS, tied-input PASS | `receipts/round2/yosys_all_tops_dd256343/`, `yosys_changed_tops_f1643214/` |
| builder bank | `sw/builder/test_builder.py --require-elaboration --require-rv32` | `f1643214` (it reads none of `2ff30f0d`'s changes) | rc 0, all gates pass except one not run for its recorded reason (needs a separate Arty build tree) | `receipts/round2/builder_bank_f1643214/` |
| aaf, crf_tx | `make -C tb/verilator/aaf`, `make -C tb/verilator/crf_tx` | working tree (in the sweep at `2ff30f0d`) | pass; crf_tx 129/129 | sweep receipts |
| detector vs f1fda3f1 | det cases on the round-1 servo | `f1fda3f1` servo | the cancellation and snapshot defects reproduced | `receipts/round2/det_vs_f1fda3f1/` |

### Environment notes (round 2)

- The sweep runner refuses an interpreter without `os.pidfd_open`; the standalone CPython 3.12.3 build on this host
  lacks it, so the sweep ran on CPython 3.12.13 (same CI constraint pins); the docs gates and lint ran on 3.12.3.
- Two clean clones, because concurrent sweeps in one tree share build directories (the runner refuses).
- MemoryCurrent reached 10-11 GB during the sweep, almost all page cache (anon under 1 GB, 8 GB inactive file).
- A Vivado OOC batch inherits `-generic` values between `synth_design` calls in one session; that run's third
  report was discarded (`receipts/round2/ooc_blocks/README.txt`).

### Loop design (unchanged gains; what changed)

Gains, poles and bandwidths as round 1 (phase pole 0.944, rate 0.70; ~0.018 / 0.11 Hz; clamp 256 ns per window).
The detector: each folded sample unwrapped against a tracking reference (the last counted window's re-folded phase,
or the era's first sample), summed, the window phase re-folded once. At +/-Ps/2 the estimate is the half-period
phase, so the pull is at the clamp and the fold is left within a window or two: closed-loop at +Ps/2 (2 ns inside)
and -Ps/2 with 8 ns truncation and +/-48 ns jitter, re-engaged at -0.49 Ps, in band 26.4 / 26.6 s, settled never
read outside the band.

## Round 1

**Status: REVIEW READY at `f1fda3f1` (2026-10-20, session 5).** Every gate passes at the head (gate table below):
the sweep (64 of 64 suites), the 17 phase mutants, route-1x1 within the resource gate and timing floor (at
`a6ae20f9`, RTL identical), lint, Yosys and the docs gates. route-1x1 had failed at `e96f3928` (R1); the servo
shrink passed it at `5537cc41` (R2) and again with the window cap at `a6ae20f9` (R3). The sweep found two fixture
timings that assumed the retired CRF divider (D5), fixed in `33a460db` and `f1fda3f1`. REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/632#issuecomment-6299127112 (head `f1fda3f1`).

- Assignment: https://github.com/kebag-logic/milan-fpga/issues/632#issuecomment-6284510903
- Addendum 1 (in/out latencies at the pins): https://github.com/kebag-logic/milan-fpga/issues/632#issuecomment-6284578201
- Addendum 2 (one reference per media clock domain; replaces addendum 1 item 1): https://github.com/kebag-logic/milan-fpga/issues/632#issuecomment-6284659263
- #764 report: https://github.com/kebag-logic/milan-fpga/issues/764#issuecomment-6283948176
- Lane: branch `632-764-media-phase` from dev `e26f1816` (checked: `git merge-base HEAD origin/dev` = e26f1816;
  origin = https://github.com/kebag-logic/milan-fpga.git). Not pushed (pushing is outside this lane).
- TAKEN (session 1): https://github.com/kebag-logic/milan-fpga/issues/632#issuecomment-6284564768. Not re-posted.
- REVIEW READY (session 5, head `f1fda3f1`): https://github.com/kebag-logic/milan-fpga/issues/632#issuecomment-6299127112

## Session history

| Session | What happened |
|---|---|
| 1 | TAKEN posted; stopped by the manager for addendum 1. No commit. |
| 2 | Stopped by the manager for addendum 2. No commit. |
| 3 | Four commits: `cd39fea0` servo phase loop; `b7d3ad20` domain event, phased CRF output, AAF time base; `5081c7b2` media_phase bench and two-interface pins; `dac4ce37` capture_coherence `[PIN]` leg. Cut by a host reset (memory error) at 10:00 with an uncommitted media_phase Makefile/suite-budget change. |
| 4 | Resumed 12:07. Found and fixed two defects in session 3's design (D1, D2 below) and one robustness gap (D3); committed the session-3 leftovers; wrote the docs; ran the gates. route-1x1 at `e96f3928` failed the resource gate (R1 below); began shrinking the servo, uncommitted, when the host reset at 14:01. |
| 5 | Resumed 14:10. Validated the shrink (all media_phase cases pass, OOC 1168 LUT / 982 FF), fixed six stale comments and the clamp mutant's removed anchor, added the HOLDOVER and INTERNAL let-go mutants, committed `6f4a2b46` + `5537cc41`; route-1x1 at `5537cc41` PASSED (R2). Found a window-phase wrap under a talker sending faster than it declares (D4) and capped the window (`e887d937`, `a6ae20f9`); route-1x1 passed at `a6ae20f9` (R3). One mutant survived the 16-bit phase (fixed, `e85df091`). The sweep found D5 (two `milan_dp` fixture timings, `33a460db`, `f1fda3f1`); every gate then passed at `f1fda3f1`; REVIEW READY posted. |

## Commits (base `e26f1816`)

| Commit | Subject |
|---|---|
| `cd39fea0` | Phase the media servo to the followed CRF stream: an exact fold, a type-2 term under a slew limit, and an integrator that carries its odd errors |
| `b7d3ad20` | Stamp the CRF output and the AAF talkers from the clock domain's media event, back-dated by each interface's derived latency |
| `5081c7b2` | Grade the phase loop at the silicon window and two interfaces at their pins, with a planted defect per loop term |
| `dac4ce37` | Grade the shipping talker's timestamps against its TDM pins in the coherence datapath leg |
| `9ca025c9` | Carry each frame's instant through the capture crossbar, count the marker latency to the frame's closing pair, re-fold the phase on a PHC slew, and grade three interfaces at their pins |
| `e96f3928` | Document the phase contract per source, the domain event and per-interface constants, the listener decision and the -0.46 Ps accounting (#632, #764) |
| `0ee46622` | Name the new event ports by their unit, split the phase harness's multi-declarators, and register the media_phase budget and mutation reader with the test-evidence gate |
| `f49851da` | Regenerate the module matrix and the CDC census for the domain event and the retired CRF divider crossing, and record the media_phase budget |
| `974f17df` | Follow the domain event's renamed PHC port in the phase campaign's back-dating anchor |
| `6f4a2b46` | Fold each phase sample to its own nearest period, take the window phase as its sum over the nominal PDU count on the low 32 bits of each instant, and grade the phase term's let-go at every hold |
| `5537cc41` | Document the per-sample fold, the window sum and the hold conditions with their let-go mutants (#632) |
| `e887d937` | Cap the phase window at the nominal count plus 1/32 so a talker sending faster than it declares cannot wrap the window phase, and grade the cap with a burst case |
| `a6ae20f9` | Document the phase window's sample cap and its burst case (#632) |
| `e85df091` | Give the uncentred-fold mutant the one phase bit its range needs, so it plants a fold into [0, Ps) rather than one that wraps back to the centred reading |
| `33a460db` | Size the #726 TX wrap run in TDM frames: the CRF talker now stamps every 96th domain event, and the counters fixture clocks the TDM bus with axis_clk |
| `f1fda3f1` | Wait out the CRF talker's slower cadence in the nxn legs: with no audio frame running it stamps every 96th media tick, 200,000 clocks at 100 MHz |

## R1: the resource gate at `e96f3928`, and the shrink

route-1x1 at `e96f3928` (`receipts/route_e96f3928/`): LUT 50,329 (+716 against the 49,613 record; tolerance +500),
FF 53,072 (+719; +600), SLICE 15,802 (+77; +80), DSP 14 (+0), WNS 0.048 ns (floor 0.030), WHS 0.033. Gate exit 1.
Per block against a route of the recorded baseline's RTL (another lane's route of dev `e9cbb676`, which equals the
record in every figure; `e26f1816` differs from it only in firmware tests and docs): servo +581 LUT / +381 FF, domain
event +6 / +79, CRF rx -11 / +65, CRF tx -22 / +51, capture crossbar -19 / +64; outside this lane's logic the
processor wrapper moved +384 LUT and the gPTP shadow -233 (no RTL change there: optimisation movement). The worst
setup path is in the soft CPU's DMA bridge (20 levels, 100 MHz), not in this lane's logic.

The shrink (`6f4a2b46`), each step measured with `syn/yosys/ooc.sh KL_mmcm_drp_servo` (`receipts/ooc/`):
base 865 LUT / 792 FF; `974f17df` 1,457 / 1,183; now 1,168 / 982.
- the PDU-to-PDU unwrap and its runaway re-fold removed: each sample folds to its own nearest whole period, so every
  pull is the short way by construction (the slew case's 27 us re-acquired as its 6.2 us fold, as before);
- the window mean's division removed: Theta is the window sum over the nominal 256 PDUs, a shift (a short window
  only pulls less; it reads settled only when full); the divider is now by the constant Ps alone;
- the detector takes the low 32 bits of the domain event and of the CRF timestamp (their difference is exact within
  2^31 ns; the fold range is 2^25 ns, 33.5 ms, against a 2 ms default Max Transit Time);
- the PI operand 48 -> 40 bits; `KL_crf_tx`'s registered event instant dropped (the engine takes `ev_ns_i` on the
  event's cycle);
- the hold replaces the re-fold: every hold condition lets the term go and spoils the open window. Each case now
  grades the let-go (`phase_o[20]` low within 5 to 200 ms of its event), with a mutant per hold condition.

## R2: route-1x1 at `5537cc41` passes

`receipts/route_5537cc41/`: LUT 49,643 (+30), FF 52,662 (+309), SLICE 15,782 (+57 of +80), RAMB36 74, RAMB18 25,
DSP 14, WNS +0.418 ns, WHS +0.013 ns, route complete; gate exit 0. Per block against the reference route
(`hier_delta_vs_ref.txt`): servo +274 LUT / +180 FF, domain event +6 / +79, CRF rx +8 / +33, CRF tx -17 / -14,
capture crossbar -60 / +63; outside the lane the processor wrapper -106 LUT and the gPTP shadow -238. Comparing the
two routes, the processor wrapper's movement alone swung by 490 LUTs (+384 at `e96f3928`, -106 here) with no
processor RTL change: the route's LUT figure carries a few hundred LUTs of placement-dependent movement that this
lane does not control. The worst setup path is the SoC's AXI-Lite-to-Wishbone bridge, outside the lane.

## R3: route-1x1 at `a6ae20f9` (the head) passes

`receipts/route_a6ae20f9/`: LUT 49,644 (+31 of +500), FF 52,641 (+288 of +600), SLICE 15,785 (+60 of +80), RAMB36 74
(+0), RAMB18 25 (+0), DSP 14 (+0), WNS +0.276 ns (floor +0.030; fall -0.061 is a rise), WHS +0.032 ns (floor 0),
route complete; gate exit 0. Per block against the reference route: servo +264 LUT / +180 FF, domain event +6 / +79,
CRF rx -1 / +33, CRF tx -15 / -14, capture crossbar -5 / +64; processor wrapper -44 LUT, gPTP shadow -232. The
worst setup path is the existing reset synchroniser into the servo's 200 MHz phase-shift domain (`psrst_sync_r`, one
LUT, 3.8 ns of routing, unchanged RTL): placement-dependent, above the floor. Not re-recorded (see the decision).

## D4: the window phase could wrap (found in session 5, fixed)

The window phase is the window sum over 256 in 16 bits; 268 samples near Ps/2 overflow it. `KL_crf_rx` checks
the declared interval (96) and the 2 ms timestamp spacing, but not the arrival rate, and it consumes EARLY PDUs, so
a talker sending faster than it declares puts more than 256 samples in a window while its timestamps stay within the
33.5 ms fold range (about 15 extra). With samples within 0.0015 Ps of Ps/2 that window's phase wrapped sign: one
window's pull, at the slew limit, the wrong way. Fix (`e887d937`): a window keeps at most `PH_CAP_C` = 264 samples
(256 + 1/32); an elaboration guard proves 264 x Ps/2 / 256 inside 16 bits. New `burst` case: the talker sends every
1.92 ms for 0.6 s from a servo window boundary (267 PDUs in 512 ms); the window keeps exactly 264, the phase holds.
Mutant `window_cap_removed` fails `[burst] the window the burst filled kept exactly 264 samples, the cap` (max 267).
OOC unchanged (1,168 / 982).

## Defects found in session 4 (and fixed)

- **D1, the AAF time base latched at the tick (found by the new `[PIN]` check).** `capture_coherence` dp leg,
  engagement DP-band-true+0 (one cycle before the walk's crossing): stamps exactly 20,833 ns off their frame. When a
  frame closes ON the tick's cycle with none pending, the crossbar's walk takes the closing frame (#74 item 2
  coincidence law) but `aaf_tbase_r` latched the domain event of the frame before. Fix: the frame's instant is banked
  in `KL_chan_map_capture` beside the frame and loaded into the walk with it (`tdm_close_ns_i` -> `tdm_frame_ns_r` ->
  `tdm_walk_ns_o`), fed by `KL_media_domain_event.mark_ns_o`. After the fix: max 15 ns at that engagement.
- **D2, the marker latency counted to the frame's end (found by reviewing every shipping shape).** The crossbar closes a
  frame on the last pair it KEEPS (at most four), so on the 8x8 TDM32 shape the marker is pair 3 of 16 (a quarter
  of the frame in) and on the Arty I2S blend it is TDM pair 2; session 3 derived the latency as one whole frame.
  Those shapes' events would have been 0.75 Ps and 0.25 Ps off. Fix: `close_pair()` and `pair_end_bits()` in
  `KL_media_if_latency_pkg`; the datapath derives from `CMAP_TDM_FRAME_PAIRS_C`. The 1x1 value is unchanged
  (20,964 ns). New interface C in the synthetic shape: the 8x8's own TDM32 front end on 98.304 MHz, graded at
  every slot's pin, max 30.6 ns; its planted control (C counted to the frame's end) fails.
- **D3, a PHC policy slew did not re-fold (found by review against #545).** A slew below the unwrap's runaway bound
  (87 us) accumulated in the unwrapped phase and the loop pulled it back the long way. Fix: `phc_slew_q_r` in
  `ph_hold_w`. New `slew` case (27 us at 200 ppm): re-acquired in 20.0 s from +0.30 Ps, the short way; its
  planted control fails (phase out of band, 10,325 ns). Superseded in session 5: no unwrap remains, so the slew
  now holds the term (graded by the let-go check and `slew_hold_removed`) and the short way is the fold's.

## Changes (file:line at `f1fda3f1`, clause)

| File:line | Change | Clause |
|---|---|---|
| `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:46-92` | banner: the phase term, its per-sample fold, window sum, cap, gains, poles, slew limit, hold conditions | Milan v1.2 7.6.1; IEEE 1722-2016 10.7 Eq. 14, 10.8 Eq. 15, 4.3.5 |
| `KL_mmcm_drp_servo.sv:323-333` | parameters `FS_HZ_P`, `PH_GAIN_LSH_P`, `PH_SLEW_NS_P`, `PH_MIN_PDU_P`, `PH_SETTLE_WIN_P` | 10.8 |
| `KL_mmcm_drp_servo.sv:438` | `IF_C = 8` integrator fractional bits (#764 floor) | 7.6.1 |
| `KL_mmcm_drp_servo.sv:444-507` | Ps as 62,500/3 exactly; fold range 2^25 ns; nominal 256 PDUs per window; `PH_CAP_C` 264 with its guard; slew clamp | 10.8, Milan 7.3.2 |
| `KL_mmcm_drp_servo.sv:703` | `ph_hold_w`: outside LOCKED, term off, mr toggle, broken history, PHC step or slew | 10.8 |
| `KL_mmcm_drp_servo.sv:763-831` | `phase_det`: per-PDU exact fold in 1/3 ns (restoring divider by Ps), window sum capped at 264, Theta = sum >> 8, verdicts | 10.7, 10.8 |
| `KL_mmcm_drp_servo.sv:836` | `pi_isum_x_w`: integ + e/2 + phase term in fixed point | 7.6.1 |
| `KL_mmcm_drp_servo.sv:948` | the phase term clamped to the slew limit, one window late | 10.8 |
| `KL_mmcm_drp_servo.sv:1308-1318` | `ph_settled_o`, `phase_o`; `MCSRV_STAT[9]` | 10.8 |
| `hdl/ieee1722/crf/KL_media_domain_event.sv` (new) | the domain media event: marker back-dated, `mark_ns_o`, liveness, alt tick | 4.3.5, 10.8 |
| `hdl/ieee1722/crf/KL_media_if_latency_pkg.sv:78-118` (new) | `cyc_ns`, `half_cyc_ns`, `close_pair`, `pair_end_bits`, `mark_lat_ns`, `slot_msb_ns` | 4.3.5, 10.8 |
| `hdl/ieee1722/crf/KL_crf_tx.sv:388-394`, `:480-483` | event grid = every 96th domain event; ts = its instant + Eq. 14 offset; /512 divider and its cdc_pulse retired | 10.7 Eq. 14, 4.3.5 |
| `hdl/ieee1722/crf/KL_crf_rx.sv:488` | `ts_p_o`/`ts_o`: the consumed timing point | 10.8 |
| `hdl/ieee1722/aaf/KL_chan_map_capture.sv:451`, `:654`, `:1284` | the frame instant banked with the frame and loaded into the walk (D1) | 4.3.5, 10.8 |
| `hdl/milan/milan_datapath.sv:6078-6108` | domain event, closing-pair latency (D2), AAF time base from the walk (the packetizer reads its low 32 bits) | 4.3.5, 10.8 |
| `milan_datapath.sv:6150-6155`, `:6320`, `:5948` | servo phase operands (low 32 bits); CRF output events; CRF rx timing point | 10.8 |
| `sw/litex/milan_soc.py`, `syn/yosys/run.sh`, `syn/yosys/ooc.sh`, `tb/verilator/milan_dp/Makefile` | source lists for the two new files | -- |
| `scripts/lint.budget` | crf 4 -> 3 (one SYNCASYNCNET fewer with `KL_crf_tx`'s cdc_pulse gone) | -- |
| `scripts/run_all_suites.sh`, `scripts/suite_shards.py`, `scripts/measure_test_evidence.py`, `scripts/measure_test_evidence_readers.py` | media_phase budget 900 s (provisional), its reader disposition | -- |
| `tb/verilator/milan_dp/stream_counters.py:180-189`, `stream_counters.hpp:300-304`, `sim_nxn.cpp:5046-5052`, `:7757-7760` | fixture waits sized for the CRF talker's domain-event cadence (D5) | -- |
| docs: `docs/design/MEDIA_CLOCK_FOLLOWING.md` (Phase alignment), `docs/design/TIME_SYNC.md`, `docs/testing/TESTING.md`, `CHANGELOG.md`, generated module matrix and CDC census, `hdl/*/README-tests.md` | contract, constants, decision, accounting, proof table | -- |

No top-level port, no register-map layout change: one reserved read-only bit, `MCSRV_STAT[9]`, now reads the phase
settled (STOP condition 1 allows new read-only status fields). Module ports changed: `KL_mmcm_drp_servo` (phase
inputs, `phase_o`, `ph_settled_o`), `KL_crf_tx` (`clk_audio_i`/`ptp_ns_i` -> `ev_p_i`/`ev_ns_i`), `KL_crf_rx`
(`ts_p_o`/`ts_o`), `KL_chan_map_capture` (`tdm_close_ns_i` defaulted, `tdm_walk_ns_o`).

## New checks (planted mutant, failing words)

media_phase campaign (`make -C tb/verilator/media_phase mutants`), 17 mutants (`tb/verilator/media_phase/phase_mutants.py`):

| Mutant | Case | Required failing check |
|---|---|---|
| phase_term_removed | engage | `[engage] phase inside +/-5 % of Ps within 45 s of the event` |
| phase_sign_flipped | engage | `[engage] phase held inside +/-5 % of Ps to the end` |
| rate_damping_removed | engage | `[engage] phase inside +/-5 % of Ps within 45 s of the event` |
| integrator_floored | carry | `[carry] the integrator moved by exactly sum(e) / 2 (no LSB floored)` |
| slew_clamp_removed (clamp at Ps/2) | engage | `[engage] the pull is slew-limited` |
| fold_not_centred | engage2 | `[engage2] the pull went the short way` |
| history_hold_removed | step | `[step] the phase term let go at the reference's history restart` |
| mr_hold_removed | mr | `[mr] the phase term let go at the mr toggle` |
| holdover_hold_removed (state and history terms; either alone suffices, so one alone survives, measured) | holdover | `[holdover] the phase term let go at HOLDOVER` |
| idle_hold_removed (state term and the IDLE reset) | internal | `[internal] the phase term let go at INTERNAL` |
| window_cap_removed (D4) | burst | `[burst] the window the burst filled kept exactly 264 samples, the cap` |
| slew_hold_removed | slew | `[slew] the phase term let go at the slew level` |
| domain_event_not_backdated | engage | `[engage] every DUT CRF timestamp is a frame instant of its own grid` |
| crf_output_off_grid | engage | `[engage] every DUT CRF timestamp is a frame instant of its own grid` |
| pins_b_constant_dropped | pins | `[pins B] every stamped frame instant is each slot's MSB pin instant less its offset, inside +/-5 % of Ps` |
| pins_constants_swapped | pins | `[pins A] ...and inside the derivation` |
| pins_c_closed_at_frame_end (D2) | pins | `[pins C] every stamped frame instant is each slot's MSB pin instant less its offset, inside +/-5 % of Ps` |

The let-go checks are new in session 5 (`sim_main.cpp` `watch_letgo`/`check_letgo`): the engaged bit `phase_o[20]`
must read low on some datapath cycle within 10 ms (step), 5 ms (mr, INTERNAL, slew) or 200 ms (HOLDOVER) of the
event. The session-4 mutants `refold_removed` and `slew_refold_removed` targeted the unwrap, which no longer exists.

capture_coherence (`mutants.py`, default target), the five #632 mutants of 25:

| Mutant | Leg | Required failing check |
|---|---|---|
| the live PHC at the walk | dp | `[PIN] every slot's MSB pin instant, less its slot offset, is its AAF timestamp less the presentation offset, inside +/-5 % of Ps` |
| the time base latched at the tick (D1) | dp-band | same |
| the marker latency's frame term dropped | dp | same |
| the marker latency's write term dropped | dp | `[PIN] ...and inside the marker latency's derivation` |
| the walk's instant latched at the snapshot (D1) | chmap | `F: tick-cycle: col 1 walk instant is frame 2's` |

Positive controls: `[PIN] control: the same stamps graded without the per-slot constant are refused`; the
clean builds of every leg pass first.

## Loop design (gains, bandwidths, why)

- Units: 1 trim unit = 1 ns per 512 ms window of rate = 1/512 ppm; the plant moves the rate one unit per unit.
- PI per window: `integ += e/2 + 3/128 x Theta_ns` (Theta: last window's phase, its sample sum over the nominal 256,
  clamped), `u = integ + e/4`.
- Linear model (desk, `receipts/loop/poles.py`, output `poles.log`, the g = 3/128 row): poles 0.944 (phase; time constant 17
  windows = 8.9 s), 0.70 (rate; 2.8 windows = 1.4 s), -0.40, 0. Phase bandwidth about 0.018 Hz, rate about 0.11 Hz:
  six times apart, so the rate loop has settled before the phase moves, and the phase term never fights it.
- Slew limit: Theta clamped at +/-5,461 ns, which makes the integrator settle at e = -256 ns per window: the phase
  moves at most 256 ns a window = 0.5 ppm. Inside the 2 ppm lock test (no LOCKED drop, no CLOCK_DOMAIN count) and
  glitch-free through the MMCM fine phase shift (no slip; TDM frames continuous).
- Pull-in from Ps/2: ~41 windows at the clamp, then the pole: 23-28 s measured.
- Fold exact: Ps = 62,500/3 ns, worked in 1/3 ns (3d mod 62,500 by a restoring divider by the constant Ps, 29
  cycles; PDUs are 2 ms apart). Each sample folds to its own nearest period; Theta = window sum >> 8 (nominal 256).

## Latency constants (per interface, derivation)

Marker latency = closing pair's last bit (2(k+1) word_bits + d - 1 bit periods) + FIFO write + 4.5 datapath cycles
(`receipts/latency/` evaluates the package): 1x1 TDM8 master 20,964 ns; 8x8 TDM32 master 5,308 ns; Arty TDM8+I2S
blend 15,756 ns; Arty I2S 21,126 ns; TDM8 slave 21,004 ns; synthetic TDM4 d=0 20,802 ns. Slot k pin offset:
(k x word_bits + d) bit periods. Listener post-grid: crossbar (streams x 4 + 2 cycles) + bank walk 9 cycles + adopt
wait phi (0.229..21.059 us, per lock) + slot offset: NOT compensated (see the open decision).

## -0.46 Ps accounting (addendum item 4)

`receipts/acct/`: base KL_crf_tx beside the TDM8 master, one audio clock and reset, three reset phases: the old CRF
divider event sits +40.4..+59.9 ns (+0.002..+0.003 Ps) after the frame sync at the pins. So the constant is the old
AAF stamp's distance from its own frame: marker latency (+0.006 Ps folded) + capture age. -0.46 Ps folds to +0.54;
less 0.006, plus 0.0025: 0.536 Ps = 11.2 us = ~559 axis cycles, unique in the recorded 256..785 band.

## Open decision (published with REVIEW READY)

The listener's post-grid pin delay cannot be "counted against the presentation time offset": the render path
(`KL_render_setpoint`) presents by fill, 8 events after accept, not at the avtp_timestamp. A timestamp-driven render
is a listener-datapath change outside the media-clock chain (STOP condition 3). Constants derived and documented.

## Stale text left outside the scope (follow-up)

`configs/endstation_ax7101_8x8.yaml:159` comment, `sw/builder/endstation_builder.py:4009-4011` comment and `:4748`
build-plan text, `sw/builder/test_builder.py:21628` comment, all "KL_crf_tx /512". The builder and configs are
outside the media-clock chain; build plans are untracked.

## Resource before/after, route timing

| Measure | Base (record, `e26f1816` inputs) | `e96f3928` | Head (`a6ae20f9` = `e85df091` RTL) |
|---|---:|---:|---:|
| route-1x1 LUT | 49,613 | 50,329 (+716, fail) | 49,644 (+31) |
| route-1x1 FF | 52,353 | 53,072 (+719, fail) | 52,641 (+288) |
| route-1x1 SLICE | 15,725 | 15,802 (+77) | 15,785 (+60) |
| RAMB36 / RAMB18 / DSP | 74 / 25 / 14 | 74 / 25 / 14 | 74 / 25 / 14 |
| WNS / WHS | +0.215 / +0.036 ns | +0.048 / +0.033 ns | +0.276 / +0.032 ns |
| servo, routed hierarchy | 897 LUT / 814 FF | 1,478 / 1,195 | 1,161 / 994 |
| servo, Yosys OOC | 865 / 792 | 1,457 / 1,183 | 1,168 / 982 |

Details and per-block movements: R1, R2, R3 above.

## Gate table (head `f1fda3f1`; the RTL is identical since `a6ae20f9`, where the route ran)

| Gate | Command | Result | Receipt |
|---|---|---|---|
| route-1x1 resource gate | `syn/ooc/pp_resource_gate.py check <gateware> --endpoint route-1x1` after the recipe route | exit 0: LUT +31, FF +288, SLICE +60, DSP/BRAM +0, WNS +0.276, WHS +0.032, route complete | `receipts/route_a6ae20f9/` |
| media_phase mutants | `make -C tb/verilator/media_phase mutants MUTANT_JOBS=4` at `e85df091` (no media_phase or RTL file changed since) | rc 0: 10 clean cases, 17 of 17 mutants fail their named checks (27 checks, 0 failures) | `receipts/media_phase_e85df091/mutants.log` |
| full sweep, shards 0-3 | `scripts/run_all_suites.sh <out> --shard i/4` (pinned Verilator 5.050, CPython 3.12.3, tsn-gen `deca300`) | shard 0 at `f1fda3f1`: 15/15, 52,903 checks, 0 failures (`milan_dp` included); its `tsn_fuzz` campaigns re-run with tsn-gen at `f1fda3f1`: 164 + 677 pass, all campaigns passed. Shard 1 at `e85df091`: 16/16, 331,441 checks, 0 failures (`media_phase` included; the diff to `f1fda3f1` is three `milan_dp` fixture files, which no shard-1 suite compiles). Shard 2 at `f1fda3f1`: 16/17 under the runner, 262,022 checks, 0 failures, and `capture_coherence` killed by the 2,400 s wall clock on two CPUs (result unknown), re-run alone at `f1fda3f1` inside the same budget: PASS in 21 min (run 20,832 checks, dp 447, campaign 35 of 35 with all 25 mutants caught; the runner's `suite_tally.py --verdict` rc 0). Shard 3 at `f1fda3f1`: 16/16, 1,540,268 checks, 0 failures | `receipts/sweep_f1fda3f1/` (with `shard2_capture_coherence_uncontended/`), `receipts/sweep_e85df091/shard1/` |
| lint | `python3 scripts/lint_rtl.py --check` | rc 0: 89 <= ratchet 89 | `receipts/lint_f1fda3f1.log` |
| Yosys synthesis gate | `syn/yosys/run.sh` (serial, every top) at `e85df091` (RTL identical) | rc 0: 59 of 59 tops PASS; tap-purity PASS | `receipts/yosys_e85df091/` |
| docs gates (49, the docs workflow's) | `scripts/docs_gates.sh` in the output dir | all 49 rc 0 at `f1fda3f1` | `receipts/docs-gates/` |
| servo OOC (Yosys) | `syn/yosys/ooc.sh KL_mmcm_drp_servo` | 1,168 LUT / 982 FF / 3 DSP (Vivado maps none) | `receipts/ooc/` |

Earlier, superseded: route-1x1 at `e96f3928` exit 1 (R1); at `5537cc41` exit 0 (R2); the mutant campaign at
`a6ae20f9` had one survivor, `fold_not_centred`, fixed in `e85df091` (`receipts/media_phase_a6ae20f9/`).

## Sweep launch note (session 5)

The first launch at 16:36 named shards `1 2 3 4` (they are 0-indexed, 0..3) and pinned them to CPUs 0-5 (session
4's script; this session is booked on 112-127). It was cancelled with TERM after 5 minutes (`CANCELLED: TERM`),
`sweep.sh` now derives its CPUs from the session's affinity, and the sweep was re-run as shards 0..3.

## D5: milan_dp counters-8 failed in the sweep (session 5, fixed in the fixture)

Sweep shard 0 at `e85df091`: `milan_dp` FAIL, `[726 TX] restart/wrap emitted enough got=0x0 exp=0x1` (both
phases) in `stream_counters.py --shape 8`; reproduced (`TX_RUN,0,8,0,2,2`: the CRF talker emitted 2 PDUs; base
`e26f1816` emits 8, AAF 64 in both). Cause: a fixture artifact the lane exposes. The nxn fixture toggles
`clk_audio_i` and `clk_tdm_i` 1:1 with `axis_clk`; the base CRF talker divided `clk_audio_i` (/512 /96: a PDU every
49,152 cycles on both shapes), the lane's counts 96 domain events, one per TDM frame: 2 x 8 x 32 = 512 cycles on
TDM8 (49,152 per PDU, as before) but 2 x 32 x 32 = 2,048 on the 8x8's TDM32 (196,608 per PDU). In hardware
`clk_tdm_i` is 98.304 MHz on that shape, so both are 48 kHz. make stopped there, so the cases after `counters-8`
(counters-*-frames, base, notify, crflic, dynmap, nxn*, nolpf, prune, ax1x1, aclk, render-mutants) never ran:
Fix (`33a460db`, test only): `stream_counters.py` passes the bus's slot count (`-DTDM_SLOTS_TB`, the same value as
`AUDIO_IF_SLOTS_P`) and `stream_counters.hpp` runs the TX wrap leg `400000 x TDM_SLOTS_TB / 8` cycles, so every
talker still crosses the six-PDU wrap seed: shape 8 now emits 9 and 8 CRF PDUs (base 8 and 8), shape 1 is
unchanged (same cycle count). The checks are untouched (`>6` emitted, counter follows the wire exactly). Then the
cases after `counters-8` were run at `33a460db` with `make -k` (`receipts/milan_dp_d5/`): all pass except `nxn4c`,
the Arty shape (TDM8 master with the I2S pair blended), three checks: `[CTRS-OUT] real q3/q4 stimuli reach every
AAF and CRF index`, `[CTRS-OUT] every real FRAMES_TX source raises dirty` (0xf of 0x1f), `class A off: a CRF PDU
still reaches the MAC`. Same cause: the nxn fixture leaves `clk_tdm_i` at 0 outside the counters build (the
fixture's own note: only `ax1x1` clocks the TDM master), so on nxn4c no audio frame runs, the domain event falls back
to the 48 kHz media tick (the designed liveness fallback) and a CRF PDU comes every 96 x 2083.3 = 200,000 clocks at
100 MHz, while the waits were sized for the old 49,152 (`RealPduWait` 52,000, `CRF_BUDGET` 160,000). The I2S-only legs
(nxn, nxndv, nxn8) keep 49,152 (I2S frame = clk_audio/512). Fix (`f1fda3f1`, test only): `CRF_PDU_MAX_CLK` = 200,000,
`RealPduWait` = it + 5,000, `CRF_BUDGET` = 2 x it + 10,000; nxn4c then passes with 0 failures. No other suite
compiles `sim_nxn.cpp` or the counters files (checked), so shard 1's pass at `e85df091` stands for the head.

## tsn-gen note (session 5)

The final shard 0 (`f1fda3f1`) passed 15 of 15 but `tsn_fuzz` declared its two field campaigns SKIPPED: the
tsn-gen checkout the sweep pointed at (another lane's temporary directory) was deleted between 16:38 and 18:07.
tsn-gen was rebuilt in this lane's scratch at CI's `TSN_GEN_REV` `deca300` (`packet_gen`, Release, as the rtl
workflow builds it) and `tsn_fuzz` re-run alone at `f1fda3f1` with it. At `e85df091` the campaigns had run (shard 0
of the superseded sweep).

## capture_coherence wall clock (session 5)

Shard 2 at `f1fda3f1` ran on two CPUs (its campaign sizes itself by affinity, and two keeps it at two builds):
`capture_coherence` hit the runner's 2,400 s wall clock with 24 of 25 mutants caught and the last in flight
(`TIMEOUT ... result UNKNOWN, not a failure`). Per the runner's contract it was re-run uncontended, alone, with the
campaign pinned to two units (`python3 mutants.py --jobs 2`, the same two builds at once) on more CPUs.

## Decision for the merge: the resource re-baseline

`docs/design/AREA_BUDGET.md` asks a merge that moves the shipping image to re-record its endpoints on the merge
result (`record --write`) with the budget and #234 findings text. That is outside the media-clock chain (STOP
condition 3), so it is not in this lane; the head's route passes the gate against the existing record. The
standalone endpoints' source list includes this lane's files (the OOC script keeps the integrated read set), so
their digests would change too; their figures should not, since the processor RTL is unchanged.

## Receipts

`receipts/INDEX.md` (generated from the files present).
