[A564]

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
