[R614] POSITIVE - exact head 169073fe9751b873d140b46d4363e02ad4f56b88

Issue #70 / PR #79, round R614-2. Tree `4396587d7017497d185c38d3c497ab3b7e04cb42`; source base `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`. [Public review start](https://github.com/Mister-M-alt/FPGA-gPTP/pull/79#issuecomment-6105582564).

All five lenses are CLEAN. There is no open BLOCKER, MAJOR or MINOR. The prior clock-binding defect is resolved. Three optional suggestions are recorded below, including two retained from the prior public review; none changes the verdict.

**Scope and independence.** The review resumed its own interrupted packet, checked the clean clone and saved receipts, and retained the completed exact-head synthesis run after verifying every exported tracked byte and mode. No repository or ancestor AGENTS.md or CONTRIBUTING.md was present; the session instructions applied. Reconstruction followed `docs/README.md`, the issue acceptance and public scope decisions, the current interface/source authorities, the complete base-to-head diff and seven-commit history, then public executable evidence. The independent verdict and five-lens ledger were written to `receipts/independent_verdict.md` before opening either prior reviewer report. No private author material, other review packets, management material, source fixes, commits, pushes, GitHub writes, hardware, delegated work, or prohibited full banks were used.

The controlling authorities are [issue #70](https://github.com/Mister-M-alt/FPGA-gPTP/issues/70), the [original scope and proof list](https://github.com/Mister-M-alt/FPGA-gPTP/issues/70#issuecomment-6101768043), and the [round-two ruling](https://github.com/Mister-M-alt/FPGA-gPTP/issues/70#issuecomment-6105265276). They require a 10 ns constraint before synthesis on both tops, six retained reports, remeasured figures with flow labels, no RTL changes, and a gate proving the clock actually bound to `clk_i`, with no unclocked registers or critical warnings. Protocol redesign and parent adoption are outside this source change.

**Acceptance and artifact evidence.**

| Requirement | Exact-head evidence and result |
|---|---|
| Apply the clock before synthesis, both tops | `syn/ooc/engine_ooc.tcl:14` precedes synthesis at :22; `ucpu_ooc.tcl:14` precedes :16. `ooc_clock.xdc:9` defines the single 10.000 ns `clk_i` clock. Own head logs show the read at :28, synthesis command at :38/:32, and full-path XDC parse at :116/:84 before mapping at :443/:372. PASS. |
| Prove the clock took effect | `check_ooc_clock.py:143-212` checks the timing summary, appended clock-source report, zero `no_clock`, critical-warning lines and final count. Both head reports show `clk {0.000 5.000} 10.000 100.000`, source `{clk_i}`, and zero unclocked registers. Both logs have zero critical warnings. PASS. |
| Reject order regression and foreign XDC | `check_ooc_clock.py:79-123,169-202`; `run.sh:31,39`; `Makefile:39-40`. Independent make-flow plants for either late read, a foreign same-basename XDC, duplicate clock and 8 ns period stop before the synthesis stub, with named findings. The clean control reaches the stub. Full-path log substitution also fails by name. PASS. |
| Retain reports and rebaseline figures | Successful own head and baseline runs retain flat utilization, hierarchical utilization and timing for each top. `receipts/measurement_comparison.txt` independently checks every published metric; raw reports are in `receipts/ooc_head/` and `receipts/ooc_main/`. PASS. |
| Label current and dated figures by flow | `docs/HDL_DEVELOPER.md:174-221`, `docs/MANAGER.md:29-66`, and flow notes at :11 in the six modified archived pages. The issue's public measurement tables agree. Archived numeric values are unchanged. PASS. |
| Preserve RTL and donor gates | `hdl`, `tb`, `bench` and `scripts` tree IDs are identical to the base, including generated images. Own contract, lint and documentation gates pass. The author's exact-head public gate receipt supplies full donor simulation coverage; it is not represented as a reviewer or manager full-bank run. PASS within the authorized review scope. |

**Independent measurements.** Vivado 2026.1, build 6511674; `xc7a100tfgg484-2`; `synth_design -mode out_of_context`; default directive; shipping ROM; 10 ns clock. The head run was recovered from this same round, completed at 04:58:41Z, and validated against the exact exported head. The baseline run was completed during the resumed session. Both used the shared exclusive synthesis lock, with the two tops run sequentially.

| Top / metric | Unconstrained base | Constrained head |
|---|---:|---:|
| Engine LUTs | 4,853 | 4,852 |
| Engine registers / BRAM tiles / DSPs | 3,652 / 1.5 / 4 | 3,652 / 1.5 / 4 |
| Engine WNS; failing / total endpoints | +1.773 ns; 0 / 12,254 | +1.773 ns; 0 / 12,254 |
| MicroCPU LUTs / registers / BRAM tiles / DSPs | 1,643 / 733 / 1.5 / 4 | 1,643 / 733 / 1.5 / 4 |
| MicroCPU WNS; failing / total endpoints | +1.941 ns; 0 / 3,165 | +1.941 ns; 0 / 3,165 |

Timing-summary bodies match after removing only Date/Host headers and the head's newly appended `report_clocks` report. Equal slack does not prove the old flow was constrained: its logs place `create_clock` after successful synthesis. The new logs demonstrate synthesis-time parsing. `receipts/source_audit.txt` also verifies both old Tcl blobs were unchanged from founding commit `c99f7a8` through the source base.

**Executable checks.**

| Check | Result / receipt |
|---|---|
| Static clock gate and 30-arm self-test | Both rc 0; `receipts/quick/static.log`, `selftest.log` |
| Documentation, diagrams and source-evidence checks | rc 0; 11 current/17 historical pages, 9 pinned assets, 3 source-bound PNGs, 20 exact source references; their self-tests pass. `receipts/quick/docs.log` |
| Contract and engine/bench lint | Both rc 0, scoped Verilator identity verified as 5.050 before use; `receipts/quick/contract.log`, `lint.log`, `identity.txt` |
| Independent checker mutation sweep | Clean control passes; 28/33 killed; five survivors assessed below. This sweep's rc convention reports valid execution, not universal mutation coverage. `receipts/checker_mutation_sweep.txt` |
| Independent report/log and make-flow probes | All 24 report/log probes and eight make-flow probes meet their expected outcomes. `receipts/boundary_probes.log`, rc 0 |
| Real renamed engine clock through shipping `run.sh` | Clean microCPU succeeds; renamed engine synthesizes with two missing-port critical warnings; final gate gives six findings, empty Clock Summary, no binding, `no_clock (4412)`; `run.sh` rc 1. Probe succeeds. `receipts/real_port_probe/` and `real_port_probe_result.log` |
| Exact prior mutation variants | Both the duplicate-clock weakening and read-echo-anywhere weakening now fail the self-test by name. `receipts/prior_resolution_probes.log` |

The real rename changed only a disposable engine copy, preserving submodule formal port names. It demonstrates failure propagation through the actual runner, not only a fixture-level rejection. The unmodified exact-head run passes. Lightweight independent gates ran concurrently; each has its own log and return code. Synthesis ran under the shared lock without another reviewer-owned heavy build. All commands were supervised to completion; nothing remains running.

**Public evidence boundaries.** The [pinned g70-r1 bundle](https://github.com/kebag-logic/milan-fpga/tree/60da4bff912a59b5fec27c850893a333ed2cd2d4/review-evidence/g70-r1) contains the author's handoff and PR body for `26622e27`, not this head's raw full gate logs. Its published hashes match (`receipts/public_evidence_identity.json`). Current source-head gate evidence is the [author's exact-head receipt](https://github.com/Mister-M-alt/FPGA-gPTP/issues/70#issuecomment-6105533391) and current PR body: `make tb`, contract, lint, docs and OOC all report rc 0; simulations report microCPU 768, parser 268, engine 1,613 in three images, engine mutation campaign 34/34, gaskets 81+5, tsn-gen 288+4 and bench-tag PASS. Those simulation totals are attributed author evidence, not independently rerun here. Own raw OOC and focused-check receipts supply the independent evidence above.

At the final public check, PR #79 still names the exact requested head, with zero submitted reviews and zero inline comments; the prior findings are in the two top-level review comments. Exact-head hosted queries return zero workflow runs and zero check runs (`receipts/hosted_runs.json`, `hosted_checks.json`), so no executed or skipped hosted context is counted as evidence.

**Prior public findings, resolved or retained.** Read only after the independent verdict and ledger were saved. Authorities: [prior internal findings](https://github.com/Mister-M-alt/FPGA-gPTP/pull/79#issuecomment-6105254592) and [prior external findings](https://github.com/Mister-M-alt/FPGA-gPTP/pull/79#issuecomment-6105263432).

| Prior ID / severity / attributable lenses | Disposition at this head | Verification |
|---|---|---|
| R614-1-F1 — MINOR — Conformance, Robustness, Tests, Docs | RESOLVED. Full-path parse, effective clock/source checks, zero-unclocked check, both critical-warning checks, named regression arms and matching documentation are present. | Clean real run passes; renamed engine run fails with six named findings; 30-arm self-test includes the original renamed-microCPU condition; full-path and period probes reject. |
| R614-1-F2 — SUGGESTION — Tests | RESOLVED, both reported survivors. Duplicate `create_clock` has a named arm; read-echo ordering now requires its own diagnostic. | `prior_resolution_probes.log`: both exact weakened rules are killed by name. |
| R615-1-01 — RESIDUE — Docs | RESOLVED with the requested exact sentence: “This repository's `syn/ooc` figures before #70 were unconstrained.” | `docs/HDL_DEVELOPER.md:219`; docs gate passes. No residue remains to carry. |
| R615-1-02 — SUGGESTION — Robustness, Tests | RESOLVED. Literal repository-relative argument and resolved full parse path are required, with same-basename foreign-file arms. | `check_ooc_clock.py:30,91,185-190`; independent make/log probes and mutation S2/L2. |
| R615-1-03 — SUGGESTION — Robustness, Tests | RETAINED as optional XDC grammar and diagnostic hardening, detailed below. | Extra XDC commands still pass the static gate; malformed numeric input exits nonzero; missing files fail by name. |
| R615-1-04 — SUGGESTION — Docs, Conformance | RETAINED as an optional future comment clarification, detailed below. | RTL comment unchanged; synthesis-script header explains the old-flow comparison; no measured figure is incorrect. |

**Open suggestions.** These are not open acceptance defects and leave their lenses CLEAN.

- **R614-2-S1 — SUGGESTION — Tests, Robustness.** Artifact: `syn/ooc/check_ooc_clock.py:269-388`; `receipts/checker_mutation_sweep.txt` S6/S7/T6/L3/L8 and `boundary_probes.log`. Authority: the gate's stated order, no-clock and final-count invariants. Five isolated weakenings survive the self-test: dropping post-synthesis `create_generated_clock` or `source`, accepting an absent `no_clock` line, accepting a parse outside the pre-mapping interval, and consulting the first rather than last count. Impact: optional regression coverage gaps; the current production checker rejects every corresponding plant for both tops. Required outcome for this review: none. Suggested outcome: add isolated named arms for these five cases. Verification: the clean control remains green and those five mutants become named self-test failures.
- **R615-1-03 — SUGGESTION — Robustness, Tests, retained.** Artifact: `check_ooc_clock.py:101-116` and the self-test; `receipts/prior_resolution_probes.log`. Authority: prior public suggestion and current XDC validation behavior. Extra generated-clock/exception commands are not forbidden by the static XDC parser; `10.0.0` yields a failing traceback; three static missing-file branches lack dedicated self-test arms. Impact: narrower grammar and clearer diagnostics would improve maintenance. The shipped XDC has exactly its intended command, malformed input fails closed, and all three missing files fail by name. No new real synthesis claim is made for the extra-command probes. Required outcome for this review: none. Suggested outcome: restrict allowed XDC commands, name malformed periods, add missing-file arms. Verification: valid XDC passes; each added plant fails with its specified diagnostic.
- **R615-1-04 — SUGGESTION — Docs, Conformance, retained.** Artifact: `hdl/ucpu/KL_gptp_ucpu.sv:11-14` and `syn/ooc/ucpu_ooc.tcl:5-12`. Authority: prior public suggestion and the issue's no-RTL scope. The older comment says the OOC delta prices exactly arithmetic growth; the new flow needs an old-order run for comparison to that historical anchor. Impact: future readers benefit from a pointer; current standalone figures reproduce identically and the Tcl header already gives the qualification. Required outcome for this review: none. Suggested outcome: clarify or link that comment in a later authorized source change. Verification: the comment names the historical flow or points to the qualified script header; no behavior changes.

**Reviewer-owned ledger.**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue acceptance and both manager scope comments; Tcl/XDC; six retained reports per flow; measurement comparison; named order/binding plants; public issue tables | R614-2 | 169073fe9751b873d140b46d4363e02ad4f56b88 |
| RTL | CLEAN | `docs/INTEGRATION.md` clock/reset authority; engine:64 and microCPU:46 clock ports and clocked processes; unchanged hdl/tb/bench/scripts tree IDs; ROM bytes; both synthesized tops; own lint/contract | R614-2 | 169073fe9751b873d140b46d4363e02ad4f56b88 |
| Robustness | CLEAN | Static/full-path/log/timing checks; `run.sh` fail propagation; 32 boundary probes; real renamed-engine rejection; prior suggestion probes; S1/03 remain optional | R614-2 | 169073fe9751b873d140b46d4363e02ad4f56b88 |
| Tests | CLEAN | 30-arm self-test; independent 33-mutant sweep; clean/negative make-flow controls; focused gates; author exact-head simulation receipt with attribution; prior exact mutant reconciliation | R614-2 | 169073fe9751b873d140b46d4363e02ad4f56b88 |
| Docs | CLEAN | HDL and manager measurement sections; `history/v1/{PROJECT_STATUS,RESOURCE_VALIDATION}.md`; `history/v1/prototype/{BENCH_TAP_WIRETRUTH,INTEGRATION_GUIDE,IP_BLOCKS,RESOURCE_VALIDATION}.md`; archive-only note diffs; clock headers; issue/PR claims; docs/diagram checks | R614-2 | 169073fe9751b873d140b46d4363e02ad4f56b88 |

The archived first-light bench figures come from `bench/arty/build.tcl`, which already reads its board XDC before synthesis and runs placement/routing; those are correctly distinct from this repository's OOC rebaseline. Other archived pages mentioning OOC without quoting its measurements do not require numeric flow annotations. No IEEE clause or certification claim is introduced by this change.

**Integrity, limits and manager duties.** `receipts/integrity_final.txt` verifies all 106 tracked blobs, executable modes, the exact HEAD/tree and index, and a clean worktree. There are zero gitlinks and no nested submodules, so no required submodule checkout is omitted. All disposable exports and mutations remain under the packet's unpublished `scratch/`. Every publishable receipt and reproduction script is listed in `MANIFEST.sha256`; receipt redactions replace host/path identifiers only, preserving diagnostics, counts and measurements. The independent verdict snapshot and its timestamp are included.

This is source validation, not validation of the final current-dev candidate. No manager source bank runs at this exact head and none is claimed or inferred. Full parent, protocol-processor, gPTP, Yosys and builder banks were not run by this review. There was no Docker/act, host act_ci, privilege escalation or hardware use. The script checker is deliberately narrow, not a general Tcl interpreter; post-synthesis evidence complements it. The OOC run has ordinary warnings and no board I/O timing constraints; it proves this scoped synthesis target, not routed or board timing. Physical calibration NOT RUN. Field skips are not hardware proof.

The manager still owns the second independent exact-head review/completion bar, any optional suggestion follow-up, hosted/act acceptance, and the final current-dev merge-candidate builder/native banks at the merge turn. The stated source base is `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`; live dev is `ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5`. Those candidate receipts must be linked on the PR when published. No publication or merge was performed here.

R614-2 FINISHED
