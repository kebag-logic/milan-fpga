# [A303] Issue #545 handoff

Status: assigned implementation and local gates complete; ready for independent review.
Head: `fc8a719fecfaade8f5cdd7e7aef5292ffebcc1b4`
Base: `5b73d3f47dfed519eb988c13d6beb1db664ef1e0`
Branch: `545-crf-servo-slew`
Executor: [A303]. Assigned independent reviewers: [R300] and [R301].

## Authority and acceptance

- [Assignment, items 1-6](https://github.com/kebag-logic/milan-fpga/issues/545#issuecomment-5827358783).
- [Coupling decision](https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5816509317).
- [Adopted processor contract](https://github.com/Mister-M-alt/FPGA-gPTP/blob/5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d/docs/INTEGRATION.md#slew-active-level).
- [Public takeover and duration clarification](https://github.com/kebag-logic/milan-fpga/issues/545#issuecomment-5827396237).

The resumed assignment explicitly adopts the registered level. Its completion
is measured, without a 0.5 s expiry. The historical decision's maximum and the
adopted contract differ; this was published before implementation. The consumer
honors the adopted level indefinitely. A 100 us correction at constant 200 ppm
lasts 0.5 s in the prescribed stimulus; this is not a producer duration bound.
The corrected references are IEEE 802.1AS Annex B.1.1 (+/-100 ppm LocalClock)
and Milan v1.2 section 7.4 (media-source accuracy better than +/-50 ppm).

| Assignment | Implementation and evidence |
|---|---|
| 1: pin and records | Fetched origin main and checked out `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`; staged gitlink; ran `cd syn/yosys && ./ooc.sh --record-rom-digests`, rc 0. No hand-edited digest. Current pin prose, diagrams, SUBMODULES and CHANGELOG updated |
| 2: level transport | Direct engine output through shadow, effective-rate release alignment in datapath, matching PHC sample stage in servo. Real-plane test and two connection mutants pass |
| 3: overlap policy | Sticky overlap suppresses PI, trim and lock qualification for every affected window, including the partial tail; boundary samples taint both intervals; first clean window resumes directly. Shared saturating `MCSRV_STAT[15:10]` counts discarded windows, so the existing CSR is the natural tally. Step and slew on the same open window count once |
| 4: simulation and failing arms | Both 100 us signs at 200 ppm, short and boundary cases, prolonged level, reset, saturation, replacing step and clean resumption. Four unit controls and two connected controls fail their named checks |
| 5: authoritative docs | TIME_SYNC policy and loop table, both GM_LOSS_RECOVERY rows, REGISTER_MAP tally; #545 paths described as closed |
| 6: area | Locally measured standalone servo delta +7 LUT / +2 FF; isolated release alignment +1 LUT / +4 FF. No network-port count or redundant-network selector is assumed |

## Change list at the head

| File:line | Change |
|---|---|
| `gptp-processor` gitlink | Adopt merged processor contract at `5dce647a`; donor worktree unmodified |
| `syn/yosys/rom_digests.tsv:20` | Repository-generated digest row for the adopted pin |
| `hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv:147`, `:685` | Documented registered-level output and direct engine connection |
| `hdl/milan/milan_datapath.sv:1455`, `:2762`, `:5568`, `:6944`, `:7036` | Test visibility, four-cycle release tail, actual servo/shadow connection, feature-off zero |
| `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:258`, `:468`, `:492`, `:588`, `:609`, `:715`, `:956` | Port, sample stage, overlap classification, sticky window, PI qualification and shared saturating status tally |
| `tb/verilator/mmcm_servo/sim_phc_step.cpp:107`, `:209`, `:447` | Physical-window slew suite, matching stimulus level, exact hold and recovery bounds |
| `tb/verilator/mmcm_servo/sim_main.cpp:615` | Reset during slew, prolonged saturation, replacement-step single count |
| `tb/verilator/mmcm_servo/slew_mutants.py:1`, `Makefile:68` | Default-owned clean control and four named negative controls |
| `tb/verilator/milan_dp/sim_gmstep.cpp:416`, `:432`, `:643`, `:1061` | Real Sync/FollowUp stimulus, actual servo-stage observation and release-edge checks |
| `tb/verilator/milan_dp/gmstep_mutants.py:112`, `README.md:518` | Explicit `--slew` connection controls; scope and execution documented |
| `tb/verilator/crf_rx/crf_talker_wrap.sv:71`, `tb/verilator/mmcm_servo/rails_wrap.sv:134`, `tb/verilator/mmcm_servo_autorepair/sim_autorepair.cpp:168` | New servo input tied inactive in unrelated test fixtures |
| `tb/verilator/gptp_shadow/gptp_shadow_wrap.sv:297`, `tb/verilator/gptp_txts/gptp_txts_wrap.sv:235` | Explained unused shadow output in existing benches |
| `scripts/measure_test_evidence.py:597` | Account for the new mutation reader and expanded connected inventory; no budget increase |
| `docs/design/TIME_SYNC.md:100`, `:173`, `:192` | Producer contract, loop policy, clock alignment and simulation bounds |
| `docs/design/GM_LOSS_RECOVERY.md:152`, `:154`, `:189` | Closed isolation paths and connected-test scope |
| `docs/reference/REGISTER_MAP.md:1968` | Existing tally includes slew-overlap windows and same-window deduplication |
| `docs/reference/SUBMODULES.md:24`, `CHANGELOG.md:31` | Pin adoption and behavioral change |
| `docs/design/GPTP_PLANE.md:32`, `docs/traceability/ieee8021as.md:53` | Current pin references |
| `docs/guides/gptp/HDL_DEVELOPER.md:33`, `MANAGER.md:23`, `SYSTEM_INTEGRATOR.md:61`, `TEST_DEVELOPER.md:30` | Current linked donor contract |
| `docs/diagrams/submodule_boundaries.svg:39`, `timesync_chain.svg:47`, corresponding `.drawio` and `.png`, `PNG_MANIFEST.json:12` | Regenerated pin diagrams and PNG provenance |

## Clock domains and window edges

Engine, shadow and servo run on `axis_clk`. The existing live PHC contract at
`milan_datapath.sv:2830` requires `gtx_clk == axis_clk`; the new level crosses no
asynchronous clock domain. Assertion is immediate. Release is held through the
shadow's addend latch, the two existing `ptp_csr_sync` rate registers, and the
counter application edge (four cycles). The servo stages this effective level
beside `ptp_now_i`. A future independent PHC clock needs coherent time/control
crossing; this patch makes no claim for that unsupported wiring.

The sticky flag records any affected sample until the measurement boundary,
including a correction wholly between two audio ticks. A shared boundary sample
belongs to both intervals. A completed clean measurement may finish its existing
PI sequence after the level rises; subsequent overlapped windows cannot commit.
A step still abandons its open window immediately, without double-counting that
same window as a slew. Audio-tick and phase-command CDC are unchanged. Reset
clears the stage, overlap memory and count; the feature-off datapath drives zero.

## Simulation and mutation evidence

The physical-window harness uses the module's real window size and 50 MHz
fabric. Its existing suite uses a 50 MHz phase-command clock; the tested command
stays below its throughput limit. The connected leg uses compressed engine
clocks and holds the audio clocks; it proves transport, not media-loop settling.

| Test | Result / bound | Receipt |
|---|---|---|
| Servo unit, including U14 | 94 checks, 0 failures | `servo-default-final.log` |
| Servo rails | 8 checks, 0 failures | `servo-default-final.log` |
| Existing physical-window step suite | 113 checks, 0 failures | `servo-default-final.log` |
| Physical-window slew suite | 87 checks, 0 failures; default-owned mutations also passed | `servo-default-final.log`; preliminary `servo-slew-first.log` |
| +100 us / 200 ppm | Integrator starts +30.625 ppm, holds exactly for both affected windows; command holds exactly; next clean integrator delta 20/512 ppm, within 1 ppm; clean close before 1.536 s from start; LOCKED throughout | Same slew receipt |
| -100 us / 200 ppm | Two affected windows, exact integrator/command hold, next integrator delta 10/512 ppm; same bounds | Same slew receipt |
| Short 100 ns correction | One affected window, including tail after level falls | Same slew receipt |
| Shared endpoint / already-closed clean window | Two adjacent windows discarded / clean in-flight PI still commits | Same slew receipt |
| Prolonged level | Seven held boundaries plus final partial window counted (8); no expiry, exact hold, direct clean resumption | Same slew receipt |
| Reset / saturation / replacing step | Count saturates at 63; reset clears count/trim; reacquires; replacing step counts its open window once | U14 in servo receipt |
| Real-plane connected slew | 56 total gmstep checks; consumes offset 80..100 us, raises actual servo level, clears after in-band pairs, checks every release-tail edge, no PHC step | `sweep-08.log` |
| CRF receiver | 13,836 unit + 1,658 discontinuity + 69 connected talker checks; 8 mutation checks pass | `crf-rx.log` |
| Shadow | 309 positive checks; nine mutation controls; lifecycle gate pass | `shadow-final.log` |
| Phase autorepair | 47 checks, 0 failures | `servo-autorepair.log` |
| Egress timestamp wrapper | 85 checks, 0 failures; source-provenance model check, not a fresh model regeneration | `gptp-txts-run.log` |
| Behavior scenarios | 344 scenarios, 1,739 steps, 14 features passed | `behave.log` |

| New negative control | Exit | Required failure | Campaign |
|---|---|---|---|
| Remove discard qualification | 1 | `[S1] overlapped window is discarded` | `servo-slew-mutants.log` |
| Tie sampled level low | 1 | Same overlap check | Same |
| Trust partial tail after deassertion | 1 | Same overlap check | Same |
| Remove slew tally increment | 1 | `[S1] discards counted` | Same |
| Tie actual datapath servo port low | 1 | `slew path: the actual servo receives the level` | `gmstep-slew-mutants.log` |
| Omit datapath release extension | 1 | `slew path: every staged sample covers the PHC tail` | Same |

Both campaigns first rebuild a passing positive control (exit 0). A compile
failure or crash does not count as a caught mutant. The unit campaign is owned
by default `make`; the two connection controls are selected with `--slew`.
The default gmstep campaign still runs its original three acceptance controls.

### Default datapath sweep

| Command index | Leg | Checks | Exit | Receipt |
|---:|---|---:|---:|---|
| 2 | gPTP plane | 181, all pass | 0 | `sweep-02.log` |
| 4 | gPTP latency corrections | 181, all pass | 0 | `sweep-04.log` |
| 8 | GM step and new slew connection | 56, all pass | 0 | `sweep-08.log` |
| 20 | default datapath | 233, all pass | 0 | `sweep-20.log` |
| 21 | notifications | 147, all pass | 0 | `sweep-21.log` |
| 22 | CRF licence and LeaveAll | 85, all pass | 0 | `sweep-22.log` |
| 23 | NxN | 1708, all pass | 0 | `sweep-23.log` |
| 24 | divergent NxN | 1710, all pass | 0 | `sweep-24.log` |
| 25 | eight-channel NxN | 3136, all pass | 0 | `sweep-25.log` |
| 26 | four-stream/four-channel shape | 1708, all pass | 0 | `sweep-26.log` |
| 27 | low-pass filter pruned | 233, all pass | 0 | `sweep-27.log` |
| 28 | all six optional blocks pruned | 33, all pass | 0 | `sweep-28.log` |
| 29 | AX7101 1x1 TDM8 shape | 230, all pass | 0 | `sweep-29.log` |
| 30 | real audio-clock ratio | 143, all pass | 0 | `sweep-30.log` |
| 31 | render mutation campaign | 6, all pass | 0 | `sweep-31.log` |
| 32 | default GM-step mutation campaign | 4, all pass | 0 | `sweep-32.log` |

The other 17 commands generate inputs or compile these legs; all return 0.

## Gate table

The entire default sweep completed: chunks 0-6, 7-13, 14-19, 20-25, and 26-32; all 33 commands returned 0.

<!-- gates:start -->
| Command | Exit | Receipt |
|---|---:|---|
| `./ooc.sh --record-rom-digests` | 0 | `record-rom-digests.log` |
| `make -C tb/verilator/mmcm_servo` | 0 | `servo-default-final.log` |
| `make -C tb/verilator/mmcm_servo mutants` | 0 | `servo-slew-mutants.log` |
| `make -C tb/verilator/crf_rx` | 0 | `crf-rx.log` |
| `make -C tb/verilator/gptp_shadow -j8` | 0 | `shadow-final.log` |
| `python3 gmstep_mutants.py --slew` | 0 | `gmstep-slew-mutants.log` |
| `python3 sw/builder/test_builder.py` | 0 | `builder.log` |
| `python3 scripts/docs_check.py` | 0 | `docs-final.log` |
| `python3 scripts/docs_check.py` | 0 | `docs-no-git-final.log` |
| `python3 scripts/check_em_dash.py --base 5b73d3f47dfed519eb988c13d6beb1db664ef1e0` | 0 | `em-dash-final.log` |
| `python3 scripts/check_doc_style.py` | 0 | `doc-style-final.log` |
| `python3 scripts/gen_toc.py --check` | 0 | `toc-final.log` |
| `python3 scripts/gen_toc.py --verify-anchors` | 0 | `anchors-final.log` |
| `python3 scripts/check_doc_paths.py` | 0 | `check_doc_paths.log` |
| `python3 docs/traceability/gen_module_matrix.py --check` | 0 | `static-recheck-4.log` |
| `python3 scripts/xvlog_gate.py --check` | 0 | `xvlog-final.log` |
| `python3 scripts/check_rtl_source_lists.py` | 0 | `check_rtl_source_lists.log` |
| `python3 scripts/check_sv_idiom.py` | 0 | `sv-final.log` |
| `python3 scripts/lint_rtl.py --check` | 0 | `lint-final.log` |
| `python3 scripts/check_cpp_idiom.py` | 0 | `cpp-final.log` |
| `python3 scripts/check_py_idiom.py` | 0 | `py-final.log` |
| `python3 scripts/check_port_contracts.py` | 0 | `check_port_contracts.log` |
| `python3 scripts/measure_naming.py --check` | 0 | `measure_naming.log` |
| `python3 scripts/measure_test_evidence.py --check` | 0 | `static-recheck-3.log` |
| `behave --no-capture -f plain` | 0 | `behave.log` |
| `git diff --check` | 0 | `diff-final.log` |
| `env OOC_TMP=/tmp/545-a303-area-base ./ooc.sh KL_mmcm_drp_servo` | 0 | `area-baseline.log` |
| `env OOC_TMP=/tmp/545-a303-area-servo ./ooc.sh KL_mmcm_drp_servo` | 0 | `area-servo.log` |
| `env OOC_TMP=/tmp/545-a303-area-alignment/results /tmp/545-a303-area-alignment/ooc.sh KL_slew_alignment` | 0 | `area-alignment.log` |
| `make -C tb/verilator/mmcm_servo_autorepair` | 0 | `servo-autorepair.log` |
| `make -C tb/verilator/gptp_txts run` | 0 | `gptp-txts-run.log` |
| Default milan_dp run sweep, exact recipe split into five foreground chunks | 0 for all 33 commands | `sweep-plan.json`, `sweep-results.jsonl`, `sweep-00.log` through `sweep-32.log` |
<!-- gates:end -->

`gates.jsonl`
records command, working directory, exit code and duration. `sweep-plan.json`
is the exact `make -n run` expansion, with display-only echoes omitted;
`sweep-results.jsonl` records each command's exit and duration. Required ROM
prerequisites were already generated from the adopted pin before planning.
Every command runs synchronously in its runner, with a four-hour deadline;
no shell pipeline hides a gate result.

The final simulation environment uses the repository-pinned 5.050 release and
eight build jobs where the recipe exposes that setting. Early focused checks
used the system 5.052 release and are retained as development evidence only.
The existing hash-pinned Markdown environment supplies documentation dependencies.
No toolchain, environment, installed package or tree export is in this packet.

Builder returned 0. Its RV32 compilation and source census ran. Gate 11's real
board-report calibration is **NOT RUN** because the required report is absent.
The no-Git documentation run passes and explicitly skips only inventory parity,
which requires Git metadata. The rest of its scrub and routing controls run.
The final analysis gate reports 0 parent findings and 4 existing pinned-processor
findings, matching its ratchet. Lint remains at 90/90 with existing waivers; no
warning budget was increased. No physical hardware result, hosted CI result or
independent review is claimed.

## Area

Repository recipe: `cd syn/yosys && ./ooc.sh KL_mmcm_drp_servo`, with a distinct
`OOC_TMP` for each measurement. The baseline ran before edits at `5b73d3f4`;
the candidate uses the final executable RTL. Mapping is
`synth_xilinx -family xc7 -flatten`, default parameters, no `-nodsp` override.
All three local measurements used Yosys 0.66 (`86f2ddebc-dirty`), as recorded
in the detailed reports; the baseline and candidate used the same installation.

| Measurement | LUT | LUTRAM | FF | RAMB36 | RAMB18 | DSP | CARRY4 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Baseline servo | 864 | 0 | 790 | 0 | 0 | 1 | 150 |
| Candidate servo | 871 | 0 | 792 | 0 | 0 | 1 | 150 |
| Servo delta | +7 | 0 | +2 | 0 | 0 | 0 | 0 |
| New isolated datapath release block | 1 | 0 | 4 | 0 | 0 | 0 | 0 |
| Sum of isolated parent additions | +8 | 0 | +6 | 0 | 0 | 0 | 0 |

All three measurement commands returned 0. Summary receipts are
`area-baseline.log`, `area-servo.log`, `area-alignment.log`; full reports are
`area-*-detail.log`. `area-alignment.sv` is the exact new datapath block with a
minimal port wrapper. `area-alignment-recipe.patch` shows the only recipe
adaptations: fixed repository/support paths and one extra top/source entry.
ROM generation, pin/digest verification, mapping and reporting remain the
repository recipe. No standalone state is added by the shadow pass-through.

This is **not** a measured whole-datapath delta: constants and shared logic can
change integrated mapping. The adopted processor has a separate published
[PR #76 measurement](https://github.com/Mister-M-alt/FPGA-gPTP/pull/76#issuecomment-5818298785):
4,773 -> 4,853 LUT (+80), 3,646 -> 3,652 registers (+6), unchanged memory/DSP.
That upstream measurement uses a different flow and is not added to the local
figures or represented as a fresh measurement here. No implementation timing or
board area measurement was run in this assignment.

## Development failures and disposition

- Initial connected build lacked visibility of the consumed offset wire;
  added the read-only simulation annotation, rebuilt and passed all 56 checks.
- Initial U14 snapshotted the tally before an unrelated window boundary;
  moved the snapshot immediately before the replacement step. No RTL behavior
  was changed for that fixture correction; the final 94-check unit run passes.
- First shadow mutation run refused an uncommitted index after its 309-check
  positive passed. Committed inputs, then restarted the full required gate.
- Documentation style/contents checks first reported wording and list spacing;
  corrected prose and regenerated the contents. The initial anchor gate lacked
  its pinned renderer; reran using the existing pinned environment.
- Evidence census initially identified the new mutation reader as unaccounted;
  added its actual disposition, preserving all ratchets. Final census passes.

All development receipts remain present; they are not substituted for final
successful gate receipts.

## Handoff boundary

One local commit, no push, PR operation, merge, other worktree/checkout, donor
edit, sub-agent or hardware action. The only submodule checkout is the exact
pin explicitly required by item 1. No private transcript was read. Review and
publication remain for the assigned independent reviewers and manager.
`PR-BODY.md` is the proposed text. All assigned gates and packet checks are complete, with the tree clean.
The final authorized action is to post `[A303] REVIEW READY` with this head
on #545, then stop.
