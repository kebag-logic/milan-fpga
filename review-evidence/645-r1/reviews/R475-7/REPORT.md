[R475] NEGATIVE - exact head 8e4b1e53e9b5a8ef5f9854095347436ab84259b6

External independent review R475-7 of issue #645 / PR #672, including the assigned #647 work. Tree `b80da0aa70f44ff35a872ffe003cb49c96cac709`; source comparison base and observed live dev `6aa25dec977c6ad78bf4ff6275de47fb81d0c246`. The focused delta is the single commit `1e79ebdc06528edff74c0a7f530f20f99e3326a2..8e4b1e53e9b5a8ef5f9854095347436ab84259b6`.

All five lenses were applied. The scheduling change passes both cold invocation forms and the 708-second replica bar. The original false-slip defect is resolved. One new MINOR concerns decimal time boundaries; the prior timing-record MINOR remains open only for missing public receipt verification. Conformance and RTL are CLEAN; Robustness, Tests and Docs are UNCLEAN. Pending hosted work is not the reason for this verdict.

The review reconstructed the repository contract and documentation map, issue acceptance and manager rulings, linked requirements/interfaces, base-to-head comparison/history and focused delta, then public executable evidence. The independent verdict and ledger were written before reading prior public review findings. No private author material, other checkout, source fix, repository write on GitHub, or delegation was used.

**Scope and authority.** The issue body requires an established cause, removal or bounded declaration of the discontinuity, and a bench repeat. Public rulings retain the bench repeat for the manager. The operative design is eight consecutive LOCKED windows under following, 2,048 qualifying ticks at INTERNAL, a 2^20-tick ceiling, and a depth-16 loopback ring targeting eleven events at PDU end. The action is symmetric and exact, spans at most two consecutive output PDUs, preserves ordering outside that span, and does not increment slip counters. Recovery requires a full quiet dwell; only a second pull starting during recovery has the declared residual. Authorities examined include `REQUIREMENTS.md:307`, `MEDIA_CLOCK_FOLLOWING.md:1060-1262`, `TIME_SYNC.md:384-386`, `REGISTER_MAP.md:1870`, `CI_WORKFLOWS.md:185-247`, and the [Round 2h ruling](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6075072415). This round changes diagnostic/scheduling behavior, not that product contract.

**R475-7-F1 - MINOR - Robustness, Tests, Docs - Decimal boundaries misplace, omit or admit measured events.**

Artifact: `tb/verilator/follow_ring/trace_table.py:67-78`, with the same bin arithmetic at line 90; the half-open contract at lines 25-29; `test_trace_table.py:65-77`.

Authority/evidence: the helper promises `[start, end)` bins and counter-based counts. The submitted five tests pass, but their boundary test uses exactly representable quarter-second intervals. `scripts/decimal_boundaries.py` uses an independent decimal-time oracle and the actual CLI. All nine cases fail, with the CLI itself returning zero:

| Event and requested interval | Required result | Observed result |
|---|---|---|
| Event 1.2 s; origin 1, from 0, to .4, step .1 | Event in the bin ending at +.30 | Event in the bin ending at +.20 |
| Event .3 s; origin .1, from .2, to .4, step .1 | Inclusive start: one event in the first bin | Event omitted; every count zero |
| Event .3 s; origin .1, from 0, to .2, step .1 | Exclusive end: no event, two bins | Event admitted and a spurious third bin emitted |

Each row reproduces independently for `dup`, `skip` and `recentre`. Binary floating-point subtraction/addition followed by `int`/`ceil` changes the requested boundaries. Receipts: `receipts/decimal-boundaries.log`, `.rc` (1), and `receipts/decimal-boundaries/`, including inputs, raw tables and expected/actual vectors. These are valid event logs, with completion markers, and need no malformed input.

Impact: the diagnostic can report zero slips in a window that includes a real counter event, count an event outside the requested window, or assign a declared action to the wrong interval. The RTL and simulation acceptance checks are unaffected. Generated measurements change, so this is not RESIDUE.

Required outcome: apply the documented time bounds consistently to event and PDU data, including decimal origins and steps. Add regressions for inclusive starts, exclusive ends and interior boundaries for all three event kinds. Preserve distinctions immediately on either side of a boundary; do not solve this with an unrestricted grace interval.

Verification: run `python3 scripts/decimal_boundaries.py <source> <packet>` from this packet: 9/9 must pass, along with the five standing CLI tests, the unchanged public recentre probe and genuine duplicate/skip controls.

**R474-5-F1 - MINOR - Tests, Docs - RETAINED in part: the new measurement figures cannot yet be matched to public raw receipts.**

Artifacts: `docs/testing/TESTING.md:315-327`, `tb/verilator/follow_ring/Makefile:22-32`, `tb/verilator/milan_dp_render/Makefile:46-57`, the PR body's Round 2h section, and `receipts/public-evidence-inventory.json`.

Authority/evidence: the original finding and Round 2h item 2 require each stated figure to match its measurement receipt. The code and measurement basis are corrected: serial outer make now overlaps the standing legs; the former hosted figures, source run/job, suite-specific ratios and margins are recorded. The older receipts substantiate 1422.5/1093.9 hosted seconds and 800.207507093/826.708349028 replica seconds. Arithmetic for the new figures is correct:

| Suite | New stated local seconds | Ratio | Projected seconds | Margin to 1440 / 1800 s |
|---|---:|---:|---:|---:|
| follow_ring | 437.204 | 1.78 | 778.2 | 661.8 / 1021.8 |
| milan_dp_render | 793.308 | 1.324 | 1050.3 | 389.7 / 749.7 |

However, the supplied public evidence commit `1747b39f600de8e8c4b22437817984aa9430a33e` and the live `645-review-evidence` tip `42e3d07b26bca054e18ec8f9d8e03ba8d114b9d6` contain author packets only through Round 2g. The live tip is “Archive R474-5 review of issue 645”; its complete recursive inventory has no Round 2h paths. The [public author summary](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6075441876) and PR body describe `round2h/jobs/`, `receipts.json` and `measured-source-binding.json`, but those receipts are absent from the supplied and discovered public packet. I could not match 437.204, 793.308 or the claimed measured-source binding to raw receipts. My independent 471.845-second follow-ring run proves the replica bar, not the provenance of those two recorded measurements. No false or fabricated measurement is alleged.

Impact: the original finding's explicit receipt-verification condition remains unmet for the new authoritative figures. This is an evidence gap concerning measurements, not a wording defect or the pending hosted run.

Required outcome: publish and link the Round 2h command, affinity/environment, elapsed-time, return-code and source-binding receipts for both measured defaults, with their manifest. Existing measurements can close this without a source change if the receipts match.

Verification: resolve the public links, verify hashes and measured-source identity, and reconcile each documented figure and margin with its receipt. The corrected scheduling behavior and successful independent replica need not be repeated merely to publish the missing evidence.

**Focused execution.** All builds and disposable probes stayed under this packet's `scratch/`. Independent jobs overlapped on disjoint CPU sets; no shell job was detached. The scoped simulator identified itself as version 5.050, revision v5.050; its launcher SHA-256 is recorded in both cold-run receipts. Unit memory peaked at 4,306,477,056 bytes, below the 12 GB cap.

| Check | Result and receipt |
|---|---|
| Cold serial outer make, CPUs 96-99, MAKEFLAGS unset | rc 0, **471.844760 s**, 236.155240 s below 708; `receipts/cold-serial.*` |
| Cold outer make -j16, CPUs 100-103, MAKEFLAGS unset | rc 0, **455.381122 s**; `receipts/cold-parallel.*` |
| Both defaults' preserved checks | Each: b8 48/0, pullin 18/0, fine pulls 10/10, controller PASS at 6.25/25/50/100 MHz; exactly one ordinary shared build |
| Instrumented make graph, both outer forms | 12 cases: one shared build, bounded dispatch, nonzero status from each failed leg and shared build; `receipts/schedule/` |
| Explicit `make -j16 ... mutants SWEEP_JOBS=4` | rc 0, **12/12 caught**, 407.204261 s; `receipts/mutants.*` and `receipts/mutant-details/` |
| Standing diagnostic tests | 5/5 PASS; `receipts/standing-trace-tests.*` |
| Independent real declared action | Normal pull-in 18/0; action 5.454116560 s prints slips 0, skips 0, recentres 1; `receipts/traces/declared.*` |
| Independent genuine duplicate | Peer stimulus -100 ppm; event 0.657956240 s prints slips 1, skips 0, recentres 0; `receipts/traces/duplicate.*` |
| Independent genuine skip | Peer stimulus +100 ppm; event 2.739738000 s prints slips 1, skips 1, recentres 0; `receipts/traces/skip.*` |
| Unchanged R474-5 margin-step probe | Head counts 0,0,0,0 and marks event evidence unavailable; parent counts 0,0,1,0; `receipts/legacy-probe-*` |
| Independent decimal boundary checks | **0/9**, raw check rc 1; R475-7-F1 |
| Evidence scheduling contract | `--check` PASS and `--selftest` 105/105; `receipts/evidence-*` |
| Documentation and traceability | docs check, style, module matrix, pinned TOC check and anchors all rc 0 |

The real duplicate/skip probes intentionally stop acquisition after 0.1 seconds and return raw rc 1 for unmet settle checks. Those statuses are preserved; these are counter-observability controls, not passing acceptance runs. The normal declared-action run returns zero. Large PDU traces remain in scratch; bounded CSV windows, event logs and whole-trace hashes are published.

The serial replica is 34.641 seconds, or 7.9%, slower than the author's stated 437.204 seconds. At the assigned 1.78 ratio, this review's result projects to 839.9 seconds, leaving 420.1 seconds to 1260, 600.1 to 1440 and 960.1 to 1800. These are projections on a shared host, not hosted measurements.

`Makefile:82` explicitly limits the recursive pool to four leg jobs even under outer `-j16`. Both ordinary targets depend on one `build`; their commands have no trace output filenames. Fine pulls use `obj_dir_fine/results`, and controller builds use `obj_dir_control/<rate>`. Each inner case has a distinct file stem. The default leg commands/checks are unchanged. The graph fault probes substitute disposable recipes only; the separate cold runs execute the real recipes and checks.

**Prior public findings at this head.** Original severities are preserved.

| Finding | Disposition | Exact-head evidence |
|---|---|---|
| R474-5-F1, MINOR, Tests/Docs | **RETAINED in part** | Scheduling/basis corrected and replica passes; new raw measurement receipts remain unavailable, as detailed above |
| R475-6-F1, MINOR, Tests/Docs | **RESOLVED** | `sim_main.cpp:618-626` emits counter/pulse events; reader separates them; original public probe and independent physical counter controls pass. Decimal-boundary handling is new R475-7-F1, not a retained margin heuristic |
| R474-5-S1, SUGGESTION, Docs | **RESOLVED** | `measure_test_evidence_readers.py:98` now says explicit mutants target, outside the default sweep |
| R474-4-F1, MAJOR, Tests/Docs | **RESOLVED defect; current acceptance still pending** | Prior exact-head hosted aggregate at `1e79ebdc` passed both suites; this delta preserves all coverage and improves dispatch. The current head still owes the new <=1260-second hosted condition |
| R474-1-F1/F2, MAJOR; R475-1-F1, MAJOR | Remain **RESOLVED** | Symmetric action, qualified arm/recovery and ruled two-PDU contract remain unchanged; fresh defaults and SINGLE-DROP/NO-ARM/NO-RECOVERY controls pass |
| R474-1-F3, BLOCKER; R475-1-F3, MINOR | Remain **RESOLVED** | Compiled-source traceability and text-input disposition unchanged; module-matrix check passes |
| R474-1-F4 and R475-1-F2, MINOR | Remain **RESOLVED** | `MEDIA_CLOCK_FOLLOWING.md:1092` states the disengaged 2048-tick dwell; four-rate controller checks pass |
| R474-2-F1, MINOR (formerly R474-1-S1) | Remains **RESOLVED** | `KL_chan_map_capture.sv:895-897` excludes held pops; HELD-DUP and STARVED-HELD-DUP each fail their named checks in the fresh campaign |
| R474-2-R1/R2; R475-2-R1/R2; R474-3-R1/R2; R474-4-R1, RESIDUE | Remain **RESOLVED** | Recovery exception and plural drops; superseded PR status; `g_src_recentre` locator; twelve-control inventory and simulation-section link are present |
| R474-2-S1, SUGGESTION, Tests | **RETAINED**, optional | `settle_control.py` still does not directly pin error magnitude 2 as non-arming; unchanged artifact |
| R474-2-S2, SUGGESTION, Tests/Docs | **RETAINED**, optional | Shipping-clock quiet/latency evidence remains distinct from the published 6.25 MHz distribution; no new shipping-clock campaign here |
| R474-2-S3 / R474-1-S2, SUGGESTION, Tests | **RETAINED**, optional | `sim_ax1x1gptp.cpp` still has the no-decision NOT RUN branch; no claim that the physical leg ran in this review |

R475-3, R475-4 and R475-5 introduced no additional findings to close. No item is judged worsened, and no new wording RESIDUE is filed.

**Reviewer-owned ledger.** Coverage is limited to this assigned delta and the unchanged artifacts explicitly examined; it does not invent fresh full-bank or physical evidence.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Frozen scope through 6075072415; `MEDIA_CLOCK_FOLLOWING.md:1084-1096,1232-1249`; `TIME_SYNC.md:384-386`; preserved four-leg checks, 12 controls and replica bar | R475-7 | 8e4b1e53e9b5a8ef5f9854095347436ab84259b6 |
| RTL | CLEAN | Base comparison of capture and settle controller; unchanged `hdl/`, configs and synthesis inputs since Round 2f; `sim_main.cpp:550-559,618-626` observation-only trace emission; `receipts/source-audit.json` | R475-7 | 8e4b1e53e9b5a8ef5f9854095347436ab84259b6 |
| Robustness | UNCLEAN | Four-rate reset/recovery/ceiling checks; paired pulls; schedule failure probes; simultaneous action/slip standing control; nine decimal boundaries, R475-7-F1 | R475-7 | 8e4b1e53e9b5a8ef5f9854095347436ab84259b6 |
| Tests | UNCLEAN | Both cold defaults; explicit mutants; original public probe; independent physical duplicate/skip/action traces; reader tests; R475-7-F1 and retained R474-5-F1 | R475-7 | 8e4b1e53e9b5a8ef5f9854095347436ab84259b6 |
| Docs | UNCLEAN | TESTING timing tables; both Makefile headers; evidence disposition; reader half-open contract; public receipt inventories; R475-7-F1 and retained R474-5-F1 | R475-7 | 8e4b1e53e9b5a8ef5f9854095347436ab84259b6 |

**Hosted snapshot and real limits.** At 2026-10-09 06:29:26 UTC, `gh pr checks` and run metadata bind [run 37892515345](https://github.com/kebag-logic/milan-fpga/actions/runs/37892515345) to the exact reviewed head. Verilator shard 3/5 and all four Yosys shards succeeded. Verilator shards 0/1/2/4, firmware-unit, elaborate and docs-check were in progress. Lint, yosys-elaboration, bdd-conformance, wire-accountability, docs-check-no-git and full-ci-gate succeeded. The required `verilator-suites` aggregate had not reported completion, and no <=1260-second follow-ring result was yet available. Physical gPTP was **SKIPPED**, not executed. `receipts/hosted-checks-final.json` and `hosted-binding.json` preserve this read-only observation. This review does not wait for that run or own its acceptance.

No full parent/processor/time-processor, portability, builder or physical bank ran here. No manager source bank exists at this exact head, and none is inferred. The author's current source-gate and builder results are public summary claims; their Round 2h raw packet was not available for verification. No vendor synthesis/place/route or hardware action ran. Physical calibration is **NOT RUN**; field skips and simulation are not hardware proof. The full arrival grids, render campaign and render timing replica were not rerun in this delta review.

`receipts/source-audit.json` proves one commit, seven changed files, unchanged target lists, unchanged suite discovery/budgets and no RTL/configuration/synthesis/resource-record change since Round 2f. The render Makefile differs only in comments. Therefore Round 2f's resource records remain applicable as prior measurements; this review does not claim new resource measurements or rebuild their entire provenance. TOC checks initially refused the missing pinned renderer, then passed after a hash-locked install confined to scratch; both initial and successful receipts are retained.

**Pending manager duties.** Obtain the decimal-boundary correction and independent re-review; publish the missing Round 2h receipts and close the retained timing-verification item. Accept exact-head hosted `verilator-suites` with follow_ring <=1260 seconds and the required local workflow replica. Build the final candidate from current dev at the merge turn, run the builder and native banks and required explicit campaigns, and link those candidate receipts on the PR. This source review does not substitute for that candidate validation. Retain the optional suggestions, run the assigned bench repeat of INTERNAL-to-AAF and AAF-to-CRF, and perform authorized merge, containment and public completion bookkeeping.

**Integrity and publication.** `receipts/integrity.log` proves all 1232 superproject tracked blobs against their exact object IDs, modes and stage-zero index, independently of quiet status flags. The index tree is the stated tree. The four required populated submodules were proved the same way: processor `2ad2f845dd583f8310075fa2380cb60a04fd091a`, time processor `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`, AXIS `48ff7a7e2ef782cf778d47910cf85835c64b1bce`, and lwSRP `9197193e47a6bb1c45a56d90a18c1784123aba44`. lwSRP was initialized at its existing gitlink for this proof. `external` remains uninitialized as received; its superproject gitlink was verified. There are no tracked changes, untracked files or ignored products in the clone. All jobs have terminated.

Local installation and home-directory prefixes in 11 receipts are replaced by `<SIMULATOR_ROOT>` or `<USER_HOME>` for publication. `receipts/path-redactions.json` binds the unchanged raw logs, retained only in scratch, to their published copies; no command flag, check or result is altered.

Portable reproduction scripts and execution receipts are listed in `MANIFEST.sha256`, with paths relative to this packet. Only that listed material and REPORT.md are publishable; scratch is excluded.

R475-7 FINISHED
