[A576]

# Issue 621 handoff

Status: REVIEW READY after round 1f, under [final ruling 6089776382](https://github.com/kebag-logic/milan-fpga/issues/621#issuecomment-6089776382). The lane invariant passes: the candidate's capture logs equal the base's, byte for byte, in all six arms and three controls. The receipt is recorded as measured in `e0ee38f9`; the input gate passes and every bound holds. At that head the static gates, Yosys (58 of 58), the 61-suite sweep (61 of 61, 2,186,819 checks) and every vendor stage pass. See "Round 1f" at the end; the round 1e and earlier STOP sections are historical.
Round 1e status (historical): STOP in round 1e. Under [ruling 6088189432](https://github.com/kebag-logic/milan-fpga/issues/621#issuecomment-6088189432), the full receipt campaign ran on Verilator 5.052 at parent 034e2e30 with donor 7dda9c3b. All six arms and three controls exit 0. Both 8x8 contract arms (CPU 50 MHz) change verdict fields: `sys_cycles`, `responses` and `reads` in captures 0 to 2, and the minimum, maximum and margin. The ruling makes any verdict-field change a STOP. Attribution places the cause on dev: the original base with the original donor writes byte-identical capture logs to the candidate's, and the receipt's measured tree reproduces the receipt. No round 1e commit was made. The sweep and vendor stages were not started. See "Round 1e STOP" at the end.
Round 1d status: STOP. The original parent base with the original donor also returns 24690 requests at capture 2, on both the pinned 5.050 simulator and the receipt's recorded 5.052. Ruling 6087655217 classifies this result as harness drift and explicitly requires STOP. The receipt's own measured tree reproduces the receipt exactly, so the drift comes from capture-SoC RTL that changed on dev after the receipt was recorded. It is not caused by the donor. No new commit was made.
Parent head: e0ee38f9d94bba29289f24f8f80a8d9645643c11.
Round 1f receipt commit: e0ee38f9d94bba29289f24f8f80a8d9645643c11.
Resume baseline: 72848a76c67611bf7abe8b5e480a80f1b517626c.
Round 1b harness commit: 034e2e30f225f3fcd755cac8ad01c60dda5b366a.
Implementation commit: a99dbccf75d2de972aeb9ac56bce73a9d94f9b57.
Parent base: 5603c353137e90c1fa95429f6d00ef7a2298d9ee.
Donor head: 7dda9c3b4d65cbbb28f72a34e1ee0efe368695d9.
Donor base: 5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d.
Branch in both repositories: 621-ascapable-phc-step.
Executor: [A576]. Independent reviewers: [R570], [R571].
All commits are local and unpushed. The parent worktree is clean.
REVIEW READY at parent `e0ee38f9` with donor `7dda9c3b`. Every gate the change touches exits as required. One open documentation follow-up is listed in "Field diff against the old receipt".
The follow-up adds positive INTERNAL-source CLOCK_DOMAIN checks beside the CRF case.
Publish the donor before the parent so its gitlink is fetchable.

## Scope and references

The assignment covers simulation reproduction, the gPTP correction and consumer validation.
The physical five-step repeat belongs to the later lane and closes #621.
No hardware access, publication, review approval or merge occurred.
The assignment and its donor-remote correction were read, together with #621,
#387, #620, docs/findings/387_SOFTWARE_GM_STEP.md and the gPTP design pages.
IEEE 802.1AS-2020 clauses 11.2.2, 11.2.19.3.3, 11.2.19.3.4 and 11.2.20 supply the cited contracts.

## Mechanism and correction

The rate calculation compared successive peer t3 and local t4 values across a local phase discontinuity.
That converted a phase correction into an apparent frequency ratio change.
The resulting link-delay rejection cleared the two-good-exchange capability ladder.

The focused test uses the real PHC counter at 8 MHz with a 125 ns increment.
The peer has an independent LocalClock and the request cadence remains one real second.
Physical link delay is 500 ns each way and responder turnaround is 800 us.
A better Announce and Sync/Follow_Up drive each signed 10 ms correction.

| Original image stimulus | Computed delay | asCapable outage |
|---|---:|---:|
| +10 ms | -3466 ns | 2000001750 ns |
| -10 ms | 4545 ns | 2000001250 ns |

The direct-engine observation preserves the signed negative result.
The parent publication normally clamps negative delay to zero.
The corrected image produces no capability loss or invalid delay in either arm.

On a servo step, the donor invalidates only the rate-history seed.
It retains the last valid ratio and delay.
A completed exchange overlapping the step supplies liveness but no replacement measurement.
The next newly issued request rearms measurement.
Both ordinary pair completion and deferred transmit-timestamp completion use that guard.
Missing replies and multiple-responder accounting retain their original paths.

The ROM uses 1016 of 1024 instructions; counter-seeded variants use 1017.
The redundant cold initialization of S_NR4 was removed to retain the existing ROM depth.
S_NR4 is read only behind a valid S_NR3 seed, and their save writes both together.

## Changes by file and line

Existing gPTP paths refer to the parent head above. Donor paths refer to the donor head.
The round 1b changes below affect only the capture harness.
Generated rasters and the gitlink are artifacts rather than line-addressable source.

| File:line or artifact | Change |
|---|---|
| tb/verilator/nvm_capture_cpu/run.py:58, :78 | Keep shared capture checks; apply the 24.5 ms bound only to production arms, with missing mutation metadata treated as production |
| tb/verilator/nvm_capture_cpu/run.py:104, :116 | Preserve ratio controls and add a 25 ms byte-only pass and production rejection |
| tb/verilator/nvm_capture_cpu/measurements.json:2, :3, :46, :95 to :1377 | Round 1f receipt refresh: 56 values in place, every one listed in "Field diff against the old receipt" |
| Donor hdl/ucode/gen_gptp_ucode.py:270 | State-validity invariant permits omitting redundant S_NR4 initialization |
| Donor hdl/ucode/gen_gptp_ucode.py:339 | Exchange-crossing state allocation |
| Donor hdl/ucode/gen_gptp_ucode.py:834 | Servo step invalidates rate seed and marks the pending exchange |
| Donor hdl/ucode/gen_gptp_ucode.py:1283, :1697 | Both completed-pair paths enter the guard |
| Donor hdl/ucode/gen_gptp_ucode.py:1298 | A new request rearms measurement |
| Donor hdl/ucode/gen_gptp_ucode.py:1353 | Remove redundant cold initialization |
| Donor hdl/ucode/gen_gptp_ucode.py:1727, :2046 | New guarded dispatch leg and its registration |
| Donor docs/INTEGRATION.md:192 | Phase-step measurement contract and standard clauses |
| Donor docs/SOURCE_EVIDENCE.md:30 | Updated source-line reference |
| Donor syn/ooc/work/gptp_ucode.hex:8 | Regenerated default image |
| Donor tb/verilator/ucpu/gptp_ucode.hex:8 | Regenerated default image |
| Donor tb/verilator/engine/gptp_ucode.hex:8 | Regenerated 2 MHz, 3000 ms cease image |
| Donor tb/tsngen/gptp_ucode.hex:8 | Regenerated 2 MHz image |
| gptp-processor gitlink | Adopt donor head |
| tb/verilator/gptp_plane/Makefile:23 | Default suite includes the focused campaign |
| tb/verilator/gptp_plane/gptp_plane_wrap.sv:36, :113 | Parameterize the PHC increment; existing default remains 8 ns |
| tb/verilator/gptp_plane/sim_phc_step.cpp:1 | Real-counter test, independent peer and overlap assertions |
| tb/verilator/gptp_plane/phc_step.py:1 | Isolated clean image and three planted microcode defects |
| tb/verilator/milan_dp/sim_gmstep.cpp:612, :714 | Independent peer timestamps at the real root boundaries |
| tb/verilator/milan_dp/sim_gmstep.cpp:243, :476, :941 | Continuous observations and public effects checks for both signs |
| docs/design/GPTP_PLANE.md:32, :97 | Adopted pin, phase-step contract, commands and simulation limits |
| docs/design/TIME_SYNC.md:115 | Adopted donor link |
| docs/guides/gptp/HDL_DEVELOPER.md:33 | Adopted donor links |
| docs/guides/gptp/MANAGER.md:23 | Adopted donor links |
| docs/guides/gptp/SYSTEM_INTEGRATOR.md:61 | Adopted donor link |
| docs/guides/gptp/TEST_DEVELOPER.md:30 | Adopted donor link |
| docs/reference/SUBMODULES.md:24, :291 | Current pin and donor references |
| docs/traceability/ieee8021as.md:53 | Current donor reference |
| docs/diagrams/submodule_boundaries.drawio:1, .svg:41, .png | Generator-rendered pin update |
| docs/diagrams/timesync_chain.drawio:1, .svg:47, .png | Generator-rendered pin update |
| docs/diagrams/PNG_MANIFEST.json:12 | Regenerated raster receipts |
| syn/yosys/rom_digests.tsv:32 | Generator-recorded images for the adopted pin |

## Tests and planted defects

Round 1f adds receipt-path checks; see "Round 1f tests and planted defects" at the end.

| Test or arm | Defect it catches | Evidence |
|---|---|---|
| Signed steps between exchanges | Keeping pre-step rate history poisons the next ratio | Original image fails 12/49 final checks; stale-rate-window mutant rejected |
| Step between returned t1 and response, both signs | Measuring an exchange spanning the discontinuity | Crossing-exchange mutant rejected |
| Step between response and follow-up | Late pair completion bypassing the epoch guard | Explicit phase assertion and crossing-exchange mutant |
| Complete response before step, deferred t1 afterward | Deferred completion bypassing the same guard | Explicit phase assertion and crossing-exchange mutant |
| Physical delay rises to 1500 ns | Permanently retaining the old measurement masks a real link fault | Never-rearm-measurement mutant rejected |
| Physical delay returns to 500 ns | A genuine fault cannot requalify | Recovery assertion passes; no separate dedicated mutant |
| Peer stops replying | Step handling manufactures liveness | Timeout assertion passes; no separate dedicated mutant |
| Parent small-step integration | Peer timestamps derived from DUT PHC can hide the rate defect | Original image fails 40/190 final checks, including capability, delay, uncertainty, GM counts and INTERNAL domain edges |
| Parent public effects | Extra uncertainty, GM counts, capability loss or transport interruption | 190 checks pass; original image rejected; 20 existing controls rejected |
| Parent CLOCK_DOMAIN observation | Assuming old tu-only semantics under selected CRF | Original image produces three INTERNAL edge pairs and is rejected; corrected image produces one |

Focused clean run: 49 checks, zero failures.
Campaign: clean image plus three required runtime failures, exit zero.
Parent integration: 190 checks, zero failures.
All new assertions observe execution or public responses; overlap positions are asserted against actual event cycles.

## Coverage

| Assigned obligation | Evidence | Status |
|---|---|---|
| Reproduce both signed 10 ms steps and approximately 2 s outage | Original-image logs and table above | Met |
| Explain mechanism with normative clauses | Rate-window analysis and documented clauses | Met |
| Preserve capability and physical delay | Six focused arms, continuous parent observations | Met |
| Prove tests reject planted defects | Three isolated mutations | Met |
| Check uncertainty and GM count effects | One tu episode and one GPTP_GM_CHANGED per step | Met |
| Check CLOCK_DOMAIN counts | Unchanged for unlocked CRF; one unlock/lock pair at INTERNAL | Met |
| Media remains unaffected | No mr change, no MEDIA_RESET, no listener unlock, continuing accepted frames | Met in simulation |
| Required full gates | Round 1f at `e0ee38f9`: static gates, input gate, Yosys, 61-suite sweep and every vendor stage pass | Met |
| Round 1b harness change and required controls | Commit above; five controls pass and both planted timing defects are rejected | Met |
| Receipt campaign and refresh | Round 1f: nine of nine capture logs byte-identical to the base; receipt recorded as measured in `e0ee38f9`; input gate passes; every bound holds | Met |
| Complete 61-suite sweep | Round 1f at `e0ee38f9`: 61 of 61 suites, 2,186,819 checks, zero failures | Met |
| Shipping resource measurement | Round 1f at `e0ee38f9`: three routes fully routed with timing met; route-1x1, ooc-1x1 and ooc-8x8 pass the resource gate with zero delta; check-baseline passes | Met |
| Physical repeat | Later lane | Not performed |

This is an executor's acceptance map, not a clean-review ledger.
No reviewer coverage is claimed for Conformance, RTL, Robustness, Tests or Docs.
The assigned independent reviewers must publish the covering round and exact head for each lens.

## Gates before round 1b

These results predate the harness commit. Current-head round 1b results appear below.

Commands below are plain shell, run from the corresponding checkout with the pinned dependencies.
Long-running gates use separate external logs and exit-status receipts.

| Command | Current result | Evidence name |
|---|---|---|
| git remote get-url origin; git rev-parse HEAD | Expected origin and original base confirmed | Initial check |
| python3 tb/verilator/gptp_plane/phc_step.py --work "$RESULTS/phc-final" --mutants | Exit 0; 49 clean checks and 3 rejected defects | phc-final.log |
| make -j1 -C tb/verilator/milan_dp gmstep VERILATOR_JOBS=2 | Exit 0; 190 checks | gmstep-clock.log |
| make -j1 in donor checkout | Exit 0; includes 34 engine mutation controls | donor-gates.log |
| make -j1 -C tb/verilator/milan_dp gmstep-mutants VERILATOR_JOBS=2 | Exit 0; 22 checks, both clean legs and 20 rejected controls | gmstep-mutants.log |
| scripts/run_all_suites.sh "$RESULTS/suite-logs" | Cancelled at STOP; 39 of 61 suites passed, through milan_dp; milan_dp_mclk interrupted | full-suites.log; full-suites.cancelled.rc |
| scripts/run_all_suites.sh "$RESULTS/physical-logs" --physical-gptp | Exit 0; 197 checks, zero failures or timeouts | physical.log |
| make -j1 -C tb/verilator/milan_dp ax1x1gptp-extended VERILATOR_JOBS=2 | Exit 0; 143 checks over 18.443625480 simulated seconds | physical-extended.log |
| syn/yosys/run.sh --results "$RESULTS/yosys-results" | Exit 0; 58 tops and structural gates | yosys.log |
| python3 scripts/lint_rtl.py --check | Exit 0; 90 violations within ratchet | lint.log |
| python3 scripts/docs_check.py | Exit 0; zero findings | docs-check.log |
| python3 scripts/check_cpp_idiom.py | Exit 0 | Recorded terminal verdict |
| python3 scripts/check_py_idiom.py | Exit 0 | Recorded terminal verdict |
| python3 scripts/check_doc_style.py | Exit 0 | Recorded terminal verdict |
| python3 scripts/check_gptp_docs.py --with-submodule | Exit 0 | Recorded terminal verdict |
| python3 scripts/check_diagram_pngs.py | Exit 0 | Recorded terminal verdict |
| python3 scripts/gen_toc.py --check | Exit 0 | Recorded terminal verdict |
| python3 scripts/check_em_dash.py --base 5603c353137e90c1fa95429f6d00ef7a2298d9ee | Exit 0 | em-dash.log |
| scripts/run_suites.sh in protocol checkout | Exit 0; 1,028,250 checks, zero failing suites | protocol-gates.log |
| behave -f plain in tests | Exit 0; 404 scenarios, 1968 steps | behave.log |
| python3 scripts/check_nvm_capture.py | Exit 0; input receipts and named controls | nvm-input-gate.log |
| CPU capture recipe: six traffic/clock cases and three named controls | Five positive cases and two controls exit 0; byte-only exits 1; 100 MHz traffic-OFF interrupted at STOP | nvm-campaign.log; nvm-results/*.rc |
| Original-base byte-only comparison, same command and inputs below | Exit 1, identical measurements and timing rejection | nvm-byte-base.log; nvm-byte-base.rc |
| Resource helper self-test, helper mutations, gate self-test and gate mutations | Exit 0; includes 174 rejected resource-gate mutations | resources/pp_*.log |
| Shipping export recipe, both shapes | Exit 0; firmware and images generated | resource-export.log |
| python3 "$RESULTS/builder-sdk-run.py" | Exit 0; RV32 and required elaborations ran; one historical calibration arm unavailable | builder-gates.log |
| python3 scripts/xvlog_gate.py --check | Not run; cancelled before vendor stage | stop-cancellation.log |
| Shipping route, all three placement directives | Not run; prepared exports retained | stop-cancellation.log |
| Standalone 1x1 and 8x8 synthesis, integrated clock | Not run | stop-cancellation.log |
| python3 syn/ooc/pp_resource_gate.py check <measurement> --endpoint <endpoint> | Not run; no measured endpoints | stop-cancellation.log |

An initial sweep failed its hard-HUP cancellation control because the detached launcher inherited HUP ignored.
The launch environment now restores the normal HUP disposition before entering the unchanged gate.
The rerun passed that preflight and selected the full suite inventory.
The domain checks follow #629 C1: no edge while following an unlocked servo, one edge pair at INTERNAL.
No production clock-domain behavior was changed.

## Historical state after round 1c STOP

The permitted round 1b harness correction is complete.
The next ruling allowed a receipt refresh only with identical production values.
The fresh run violates that condition, as recorded below.
A public disposition of the production-value mismatch is needed before resuming.
No receipt field or gate enforcement was changed.

After that disposition, complete the capture campaign, the full parent sweep and
resource recipe, including the vendor frontend and all measured endpoints.
Earlier partial runs do not establish a complete local-bar pass.
The shipping exports remain available, but no endpoint was measured.
The later physical repeat remains outside this implementation lane.
No push, PR operation or merge is authorized.

## Focused evidence artifacts

- phc-original.log: original image under the final 49-check harness.
- phc-corrected.log: the corrected image under that same compiled harness.
- phc-mutations.log: clean result and all three named defect rejections.
- effects-original.log: original image under the final 190-check integration harness.
- effects-corrected.log: corrected-image simulation output, extracted from the build log.
- effects-mutations.log: both clean legs and all 20 named control verdicts.

The expanded original-image control must fail capability, delay and CLOCK_DOMAIN assertions.
Its control driver exits zero only after confirming those runtime failures.

The builder compatibility check maps only the canonical compiler selector's argv[0]
to the verified SDK. Remaining arguments and gate oracles are unchanged.
The audit records both requested and executed compiler commands.
The host's existing compiler installation was not modified.

## Validation provenance

The isolated parent sweep started on the implementation commit.
Before it reached the datapath suite, its checkout advanced to the final parent head.
Only the integration test and its design-page description changed in that advance;
already completed suites consume neither file. All production synthesis inputs are identical.
The explicit effects campaign and both shipping exports use the final head.
The donor and protocol sweeps use the respective pinned revisions.

The prepared shipping measurement uses single-thread synthesis, the shipping constraints and
full initialized firmware. The queued default route would compare with the recorded resource policy.
The two additional placement directives are prepared to reuse that synthesis checkpoint.
No synthesis checkpoint or routed timing report was produced. The standalone endpoints use the elaborated 50 MHz clock.
The 8x8 standalone parameters come from the recipe's permitted RTL elaboration.

The builder command executes the unchanged `test_builder.py` with
`--require-rv32 --require-elaboration` through the documented SDK selector mapping.
Its return code is zero and no required elaboration was skipped for a toolchain reason.
One unrelated historical resource-calibration arm did not run: its archived Arty
placement report is absent. This result does not claim coverage for that arm.
The physical campaign and extended arm run independently in isolated final-head checkouts;
all simulation builds share a two-build limit.

`ARTIFACTS.tsv` records byte sizes and SHA-256 values for external raw logs,
reports, commands and the gPTP and CPU comparison executables.
It is refreshed at handoff; raw build trees and large files remain outside this directory.

The CPU capture campaign builds the changed gPTP image even though it is outside
the default sweep. Its documented six positive cases use 16 captures each;
`skip-copy`, `no-traffic` and `byte-only` use two captures each. The latter binds
the newly measured 8x8/50 MHz traffic-ON baseline. All four workers use offline
network namespaces, cached dependencies and the pinned simulator. These runs
grade capture behavior and timing; they do not establish gPTP behavior.

The CPU campaign initially used two workers. It was rescheduled to four isolated
workers to run independent clock/traffic cases concurrently. The completed 1x1
traffic-ON case is retained at the unchanged head, with its zero exit receipt and
all 16 graded rows. Incomplete runs were archived and restarted, without changing
arguments or oracles. The shared two-build limit remains in force.

The extended physical-clock arm passed all 143 checks over 922181274 cycles.
It checked 7074624 payload comparisons, 884326 sample-order comparisons and
147544 packet-sequence comparisons; both declared recentres completed.
Its scope excludes licensed ACMP/SRP streaming, physical TDM render, CRF recovery,
multiple-responder cease, PHY/MAC calibration, CPU/DDR and physical compliance.
The first 10 ms of payload comparisons in each reset epoch is declared warm-up.

## CPU capture reproduction

The consumer recipe is `tb/verilator/nvm_capture_cpu/README.md`.
Each row invokes the following command from its isolated final-head checkout:

```sh
python3 tb/verilator/nvm_capture_cpu/run.py --shape "$SHAPE" --cpu-hz "$CPU_HZ" --captures "$CAPTURES" --traffic "$TRAFFIC" --mutation "$MUTATION" --build-dir "$RESULTS/$CASE"
```

| Case | SHAPE | CPU_HZ | CAPTURES | TRAFFIC | MUTATION |
|---|---|---:|---:|---|---|
| 1x1-50-on | endstation_ax7101_1x1_tdm8 | 50000000 | 16 | on | none |
| 1x1-50-off | endstation_ax7101_1x1_tdm8 | 50000000 | 16 | off | none |
| 8x8-50-on | endstation_ax7101_8x8 | 50000000 | 16 | on | none |
| 8x8-50-off | endstation_ax7101_8x8 | 50000000 | 16 | off | none |
| 8x8-100-on | endstation_ax7101_8x8 | 100000000 | 16 | on | none |
| 8x8-100-off | endstation_ax7101_8x8 | 100000000 | 16 | off | none |
| 1x1-skip-copy | endstation_ax7101_1x1_tdm8 | 50000000 | 2 | on | skip-copy |
| 1x1-no-traffic | endstation_ax7101_1x1_tdm8 | 50000000 | 2 | on | no-traffic |
| 8x8-byte-only | endstation_ax7101_8x8 | 50000000 | 2 | on | byte-only |

The byte-only row additionally supplies
`--baseline-measurement "$RESULTS/8x8-50-on/measurement.json"`.
Skip-copy must expose missing descriptor records; no-traffic must expose missing
concurrent request/response traffic; byte-only must exceed 1.5 times the matching
baseline maximum. Round 1b removes the production-only duration bound from this
control while retaining its shared capture checks.
The 100 MHz rows are comparison measurements, not the shipping-clock contract.

## Historical round 1a STOP: base-reproduced validation blocker

The candidate byte-only CPU capture control's first row measured 2543094 system
cycles at 100 MHz, or 25.43094 ms. The unchanged ordinary timing oracle permits
at most 24.5 ms (`tb/verilator/nvm_capture_cpu/run.py:79`). The normal word-copy
candidate passed all 16 captures, with a maximum of 13.86318 ms.
The control finished with driver exit 1. Its second row measured 2542688 cycles,
or 25.42688 ms. Both native byte/record checks passed; the duration oracle rejected
the completed run. The original parent base, with the original donor pin, also exits 1 and produces
identical rows: 2543094 and 2542688 cycles. The native simulator finishes three
checks with zero failures on both revisions; the unchanged Python duration oracle
rejects each completed run. The firmware ROM and all memory initialization bytes
are identical between the comparisons, while the gPTP ROM hashes differ.
See capture-blocker.log and capture-inputs.tsv. No capture implementation, threshold or acceptance criterion changed.
A fix outside the gPTP plane or its tests requires STOP under the assignment.

The original-base comparison reused the completed traffic-OFF worker checkout only
after its candidate run had finished. That checkout now holds the original base;
its earlier 50 MHz traffic-OFF receipt belongs to the candidate head. The candidate
and base byte-only runs use separate build directories and logs. The comparison
supplies the candidate word-copy baseline, but the ordinary duration rejection
occurs before the slowdown comparison reads that baseline.

At STOP, the parent sweep and CPU campaign received cancellation signals and their
owned children exited. The resource coordinator was cancelled before any vendor
command. The base diagnostic was allowed to finish and returned its own exit 1.
No background validation job remains. The expected failing old-ROM gPTP controls
are distinct from this blocking consumer-gate failure.

| Completed CPU case | Captures | Maximum ms | Driver result |
|---|---:|---:|---|
| 1x1 / 50 MHz / traffic ON | 16 | 3.96728 | 0 |
| 1x1 / 50 MHz / traffic OFF | 16 | 3.91182 | 0 |
| 8x8 / 50 MHz / traffic ON | 16 | 13.86318 | 0 |
| 8x8 / 50 MHz / traffic OFF | 16 | 13.69390 | 0 |
| 8x8 / 100 MHz / traffic ON | 16 | 10.42973 | 0 |
| Candidate byte-only / 50 MHz | 2 | 25.43094 | 1 |
| Original-base byte-only / 50 MHz | 2 | 25.43094 | 1 |

The shipping-clock maxima across both traffic arms are 3.96728 ms for 1x1 and
13.86318 ms for 8x8. The 100 MHz traffic-OFF run was interrupted, so no combined
100 MHz maximum is claimed. Skip-copy and no-traffic each caught their named fault
with two captures and driver exit 0.

## Round 1b resume

The [manager ruling](https://github.com/kebag-logic/milan-fpga/issues/621#issuecomment-6087415319)
permits one separate change to `tb/verilator/nvm_capture_cpu/run.py`.
The production bound stays 24.5 ms. The byte-only control retains every
completion, byte, record, ownership, traffic and slowdown check.
The census growth in `d81198c2` exposed the prior grading error.
Both resumed heads were verified against the requested revisions.
No new takeover comment was posted.

The grader controls passed and the permitted commit is complete. The input gate
then stopped this round before the capture campaign, full sweep or vendor jobs
started. Existing successful evidence above remains evidence for its recorded
head and unchanged inputs; it does not establish a complete current-head pass.

### Round 1b change and tests

Only `tb/verilator/nvm_capture_cpu/run.py` changed in this round.
No capture implementation, firmware, production bound or measurement changed.
`grade_rows` continues to validate completion, bytes, records, ownership and traffic.
`spec.get('mutation', 'none')` retains the production bound for recorded arms
whose metadata omits the mutation key.

| Test | Planted defect or invalid input detected | Result |
|---|---|---|
| Existing 1.5x equality | An erroneously strict ratio boundary | Pass |
| Existing 14.99999 ms against 10 ms baseline | Inert or insufficient byte-only slowdown | Rejected |
| Existing clock mismatch | Comparing different capture scenarios | Rejected |
| New 25 ms byte-only row against 10 ms baseline | Applying the production duration bound to the slow control | Pass; replacing the production predicate with true fails this test |
| Same 25 ms row with mutation none | Removing the production duration bound | Rejected; replacing the production predicate with false fails this test |
| Existing input-gate controls | Changed census/clocks, omitted OFF maximum, one-tick production overrun | All detected before receipt rejection |

The two timing mutations were applied only in memory for the test.
The source file and the recorded measurements were not mutated.

| Round 1b command or gate | Exit | Evidence |
|---|---:|---|
| `PYTHONPATH=tb/verilator/nvm_capture_cpu python3 -B -c 'import run; run.byte_only_controls()'` | 0 | resume-controls.log; terminal control results |
| In-memory production-predicate mutations described above | 0 | Both defects rejected by the controls |
| `python3 -B scripts/check_py_idiom.py` | 0 | 368 modules; no new idiom violations |
| `git diff --check` before committing | 0 | Clean whitespace |
| `python3 scripts/check_nvm_capture.py` | 1 | resume-nvm-input-gate.log |
| Capture campaign, all six positive cases and three controls | Not run | STOP before restart |
| Complete parent sweep, 61 suites | Not run | STOP before restart |
| Vendor frontend, routes and resource measurements | Not run | STOP before restart |

### Round 1b STOP: receipt outside the authorized file

`scripts/check_nvm_capture.py:61` hashes every Python and C++ harness file.
It compares those hashes with `measurements.json` before grading its measurements.
The permitted `run.py` edit necessarily changes its hash.

| Receipt field | SHA-256 |
|---|---|
| `tb/verilator/nvm_capture_cpu/measurements.json:46` | `1bddc676e452a885f11f8cc1e6fe75a3b6e0df8f8d704baade0ee1f5f72d5dea` |
| Current committed `run.py` | `c230cb3e6289bf991554b8d967e0993ec7860e119afb44579580c339a8191659` |

The gate exits 1 with `measurement harness changed; refresh measured evidence`.
Updating the receipt requires modifying another file. The resumed assignment
limits the extra commit to `tb/verilator/nvm_capture_cpu/run.py`; the manager
ruling also prohibits changing recorded measurements. The receipt and the gate
remain untouched. A public scope decision on refreshing the receipt is needed
before the complete local bar can pass. Fresh campaign evidence must accompany
any authorized receipt refresh; this round claims no new measurement.

All validation processes started in this round have exited. No background job
was started, and no vendor lock was acquired. Both worktrees remain clean.
No push, PR operation, merge, hardware operation or second TAKEN comment occurred.
A new STOP comment records the current parent and unchanged donor heads.

## Round 1c resume

The [receipt-refresh ruling](https://github.com/kebag-logic/milan-fpga/issues/621#issuecomment-6087498843) authorizes a separate campaign-generated receipt commit. Production values must remain byte-identical. Only harness hashes and recorded byte-only control fields may differ. The input gate stays unchanged. Parent 034e2e30 and donor 7dda9c3b were verified; no second takeover comment was posted.

### Fresh production-value failure

The first resumed production case uses 1x1, CPU 50 MHz, system 100 MHz,
traffic ON, mutation none, and requests all 16 captures.
It rebuilds from the unchanged parent head and pinned donor.
The simulation emits four complete rows before cancellation.
Row 2 differs from `tb/verilator/nvm_capture_cpu/measurements.json:95`.

| Source | index | ok | sys_cycles | raw | records | mismatches | open | requests | responses | reads |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Committed receipt | 2 | 1 | 396442 | 3290 | 54 | 0 | 0 | 24691 | 26 | 1006 |
| Fresh production capture | 2 | 1 | 396442 | 3290 | 54 | 0 | 0 | 24690 | 26 | 1006 |

Only `requests` differs among the four observed rows.
The observed duration and byte/ownership checks do not differ.
The ruling covers every production value, so this counter difference requires STOP.
The owned background process group was terminated immediately after detection.
Cancellation is recorded as 143; no campaign pass is claimed.
No aggregate receipt or completed per-case measurement was generated.

The product firmware source retains SHA-256
`a73ecc25c77bfb7c4e1c2c711d72f0b560dd7e8d18cde92f40e67efcc84f0eb3`.
The rebuilt BIOS matches the receipt's SHA-256
`afb2f54f1a80549c12ed853a6ce9789da822da1408e15f6be0a8c4e859eaed57`.
The required pinned simulator is version 5.050; the historical receipt names 5.052.
The current donor also differs from that historical receipt's donor.
Neither difference had been established as the counter discrepancy's cause in round 1c.
Round 1d below rules out both and establishes the cause.
No environment change or production-value relaxation was attempted.

### Round 1c commands and gates

The production command runs from an isolated checkout at the parent head.
It uses the product interpreter, offline dependencies and a network namespace with networking disabled, as the recipe requires:

```sh
python3 tb/verilator/nvm_capture_cpu/run.py --shape endstation_ax7101_1x1_tdm8 --cpu-hz 50000000 --captures 16 --traffic on --mutation none --build-dir "$RESULTS/round1c-capture/1x1-50-on"
```

The command uses the same shapes, clocks, phase, capture count and traffic
parameters as the receipt. The explicit `mutation none` is the default.
The environment retains offline dependencies and `PYTHONHASHSEED=0`.
The build uses eight workers, with no second concurrent build.
Peak service memory was 2.88 GiB. Final free data space was 76.54 GiB.

| Gate or operation | Result | Evidence |
|---|---|---|
| Verify expected parent origin and both requested heads | Pass; unchanged revisions | Initial terminal checks |
| Fresh production generation and native build | Exit 0; simulation started | External round1c-capture.log, SHA-256/size receipt |
| Production campaign, 16 captures requested | Cancelled, 143; four rows captured | round1c-capture.log; round1c-cancellation.log |
| Compare emitted production rows against committed receipt | Exit 1; row 2 requests differs | round1c-production-diff.json |
| Product firmware source and rebuilt BIOS hashes | Equal to committed receipt | round1c-inputs.json |
| Receipt refresh and separate commit | Not performed under STOP condition | Empty tracked diff |
| Remaining capture cases and controls | Not restarted | STOP before continuation |
| Full 61-suite sweep | Not restarted | STOP before continuation |
| Vendor frontend, route and standalone resources | Not started | No exclusive vendor lock acquired |

The row comparison detects any unequal field in each emitted production row;
its concrete failing input is the request-count difference above.
This administrative invariant is additional to the harness's runtime checks.
The existing production-duration bound and capture oracles were not changed.

### Receipt diff and file state

```sh
git diff --numstat 034e2e30f225f3fcd755cac8ad01c60dda5b366a -- tb/verilator/nvm_capture_cpu/measurements.json
git diff 034e2e30f225f3fcd755cac8ad01c60dda5b366a -- tb/verilator/nvm_capture_cpu/measurements.json
```

Both outputs are empty: 0 added lines, 0 deleted lines, 0 changed files.
The unchanged 36,969-byte receipt has SHA-256
`ed871bdd09bde7ebde1ae021cd647e3cad354d3f8682c5b7308cda91e4cbd72a`.
There are no new source changes or commits in round 1c.
`check_nvm_capture.py` remains unchanged and its stale-hash rejection remains unresolved.
The round 1b grading correction and its two planted timing controls remain committed.

The small evidence files include the full before/after rows and raw capture.
`ROUND1C-ARTIFACTS.tsv` records external build logs, executables and generated
inputs by size and SHA-256. Large files and build trees remain in scratch.
No background validation process remains. Nothing was pushed or opened as a PR.
A new STOP comment records the unchanged heads and the production rows.


## Round 1d STOP: original-base attribution reproduces the discrepancy

The [correction](https://github.com/kebag-logic/milan-fpga/issues/621#issuecomment-6087655217)
keeps every timing and correctness field byte-identical. It permits traffic-counter
differences only after its prescribed attribution: the same 1x1 traffic-ON arm at the
parent base with the original donor. A base result of 24691 at capture 2 accepts the
delta as donor-caused. A base result of 24690 is harness drift and requires STOP.
The original base returns 24690. STOP is therefore mandatory.

Two sessions ran this round. The first ran the attribution on the pinned 5.050 simulator.
It cancelled that run after three rows, once capture 2 had settled the outcome.
That session ended on an external usage limit before its STOP comment was posted.
The second session noticed that the receipt and the capture recipe name Verilator 5.052
(`tb/verilator/nvm_capture_cpu/README.md:158`). It reran the attribution on 5.052
and added two controls: the candidate, and the receipt's own measured tree.
The STOP outcome is unchanged. The source of the drift is now established.

### Attribution inputs

| Run | Parent | gPTP donor | Protocol processor | Simulator | Result |
|---|---|---|---|---|---|
| Receipt's measured tree | `a2f1734283f367d0d522c8c7cda09b79aff60d06` | `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d` | `b2db3a970cedbbff2f8ba813acb96122c442bc58` | 5.052 | 16 rows, exit 0 |
| Original base | `5603c353137e90c1fa95429f6d00ef7a2298d9ee` | `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d` | `2ad2f845dd583f8310075fa2380cb60a04fd091a` | 5.050 | 3 rows, cancelled 143 |
| Original base | `5603c353137e90c1fa95429f6d00ef7a2298d9ee` | `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d` | `2ad2f845dd583f8310075fa2380cb60a04fd091a` | 5.052 | 16 rows, exit 0 |
| Candidate, round 1c | `034e2e30f225f3fcd755cac8ad01c60dda5b366a` | `7dda9c3b4d65cbbb28f72a34e1ee0efe368695d9` | `2ad2f845dd583f8310075fa2380cb60a04fd091a` | 5.050 | 4 rows, cancelled 143 |
| Candidate | `034e2e30f225f3fcd755cac8ad01c60dda5b366a` | `7dda9c3b4d65cbbb28f72a34e1ee0efe368695d9` | `2ad2f845dd583f8310075fa2380cb60a04fd091a` | 5.052 | 16 rows, exit 0 |

The receipt's provenance field names `a2f17342` as the tree its six arms ran from.
Its `tree` field, `c28595df81fb96ae7cb554216c76a23917105169`, is that commit's tree object.
Its `processor_pins` match the pins above. At `a2f17342`, the harness hashes and the
product firmware hash equal the receipt's recorded values.
All checkouts are clean, with axis pin `48ff7a7e2ef782cf778d47910cf85835c64b1bce`.
Each submodule root was verified before its revision was read.

Every run uses 1x1, CPU 50 MHz, system 100 MHz, aligned rising edges, traffic ON and
production mutation `none`, either explicit or by default. All runs use the product interpreter,
offline dependencies, networking disabled, `PYTHONHASHSEED=0` and a two-build limit.
Every rebuilt BIOS has the receipt's SHA-256
`afb2f54f1a80549c12ed853a6ce9789da822da1408e15f6be0a8c4e859eaed57`.

### Results, every row

Each cell is the `requests` counter, with its delta from the committed receipt.
Every other field equals the receipt in every observed row of every run:
`index`, `ok`, `sys_cycles`, `raw`, `records`, `mismatches`, `open`, `responses` and `reads`.
The `responses` and `reads` deltas are therefore zero throughout.
For the three 16-row runs, every summary field equals the receipt's 1x1 traffic-ON arm.
That covers minimum, maximum, hold, floor and margin.

| Capture | Receipt | Receipt tree, 5.052 | Base, 5.052 | Candidate, 5.052 | Base, 5.050 | Candidate, 5.050 |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 24709 | 24709 (+0) | 24709 (+0) | 24709 (+0) | 24709 (+0) | 24709 (+0) |
| 1 | 24678 | 24678 (+0) | 24678 (+0) | 24678 (+0) | 24678 (+0) | 24678 (+0) |
| 2 | 24691 | 24691 (+0) | 24690 (-1) | 24690 (-1) | 24690 (-1) | 24690 (-1) |
| 3 | 24664 | 24664 (+0) | 24664 (+0) | 24664 (+0) | not run | 24664 (+0) |
| 4 | 24694 | 24694 (+0) | 24693 (-1) | 24693 (-1) | not run | not run |
| 5 | 24709 | 24709 (+0) | 24709 (+0) | 24709 (+0) | not run | not run |
| 6 | 24684 | 24684 (+0) | 24684 (+0) | 24684 (+0) | not run | not run |
| 7 | 24697 | 24697 (+0) | 24698 (+1) | 24698 (+1) | not run | not run |
| 8 | 24665 | 24665 (+0) | 24664 (-1) | 24664 (-1) | not run | not run |
| 9 | 24665 | 24665 (+0) | 24664 (-1) | 24664 (-1) | not run | not run |
| 10 | 24665 | 24665 (+0) | 24664 (-1) | 24664 (-1) | not run | not run |
| 11 | 24690 | 24690 (+0) | 24691 (+1) | 24691 (+1) | not run | not run |
| 12 | 24671 | 24671 (+0) | 24672 (+1) | 24672 (+1) | not run | not run |
| 13 | 24664 | 24664 (+0) | 24664 (+0) | 24664 (+0) | not run | not run |
| 14 | 24690 | 24690 (+0) | 24691 (+1) | 24691 (+1) | not run | not run |
| 15 | 24664 | 24664 (+0) | 24664 (+0) | 24664 (+0) | not run | not run |

The offending receipt value for capture 2 is at `tb/verilator/nvm_capture_cpu/measurements.json:95`.
All traffic counters are positive in these traffic-ON rows.
No traffic-OFF arm was run in this round.

### Established source of the drift

- The receipt's measured tree reproduces all 16 receipt rows and every summary field exactly.
  The receipt is a faithful record of that tree.
- The simulator version is not the cause. 5.050 and 5.052 give identical rows wherever both
  were observed: base captures 0 to 2 and candidate captures 0 to 3.
- The donor correction is not the cause. Base and candidate on 5.052 write byte-identical
  capture logs, with SHA-256 `01f72663af25e764b3d2336799533ae6c9ce0d95bd5c7817da78917de0be43b1`.
  Their generated gPTP ROMs differ:
  `78c8418a00b35cdae75c459c5269ca3892355507c4dc8af9eb2c29d81b87673b` at base and
  `fd3dad06a18b590aa5cdf4aa9bc7bf0a77220fe7e6214ea940870980f12de9f1` at the candidate.
  Their 116 capture-SoC source files are identical.
- Between the receipt tree and the base, the capture SoC compiles the same 116-file source set.
  30 of those files changed on dev after the receipt was recorded.
  The harness, product firmware, BIOS, census and external CPU sources did not change.
  - 7 parent RTL files: `hdl/ieee1722/aaf/KL_aaf_packetizer.sv`,
    `hdl/ieee1722/aaf/KL_chan_map_capture.sv`, `hdl/ieee1722/crf/KL_crf_rx.sv`,
    `hdl/ieee1722/maap/KL_maap.sv`, `hdl/milan/KL_nvm_backend.sv`,
    `hdl/milan/KL_pp_shadow.sv` and `hdl/milan/milan_datapath.sv`.
  - 23 protocol-processor files, from pin `b2db3a97` to `2ad2f845`.
    These include the AECP engine, descriptor store, packet-engine receive validator,
    NVM port and processor top. The per-file list is in `round1d-capture-source-diff.txt`.
- `scripts/check_nvm_capture.py` hashes the harness and product firmware, and checks
  the census and clocks. It does not hash capture-SoC RTL, so it does not flag this drift.

The drift is not narrowed to a single dev commit. No bisection was run.
These are traffic counters only; the capture's timing and correctness are unchanged.

### Decisions a refresh would still need

A campaign-recorded refresh at the candidate head would also change receipt fields
that neither ruling lists. Ruling 6087498843 limits the diff to harness hashes and
byte-only control fields; the correction adds traffic counters. Without a decision,
a refresh would reach another STOP on these fields:

- Each arm's `gptp_ucode_sha256`. For 1x1 at 50 MHz, the value changes from `78c8418a…` to `fd3dad06…`.
- `processor_pins`: gPTP `7dda9c3b`, protocol processor `2ad2f845`.
- The `base`, `tree`, `date` and `provenance` fields, which name `a2f17342`.
- `simulator`, which records 5.052. The assignment's pinned simulator is 5.050.
  Rows agree wherever both were observed, but a refresh records exactly one simulator.

### Reproduction

Run each command from the corresponding clean checkout in the capture recipe's environment:
the product interpreter, offline dependencies and networking disabled. Put Verilator 5.052,
the receipt's recorded simulator, first on `PATH`. The base and candidate command is:

```sh
python3 tb/verilator/nvm_capture_cpu/run.py --shape endstation_ax7101_1x1_tdm8 --cpu-hz 50000000 --captures 16 --traffic on --mutation none --build-dir "$RESULTS/1x1-50-on"
```

The receipt-tree command is the receipt's recorded command, with mutation `none` by default:

```sh
python3 -B tb/verilator/nvm_capture_cpu/run.py --shape endstation_ax7101_1x1_tdm8 --cpu-hz 50000000 --captures 16 --traffic on --build-dir "$RESULTS/receipt-tree-1x1-50-on"
```

### Changes, tests and gate table

No source file, generated repository artifact, receipt or enforcement code
changed in round 1d. No commit was created.
The earlier file:line and planted-defect tables remain unchanged.
This round plants no new implementation defect. It runs the mandated attribution control.
It also runs one positive control, the receipt tree, which must reproduce the receipt.
That control would expose a nondeterministic harness or simulator.

| Gate or operation | Result | Evidence |
|---|---|---|
| Expected origin, resumed heads and original-base pins | Pass; exact requested revisions, clean worktrees | round1d-inputs.json |
| Original base, 5.050, 16 captures requested | Cancelled, 143 after three rows | round1d-cancellation.log; round1d-base-capture.log |
| Original base, 5.052, 16 captures | Exit 0; harness grading passes | round1d-sim5052-base-capture.log; round1d-sim5052-base-measurement.json |
| Candidate, 5.052, 16 captures | Exit 0; harness grading passes | round1d-sim5052-candidate-capture.log; round1d-sim5052-candidate-measurement.json |
| Receipt tree, 5.052, 16 captures | Exit 0; harness grading passes | round1d-receipt-tree-capture.log |
| Receipt tree rows and summary against receipt | Exit 0; all 16 rows and all summary fields equal | round1d-receipt-tree-compare.json |
| Capture-2 attribution requirement, base 24691 | Exit 1; base gives 24690 on both simulators; mandated STOP | round1d-attribution-invariant.rc; round1d-attribution-result.json |
| Base rows against candidate rows, 5.052 | Equal; byte-identical capture logs | ROUND1D-SIM5052-ARTIFACTS.tsv |
| Receipt and input enforcement | Unchanged; prior stale-hash rejection remains unresolved | Empty tracked diff |
| Remaining five capture arms, three controls and receipt commit | Not run after STOP | Receipt unchanged |
| Complete 61-suite parent sweep | Not restarted | STOP before continuation |
| Vendor frontend, routes and standalone resources | Not started | No vendor lock acquired |
| Final whitespace and clean-worktree checks | Exit 0; clean parent and donor | Final verification |

The three exit-0 runs are single-arm harness results, not a campaign.
They do not update the receipt.
Peak service memory in round 1d was 4.73 GiB.
Final free data space was 76.54 GiB.
`ROUND1D-ARTIFACTS.tsv` and `ROUND1D-SIM5052-ARTIFACTS.tsv` record each external log,
executable, generated input, driver and comparison script by size and SHA-256.
Large logs, native executables and generated trees remain in scratch.

### Receipt diff and disposition

```sh
git diff --numstat 034e2e30f225f3fcd755cac8ad01c60dda5b366a -- tb/verilator/nvm_capture_cpu/measurements.json
git diff 034e2e30f225f3fcd755cac8ad01c60dda5b366a -- tb/verilator/nvm_capture_cpu/measurements.json
```

Both outputs are empty: 0 added lines, 0 deleted lines, 0 changed files.
The 36,969-byte receipt retains SHA-256
`ed871bdd09bde7ebde1ae021cd647e3cad354d3f8682c5b7308cda91e4cbd72a`.
The input gate remains byte-identical as well.

Both resumed heads remain unchanged. The local verification bar remains
incomplete, and this lane is not REVIEW READY. Resuming the receipt refresh and the later
gates needs a public disposition of the dev drift, plus the four field decisions above.
The later physical repeat still closes #621.
No second TAKEN, push, PR operation, merge or hardware operation occurred.
A new STOP comment records the attribution result and both heads.

Posted: [round 1d STOP](https://github.com/kebag-logic/milan-fpga/issues/621#issuecomment-6088167483).

## Round 1e STOP: dev drift reaches 8x8 verdict fields

[Ruling 6088189432](https://github.com/kebag-logic/milan-fpga/issues/621#issuecomment-6088189432)
accepts the round 1d request-count drift and authorizes a campaign-recorded receipt refresh.
The campaign uses the receipt's recipe on Verilator 5.052. Every provenance field must describe the measured tree.
These verdict fields must stay byte-identical: `ok`, `sys_cycles`, `raw`, `records`, `mismatches`, `open`,
`responses`, `reads`, and the minimum, maximum and margin. Any change to one of them is a STOP.

The complete campaign ran. All six arms and all three controls exit 0.
Both 8x8 contract arms (CPU 50 MHz) change verdict fields in their first three captures.
The ruling makes that a STOP. No round 1e commit was made, and the receipt is unchanged.
Attribution shows a dev-side cause, not this lane:
- The original parent base, with the original donor, writes byte-identical capture logs to the candidate's in both 8x8 arms.
- The receipt's own measured tree reproduces all 16 receipt rows of both arms.

Parent head `034e2e30f225f3fcd755cac8ad01c60dda5b366a` and donor head
`7dda9c3b4d65cbbb28f72a34e1ee0efe368695d9` were verified and are unchanged.
No second TAKEN comment was posted.

### Campaign recipe

The measured tree is the parent head after the round 1b `run.py` commit: `034e2e30`, tree
`a5d1a1b02212c04de89292893fcf022b39620848`, donor `7dda9c3b`, protocol processor `2ad2f845`, axis `48ff7a7e`.
Four clean checkouts of that tree ran the nine runs, four at a time, each from its checkout root.
The composer checks that each arm's executed command equals that arm's `command` field in the receipt, byte for byte.
That field also records the recipe's network-namespace launcher and the product interpreter's `-B` flag.
As plain shell, with `$SCRATCH` the external build directory, the 8x8 traffic-ON arm is:

```sh
python3 tb/verilator/nvm_capture_cpu/run.py --shape endstation_ax7101_8x8 --cpu-hz 50000000 --captures 16 --traffic on --build-dir "$SCRATCH/capture-8x8-50-on"
```

The other five arms change only `--shape`, `--cpu-hz`, `--traffic` and the build directory, as each
arm's `command` field records. The controls follow the capture README, with the same launcher and environment:

```sh
python3 tb/verilator/nvm_capture_cpu/run.py --shape endstation_ax7101_8x8 --captures 2 --mutation byte-only --build-dir "$SCRATCH/capture-byte-only" --baseline-measurement "$SCRATCH/capture-8x8-50-on/measurement.json"
python3 tb/verilator/nvm_capture_cpu/run.py --shape endstation_ax7101_1x1_tdm8 --captures 2 --mutation skip-copy --build-dir "$SCRATCH/capture-skip-copy"
python3 tb/verilator/nvm_capture_cpu/run.py --shape endstation_ax7101_1x1_tdm8 --captures 2 --mutation no-traffic --build-dir "$SCRATCH/capture-no-traffic"
```

The environment follows the receipt's `reproduction_environment`: `PYTHONHASHSEED=0`, `COURSIER_MODE=offline`,
`SBT_OPTS=-Dsbt.offline=true`, `PRODUCT_PYTHON` and `PYTHON` set to the product interpreter, and the
product environment first on `PATH`, with host utilities before the SDK. A scratch wrapper ahead of it
admits at most two simulator builds at once and runs Verilator 5.052 unchanged.
Every native executable embeds `5.052 2026-09-05`; none embeds 5.050.
The SoC component revisions, CPU generator revision, compiler, product firmware hash and BIOS patch hash
all equal the receipt's recorded values.

### Results

| Arm | Rows | Exit | Minimum ms | Maximum ms | Margin | Verdict-field changes | `requests` changes |
|---|---:|---:|---:|---:|---:|---|---|
| 1x1-50-on | 16 | 0 | 3.96022 | 3.96728 | 12.35103 | none | 9 |
| 1x1-50-off | 16 | 0 | 3.90676 | 3.91182 | 12.52614 | none | none |
| 8x8-50-on | 16 | 0 | 13.84836 -> 13.84682 | 13.86484 -> 13.86318 | 3.53412 -> 3.53454 | 7 | 5 |
| 8x8-50-off | 16 | 0 | 13.67682 -> 13.68947 | 13.69390 | 3.57824 | 1 | none |
| 8x8-100-on | 16 | 0 | 10.41821 | 10.42973 | 4.69811 | none | 10 |
| 8x8-100-off | 16 | 0 | 10.41356 | 10.41566 | 4.70445 | none | none |

Verdict-field changes, each against its committed receipt line:

| Arm | Capture | Field | Receipt line | Receipt | Candidate | Delta |
|---|---:|---|---|---:|---:|---:|
| 8x8-50-on | 0 | `sys_cycles` | `measurements.json:496` | 1385074 | 1385678 | +604 |
| 8x8-50-on | 0 | `responses` | `measurements.json:502` | 91 | 92 | +1 |
| 8x8-50-on | 0 | `reads` | `measurements.json:503` | 3549 | 3558 | +9 |
| 8x8-50-on | 1 | `sys_cycles` | `measurements.json:508` | 1386484 | 1384682 | -1802 |
| 8x8-50-on | 1 | `responses` | `measurements.json:514` | 92 | 91 | -1 |
| 8x8-50-on | 1 | `reads` | `measurements.json:515` | 3587 | 3575 | -12 |
| 8x8-50-on | 2 | `sys_cycles` | `measurements.json:520` | 1386318 | 1386046 | -272 |
| 8x8-50-off | 0 | `sys_cycles` | `measurements.json:711` | 1367682 | 1369030 | +1348 |

`requests` deltas in every traffic-ON row (receipt -> candidate, delta):

| Capture | 1x1-50-on | 8x8-50-on | 8x8-100-on |
|---:|---:|---:|---:|
| 0 | 24709 (+0) | 86480 -> 86518 (+38) | 130120 -> 130119 (-1) |
| 1 | 24678 (+0) | 86569 -> 86456 (-113) | 130113 (+0) |
| 2 | 24691 -> 24690 (-1) | 86559 -> 86541 (-18) | 130105 -> 130104 (-1) |
| 3 | 24664 (+0) | 86466 (+0) | 130119 -> 130118 (-1) |
| 4 | 24694 -> 24693 (-1) | 86479 (+0) | 130206 -> 130207 (+1) |
| 5 | 24709 (+0) | 86521 (+0) | 130119 -> 130118 (-1) |
| 6 | 24684 (+0) | 86518 (+0) | 130206 (+0) |
| 7 | 24697 -> 24698 (+1) | 86466 (+0) | 130119 (+0) |
| 8 | 24665 -> 24664 (-1) | 86483 (+0) | 130206 (+0) |
| 9 | 24665 -> 24664 (-1) | 86466 -> 86465 (-1) | 130118 -> 130119 (+1) |
| 10 | 24665 -> 24664 (-1) | 86481 (+0) | 130207 -> 130206 (-1) |
| 11 | 24690 -> 24691 (+1) | 86558 (+0) | 130249 (+0) |
| 12 | 24671 -> 24672 (+1) | 86472 -> 86471 (-1) | 130216 -> 130217 (+1) |
| 13 | 24664 (+0) | 86558 (+0) | 130187 (+0) |
| 14 | 24690 -> 24691 (+1) | 86472 (+0) | 130217 -> 130216 (-1) |
| 15 | 24664 (+0) | 86558 (+0) | 130187 -> 130188 (+1) |

The changed summary fields are at `measurements.json:487`, `:488` and `:491` (8x8 traffic ON minimum,
maximum and margin), `:702` (8x8 traffic OFF minimum), and `:1350` and `:1351` (the published 8x8 / 50 MHz
maximum and margin). The 8x8 / 50 MHz published maximum falls from 13.86484 ms to 13.86318 ms.
Its margin rises from 3.53412 to 3.53454. Every capture stays below the 24.5 ms bound.
The 1x1 and 8x8 / 100 MHz maxima are unchanged. Captures 3 to 15 of both 8x8 / 50 MHz arms keep every verdict field.
Every traffic-ON `requests` value stays positive and every traffic-OFF counter stays zero.

### Attribution

Both 8x8 / 50 MHz arms ran at two more trees, with the same recipe and simulator:
- the original parent base `5603c353`, with original donor `5dce647a`, protocol processor `2ad2f845` and tree `472a2a9a`;
- the receipt's measured tree `a2f17342`, with donor `5dce647a`, protocol processor `b2db3a97` and tree `c28595df`, as a positive control.

"same" means equal to the committed receipt row.

8x8 / 50 MHz / traffic OFF, `sys_cycles`:

| Capture | Receipt | Receipt tree a2f17342 | Base 5603c353 | Candidate 034e2e30 |
|---:|---:|---:|---:|---:|
| 0 | 1367682 | same | 1369030 | 1369030 |
| 1 | 1368947 | same | same | same |
| 2 | 1369390 | same | same | same |
| 3 | 1369390 | same | same | same |
| 4 | 1369390 | same | same | same |
| 5 | 1369390 | same | same | same |
| 6 | 1369390 | same | same | same |
| 7 | 1369390 | same | same | same |
| 8 | 1369390 | same | same | same |
| 9 | 1369030 | same | same | same |
| 10 | 1369030 | same | same | same |
| 11 | 1369390 | same | same | same |
| 12 | 1369390 | same | same | same |
| 13 | 1369390 | same | same | same |
| 14 | 1369390 | same | same | same |
| 15 | 1369390 | same | same | same |

8x8 / 50 MHz / traffic ON, `sys_cycles`/`requests`/`responses`/`reads`:

| Capture | Receipt | Receipt tree a2f17342 | Base 5603c353 | Candidate 034e2e30 |
|---:|---:|---:|---:|---:|
| 0 | 1385074/86480/91/3549 | same | 1385678/86518/92/3558 | 1385678/86518/92/3558 |
| 1 | 1386484/86569/92/3587 | same | 1384682/86456/91/3575 | 1384682/86456/91/3575 |
| 2 | 1386318/86559/91/3549 | same | 1386046/86541/91/3549 | 1386046/86541/91/3549 |
| 3 | 1384836/86466/91/3559 | same | same | same |
| 4 | 1385052/86479/91/3549 | same | same | same |
| 5 | 1385722/86521/91/3569 | same | same | same |
| 6 | 1385678/86518/92/3558 | same | same | same |
| 7 | 1384836/86466/91/3559 | same | same | same |
| 8 | 1385110/86483/92/3558 | same | same | same |
| 9 | 1384836/86466/91/3559 | same | 1384836/86465/91/3559 | 1384836/86465/91/3559 |
| 10 | 1385074/86481/91/3549 | same | same | same |
| 11 | 1386318/86558/91/3549 | same | same | same |
| 12 | 1384932/86472/91/3549 | same | 1384932/86471/91/3549 | 1384932/86471/91/3549 |
| 13 | 1386318/86558/91/3549 | same | same | same |
| 14 | 1384932/86472/91/3549 | same | same | same |
| 15 | 1386318/86558/91/3549 | same | same | same |

- The receipt tree reproduces every row and every summary field of both arms. The receipt is a faithful record of that tree.
- The original base writes byte-identical capture logs to the candidate's: SHA-256 `6399c81c…` (OFF) and `1e637b00…` (ON).
  The donor correction, with its different gPTP ROM, therefore has no effect on either arm.
- The firmware side is identical in all three trees. The AEM image is 19520 bytes, CRC `0x2104c2d3`.
  The BIOS and every memory initialization file match, and the generated `soc.h` differs only in its timestamp.
  The 8x8 configuration did change on dev (`6178aa1bd`, a descriptor-model lint waiver), which moves
  `config_sha256`. It does not change the flash image.
- Hence the drift is the capture-SoC RTL that changed on dev between `a2f17342` and the base.
  Round 1d listed those 30 files: 7 parent RTL files and 23 protocol-processor files.
  It shifts the first three 8x8 / 50 MHz captures, then the rows realign with the receipt.
  No single commit was isolated.
- The 1x1 traffic-ON capture log is byte-identical to the round 1d base and candidate runs
  (`01f72663…`). The harness is deterministic across sessions.

### What the refresh would record

The composer takes rows and summaries verbatim from each arm's `measurement.json`. It recomputes hashes and
provenance from the measured tree and the builds, checks every verdict field, and lists every changed field.
It refused to write a receipt because 14 verdict fields changed. Its complete field-level diff
(`round1e-receipt-diff.json`, `round1e-compose.log`) has 56 changes: 18 provenance fields, 24 `requests` values and 14 verdict fields.

| Field | Change | Basis |
|---|---|---|
| `date`, `base`, `tree`, `provenance` | `2026-10-02`, `a2f17342`, `c28595df` → `2026-10-09`, `034e2e30`, `a5d1a1b0`, new text | Listed in the ruling |
| `processor_pins` | protocol `b2db3a97` → `2ad2f845`; gPTP `5dce647a` → `7dda9c3b`; axis unchanged | Listed in the ruling |
| Six arms' `gptp_ucode_sha256` | `78c8418a…` → `fd3dad06…` | Listed in the ruling |
| `harness_sha256.run.py` | `1bddc676…` → `c230cb3e…` | Ruling 6087498843 |
| `simulator` | unchanged, Verilator 5.052 | Listed in the ruling |
| 24 traffic-ON `requests` values | table above | Ruling 6088189432 |
| Four 8x8 arms' `config_sha256` | `a3f90aab…` → `ca491ba5…` | Provenance; dev `6178aa1bd`, not listed in the ruling |
| `remeasurement_assignment` | the #629 assignment → ruling 6088189432 | Provenance; not listed in the ruling |
| 14 verdict fields | table above | STOP |

Unchanged: every `cpu_netlist_sha256`, `instrumented_firmware_sha256`, `bios_sha256` and `command`, plus `measured_for`,
`product_firmware_sha256`, the 1x1 and 8x8 / 100 MHz maxima and every other top-level field.

A refresh with these values also leaves the design page stale. `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1625`
to `:1628` name the measured commit, tree and protocol pin. Lines `:1641` to `:1643` quote 13.86484 ms, 3.5341x and
10.63516 ms. The table at `:1660` and `:1661` quotes the 8x8 / 50 MHz minima and maxima. Editing that page is outside this lane's scope.

### Controls

| Control | Captures | Result |
|---|---:|---|
| `skip-copy` | 2 | Exit 0; every raw byte poisoned, caught by the destination-byte oracle |
| `no-traffic` | 2 | Exit 0; every traffic counter zero while copying continues |
| `byte-only` | 2 | Exit 0; 25.42688 and 25.43094 ms, slowdown 1.834 against this campaign's 8x8 traffic-ON maximum |

The byte-only rows equal the round 1a rows. Under the round 1b grading, the production bound no longer
applies to the control; its 1.5x ratio does.
The composer refuses the 14 verdict changes found here. No separate planted defect was needed to show
that refusal. The row comparison is a second, independent script, and it reports the same changes.

### Gates

| Gate or operation | Result | Evidence |
|---|---|---|
| Expected origin and both resumed heads | Pass; exact revisions, clean worktrees | round1e-inputs.json |
| Campaign, six arms, 16 captures each | Exit 0 each; harness grading passes | ROUND1E-ARTIFACTS.tsv |
| Controls skip-copy, no-traffic, byte-only | Exit 0 each; named faults caught, 1.834x | ROUND1E-ARTIFACTS.tsv |
| Composer verdict invariant | Exit 1; 14 verdict fields changed; no receipt written | round1e-compose.log; round1e-receipt-diff.json |
| Row comparison against the receipt | 8 row and 6 summary verdict changes, all in 8x8 / 50 MHz | round1e-compare.json |
| Attribution, base 8x8 / 50 MHz ON and OFF | Exit 0 each; logs byte-identical to the candidate's | round1e-compare.json |
| Positive control, receipt tree, 8x8 / 50 MHz ON and OFF | Exit 0 each; all 16 rows and summaries equal the receipt | round1e-compare.json |
| Receipt commit | Not made; STOP | Receipt SHA-256 unchanged |
| 61-suite sweep | Not started; STOP | Prepared only |
| Resource export and vendor stages | Not started; no vendor lock taken | Prepared only |

Peak service memory reached 10.10 GiB once, while four builds overlapped at about 22:55. Anonymous memory
was about 5.3 GiB; the rest was reclaimable page cache. From then on, a watcher reclaimed page cache above 8 GiB.
Later samples peaked at 6.75 GiB, with 5.24 GiB anonymous. Free data space stayed above 62 GiB.
`ROUND1E-ARTIFACTS.tsv` records 140 external logs, receipts, executables, ROMs, BIOS images and scripts by size and SHA-256.

### Receipt state and decision needed

```sh
git diff --numstat 034e2e30f225f3fcd755cac8ad01c60dda5b366a -- tb/verilator/nvm_capture_cpu/measurements.json
```

The output is empty. The receipt keeps SHA-256 `ed871bdd09bde7ebde1ae021cd647e3cad354d3f8682c5b7308cda91e4cbd72a`.
The input gate is unchanged. Both worktrees are clean, no validation job remains and nothing was pushed.

These decisions are needed:
- The 14 dev-caused verdict-field changes in the 8x8 / 50 MHz arms.
- The two provenance fields the ruling does not list.
- Whether this lane updates the stale design-page figures.

The nine completed runs are at these heads and this recipe. A ruling accepting their values lets the refresh
commit be composed from them without rerunning. The sweep and vendor stages follow, with scripts already prepared.
The later physical repeat still closes #621.

Posted: [round 1e STOP](https://github.com/kebag-logic/milan-fpga/issues/621#issuecomment-6089759400).

## Round 1f: final ruling, lane invariant and receipt refresh

[Final ruling 6089776382](https://github.com/kebag-logic/milan-fpga/issues/621#issuecomment-6089776382)
replaces the receipt invariants of 6087498843, 6087655217 and 6088189432.
Its lane invariant is that the candidate's capture logs equal the base's, byte for byte, in every arm and named control.
The refresh then records the candidate's values as measured.
Both resumed heads were verified before work started: parent `034e2e30` and donor `7dda9c3b`.
No second takeover comment was posted.

| Ruling item | Result | Evidence |
|---|---|---|
| 1. Lane invariant, every arm and control | Pass: nine of nine capture logs byte-identical | round1f-invariant.json; table below |
| 2. Refresh through the record path, separate commit | `e0ee38f9`; `scripts/check_nvm_capture.py` exits 0 | round1f-receipt-diff.json; gate table |
| 3. Bounds | Pass: 24.5 ms production bound, byte-only 1.834x, every margin above 2 | Bounds section |
| 4. Record the field diff and its attribution | 56 fields, listed below | Field diff section |
| 5. STOP conditions | Neither occurred | Items 1 and 3 |
| Full bar: sweep and vendor stages | 61 of 61 suites pass; every vendor stage passes | Gate table |

### Lane invariant

Candidate: parent `034e2e30` with donor `7dda9c3b`, the round 1e campaign runs.
Base: parent `5603c353` with donor `5dce647a` and protocol processor `2ad2f845`.
The two 8x8 / 50 MHz base runs are the round 1e attribution runs; the other seven ran in round 1f.
Every pair uses the same `run.py` arguments, launcher, interpreter, environment and Verilator 5.052.
Only the checkout and the external build directory differ.
The comparison script re-reads each checkout's head, donor and cleanliness.
It also confirms that both native executables embed 5.052.
Each pair's gPTP ROMs differ (`fd3dad06…` candidate, `78c8418a…` base), so the donor change is present in every candidate build.

| Arm or control | Rows | Candidate exit | Base exit | Capture log bytes | SHA-256 (both) | Base log source |
|---|---:|---:|---:|---:|---|---|
| 1x1-50-on | 16 | 0 | 0 | 4056 | `01f72663af25e764…` | round 1f |
| 1x1-50-off | 16 | 0 | 0 | 3775 | `5ade9a6e67b903d9…` | round 1f |
| 8x8-50-on | 16 | 0 | 0 | 4076 | `1e637b00877cba32…` | round 1e attribution |
| 8x8-50-off | 16 | 0 | 0 | 3913 | `6399c81cc09b798e…` | round 1e attribution |
| 8x8-100-on | 16 | 0 | 0 | 4125 | `63afb13860f998a6…` | round 1f |
| 8x8-100-off | 16 | 0 | 0 | 3913 | `ff4a2e45e2fe2fc7…` | round 1f |
| skip-copy | 2 | 0 | 0 | 2416 | `eb1ac8583dd179a4…` | round 1f |
| no-traffic | 2 | 0 | 0 | 1893 | `914d1c10dadb5138…` | round 1f |
| byte-only | 2 | 0 | 1 | 2366 | `19327660eae0953a…` | round 1f |

The base byte-only run exits 1 by design of the base grader.
At the base, `tb/verilator/nvm_capture_cpu/run.py:79` applies the 24.5 ms production bound to that control too.
This is the round 1a finding that the round 1b commit `034e2e30` corrects.
Its simulator output is byte-identical to the candidate's: rows of 2543094 and 2542688 cycles,
and `checks: 3 failures: 0`.

The comparison can detect a difference.
With one byte appended in memory to the candidate's 8x8 / 100 MHz ON log, it exits 1.
It does the same when one byte is appended to the byte-only log.

### Refresh

The record path is the round 1e composer, adjusted to this ruling (`round1f-compose.py`, size and SHA-256 in `ROUND1F-ARTIFACTS.tsv`).
It takes each arm's rows and summary verbatim from that arm's `run.py` `measurement.json` in the candidate campaign.
It recomputes the input hashes and provenance from the measured tree and the builds.
It also re-checks that each arm executed the receipt's recorded `command`, byte for byte.
It refuses to write unless the lane invariant passed and every bound holds.
It records every field as measured and lists every changed field, classified as verdict, `requests` or provenance.

| Item | Value |
|---|---|
| Commit | `e0ee38f9d94bba29289f24f8f80a8d9645643c11`, one file: `tb/verilator/nvm_capture_cpu/measurements.json`, 56 lines changed |
| Old receipt | 36,969 bytes, SHA-256 `ed871bdd09bde7ebde1ae021cd647e3cad354d3f8682c5b7308cda91e4cbd72a` |
| New receipt | 37,132 bytes, SHA-256 `3ac54ed94f1bdad2046eea253ab82d22f60d36ca7a94aa065d0b4e63a1f9dc5b` |
| Measured tree | `034e2e30`, tree `a5d1a1b02212c04de89292893fcf022b39620848` |
| Pins | gPTP `7dda9c3b`, protocol processor `2ad2f845`, axis `48ff7a7e` |
| Simulator | Verilator 5.052, unchanged field |
| `remeasurement_assignment` | ruling 6089776382 |
| `date` | 2026-10-09, the campaign date |

Unchanged fields: every `cpu_netlist_sha256`, `instrumented_firmware_sha256`, `bios_sha256` and `command`.
`measured_for`, `product_firmware_sha256`, `bios_dispatch_patch_sha256`, `soc_component_revisions`,
`cpu_generator_revision`, `compiler`, `assignment` and `reproduction_environment` are unchanged too.
So are the 1x1 and 8x8 / 100 MHz maxima.

### Bounds

| Bound | Limit | Measured | Result |
|---|---|---|---|
| Production capture, every row of all six arms | at most 24.5 ms (half the 49 ms floor), regraded by `run.grade_rows` | worst 13.86318 ms (8x8 / 50 MHz ON, captures 11, 13 and 15) | Pass |
| Published maxima, margin to the 49 ms hold floor | at least 2 | 12.3510 (1x1), 3.5345 (8x8 / 50), 4.6981 (8x8 / 100) | Pass |
| Byte-only control against the candidate 8x8 / 50 MHz ON maximum | at least 1.5x | 25.42688 / 13.86318 = 1.834x | Pass |
| Input gate's OFF time limit | half floor passes, one tick over fails | both detected | Pass |

### Field diff against the old receipt

Line numbers are the same in the old and new receipt: the refresh changes 56 values in place.
Each `Receipt line` is cross-checked against the committed text at `034e2e30`: the line carries that field and its old value.

| # | Receipt line | Field | Old | New | Class |
|---:|---:|---|---|---|---|
| 1 | 2 | `/date` | `"2026-10-02"` | `"2026-10-09"` | provenance |
| 2 | 3 | `/base` | `a2f17342…` | `034e2e30…` | provenance |
| 3 | 46 | `/harness_sha256/run.py` | `1bddc676…` | `c230cb3e…` | provenance |
| 4 | 95 | `/measurements/0/rows/2/requests` | `24691` | `24690` | requests |
| 5 | 119 | `/measurements/0/rows/4/requests` | `24694` | `24693` | requests |
| 6 | 155 | `/measurements/0/rows/7/requests` | `24697` | `24698` | requests |
| 7 | 167 | `/measurements/0/rows/8/requests` | `24665` | `24664` | requests |
| 8 | 179 | `/measurements/0/rows/9/requests` | `24665` | `24664` | requests |
| 9 | 191 | `/measurements/0/rows/10/requests` | `24665` | `24664` | requests |
| 10 | 203 | `/measurements/0/rows/11/requests` | `24690` | `24691` | requests |
| 11 | 215 | `/measurements/0/rows/12/requests` | `24671` | `24672` | requests |
| 12 | 239 | `/measurements/0/rows/14/requests` | `24690` | `24691` | requests |
| 13 | 261 | `/measurements/0/gptp_ucode_sha256` | `78c8418a…` | `fd3dad06…` | provenance |
| 14 | 476 | `/measurements/1/gptp_ucode_sha256` | `78c8418a…` | `fd3dad06…` | provenance |
| 15 | 487 | `/measurements/2/minimum_ms` | `13.848360000000001` | `13.84682` | verdict |
| 16 | 488 | `/measurements/2/maximum_ms` | `13.86484` | `13.86318` | verdict |
| 17 | 491 | `/measurements/2/margin` | `3.5341193984207537` | `3.534542579696722` | verdict |
| 18 | 496 | `/measurements/2/rows/0/sys_cycles` | `1385074` | `1385678` | verdict |
| 19 | 501 | `/measurements/2/rows/0/requests` | `86480` | `86518` | requests |
| 20 | 502 | `/measurements/2/rows/0/responses` | `91` | `92` | verdict |
| 21 | 503 | `/measurements/2/rows/0/reads` | `3549` | `3558` | verdict |
| 22 | 508 | `/measurements/2/rows/1/sys_cycles` | `1386484` | `1384682` | verdict |
| 23 | 513 | `/measurements/2/rows/1/requests` | `86569` | `86456` | requests |
| 24 | 514 | `/measurements/2/rows/1/responses` | `92` | `91` | verdict |
| 25 | 515 | `/measurements/2/rows/1/reads` | `3587` | `3575` | verdict |
| 26 | 520 | `/measurements/2/rows/2/sys_cycles` | `1386318` | `1386046` | verdict |
| 27 | 525 | `/measurements/2/rows/2/requests` | `86559` | `86541` | requests |
| 28 | 609 | `/measurements/2/rows/9/requests` | `86466` | `86465` | requests |
| 29 | 645 | `/measurements/2/rows/12/requests` | `86472` | `86471` | requests |
| 30 | 691 | `/measurements/2/gptp_ucode_sha256` | `78c8418a…` | `fd3dad06…` | provenance |
| 31 | 692 | `/measurements/2/config_sha256` | `a3f90aab…` | `ca491ba5…` | provenance |
| 32 | 702 | `/measurements/3/minimum_ms` | `13.67682` | `13.68947` | verdict |
| 33 | 711 | `/measurements/3/rows/0/sys_cycles` | `1367682` | `1369030` | verdict |
| 34 | 906 | `/measurements/3/gptp_ucode_sha256` | `78c8418a…` | `fd3dad06…` | provenance |
| 35 | 907 | `/measurements/3/config_sha256` | `a3f90aab…` | `ca491ba5…` | provenance |
| 36 | 931 | `/measurements/4/rows/0/requests` | `130120` | `130119` | requests |
| 37 | 955 | `/measurements/4/rows/2/requests` | `130105` | `130104` | requests |
| 38 | 967 | `/measurements/4/rows/3/requests` | `130119` | `130118` | requests |
| 39 | 979 | `/measurements/4/rows/4/requests` | `130206` | `130207` | requests |
| 40 | 991 | `/measurements/4/rows/5/requests` | `130119` | `130118` | requests |
| 41 | 1039 | `/measurements/4/rows/9/requests` | `130118` | `130119` | requests |
| 42 | 1051 | `/measurements/4/rows/10/requests` | `130207` | `130206` | requests |
| 43 | 1075 | `/measurements/4/rows/12/requests` | `130216` | `130217` | requests |
| 44 | 1099 | `/measurements/4/rows/14/requests` | `130217` | `130216` | requests |
| 45 | 1111 | `/measurements/4/rows/15/requests` | `130187` | `130188` | requests |
| 46 | 1121 | `/measurements/4/gptp_ucode_sha256` | `78c8418a…` | `fd3dad06…` | provenance |
| 47 | 1122 | `/measurements/4/config_sha256` | `a3f90aab…` | `ca491ba5…` | provenance |
| 48 | 1336 | `/measurements/5/gptp_ucode_sha256` | `78c8418a…` | `fd3dad06…` | provenance |
| 49 | 1337 | `/measurements/5/config_sha256` | `a3f90aab…` | `ca491ba5…` | provenance |
| 50 | 1350 | `/maxima/1/maximum_ms` | `13.86484` | `13.86318` | verdict |
| 51 | 1351 | `/maxima/1/margin` | `3.5341193984207537` | `3.534542579696722` | verdict |
| 52 | 1360 | `/remeasurement_assignment` | (text) | (text) | provenance |
| 53 | 1362 | `/processor_pins/protocol-processor` | `b2db3a97…` | `2ad2f845…` | provenance |
| 54 | 1363 | `/processor_pins/gptp-processor` | `5dce647a…` | `7dda9c3b…` | provenance |
| 55 | 1366 | `/tree` | `c28595df…` | `a5d1a1b0…` | provenance |
| 56 | 1377 | `/provenance` | (text) | (text) | provenance |

Attribution, by class:
- **Measured values: 14 verdict fields and 24 `requests` values.** These come from dev's capture-SoC RTL drift between `a2f17342` and `5603c353`.
  - The base writes byte-identical capture logs to the candidate's, so this lane causes none of them.
  - The receipt's measured tree `a2f17342` reproduces the old values in each arm rerun there:
    1x1 / 50 MHz ON (round 1d), and 8x8 / 50 MHz ON and OFF (round 1e).
  - Round 1d lists the 30 capture-SoC source files that changed between those trees:
    7 parent RTL files and 23 protocol-processor files.
  - The firmware side is identical: product firmware, BIOS, AEM image and memory initialization.
- **Provenance from this lane.**
  - `harness_sha256/run.py` comes from the round 1b commit `034e2e30`.
  - The six `gptp_ucode_sha256` values and `processor_pins/gptp-processor` come from the donor change `7dda9c3b`.
  - `date`, `base`, `tree`, `provenance` and `remeasurement_assignment` describe this remeasurement.
- **Provenance from dev.**
  - `processor_pins/protocol-processor` moved from `b2db3a97` to `2ad2f845` on dev.
  - The four 8x8 `config_sha256` values come from `6178aa1bd`, a model lint waiver, which does not change the flash image.

**The old receipt was already stale at the base.** At `5603c353` with its own pins, the capture logs are the candidate's in every arm and control.
The base would therefore have measured these same values, not the old receipt's.
Its protocol-processor pin and its 8x8 configuration hash also already differed from the receipt.
`scripts/check_nvm_capture.py` passed there anyway.
It hashes the harness and product firmware, but not the capture-SoC RTL, configuration or pins.

The design page still quotes the old figures.
`docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1619` and `:1622` name the old measurement date and assignment.
`:1625`, `:1626` and `:1628` name the old measured commit, tree and protocol pin.
`:1641` to `:1643` quote 13.86484 ms, 3.5341x and 10.63516 ms.
`:1660` and `:1661` quote the old 8x8 / 50 MHz ranges and ratios.
`:1808`, `:1810` and `:1811` repeat 13.86484 ms, 3.5341x and 10.63516 ms.
The ruling does not authorize edits outside the gPTP plane, so this lane leaves the page unchanged.
No gate reads those figures. A follow-up should update the page to the new receipt.
`sw/firmware/ctrl_nvm/README.md:329`'s rounded 13.86 ms is still correct.

### Round 1f tests and planted defects

| Check | Planted defect | Result |
|---|---|---|
| Lane invariant (`round1f-invariant.py`) | One byte appended to the candidate 8x8 / 100 MHz ON log | Exit 1, `capture_log_identical=False` |
| Lane invariant | One byte appended to the candidate byte-only log | Exit 1 |
| Composer bound | One 8x8 / 50 MHz ON row set to 2450001 cycles (24.50001 ms) | Refused: exceeds half the 49 ms floor; nothing written |
| Composer bound | Published 8x8 / 50 MHz margin set to 1.99 | Refused; nothing written |
| Composer bound | Byte-only minimum set just under 1.5x the baseline | Refused by `run.grade_byte_only`; nothing written |
| Composer counters | A non-zero `requests` in a traffic-OFF row | Refused; nothing written |
| Composer precondition | Lane invariant result absent | Refused; nothing written |
| `scripts/check_nvm_capture.py --mutation bytes`, `records`, `clock`, `ignore-off-timing` | The gate's own named mutations | Each exits 1 at the final head |
| `run.byte_only_controls()` | Production bound applied to byte-only, or removed from production | Pass at the final head; both planted predicates were rejected in round 1b |

### Gates at the final head

Parent head `e0ee38f9d94bba29289f24f8f80a8d9645643c11`, donor `7dda9c3b4d65cbbb28f72a34e1ee0efe368695d9`.
The parent diff from the round 1b resume baseline `72848a76` is two files: `run.py` and `measurements.json`.

| Gate (plain shell, from the checkout root) | Exit | Result | Evidence |
|---|---:|---|---|
| `git diff --check 5603c353 HEAD` | 0 | Clean whitespace over the branch | round1f-static/diff-check.log |
| `python3 scripts/check_nvm_capture.py` | 0 | `PASS`; every control detected | round1f-static/nvm-capture.log |
| `python3 scripts/check_nvm_capture.py --mutation bytes` | 1 | Must fail: input change detected | round1f-static/nvm-capture-bytes.log |
| `python3 scripts/check_nvm_capture.py --mutation records` | 1 | Must fail: input change detected | round1f-static/nvm-capture-records.log |
| `python3 scripts/check_nvm_capture.py --mutation clock` | 1 | Must fail: input change detected | round1f-static/nvm-capture-clock.log |
| `python3 scripts/check_nvm_capture.py --mutation ignore-off-timing` | 1 | Must fail: OFF timing omitted | round1f-static/nvm-capture-ignore-off-timing.log |
| `python3 scripts/lint_rtl.py --check` | 0 | 90 violations within the ratchet of 90 | round1f-static/lint.log |
| `python3 scripts/docs_check.py` | 0 | 0 findings | round1f-static/docs-check.log |
| `python3 scripts/check_cpp_idiom.py` | 0 | Pass | round1f-static/cpp-idiom.log |
| `python3 scripts/check_py_idiom.py` | 0 | Pass | round1f-static/py-idiom.log |
| `python3 scripts/check_doc_style.py` | 0 | Pass | round1f-static/doc-style.log |
| `python3 scripts/check_gptp_docs.py --with-submodule` | 0 | Pass | round1f-static/gptp-docs.log |
| `python3 scripts/check_diagram_pngs.py` | 0 | Pass | round1f-static/diagram-pngs.log |
| `python3 scripts/gen_toc.py --check` | 0 | Pass | round1f-static/toc.log |
| `python3 scripts/check_em_dash.py --base 5603c353` | 0 | 0 findings over 71 added lines | round1f-static/em-dash.log |
| `PYTHONPATH=tb/verilator/nvm_capture_cpu python3 -B -c 'import run; run.byte_only_controls()'` | 0 | Pass | round1f-static/byte-only-controls.log |
| `git status --porcelain` | 0 | Empty after the static gates | round1f-static/clean-after.log |
| `syn/yosys/run.sh --results "$RESULTS/yosys"` | 0 | 58 of 58 tops, tap purity pass | round1f-yosys.log |
| `scripts/run_all_suites.sh "$RESULTS/suites"`, first attempt | 2 | Preflight cancellation self-test: a descendant outlived the 4 s reap deadline at load average 30 on 16 cores; no suite ran | round1f-sweep.attempt1.log |
| `scripts/run_all_suites.sh "$RESULTS/suites"`, rerun unchanged | 0 | 61 of 61 suites, 2,186,819 checks, 0 failures, 0 timeouts | round1f-sweep.log; suite-logs-r1f |
| `python3 scripts/xvlog_gate.py --check` | 0 | 0 findings, equal to the ratchet: 0 in hdl/, 0 in the pinned processors; image receipts recheck exit 0 | resources-r1f/xvlog-command.log |
| Shipping 1x1 route, default placement directive | 0 | 101,396 of 101,396 nets routed, 0 routing errors; WNS +0.299 ns, TNS 0, WHS +0.031 ns; all constraints met; image receipts recheck exit 0 | resources-r1f/route-1x1-command.log |
| 8x8 RTL elaboration | 0 | Recipe standalone parameters; 0 Synth 8-4445; image receipts recheck exit 0 | resources-r1f/elaborate-8x8-command.log |
| `python3 syn/ooc/pp_baseline.py` 1x1 standalone preparation | 0 | Integrated clock; image receipts recheck exit 0 | resources-r1f/prepare-ooc-1x1-command.log |
| `python3 syn/ooc/pp_baseline.py` 8x8 standalone preparation | 0 | Integrated clock; image receipts recheck exit 0 | resources-r1f/prepare-ooc-8x8-command.log |
| Standalone 1x1 synthesis | 0 | Integrated clock; 0 Synth 8-4445; image receipts recheck exit 0 | resources-r1f/ooc-1x1-command.log |
| Standalone 8x8 synthesis | 0 | Integrated clock; 0 Synth 8-4445; image receipts recheck exit 0 | resources-r1f/ooc-8x8-command.log |
| `python3 syn/ooc/pp_resource_gate.py check "$WORK/ax7101/gateware" --endpoint route-1x1` | 0 | PASS; LUT 50267, FF 54413, SLICE 15779, RAMB36 74, RAMB18 27, DSP 14, WNS and WHS all equal to the baseline; image receipts recheck exit 0 | resources-r1f/check-route-1x1-command.log |
| `python3 syn/ooc/pp_resource_gate.py check "$WORK/ax7101-ooc" --endpoint ooc-1x1` | 0 | PASS; LUT 23179, FF 19779, RAMB36 16, RAMB18 3, DSP 8, all equal to the baseline; image receipts recheck exit 0 | resources-r1f/check-ooc-1x1-command.log |
| `python3 syn/ooc/pp_resource_gate.py check "$WORK/ax8x8-ooc" --endpoint ooc-8x8` | 0 | PASS; LUT 30135, FF 27380, RAMB36 21, RAMB18 5, DSP 8, all equal to the baseline; image receipts recheck exit 0 | resources-r1f/check-ooc-8x8-command.log |
| Shipping 1x1 route, AltSpreadLogic_high | 0 | Same synthesis checkpoint; 101,431 of 101,431 nets routed, 0 errors; WNS +0.100 ns, WHS +0.035 ns; met; image receipts recheck exit 0 | resources-r1f/route-AltSpreadLogic_high-command.log |
| Shipping 1x1 route, ExtraTimingOpt | 0 | Same synthesis checkpoint; 101,466 of 101,466 nets routed, 0 errors; WNS +0.201 ns, WHS +0.034 ns; met; image receipts recheck exit 0 | resources-r1f/route-ExtraTimingOpt-command.log |
| `python3 syn/ooc/pp_resource_gate.py check-baseline` | 0 | `baseline PASS: 3 endpoints` | resources-r1f/check-baseline.log |
| Vendor stage driver (all of the above, then cleanup and clean-tree check) | 0 | Symlinks removed; `git diff --check` and `git status --porcelain` clean | round1f-vendor.log |

The four `--mutation` rows must exit 1, and do; each logs the expected `FAIL:` reason.
Within the sweep, `gptp_plane` re-ran `phc_step` at this head: 49 checks, 0 failures, and its campaign passed 4 of 4 with the three planted microcode defects rejected.
`milan_dp` re-ran `gmstep`: 190 checks, 0 failures.
The separate 20-control `gmstep-mutants` target, the physical-clock campaign and the extended arm ran at `72848a76`.
No input to them has changed since.
The sweep ran in a separate clean checkout of the final head and took 2 h 54 min.
Its first attempt stopped in the preflight cancellation self-test before any suite ran.
`scripts/owned_process.py` allows 4 s to reap descendants, and the host load average was then 30 on 16 cores.
The unchanged rerun passed the same self-test and every suite.
The `tsn_fuzz` field campaign rewrites the timestamp line of two in-tree `TEST_RESULTS.md` files in that checkout, as designed:
`hdl/ieee1722/avtp/doc/TEST_RESULTS.md` and `hdl/ieee8021as/gptp_plane/doc/TEST_RESULTS.md`.
Their pass counts are unchanged at 164 and 677. The lane worktree was not touched.
Yosys ran in its own clean checkout of the final head, which stayed clean.
Service memory exceeded the 9 GB guideline once, during the 1x1 integrated synthesis between 05:07 and 05:10.
The cgroup's peak counter records 10.03 GiB (10.77 GB), and the watcher sampled 9.30 and 9.34 GB before reclaiming page cache.
Anonymous memory was 7.47 GiB at the last minute sample before the first reclaim; its share at the peak itself was not sampled.
It stayed under the 12 GiB cap. The watcher was then tightened to reclaim above 7 GiB every 3 s,
and the remaining Vivado stages peaked at 7.27 GiB, with 6.49 GiB anonymous.
Before that, four concurrent base-capture builds reached 8.28 GiB once, at 23:52, with 5.26 GiB anonymous.
Free data space never fell below 59 GB.
The vendor stages held the exclusive lock one Vivado run at a time and waited behind other lanes' runs.
None of this lane's Verilator jobs ran while they did.
The output-directory copies of `round1f-compose.log` and `round1f-invariant.json` have host path prefixes replaced by placeholders.
`ROUND1F-ARTIFACTS.tsv` records the size and SHA-256 of the scratch originals.

### Reproduction

From a clean checkout of each tree, in the capture recipe's environment, with Verilator 5.052 first on `PATH`.
The environment uses the product interpreter, offline dependencies, `PYTHONHASHSEED=0` and networking disabled.
Each arm runs its receipt `command`; for example:

```sh
python3 tb/verilator/nvm_capture_cpu/run.py --shape endstation_ax7101_8x8 --cpu-hz 100000000 --captures 16 --traffic on --build-dir "$SCRATCH/capture-8x8-100-on"
python3 tb/verilator/nvm_capture_cpu/run.py --shape endstation_ax7101_8x8 --captures 2 --mutation byte-only --build-dir "$SCRATCH/capture-byte-only" --baseline-measurement "$SCRATCH/capture-8x8-50-on/measurement.json"
cmp "$CANDIDATE/capture-8x8-100-on/capture.log" "$BASE/capture-8x8-100-on/capture.log"
python3 scripts/check_nvm_capture.py
```

Expected: every `cmp` is silent with exit 0. Every candidate run exits 0; the base byte-only run exits 1 as explained above.
The input gate prints `PASS`.

Posted: [round 1f REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/621#issuecomment-6094760924).
