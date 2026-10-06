[A551]

# Issue 667 handoff

Status: Local validation complete; ready for independent review.

Candidate: 5d6164a2da2d4f7374558bf33b464bcd8a9b4fc2.
Base: 423ac5d910d09ab189b3acc39ae3ae1d10d50b19.
Branch: 667-talker-start. The lane worktree is clean.
Executor: [A551]. Internal reviewer: [R514]. External reviewer: [R515].

The assignment is issue comment 6011846710 on #667.
The complete Issue, PR #676 at afa4e687, its findings page,
and B12's startup characterization were read.
TAKEN was posted as issue comment 6011869694.
The project item was moved from Ready to In progress.
No existing comment was changed. No push, PR change, merge,
rebase, hardware access or flashing occurred.

Resumed TAKEN: comment 6012860220. The resume made no implementation edit
and no new commit. The original static evidence remains at the same head.

## Prior STOP and authorized continuation

The shipping render campaign's unmutated `--epoch-only` control fails.
The candidate and the original packetizer both complete 114 checks with
four failures and return 1. The complete logs are in this packet:
`render-candidate-epoch.log` and `render-base-epoch.log`.

| Assertion in tb/verilator/milan_dp_render/sim_tdm8_render.cpp | Base | Candidate |
|---|---|---|
| 3408: selection fires the settled-grid trigger once | got 0, expected 1 | got 0, expected 1 |
| 3411: exactly one render recentre pulse | got 0, expected 1 | got 0, expected 1 |
| 3413: stage executes exactly one recentre | got 0, expected 1 | got 0, expected 1 |
| 3428: no second recentre follows the settled one | got 0, expected 1 | got 0, expected 1 |

The comparison uses the same unchanged shipping harness, parameters,
source closure and dependencies. Only the packetizer is substituted with
the exact file from 423ac5d9; its bytes were verified against that commit.
Both executable sizes and hashes are in source-hashes.json.
The base comparison build returned 0. This establishes a pre-existing
failure for this mode; its cause has not been diagnosed.

Ruling 6012843714 identifies these failures as #657 and authorizes continuation.
The full campaign must have the same results at base and head.
The clean epoch stdout and its four failure lines must be byte-identical.
No assertion, test expectation or campaign verdict is changed.
The retained epoch logs share SHA-256
`7876a3a277df5e06a9381e502249b9638b7a4e04ec676fefba207150b41d4007`.
The historical `8f6ebaae...` receipt in #657 used the older processor pin
`631eeb34`; the assigned base and candidate both use `ead80360`.
Equality is measured against the assigned base, with that difference disclosed.

Reproduce the candidate failure from the repository root:

```sh
make -j16 -C tb/verilator/milan_dp_render tdm8render-build
(cd tb/verilator/milan_dp_render && ./obj_tdm8r/Vmilan_dp_tdm8r --epoch-only)
```

The retained original substitution recipe is below; the resumed comparison also
builds the complete assigned base in its own initialized worktree.
For the original control, export the base packetizer into physical scratch.
From `tb/verilator/milan_dp_render`, obtain `SRCS` with
`make --no-print-directory -s -C ../milan_dp print-srcs`.
Replace its sole `../../../hdl/ieee1722/aaf/KL_aaf_packetizer.sv` token
with the exported file. Run the same `tdm8render-build` target with that
`SRCS` value and a distinct `TDM8R_MDIR`, then run its executable with
`--epoch-only` from the same suite directory. The saved comparison recipe
and build log are indexed in ARTIFACTS.json.

The resumed full-base clean epoch stdout has the same hash above.
The original campaign driver is unchanged. A recording wrapper retains its
returned stdout and rc without changing any judgment. Every clean, stimulus,
skew and RTL-mutant arm is compared. All 32 run stdout files and return codes are byte-identical at base and head;
the independent comparison returns 0. Both raw campaigns return 1, with
28/32 passing judgments and the same four known #657 findings.
The surviving uncounted-repeat mutant
remains explicitly reported as a coverage gap. It is not called caught.

## Red run and first ten PDUs

The pre-edit RTL was exactly the assigned base.
The initial probe uses N_TALKERS_P=1 and WIRE_CHANS_P=8.
Four pair slots form each 48 kHz sample at 50 MHz.
Enable arrives at seven phases across that sample.
Two PHC origins give fourteen starts in the initial probe.

A warm-up stream seeds a real previous presentation timestamp.
The probe disables admission with a partial epoch retained.
It advances the PHC 3.8 seconds while disabled.
Disabled clock cycles are elided, preserving disabled capture state.

Starts at slots 1, 2 and 3 fail at both origins.
The other eight starts pass. The executable returns 1.
Every case retains ten PDUs in red-startup.log.
The complete source is start_probe.cpp in this packet.

Representative failing case: origin 1000000000 ns, phase 1.

| PDU | Sequence | tv | Timestamp (hex) | Signed step (ns) |
|---|---|---|---|---|
| 1 | 2 | 1 | 3bbd1fb0 | -- |
| 2 | 3 | 1 | 1e3ebfec | -494821316 |
| 3 | 4 | 1 | 1e40a834 | 125000 |
| 4 | 5 | 1 | 1e42907c | 125000 |
| 5 | 6 | 1 | 1e4478c4 | 125000 |
| 6 | 7 | 1 | 1e46610c | 125000 |
| 7 | 8 | 1 | 1e484954 | 125000 |
| 8 | 9 | 1 | 1e4a319c | 125000 |
| 9 | 10 | 1 | 1e4c19e4 | 125000 |
| 10 | 11 | 1 | 1e4e022c | 125000 |

The subsequent initial standing leg had 8766 graded assertions.
It failed 162 assertions on the unedited RTL.
Its make command returned 2 because the executable returned 1.
That was before the later spacing and sequence-wrap expansion.

This is a packetizer-boundary reproduction, not an ACMP exchange.
It drives the post-bind stream enable presented by the datapath.
The integrated datapath verdicts are recorded in the gate table below.

## Root cause

All base citations below refer to 423ac5d9.

| Artifact | Finding |
|---|---|
| hdl/ieee1722/aaf/KL_aaf_packetizer.sv:314 | pair_ok_w admits any owned pair immediately when stream_en_i rises. |
| hdl/ieee1722/aaf/KL_aaf_packetizer.sv:712 | The last pair advances nsamp_r, even when preceding pairs were disabled. |
| hdl/ieee1722/aaf/KL_aaf_packetizer.sv:720 | Timestamp capture requires sample zero and pair zero together. |
| hdl/ieee1722/aaf/KL_aaf_packetizer.sv:725 | tsw_val_r captures PHC plus this talker's presentation offset. |
| hdl/ieee1722/aaf/KL_aaf_packetizer.sv:651 | E_DRD_S loads ets_r from retained TCTX w4. |
| hdl/ieee1722/aaf/KL_aaf_packetizer.sv:734 | Disable clears accumulation and pending state, not TCTX w4. |
| hdl/milan/milan_datapath.sv:1994 | The composed talker gate can rise independently of pair position. |
| hdl/milan/milan_datapath.sv:1392 | That gate reaches stream_en_i without sample-boundary alignment. |

Enabling after pair zero skips the timestamp capture.
The last pair still advances sample zero to sample one.
The first completed bank therefore reads the previous presentation timestamp.
The next bank captures pair zero normally and restores steady steps.

The packetizer's current timestamp read is at line 657.
Its current admission guard is at line 319.
The added state resets at 591, sets at 715,
and clears on disable at 742.

The AVTP path supplies restart and validity metadata separately.
The latency-tap bank is a pure observer of handshakes.
Neither produces the stale timestamp; TCTX w4 does.
Media-clock following and the presentation-offset interface remain unchanged.

## Authorities and clause correction

IEEE 1722-2016 7.5 requires valid timestamps for normal-mode AAF.
It associates presentation time with the first audio sample frame.
Sections 4.3.2, 4.4.4.5 and 4.4.4.9 supply timing and encoding.
Section 7.3.5 requires chronological multichannel sample interleave.
Milan v1.2 5.3.8.10, Table 5.6 defines EARLY/LATE_TIMESTAMP.
Milan v1.2 4.4.2.1 defines listener buffering support.

The assignment's 5.4.4 citation concerns IEC 61883 encapsulation.
Its 7.3.4 citation concerns bit depth.
The required AAF behavior agrees with 7.5; no behavior decision changes.
The cited standards were checked against the local primary documents.

B12 saw -23612829 and +521369096 ns first steps.
B13 saw fourteen backward steps among one hundred starts.
The simulated stale-register mechanism is consistent with those observations.
Absolute bench gPTP correlation remains unmeasured in both findings.
Simulation does not establish a bench incidence rate.

## Change

Eight RTL lines add one admission flag per talker.
Capture waits for that talker's pair zero after disable or reset.
The ordinary first-pair path then records sample time plus offset.
Partial first samples cannot complete an epoch with retained timestamps.
No port, register-map or parameter declaration changes.

The standing test lives in tb/verilator/aaf/sim_start.cpp.
The existing AAF default target includes it and its controls.
TIME_SYNC.md records the admission behavior.
The suite README records stimulus, checks and limits.

## Exact-text mutation preservation

preedit-grep.txt records searches for every added RTL line.
Searches covered tb/**/*.patch and exact-text Python tables.
No tracked patch file existed under tb.
No existing mutation table consumed an added RTL line.

preedit-arms.tsv records successful planting before RTL edits:

| Inventory | Arms or sites checked |
|---|---|
| milan_dp render | 4 arms |
| milan_dp CRF licence | 6 arms |
| milan_dp GET_STREAM_INFO | 8 arms |
| milan_dp unbind | 5 arms |
| milan_dp GM step | 20 arms |
| milan_dp_render | 21 arms |
| milan_dp_mclk | All 19 edit sites, covering 16 schemata mutants |

Each exact-text edit was applied to an in-memory source copy.
Every site appeared exactly once at its application point.
The campaign verdicts are recorded in the gate table below.

## Standing checks and failing mutants

Final focused command:

```sh
make -j16 -C tb/verilator/aaf startup-mutants START_MDIR="$SCRATCH/standing-green"
```

The environment exported the pinned HDL simulator, release 5.050.
TMPDIR named physical scratch storage, outside the lane.
The driver ran with --jobs 4; all eight arms returned 1.
The overall command returned 0 and retained each named failure.

| Check group | Failing mutant | Result |
|---|---|---|
| First-to-second and later steps equal steady | Restore the stale admission path | Caught |
| Re-enable acquires a fresh timestamp | Disable retains started_r | Caught |
| Reset independently re-arms capture | Reset retains started_r | Caught |
| Timestamp equals payload sample time plus offset | Omit the presentation offset | Caught |
| Normal-mode tv remains valid | Clear tv | Caught |
| Consecutive sequence through wrap | Hold sequence number | Caught |
| Ten complete PDUs arrive within bounded samples | Never publish the completed bank | Caught |
| Complete, ordered sample rows | Corrupt left sample bits | Caught |

The first reset fixture allowed disable to clear the flag.
Its reset-only control survived that version.
The corrected fixture holds enable high through reset.
It now fails independently when the reset assignment is removed.

## Start-phase sweep

The final sweep grades 486 starts and 4860 PDUs.
All 34020 assertions pass. start-phase-sweep.csv retains every row.

| Dimension | Values |
|---|---|
| Pair spacing, cycles | 1, 26, 260 |
| Enable phase | 0, 1, each later pair and following cycle, 1040 |
| PHC origin, ns | 0, 1000000000, 4292870144 |
| Disabled time, ns | Cold start, 500000000, 3800000000 |
| Start history | Disable/re-enable; reset with enable held high |
| Ready | Continuous; five stalled cycles in every seventeen |
| Sequence | Seed 248, including modulo-256 wrap |
| First step, all final cases | 125000 ns |
| Steady step, all final cases | 125000 ns |
| Tolerance | 0 ns: six rational sample periods are exact |

The compact spacing repeats some phase values intentionally.
No first PDU is skipped, and missing packets fail explicitly.
The source models pair delivery; it does not instantiate TDM capture.
Both production capture paths remain subject to integrated regression.

## OOC 1x1 before and after

Both measurements completed with rc 0 under the shared synthesis lock.
They ran separately from this lane's other builds.
The output reports are indexed by size and SHA-256 in ARTIFACTS.json.
area.csv retains the selected hierarchy rows.
ooc-recipe.tcl retains the adapter without host identifiers.

Recipe: the repository's milan_datapath_ooc.tcl source and image checks;
shipping endstation_ax7101_1x1_tdm8 header; xc7a100tfgg484-2;
OOC synthesis, default directive, no explicit placement seed;
N_STREAMS=1, TALKER_WIRE_CHANS_P=8, AUDIO_IF_SLOTS_P=8,
AUDIO_IF_MASTER_P=1, AUDIO_IF_RENDER_SLOTS_P=8, LOOPBACK_P=1,
I2SPB_P=0, LPF_P=0, MILAN_CLK_FREQ_HZ=50000000.
All other generics retain the repository recipe's defaults.
The source-list record derives from the repository's portability closure.
The adapter changes the selected shape include and elaboration generics.

| Hierarchy scope | Before LUT / FF | After LUT / FF | Delta LUT / FF |
|---|---|---|---|
| Complete datapath, cumulative | 46425 / 43501 | 46502 / 43515 | +77 / +14 |
| Datapath local-only row | 239 / 2861 | 239 / 2861 | 0 / 0 |
| Changed packetizer, own logic | 868 / 1344 | 864 / 1344 | -4 / 0 |
| Processor wrapper, cumulative | 25598 / 18759 | 25689 / 18759 | +91 / 0 |
| Timing wrapper, cumulative | 6673 / 5906 | 6673 / 5906 | 0 / 0 |
| Datapath excluding both processor subtrees | 14154 / 18836 | 14140 / 18850 | -14 / +14 |

Rows overlap; they must not be summed.
The last row subtracts the two processor subtrees from the cumulative total.
Both that fabric subtotal and the changed packetizer are below the limit.
The packetizer contains no child module hierarchy.
Complete BRAM36, BRAM18 and DSP counts remain 22, 11, 14.
Packetizer BRAM36 and BRAM18 counts remain 1 and 1.

The recipe's timing report uses a 10 ns axis constraint.
Other OOC clock-reference warnings remain visible in the logs.
These are synthesis-area measurements, not routed timing sign-off.
No seed or directive search was used to seek a passing delta.
The own-logic delta is within the assigned limit.


## Gate table

Commands ran directly, without pipelines. Cancelled attempts are retained as
history and are not final passing evidence. Earlier static results below
remain valid at the unchanged head.

| Check | Command or recipe | Final result |
|---|---|---|
| Base red probe | Direct build, 1x1 eight-channel packetizer | Build 0; run 1, expected red |
| Initial standing red | make -j16 -C tb/verilator/aaf startup, base RTL | Make 2; executable 1, expected red |
| Final startup and controls | make -j16 -C tb/verilator/aaf startup-mutants | 0; 34020 checks, 8/8 caught |
| Whole-tree lint | python3 scripts/lint_rtl.py --check --self-test | 0 |
| Derived processor sources | python3 scripts/pp_srcs.py --check --selftest | 0 |
| Source-list closure | python3 scripts/check_rtl_source_lists.py | 0 |
| Documentation | python3 scripts/docs_check.py | 0 |
| Documentation style | python3 scripts/check_doc_style.py | 0 after paragraph correction |
| Contents | python3 scripts/gen_toc.py --check | 0 |
| Documentation paths | python3 scripts/check_doc_paths.py | 0 |
| Em-dash additions | python3 scripts/check_em_dash.py --base 423ac5d9 | 0; 339/339 controls |
| Bare-metal scope | python3 scripts/check_baremetal_only.py --check | 0 |
| C++ idioms | python3 scripts/check_cpp_idiom.py | 0 |
| HDL idioms | python3 scripts/check_sv_idiom.py | 0 |
| Python idioms | python3 scripts/check_py_idiom.py | 0 after adding main's docstring |
| Traceability | python3 docs/traceability/gen_module_matrix.py --check | 0 |
| Naming | python3 scripts/measure_naming.py --check | 0 |
| Port contracts | python3 scripts/check_port_contracts.py | 0 |
| Hygiene | python3 scripts/check_hygiene.py --check | 0 |
| Test-evidence policy | python3 scripts/measure_test_evidence.py --check | 0 after explicit mutation-reader classification |
| Control-flow / cohesion | python3 scripts/measure_control_flow.py; python3 scripts/measure_cohesion.py | 0 / 0; measurements, not threshold gates |
| Whitespace | git diff --cached --check; git diff --check | 0 |
| OOC before / after | Serialized repository recipe with shipping shape | 0 / 0; own logic within threshold |
| Default datapath shard | `bash scripts/run_all_suites.sh "$SCRATCH/default-heavy-logs" --shard 1/2` | rc 0; 11877 checks, zero failures; complete milan_dp suite with SIM_JOBS=2 |
| Default remainder 0 | `bash scripts/run_all_suites.sh "$SCRATCH/rest-0-logs" --shard 0/5` | rc 0; 11 selected suites; SIM_JOBS=2 |
| Default remainder 1 | `bash scripts/run_all_suites.sh "$SCRATCH/rest-1-logs" --shard 1/5` | rc 0; 23 selected suites; SIM_JOBS=2 |
| Default remainder 2 | `bash scripts/run_all_suites.sh "$SCRATCH/rest-2-logs" --shard 2/5` | rc 0; 13 selected suites; SIM_JOBS=2 |
| Default remainder 3 | `bash scripts/run_all_suites.sh "$SCRATCH/rest-3-logs" --shard 3/5` | rc 0; 12 selected suites; SIM_JOBS=2 |
| 60-suite aggregate | `python3 scripts/suite_tally.py "$SCRATCH/default-heavy-logs" "$SCRATCH/rest-0-logs" "$SCRATCH/rest-1-logs" "$SCRATCH/rest-2-logs" "$SCRATCH/rest-3-logs" --quiet --expect-suite-root tb/verilator` | rc 0; 60 distinct suites; 2184191 checks; zero failures, skips or timeouts |
| Portability sweep | `bash syn/yosys/run.sh --results "$SCRATCH/portability-results"` | rc 0; 58 tops; tied-input and observer-purity checks pass |
| Portability aggregate | `python3 scripts/yosys_tally.py "$SCRATCH/portability-results" --expected "$SCRATCH/expected-tops.txt" --require-structural` | rc 0; 58 expected, 58 observed, zero errors |
| Builder bank | `python3 sw/builder/test_builder.py --require-elaboration --require-rv32` | rc 0; Required arms ran; optional gate 11 calibration NOT RUN, missing historical placement report |
| Full render at base | `python3 tdm8_render_mutants.py` | rc 1; Original campaign judgments; known #657 results retained |
| Full render at head | `python3 tdm8_render_mutants.py` | rc 1; Original campaign judgments; known #657 results retained |
| Render comparison | `Compare stdout, return codes and verdicts for all 32 runs` | rc 0; Ruling 6012843714 acceptance |
| Full GM-step campaign | `python3 gmstep_mutants.py --all` | rc 0; 22/22 checks pass |
| Unbind campaign | `python3 unb_mutants.py` | rc 0; 6/6 checks pass; all five mutants caught |
| Stream-info campaign | `python3 gsi_mutants.py` | rc 0; 9/9 checks pass; all eight mutants caught |
| CRF licence campaign | `python3 crflic_mutants.py` | rc 0; 7/7 checks pass; all six mutants caught |
| Physical timing integration | `bash scripts/run_all_suites.sh "$SCRATCH/physical-logs" --physical-gptp` | rc 0; 139 physical checks and 40 failure-path accounting checks pass |
| Render boundary campaign | `make -j16 tdm8render-law-boundary LAW_BOUNDARY_JOBS=16` | rc 0; 81/81 diagnostic rounds; both setpoint mutants fail every gradable window; near-boundary windows remain explicitly NOT GRADABLE |
| Native control-processor bank | `bash scripts/run_suites.sh` | rc 0; 1021627 checks, zero failures |
| Native timing-processor bank | `make -j16 contract tb` | rc 0 |
| Pinned timing wire-field repeat | `make -j16 -C tb/tsngen` | rc 0; 290 clean checks and 4 campaign checks pass |
| Standalone runner self-test | `bash scripts/run_litex_sims.sh --selftest` | rc 0 |
| Standalone simulations | `bash scripts/run_litex_sims.sh "$SCRATCH/standalone-logs"` | rc 0; 4/4 pass, no skips or timeouts |
| Hosted checks and independent reviews | Manager follow-up | NOT RUN; no push authorized |
| Bench repeat | Manager after merge and flashing | NOT RUN |

Explicit datapath campaign commands run from tb/verilator/milan_dp.
Render commands run from tb/verilator/milan_dp_render.
Native bank commands run from their respective pinned submodules.
The behavior layer also passed: 404 scenarios, 1968 steps, rc 0.
Vendor parsing passed: 133 files, two existing processor findings, no new finding.
Their commands were `behave --no-capture -f plain` and
`python3 scripts/xvlog_gate.py --check` under the shared lock.

## Execution and handoff limits

The environment exports the pinned HDL simulator, release 5.050.
All generated outputs and TMPDIR use physical scratch. Independent suites,
campaigns and builds run concurrently in isolated initialized checkouts.
Make uses -j16. Ordinary simulations use SIM_JOBS=2, the enforced ceiling.
Other campaign drivers exposing --jobs receive 4 within their own bounds.
The independent boundary diagnostic uses --jobs 16; its scratch launch wrapper
prints that effective setting. Compiler concurrency is bounded at eight
within the 12 GB service cap. New compiler admission pauses below
34 GiB free physical storage to protect the requested 30 GB floor.
A host-wide storage dip reached 29.63 GB while this lane admitted no new
compilers. Removing 410.6 MB of inactive generated builds and external
reclamation restored headroom; queued work then resumed. Removed artifacts
have sizes and hashes in the retained cleanup receipt.
Synthesis ran separately under its lock.
No source input in the implementation lane was generated or modified by resume gates.

Only the required three RTL submodules were initialized. Before every Git
inspection inside each submodule, its top-level directory was verified.
The pins are ead8036035affd53ef4b29979190f2f4f67084c0 for the control processor,
5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d for the timing processor, and
48ff7a7e2ef782cf778d47910cf85835c64b1bce for the stream library.
The wire-field generator is pinned at deca300c9eb4863fa13383b45ba6cb6fd0828671.

The builder bank runs in a separate checkout because its preservation controls
temporarily rewrite generated inputs. Its first resume attempt was cancelled
before those controls with rc -15. builder-isolated.rc is the completed verdict.
Optional gate 11 calibration is unmeasured because its historical placement
report is absent. Required elaboration was not skipped.

An earlier compiler helper removed precompiled headers too early. That GM-step
attempt was cancelled with rc 143. Cleanup now occurs only after successful
executable linking in scratch. The fresh complete campaign returned zero.
The first resumed default sweep inherited SIM_JOBS=4. milan_dp refused that
setting before its ordinary simulation pool because the ceiling is 2. That
completed attempt and its aggregate receipt remain retained. The initial
log tally returned 0, but it does not replace the runner exit status; that
setup-invalid sweep is not counted as a passing full gate. The dedicated datapath shard passed with SIM_JOBS=2. The serial remainder
had just begun and was cancelled through its owner before any suite verdict.
Four disjoint remainder shards replace it for a new full-inventory verdict.
Their selections contain 11, 23, 13 and 12 suites; together with the dedicated
datapath result they cover all 60 defaults. The two generated result-page
date updates in the scratch verification checkout were preserved before
restoring those pages to the candidate bytes for the new run.
Earlier invocation/style failures and their corrected receipts remain indexed.
The mutation-reader evidence classification is exact-file; no budget was raised.
No test or acceptance criterion was weakened.

Large logs, executables, reports and checkouts remain in scratch. Artifact
indexes record relative names, exact sizes and SHA-256. The output packet
contains no installed packages, environments, toolchains, tree exports or
files above 200 KB. MANIFEST.sha256 covers the small delivered packet.

Hosted checks, independent reviews and merge validation remain manager follow-up.
The manager retains the B13-style bench repeat after merge and flashing.
This handoff supplies local evidence, not a review verdict or merge approval.

## Final receipt audit

The completed default inventory contains exactly 60 distinct suites, with
2184191 checks and zero failures, skips or timeouts. The independent
portability inventory contains all 58 expected tops. Both aggregate receipts
return zero. The separate boundary diagnostic passes all 81 rounds.
[i] law boundary: the largest walk over 564 windows is 3 cycles (the unmutated gateware, descending, +2066); the leg states a walk of 5

Boundary executable sizes and hashes were retained before temporary-build
cleanup in boundary-executables.json. The final implementation-state receipt
confirms the remote, unchanged head, clean branch and clean pinned submodules.
Peak memory was 9.53 GiB; no out-of-memory event occurred.

REVIEW READY was posted and its body verified at https://github.com/kebag-logic/milan-fpga/issues/667#issuecomment-6015760986.
All validation workers have exited. The branch remains local and unpushed.
