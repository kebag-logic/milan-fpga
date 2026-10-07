[A564]

Current status: REVIEW READY, Round 2, local head ba080007a402dced74fa74656338710e0b6cb880. All requested Round 2 gates have completed with rc 0. The saved retired-board calibration arm remains explicitly NOT RUN. The earlier STOP records below are history; ruling 6045752839 supersedes their timing interpretation and assignment 6046111178 authorizes this continuation. No push occurred.

STOP — ROUND 1B. All six full IOB checks pass, but the #645 overlay with `ExtraTimingOpt` misses the required setup margin: Slow 0 C and 85 C WNS +0.013 ns versus the +0.030 ns minimum, a 0.017 ns shortfall. Its WHS is +0.069 ns at those corners; Fast WNS/WHS is +1.561/+0.036 ns. Acceptance 4 is not met. Ruling 6042557053 requires STOP on any failed row. The head is unchanged; no directive retry, source change or further gate run was started after this result. All long jobs have ended.

Issue: #691. Branch: `691-rx-iob`. Base: `e21c1ca024d37ea188ad15b5c8f9c2dae18628df`.
Head: `35fb2a95007ce6dd1ec4f51c2dcb793800623cfd`.
Executor: [A564]. Independent reviewers: [R546] and [R547].

In round 1, the dev full-image synthesis reached the 570-second foreground bound in iterative area optimization and was terminated. It wrote no complete synthesis checkpoint. The matching previous #645 synthesis report records 29 minutes 34 seconds for synthesis alone. That round treated the command limit as a job limit; ruling 6042557053 authorizes detached jobs with bounded foreground waits. That round claimed no packing or timing pass for either full tree; round 1b results are below. `REFERENCE-SYNTHESIS.json` records the earlier report line, size and SHA-256. `COMMANDS.json` records this run's time and termination status.

In round 1, the full builder and last physical-clock simulation also exceeded the foreground bound. Those interrupted runs remain incomplete. Round 1b supplies their completed results below.

## Round 1b continuation

The manager ruling in comment 6042557053 authorized long jobs at the unchanged head. Round 1 evidence below is retained. Round 1b completed the builder rerun (rc 0, 1,220.57 seconds; one retired-board calibration arm NOT RUN), the final physical-clock leg (193 checks, zero failures, rc 0, 586.24 seconds), both full-image syntheses and all six implementation rows. Five timing rows pass; the sixth triggers STOP. Full IOB packing passes in all six rows: 21 PASS, one expected INERT, zero FAIL, including all nine required RX captures.

The failing row's implementation commands completed; the manual-margin qualification then returned rc 1. Positive timing slack alone does not satisfy the AX7101 +0.030 ns requirement in `docs/integration/BUILDING.md:667` and `docs/testing/RUNNING_TESTS.md:208`. No acceptance threshold was changed.

Each long job has a separate session, log, PID and return-code file in scratch `round1b/`. Foreground waits remain below nine minutes. Synthesis runs alone except for the authorized builder and physical-clock jobs. At most two implementation rows run together, with 12 threads each, under the exclusive lock. No candidate file or commit changed during this round.

## Authority and tree identity

Read exactly: the #691 body and assignment comment 6041364533; #645 STOP comment 6041331463; #475, its check and self-test; `CONTRIBUTING.md`, `docs/README.md`, `REQUIREMENTS.md`, the relevant build and test documentation.

The initial remote and head matched the assigned repository and base. The branch was clean. The second input was fetched as `origin/645-ring-slip`, head `2525eae9567865a8bc741901914bdf5a1caf2c26`. Work remained on the assigned branch. Isolated scratch exports were used for generated build products. Submodule top-level directories were verified before submodule Git operations. The shared installed dependencies were not edited.

| Input | Exact identity | State |
|---|---|---|
| Candidate from dev | Commit `35fb2a95007ce6dd1ec4f51c2dcb793800623cfd`; tree `430abfdcb667dded3fd9b874a0a69c464ae1bd7c` | Committed, clean |
| #645 round 2d plus this change | Base `2525eae9567865a8bc741901914bdf5a1caf2c26`; overlay tree `01f65c3b2693d2b1c494e0738b9562a1778740b5` | Scratch export only |

`SOURCE-PROVENANCE.json` proves that the 116 recorded synthesis inputs for each export remained unchanged after the final test-only commits. The two `*-synthesis-inputs.json` files give individual sizes and SHA-256 values. Compact placement preceded the test-only commits; production capture and generated synthesis inputs did not change afterward.

| Commit | Subject |
|---|---|
| `39c99efada3903471db256217c2e54637b2c93dd` | Keep GMII receive reset logic after IOB capture |
| `f3132d5e0b8fd0e187f0c47d1498ff49a95ee5b5` | Exercise GMII last-byte transitions under reset controls |
| `35fb2a95007ce6dd1ec4f51c2dcb793800623cfd` | Emit the simulation runner verdict on its own line |

## Mechanism and changes

The shipping AX7101 build instantiates GMII at `sw/litex/milan_soc.py:1454`. Its IOB constraints at `sw/litex/milan_soc.py:1490` cover eight data pins, RX-valid and RX-error. RX-error is unused and is INERT under the checker contract. MII RX has no required IOB constraint. This lane changes the actual GMII receiver through the existing patch series.

Each data/valid input flop now has a direct pad D, no reset and no enable. Reset is sampled in parallel, and its registered value masks the capture outputs. There is no input-flop synchronous reset for the control-set heuristic to move ahead of D. The output still represents the preceding edge, reset still takes effect at that edge, and `last` retains its original dependence on current pad-valid and delayed valid. The production fix has no preservation attribute. Only the deliberately defective fixture preserves its planted LUTs so that synthesis cannot repair the experiment.

| File:line | Change | Purpose |
|---|---|---|
| `sw/litex/patches/0007-liteeth-gmii-rx-capture.patch:13` | Resetless pad capture and sampled reset masking | Remove the input control-set dependency without adding latency |
| `sw/litex/patches/apply.sh:35` | Add the new patch immediately after the existing GMII patch | Reproduce the fix through the maintained series |
| `sw/litex/patches/README.md:11` | Describe capture and reset semantics | Document dependency behavior |
| `sw/litex/test_gmii_rx_capture.py:22` | Instantiate the actual receiver with controllable pads/reset | Test the real dependency implementation |
| `sw/litex/test_gmii_rx_capture.py:43` | Independent pad-sample oracle, frame boundaries and exhaustive byte/reset/valid cases | Detect latency, data and reset changes |
| `sw/litex/test_gmii_rx_capture.py:87` | Generate positive and reset-before-D placement fixtures | Exercise the real placement checker without editing generated RTL |
| `scripts/run_litex_sims.sh:101` | Add capture simulation to the pinned inventory | Keep the behavioral check in the aggregate gate |
| `sw/litex/iob_pack_selftest.py:386` and `:506` | Add a pad-to-LUT-to-register netlist arm | Refuse the original failure topology |
| `docs/integration/BUILDING.md:607` | Explain the capture mechanism and fixtures | Keep the authoritative build contract current |

No register-map, configuration selection, deployed image or hardware changes were made. No default all-fabric behavior was changed beyond the assigned RX capture structure. Generated artifacts remain outside the working tree.

## Tests and planted defects

| Test | Planted defect or exercised failure | Result and limitation |
|---|---|---|
| Capture comparison | Live reset replaces sampled reset in valid masking | Mutant returns 1; final harness catches it |
| Capture comparison | `source.last` forced to zero | Mutant returns 1; explicit frame-end transitions catch it |
| Capture comparison | Top data bit lost during capture | Mutant returns 1; exhaustive bytes catch it |
| Capture comparison, positive and original receiver | Every byte with both reset and valid levels; reset changes between edges and during frames; ready and unused error toggle | Both implementations pass 1,036 comparisons; `rx-controls.json` records all three refusals |
| Compact physical fixture | Preserved reset mask before D on all eight data pins and valid | Good capture: 9/9 ILOGIC PASS. Defective capture: 9/9 FAIL, child rc 1, before routing sentinel. Expected-refusal wrapper rc 0 |
| IOB self-test | New reset-before-D topology plus existing unsupported/misplaced structures and checker mutations | 22 arms, 21 mutants, no failure; rc 0 |
| Patch reconstruction and gate controls | Each of five patches omitted | Five patches reconstruct four files; stacked GMII patches compose; 5/5 missing-patch controls caught; rc 0 |
| Simulation inventory self-test | Existing inventory/runner failure controls | rc 0; the new test is a required inventory member |
| Standalone simulations | Existing CDC, timestamp, boot-freeze and memory-bridge regressions; capture mutations above | 5/5 pass, zero skipped. No new mutations planted in the four unchanged tests |
| RX filter | Existing malformed/drop/filter stimuli and two five-control groups | 78 functional checks plus 5+5 controls pass |
| RMON | Existing event-count and reset stimuli | 28+28 checks pass; no additional lane mutation |
| TX reset | Existing reset during transmission stimuli | 40 checks pass; no additional lane mutation |
| Link guard | Existing reset/liveness/link transitions | 104 checks pass; no additional lane mutation |
| Datapath prerequisite legs | Existing gPTP baseline, latency and grandmaster-step scenarios | 182, 182 and 104 checks pass |
| Default datapath pool | Existing protocol, shape, channel mapping, feature pruning and physical-clock scenarios | Round 1: all variants build and preceding 11 legs finish without failure; aggregate interrupted. Round 1b: final physical-clock executable rerun passes 193/0, rc 0. Constituent completion is recorded; no fresh aggregate verdict is claimed |
| Render mutation campaign | Existing six controls including dropped clock-source recentre trigger | 6/6 controls pass |
| Grandmaster-step mutation campaign | Existing six controls including lost CRF restart propagation and missing render recentre | 6/6 controls pass |
| Builder | Existing clock/configuration contracts and their planted negative cases, including patch omission, reset polarity, clock-source and descriptor/capacity mutations | Round 1 interruption retained. Round 1b complete rerun returns rc 0: all executed gates pass; gate 11 saved retired-board calibration report unavailable, explicitly NOT RUN |
| Full shipping placements | Real #645 tree previously failed RX packing; no additional defect planted in these runs | All six complete IOB checks pass; every row retains the raw report |
| Full shipping timing and qualification | Reject any declared corner below WNS +0.030 ns or WHS 0 | Five rows pass; #645 `ExtraTimingOpt` is correctly refused at +0.013 ns Slow WNS, rc 1 |

The physical negative control uses explicit preserved LUT2 instances only in the fixture. An ordinary combinational mask was optimized back into reset pins, so it did not preserve the intended defect. That earlier attempt is superseded. The first behavioral vector set missed the missing-last mutant; the frame transitions were added and all three mutants were rerun. The initial aggregate runner rejected a suffixed verdict line; the committed test now emits the exact required verdict and the aggregate rerun passes. None of those superseded runs is counted as current evidence.

## Acceptance coverage

| # | Acceptance | Current evidence | Status |
|---|---|---|---|
| 1 | Required RX captures robust to control-set remapping | Structural patch, threshold-100 fixture and all six full placements pack all nine RX captures | Met |
| 2 | IOB check passes on dev and #645 round 2d | Dev 3/3 and #645 3/3: 21 PASS, 1 expected INERT, zero FAIL per row | Met |
| 3 | RX behavior preserved and reset-before-D defect rejected | Round 1 capture, Ethernet, completed datapath legs and mutation checks; round 1b physical-clock completion: 193/0, rc 0 | Met by constituent runs; round 1 aggregate interruption remains recorded |
| 4 | Full shipping timing sweep with WNS/WHS per directive | All six rows measured; dev 3/3 and #645 2/3 pass; #645 `ExtraTimingOpt` Slow WNS +0.013 ns is below +0.030 ns | NOT MET — STOP |
| 5 | Default function/register map/image unchanged beyond capture | Seven-file diff remains unchanged at the assigned head | Met by change scope; independent review pending |

## Full-image timing coverage

Recipe: AX7101 `xc7a100t-fgg484-2`, shipping 1x1 TDM8 with eight wire channels, all-fabric control planes, 50 MHz Milan clock, inverted transmit clock and shipping floorplan. Cacheless RV32 bare-metal management CPU; playback and render low-pass filter disabled; loopback and fabric gPTP enabled; ingress/egress latency 656/219 ns. Arguments derive from the unchanged shipping dry-run recipe. Synthesis `AreaOptimized_high`; optimize `ExploreArea`; routing and physical optimize `AggressiveExplore`; default seed. The staged scripts split the generated recipe at its saved checkpoints. Synthesis uses one thread; implementation uses 12 threads per row under the round 1b ruling. All physical jobs hold the prescribed lock.

Each corner cell below is WNS / WHS in ns. Required margins are WNS at least +0.030 ns and WHS at least zero at every corner. The 0 C and 85 C endpoint reports repeat fixed Slow/Fast timing models; they are not temperature-interpolated models. `TIMING.json` records TNS and THS too. `ROUND1-TIMING.json` preserves the unmeasured round 1 table.

| Tree | Placement directive | Full IOB check | Slow 0 C | Slow 85 C | Fast 0 C | Fast 85 C | Result |
|---|---|---|---|---|---|---|---|
| dev + fix | ExtraPostPlacementOpt | 21 PASS, 1 INERT, 0 FAIL | +0.492 / +0.040 | +0.492 / +0.040 | +1.660 / +0.007 | +1.660 / +0.007 | PASS |
| dev + fix | AltSpreadLogic_high | 21 PASS, 1 INERT, 0 FAIL | +0.064 / +0.052 | +0.064 / +0.052 | +1.638 / +0.029 | +1.638 / +0.029 | PASS |
| dev + fix | ExtraTimingOpt | 21 PASS, 1 INERT, 0 FAIL | +0.098 / +0.074 | +0.098 / +0.074 | +1.362 / +0.036 | +1.362 / +0.036 | PASS |
| #645 round 2d + fix | ExtraPostPlacementOpt | 21 PASS, 1 INERT, 0 FAIL | +0.238 / +0.102 | +0.238 / +0.102 | +1.518 / +0.036 | +1.518 / +0.036 | PASS |
| #645 round 2d + fix | AltSpreadLogic_high | 21 PASS, 1 INERT, 0 FAIL | +0.227 / +0.071 | +0.227 / +0.071 | +1.521 / +0.035 | +1.521 / +0.035 | PASS |
| #645 round 2d + fix | ExtraTimingOpt | 21 PASS, 1 INERT, 0 FAIL | +0.013 / +0.069 | +0.013 / +0.069 | +1.561 / +0.036 | +1.561 / +0.036 | FAIL |

Round 1 stopped dev synthesis at 570.14 seconds without a checkpoint. Round 1b completed that synthesis in 1,834.81 seconds and the #645 overlay synthesis in 1,776.64 seconds, both rc 0. Every implementation row completed placement, routing and reporting. Each has its complete 22-port IOB report, generated evaluation bitstream and layout manifest in scratch. The failed row's bitstream is not a passing candidate: margin qualification returned 1 after reports and bit generation. No artifact was deployed or substituted for the shipping image.

All 24 corner reports have zero TNS and THS. The five passing rows meet the additional setup margin; the sixth does not. Each clock-interaction report contains all four Ethernet crossings as `Max Delay Datapath Only` with an 8 ns requirement and positive slack; none contains an Unsafe row. The combined synthesis/implementation logs contain no rejected-constraint diagnostics (12-4739, 20-1307, 12-5201) and no critical warnings. `ROUND1B-CLOCK.json` records the six report extracts and warning census.

The failed Slow report locates its worst setup path at `ring-timing/ExtraTimingOpt/alinx_ax7101_signoff_Slow_0C_timing.rpt:2645`: `milan_datapath/pp_shadow/u_pp/u_notify/wr_ix_r_reg[1]/C` to `milan_datapath/pp_shadow/u_pp/u_tx_arbiter/slot_r_reg[1]/D`, in the 20 ns clock group. Data-path delay is 20.016 ns (5.548 ns logic, 14.468 ns route), with 41 logic levels. This identifies the reported path; it does not establish that the capture change caused the shortfall. No timing repair or directive substitution was attempted. `ROUND1B-STOP-EVIDENCE.json` retains the excerpt and threshold source.

## Gate table

Round 1b reruns and completions are recorded separately in `ROUND1B-GATES.json`; completed artifact sizes and hashes are in `ROUND1B-ARTIFACTS.json`. The first table gives round 1b reruns and completions. The second preserves round 1 receipts, including its interruptions. The resumed builder and physical-clock results supersede those two incomplete execution windows.

| Round 1b gate / receipt key | Result | Evidence |
|---|---|---|
| `builder` | rc 0, executed gates PASS; 1 NOT RUN | 1,220.57 s; absent gate 11 retired-board calibration report remains a limitation |
| `datapath-physical` | PASS, rc 0 | 586.24 s; 193 checks, zero failures |
| `dev-synthesis` | PASS, rc 0 | 1,834.81 s; completed checkpoint |
| `dev-ExtraPostPlacementOpt` | PASS, rc 0 | 854.45 s; complete IOB and four corners |
| `dev-AltSpreadLogic_high` | PASS, rc 0 | 1,593.80 s; complete IOB and four corners |
| `dev-ExtraTimingOpt` | PASS, rc 0 | 1,920.74 s; complete IOB and four corners |
| `ring-synthesis` | PASS, rc 0 | 1,776.64 s; completed checkpoint |
| `ring-ExtraPostPlacementOpt` | PASS, rc 0 | 967.47 s; complete IOB and four corners |
| `ring-AltSpreadLogic_high` | PASS, rc 0 | 1,428.62 s; complete IOB and four corners |
| `ring-ExtraTimingOpt` | FAIL, rc 1 — STOP | 1,675.62 s; IOB passes; Slow WNS +0.013 ns < +0.030 ns |
| `dev-pair`, `dev-third`, `ring-pair`, `ring-third` | Group receipts: 0, 0, 0, 1 | Waiting/lock ownership records; not additional independent gates |
| Complete root sweep, portability, native processor suites and behavior aggregate | NOT RUN in round 1b | Setup prepared before the final physical result; no run started after mandatory STOP |

Every PASS below has process rc 0. `COMMANDS.json` gives exact argument arrays and working directories with portable path variables. `GATES.json` also retains interrupted and superseded attempts. `ARTIFACTS.json` identifies raw logs, generated RTL and checkpoints by scratch-relative name, byte size and SHA-256.

| Gate or receipt keys | Result | Evidence |
|---|---|---|
| `rx-equivalence`, `rx-prepatch-control`, `rx-negative-controls` | PASS | 1,036 comparisons on both receiver versions; three behavioral mutants caught |
| `capture-place`, `placement-control-verdict` | PASS | Nine packed pads; preserved defect rejected on all nine |
| `capture-defect-preserved` | EXPECTED REFUSAL, rc 1 | Negative child result; wrapper verifies refusal and exits 0 |
| `iob-selftest`, `patch-contract`, `sim-inventory` | PASS | Checker, patch-series and runner controls |
| `litex-sims-final` | PASS | 5/5, no skip, 181.12 seconds |
| `ethernet-filter`, `ethernet-rmon`, `ethernet-reset`, `link-guard` | PASS | Counts in test table |
| `datapath-gptp`, `datapath-latency`, `datapath-gmstep` | PASS | Three prerequisite legs |
| `datapath-*-build` | PASS | All default variants compiled with two compiler jobs |
| `datapath-render-controls`, `datapath-gmstep-controls` | PASS | 6/6 and 6/6; 483.41 and 396.32 seconds |
| `datapath-pool` | INCOMPLETE, rc -15 | 570.43-second bound in final physical-clock leg |
| `builder`, `builder-chunk-01` | INCOMPLETE, rc -15 | 570-second bounds; twelve individual passes retained |
| `dev-elaborate`, `ring-elaborate` | PASS | Both shipping configurations generate successfully |
| `dev-synthesis` | INCOMPLETE, rc -15 | 570.14-second bound; no completed synthesis checkpoint |
| `lint` | PASS | Existing ratchet respected |
| `vendor-parser` | PASS | 81 owned plus 52 pinned processor files; 0 owned findings, 2 unchanged processor findings equal ratchet |
| `docs`, `doc-style`, `toc`, `em-dash`, `doc-paths` | PASS | Documentation and references |
| `py-idiom`, `shell-idiom`, `final-style` | PASS | Python, shell, prose and naming checks |
| `source-lists`, `source-selftests`, `source-shape` | PASS | Source inventories, processor derivation, CI event and sweep controls |
| `evidence`, `fail-fast`, `hardware-hygiene` | PASS | Existing test-evidence, failure propagation and hygiene ratchets |
| Complete general RTL sweep and portability gate | NOT RUN | Still pending at round 1b STOP; no claim of complete local verification bar |
| Hosted checks, local CI replica, independent review, merge checks | NOT RUN | No push or PR authorized; no review verdict claimed |

Round 1 service memory stayed below 9 GB; maximum across gate receipts was 8,014,589,952 bytes. Free space was above the 30 GB floor throughout, with 182,365,011,968 bytes free in its final recorded inspection. No heavy child remained after the final gate. Installed dependencies, source exports and large logs/checkpoints remain in scratch. This packet contains summaries and small evidence only.

Round 1b maximum sampled memory across job receipts was 10,716,278,784 bytes, below 13 GB. Minimum free space was 180,799,868,928 bytes, above the 30 GB floor. Every job has a completed rc file; none remains in flight. Source exports and preparatory packages for the unstarted broader gates remain in scratch. Packet files contain only documentation, small reports and artifact hashes/sizes.

## Reproduction and continuation

Variables: `REPO` is the candidate checkout; `SCRATCH` is its assigned scratch area; `PACKET` is this packet; `PYTHON` is the existing project Python environment; `BASE_PHY` is the original dependency tree with the preceding patch series; `RTL_SIM` is the pinned 5.050 simulator; `SYNTH` is the installed implementation executable; `SYNTH_LOCK` is the prescribed exclusive lock. `COMMANDS.json` substitutes those variables for machine-specific paths. Run gates without pipelines. For long jobs, use the round 1b detached-job and bounded-wait procedure.

For the targeted checks, use the isolated patched dependency in `SCRATCH/deps` as the first Python import path. It is a copied package from the original environment with the new patch applied; the shared installation was preserved.

```sh
cd "$REPO"
export PYTHONPATH="$SCRATCH/deps"
export PYTHONDONTWRITEBYTECODE=1
export PYTHONHASHSEED=0
export MILAN_LITEX_PYTHON="$PYTHON"
export VERILATOR="$RTL_SIM"
export VERILATOR_JOBS=2
export SIM_JOBS=2
export TMPDIR="$SCRATCH/tmp"
"$PYTHON" sw/litex/test_gmii_rx_capture.py
"$PYTHON" sw/litex/iob_pack_selftest.py
"$PYTHON" -c 'import sys; sys.path.insert(0,"sw/builder"); import test_builder as t; t.test_toolchain_patches_are_applied(); t.test_toolchain_patch_gate_bites()'
bash scripts/run_litex_sims.sh --selftest
bash scripts/run_litex_sims.sh "$SCRATCH/litex-sim-repeat"
```

`capture-check.tcl` and `capture.xdc` reproduce the compact placement. Generate both RTL files with the committed generator, create a separate directory for each case, copy the supplied XDC into each, and run the check under the exclusive lock. The positive process must return 0 with nine PASS rows; the negative process must return 1 with nine FAIL rows and no routing sentinel. Treat the expected negative return as data, then require those exact assertions in a wrapper that returns 0. Do not count the child refusal as a failed positive gate.

```sh
export REPO
"$PYTHON" sw/litex/test_gmii_rx_capture.py --emit-dir "$SCRATCH/capture-repeat"
mkdir -p "$SCRATCH/capture-repeat/capture" "$SCRATCH/capture-repeat/reset_before_d"
cp "$PACKET/capture.xdc" "$SCRATCH/capture-repeat/capture/capture.xdc"
cp "$PACKET/capture.xdc" "$SCRATCH/capture-repeat/reset_before_d/capture.xdc"
cd "$SCRATCH/capture-repeat/capture"
flock "$SYNTH_LOCK" "$SYNTH" -mode batch -nojournal -notrace -log vendor.log -source "$PACKET/capture-check.tcl" -tclargs capture
```

Run the same command from the sibling negative directory with `-tclargs reset_before_d`, handling its expected return in the assertion wrapper. `rx-controls.json` and the test table identify the three independent behavioral mutations; the retained `rx_controls.py` applies them to separate copied packages.

Round 1b follows ruling 6042557053. The detached job launcher retains a log, PID, command receipt and rc file for each long job. Wait in foreground intervals below nine minutes until every job ends. An elapsed wait is never a gate verdict. Synthesis precedes implementation; two implementation rows may share one held exclusive lock, with 12 threads each. Any packing or timing failure requires STOP with its numbers, without changing the directive or candidate.

`ROUND1B-GATES.json` gives portable command receipts. Scratch `round1b/implementation.py` runs placement, routing, reports and qualification in order. The updated stage generator preserves the generated shipping recipe while using the authorized thread limits. Original helper bytes remain in `round1b/stages-before.py` and `round1b/export-before.py`. The packet records hashes rather than copying build products or installed dependencies. Independent review and a reviewer-owned lens ledger remain required after acceptance evidence is complete.

## Review coverage

This is an executor handoff, not a review. No review was run in this session and no clean lens is banked.

| Lens | Covering round | Head |
|---|---|---|
| Conformance | Pending independent review | None |
| RTL | Pending independent review | None |
| Robustness | Pending independent review | None |
| Tests | Pending independent review | None |
| Docs | Pending independent review | None |

Round 1 TAKEN is comment 6041397049; its STOP is comment 6042535076. No new TAKEN was posted. The final authorized action is to publish the new `STOP-ROUND1B.md` comment on #691, naming this unchanged head and these numbers, then stop. No existing comment was edited or deleted. No push, PR creation, merge, hardware access or flashing occurred. Continuation requires a new ruling; this packet proposes no source or configuration change.

## Round 2

Assignment: issue #691 comment 6046111178. Review: PR #693 comment 6046104655.
Starting head: `35fb2a95007ce6dd1ec4f51c2dcb793800623cfd`.
Origin and PR head confirmed. Working tree initially clean.

Scope: regenerate the stale converted MAC model through its generator with the complete pinned patch series; commit and document the compact placement recipe; apply R1/R2 wording; add the recommended structural guard and controls. The capture implementation remains unchanged.

### Changes

| File:line | Change |
|---|---|
| `tb/verilator/gptp_txts/generated/mac_tx_chain.v:52,825,2208` | Regenerated RX declarations, output masking and clocked capture through the pinned converter. TX and every other stage are unchanged; exact diff in ROUND2-MODEL.diff. |
| `tb/verilator/gptp_txts/generated/manifest.json:17` | Generator updates only the Verilog hash to f3f110e9825516aa8ede44b56df5418aaf378e015e4e5f31ea1052616bba78e8. |
| `sw/litex/gmii_rx_capture.xdc:1` | Compact shipping-pad fixture constraints. |
| `sw/litex/gmii_rx_capture_check.tcl:5` | Reproducible two-fixture synthesis and placement; checks nine positive rows and nine expected pad-to-D refusals. |
| `sw/litex/test_gmii_rx_capture.py:88,96,110,141` | Shared conversion, fail-closed structural assertion and six permanent planted controls in the default test. |
| `sw/litex/patches/apply.sh:9` | Exact R1 header insertion; execution is unchanged. |
| `docs/integration/BUILDING.md:614` | Exact placement command, constraints, expected exits and report locations. |
| `PR-BODY.md`, Description | Exact R2 sentence; Round 2 section added. |
| `ROUND2-IOB.json` | All six rows recomputed from the preserved reports; supersedes the incomplete two-row ROUND1B-IOB.json summary (S2). |

Local commit: `ba080007a402dced74fa74656338710e0b6cb880`. No push.

The artifact census used `git ls-files '*generated*' '*.v'` and `rg` across the conversion entry points for LiteEth PHY and Verilog conversion calls. Only the timestamp suite carries a committed converted RX artifact. The capture fixtures are generated into scratch. No additional stale committed conversion was found.

The complete five-patch reconstruction passed: all four installed files match byte for byte and all five missing-patch controls are rejected. The regenerated MAC hash also matches the independent review probe.

Ruling 6045752839 replaces the earlier per-row interpretation of timing acceptance: each tree is judged by its kept best-WNS build. Both keep ExtraPostPlacementOpt and meet the setup and hold floors. The earlier STOP narrative above remains historical, including the unkept +0.013 ns row. The full root sweep and merge-time banks remain manager-owned under that ruling.

### Tests and planted defects

| Test | Planted defect or failure it detects | Round 2 evidence |
|---|---|---|
| Strong generated-model check and stale control | Restoring the exact previous RX artifact while retaining its valid old manifest must fail re-conversion | Stale fixture returns 1; regenerated artifact returns 0; control driver rc 0 |
| Timestamp closed loop | Disconnected observer; observer delayed one transmit cycle; dropped observer, crossing or mean-phase correction; forced rather than measured delta | 85 checks, zero failures; 6/6 controls caught by their named checks; default make target rc 0 |
| Capture cycle contract | Live-reset masking, lost last-byte behavior and data corruption violate the pad-sample oracle | 1,036 comparisons; preserves the established oracle |
| Converted capture structural guard | Reset on valid; reset on data; valid input logic; data input logic; capture enable; missing data bit | 6/6 new permanent controls caught; nine unconditional direct captures required |
| Live placement fixture | Nine preserved reset-before-D LUT2s prevent any capture register from reading its pad directly | 9 PASS in ILOGIC / 9 expected FAIL for "no register reads the pad"; driver rc 0 |
| IOB checker self-test | Unpacked/absent registers, inaccessible netlists, hidden or contradictory constrained ports and reset LUTs before D | 22 arms, 21 mutants, zero failures; documentation command 41 rc 0 |
| CPU memory CDC simulation | Direct unequal-clock AXI connection loses/duplicates beats | PASS inside five-member simulation aggregate |
| Timestamp conversion simulation | Converted and source chains disagree on frame bytes or inter-frame gap | PASS inside five-member simulation aggregate |
| Boot-bus freeze simulation | Always-open and never-open memory gates; unanswered reads prevent handover recovery | PASS inside five-member simulation aggregate |
| Processor memory bridge simulation | Old ack-only FSM remains wedged on an unanswered access; watchdog path must release it | PASS inside five-member simulation aggregate |
| Simulation inventory self-test | Failing/missing/unlisted scripts, masked verdict, skipped dependency, explicit invalid interpreter and timeout | 10/10 checks pass; rc 0 |
| Builder and patch contract | Missing patch, drifted installed bytes, unsupported options, malformed manifests and existing firmware/elaboration mutations | Complete run rc 0; all executed gates passed. Gate 11 retained calibration report absent, explicitly NOT RUN. Five-patch reconstruction and five omission controls passed |
| Documentation, source and quality gates | Broken links, stale generated docs, incorrect source lists and their existing planted policy violations | 76 selected workflow documentation/source/policy commands passed; exact per-command gate table follows |

Both emitted placement fixtures equal their Round 1 counterparts plus one trailing newline. This is an emitter serialization change only; the structural capture fix and all production source inputs are untouched.

### Coverage table

| Finding | Planned evidence | Status |
|---|---|---|
| F1 | Generator diff restricted to RX; strong reconstruction; 85/0 suite; 6/6 controls | Addressed; independent re-review pending |
| F2 | Tree-owned fixture constraint/driver; live 9 PASS / 9 expected FAIL; rc 0 | Addressed; independent re-review pending |
| R1 | Exact header insertion at apply.sh:9 | Applied |
| R2 | Exact sentence in PR-BODY.md Description | Applied |
| S1 | Default converted structure guard; 6/6 planted controls | Added and passing |

### Gate table

Round 2 software gates used isolated checkouts of the committed head.
The compact driver read the committed lane source and built only in scratch.
Compilation was limited to eight jobs, with VERILATOR_JOBS=2.
The simulator wrapper delegates to the prescribed 5.050 executable.
It changes only the nested build-job count from unlimited to eight.
Every long job used a detached session, its own log/rc files, and bounded foreground waits.

| Gate | Exact command | Result |
|---|---|---|
| Timestamp chain | `make -j8 -C tb/verilator/gptp_txts` with the full pinned interpreter | rc 0; model reconstruction, 85 checks and 6 controls |
| Standalone simulations | `bash scripts/run_litex_sims.sh "$SCRATCH/round2/litex-sim-logs"` | rc 0; 5 passed, 0 skipped |
| Simulation inventory | `bash scripts/run_litex_sims.sh --selftest` | rc 0; 10/10 controls |
| Strong model refusal | `"$MILAN_LITEX_PYTHON" "$SCRATCH/round2/model_control.py"` | rc 0; previous generated RX refused, corrected RX reconstructs |
| Builder | `"$MILAN_LITEX_PYTHON" -u sw/builder/test_builder.py --require-rv32` | rc 0; all executed gates pass, saved retired-board calibration absent |
| Documentation/source/policy | The 76 commands below, individually logged | All rc 0 |
| Compact placement | `flock "$VIVADO_LOCK" "$VIVADO" -mode batch -nojournal -source "$REPO/sw/litex/gmii_rx_capture_check.tcl" -tclargs "$SCRATCH/round2/capture"` | rc 0; 9 PASS / 9 expected FAIL |

The initial documentation attempt refused the missing pinned parser (rc 2).
After installing the hash-locked parser into isolated scratch, the same gate and all remaining selected commands passed.
No source change, exemption or weakened check was used.
The environment installers and local workflow-orchestrator self-test are not included in this 76-command claim.
The latter belongs inside its disposable workflow boundary.
The full candidate bank, hosted checks and workflow replica remain manager duties under ruling 6045752839.

| # | Exact documentation/source/policy command | Exit |
|---|---|---|
| 1 | `python3 scripts/gen_hdl_reference.py --selftest` | 0 |
| 2 | `python3 scripts/gen_hdl_reference.py --output $SCRATCH/round2/tmp/milan-hdl-reference` | 0 |
| 3 | `python3 scripts/docs_check.py` | 0 |
| 4 | `python3 scripts/check_em_dash.py --base e21c1ca024d37ea188ad15b5c8f9c2dae18628df` | 0 |
| 5 | `python3 scripts/check_doc_style.py` | 0 |
| 6 | `python3 scripts/check_doc_style.py --selftest` | 0 |
| 7 | `python3 scripts/check_gptp_docs.py` | 0 |
| 8 | `python3 scripts/check_gptp_docs.py --selftest` | 0 |
| 9 | `python3 docs/DOC_MAP.gen.py --check` | 0 |
| 10 | `python3 docs/DOC_MAP.gen.py --selftest` | 0 |
| 11 | `python3 docs/diagrams/timesync_chain.gen.py --check` | 0 |
| 12 | `python3 docs/diagrams/timesync_chain.gen.py --selftest` | 0 |
| 13 | `python3 scripts/check_solution_docs.py` | 0 |
| 14 | `python3 scripts/check_solution_docs.py --selftest` | 0 |
| 15 | `python3 docs/diagrams/submodule_boundaries.gen.py --check` | 0 |
| 16 | `python3 docs/diagrams/submodule_boundaries.gen.py --selftest` | 0 |
| 17 | `python3 scripts/check_submodule_docs.py` | 0 |
| 18 | `python3 scripts/check_submodule_docs.py --selftest` | 0 |
| 19 | `python3 scripts/gen_wavedrom.py --selftest` | 0 |
| 20 | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_axis_backpressure.json --background=white --check` | 0 |
| 21 | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_cdc_handshake.json --background=white --check` | 0 |
| 22 | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_gptp_pdelay.json --background=white --check` | 0 |
| 23 | `python3 scripts/check_diagram_pngs.py` | 0 |
| 24 | `python3 scripts/check_diagram_pngs.py --selftest` | 0 |
| 25 | `python3 scripts/check_feature_status.py --self-test` | 0 |
| 26 | `python3 docs/traceability/gen_module_matrix.py --check` | 0 |
| 27 | `python3 scripts/check_gptp_docs.py --with-submodule` | 0 |
| 28 | `make -C gptp-processor docs` | 0 |
| 29 | `python3 scripts/measure_control_flow.py --selftest` | 0 |
| 30 | `python3 scripts/measure_cohesion.py --selftest` | 0 |
| 31 | `python3 scripts/check_baremetal_only.py --check` | 0 |
| 32 | `python3 scripts/check_baremetal_only.py --selftest` | 0 |
| 33 | `python3 sw/builder/test_firmware_compiler.py --selftest` | 0 |
| 34 | `python3 sw/builder/test_firmware_compiler.py --absent --audit $SCRATCH/round2/tmp/rv32-absent.jsonl` | 0 |
| 35 | `python3 scripts/check_nvm_record_space.py` | 0 |
| 36 | `python3 scripts/check_nvm_record_space.py --self-test` | 0 |
| 37 | `python3 scripts/check_nvm_capture.py` | 0 |
| 38 | `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | 0 |
| 39 | `python3 scripts/check_soc_sources.py` | 0 |
| 40 | `python3 scripts/check_soc_sources.py --selftest` | 0 |
| 41 | `python3 sw/litex/iob_pack_selftest.py` | 0 |
| 42 | `python3 scripts/check_rtl_source_lists.py` | 0 |
| 43 | `python3 scripts/check_rtl_source_lists.py --selftest` | 0 |
| 44 | `python3 scripts/measure_naming.py --check` | 0 |
| 45 | `python3 scripts/measure_naming.py --selftest` | 0 |
| 46 | `python3 scripts/check_port_contracts.py` | 0 |
| 47 | `python3 scripts/check_port_contracts.py --selftest` | 0 |
| 48 | `python3 scripts/measure_fail_fast.py --check` | 0 |
| 49 | `python3 scripts/measure_fail_fast.py --selftest` | 0 |
| 50 | `python3 scripts/check_todo_ownership.py` | 0 |
| 51 | `python3 scripts/check_todo_ownership.py --selftest` | 0 |
| 52 | `python3 scripts/measure_test_evidence.py --check` | 0 |
| 53 | `python3 scripts/measure_test_evidence.py --selftest` | 0 |
| 54 | `python3 scripts/check_hygiene.py --check` | 0 |
| 55 | `python3 scripts/check_hygiene.py --selftest` | 0 |
| 56 | `python3 scripts/check_sv_idiom.py` | 0 |
| 57 | `python3 scripts/check_sv_idiom.py --selftest` | 0 |
| 58 | `python3 scripts/check_cpp_idiom.py` | 0 |
| 59 | `python3 scripts/check_cpp_idiom.py --selftest` | 0 |
| 60 | `python3 scripts/check_py_idiom.py` | 0 |
| 61 | `python3 scripts/check_py_idiom.py --selftest` | 0 |
| 62 | `python3 scripts/check_sh_idiom.py` | 0 |
| 63 | `python3 scripts/check_sh_idiom.py --selftest` | 0 |
| 64 | `python3 scripts/ci_events.py --check` | 0 |
| 65 | `python3 scripts/ci_events.py --selftest` | 0 |
| 66 | `python3 scripts/check_doc_paths.py` | 0 |
| 67 | `python3 scripts/check_archive.py` | 0 |
| 68 | `python3 scripts/check_archive.py --selftest` | 0 |
| 69 | `python3 scripts/gen_toc.py --selftest` | 0 |
| 70 | `python3 scripts/gen_toc.py --verify-anchors` | 0 |
| 71 | `python3 scripts/gen_toc.py --check` | 0 |
| 72 | `python3 avdecc/gen_aem_store.py --self-test` | 0 |
| 73 | `python3 scripts/check_sweep_shape.py --self-test` | 0 |
| 74 | `python3 scripts/check_deploy_shape.py --self-test` | 0 |
| 75 | `python3 scripts/check_entity_shape.py --self-test` | 0 |
| 76 | `python3 scripts/check_wire_accountability.py --self-test` | 0 |


### Review coverage

R546-1 left Conformance, RTL, Tests and Docs unclean at the starting head. Robustness was clean at that head. The new head requires independent re-review; this author makes no reviewer coverage verdict.

### Completed evidence and remaining review

All seven principal jobs ended with rc 0. The 76 documentation/source/policy commands each ended with rc 0. The compact driver ran under the shared exclusive lock after every other heavy job in this lane ended. It reported nine ILOGIC PASS rows and nine expected FAIL rows, each naming "no register reads the pad". These are new live receipts from the committed driver. No full-image synthesis, timing sweep or deployment was performed in Round 2.

The timestamp default make target includes strong reconstruction, 85 successful checks and all six caught controls. The five standalone simulations ran without a skip or timeout. The inventory self-test passed 10/10. Builder --require-rv32 passed every executed gate; only gate 11's absent saved retired-board calibration report is NOT RUN. This limitation is retained explicitly.

ROUND2-GATES.json records principal commands, durations, exits and resource samples. ROUND2-DOC-GATES.json records all 76 individual commands. ROUND2-ARTIFACTS.json records original artifact sizes/hashes and the hashes of normalized compact receipts. Large outputs and installed dependencies remain in scratch. ROUND2-MODEL.diff is the exact generated-artifact diff. ROUND2-SOURCE.json records the unchanged capture patch and seven-file scope. ROUND2-IOB.json supplies all six historical full-image rows.

Maximum sampled service memory was 2,838,745,088 bytes; minimum sampled free space was 162,539,114,496 bytes. All job rc files are complete. No job remains running.

| Lens | Prior public result at 35fb2a95 | Round 2 disposition at ba080007 |
|---|---|---|
| Conformance | R546-1 unclean through F1 | F1 addressed; independent re-review required |
| RTL | R546-1 unclean through F1 | Generated RX corrected; capture patch unchanged; independent re-review required |
| Robustness | R546-1 clean | Production capture unchanged; reviewer decides retained coverage |
| Tests | R546-1 unclean through F1/F2 | Both addressed; new structural controls pass; independent re-review required |
| Docs | R546-1 unclean through F2 | Reproducible command and wording corrected; independent re-review required |

This is an author evidence table, not a reviewer-owned completion ledger. No lens is newly approved here. The manager owns push, hosted and local workflow evidence, the complete candidate bank and subsequent review/merge handling. No push, PR edit, merge, rebase, amend, identity override, hardware access or flashing was performed. The final authorized public action is REVIEW READY on #691 at the local head above.
