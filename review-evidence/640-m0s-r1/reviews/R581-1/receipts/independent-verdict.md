[R581] POSITIVE - exact head bc89f84e6757f8fcddf21958e99f40f17bc0ee1e

R581-1 is the external independent review of PR #702's authorized M0s tooling step. All five lenses are CLEAN. No BLOCKER, MAJOR or MINOR was found. One wording RESIDUE is recorded below. This verdict does not complete issue #640, qualify a split image, or authorize merge.

The reviewed tree is `b498495714ea3ca8e3ab8e38781cc7ff54b68967`. Its sole commit follows base `7c1b52bee26b497080ee22b1c1986109f80a5ee7`. The nine-file diff changes six measurement/test scripts and three documentation files. It changes no RTL, firmware, workflow, dependency pin, accepted resource record or policy value.

Scope was reconstructed from AGENTS.md and CONTRIBUTING.md, docs/README.md, the frozen issue and public scope decisions, requirements and interface authorities, then the complete diff and commit history. Public executable evidence was read afterwards. No private author material or other reviewer's report informed the independent pass. The independent verdict and ledger were frozen before the prior-public-finding audit.

The [assignment](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6086604096) explicitly permits step 2 alone when the route prerequisite fails. The [STOP](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6087021702) is correct at this head: `sw/litex/milan_soc.py:2505` describes the disconnected mailbox, `:2549` ties link/GM/RX idle and discards TX, and `hdl/milan/milan_datapath.sv:8003` instantiates the wrapper unconditionally. The switch at `sw/litex/milan_soc.py:3612` only adds the mailbox foundation. `sw/firmware/ctrl/maap/README.md:85` and `sw/firmware/milan_baremetal/Makefile:6` likewise establish no replacement shipping entry point. No selected route was required or justified under that prerequisite.

REQUIREMENTS.md section 1 and `docs/ARCHITECTURE_HW_SW_SPLIT.md:30` require one owner per selected function, retain fabric media/gPTP, and keep shipping all-fabric until qualification. D7, the plan's lane sequence, and AREA_BUDGET.md retain the last accepted record until M9. NFR-RES-01 remains 38,040 LUT with timing met. The 121.5-tile ceiling preserves the separate 13.5-tile reserve. The approximately 50-tile firmware budget is not a measured allocation.

[R581] PASS Conformance - `syn/ooc/pp_baseline.py:259`, `syn/ooc/pp_resource_gate.py:278`, `:731`, `docs/design/MARK_II_AREA_PLAN.md:634` - The three named selections implement the scoped measurement contract. Split exports require explicit matching placement, whole-image reports, input identity, route completion and the existing comparison policy. Intermediate split writes are refused. The STOP and intermediate ledger claim no split figure.

[R581] PASS RTL - `syn/ooc/pp_placement.py:18`, `:34`, `:88`, `sw/litex/milan_soc.py:2549`, `hdl/milan/milan_datapath.sv:8003`, `protocol-processor/hdl/top/protocol_processor_top.sv:1918` - Module identities were checked against the actual parent and pinned processor. Partial placement retains AECP/notifications and permits zero or one wrapper; complete placement requires their absence. Both split selections require mailbox/gPTP and exclude ADP, both ACMP engines, SRP and both MAAP implementations. The exact diff and blob verification show no clock, reset, CDC, FSM, width, interface or implementation change. Integration remains a separate prerequisite.

[R581] PASS Robustness - `syn/ooc/pp_placement.py:51`, `:63`, `syn/ooc/pp_baseline.py:154`, `syn/ooc/pp_resource_gate.py:297`, `:323`, and `receipts/independent-probes.log` - Missing, duplicated, mislabelled, malformed and incorrect populations fail by name. Retained ROM geometry and pre-synthesis diagnostic enforcement remain. Primitive growth, BRAM ceiling, timing, incomplete routing and identity changes retain their existing nonzero outcomes. The entire generated Tcl was exercised with controlled design queries: early retained ADP and late missing mailbox both stop their intended stage. The legacy missing-wrapper refusal also executes and names the wrapper.

[R581] PASS Tests - `syn/ooc/pp_placement_selftest.py:55`, `:73`, `:156`, `syn/ooc/pp_baseline_mutants.py:13`, `syn/ooc/pp_resource_gate_mutants.py:283`, `receipts/checks.json`, and `scripts/independent_probes.py` - Positive controls, role reversals, wrapper-free fixtures, legacy compatibility and enforcement-removal campaigns were executed. Every added placement guard mutation is detected; no retained legacy detector was dropped. Independent probes compare the base and head and execute generated scripts, supplementing the committed fixtures.

[R581] PASS Docs - `docs/testing/PP_SHADOW_BASELINE_RECIPE.md:183`, `docs/design/MARK_II_AREA_PLAN.md:634`, `docs/design/AREA_BUDGET.md:358`, PR #702 body and the published author packet - Recipe selections, census limits, STOP, intermediate figures, memory obligations and M9-only re-recording are consistent with public scope. Documentation gates pass. The wording residue below changes no technical or acceptance claim.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Assignment 6086604096; REQUIREMENTS.md section 1; recipe:259; resource gate:278/731; plan:634 | R581-1 | bc89f84e6757f8fcddf21958e99f40f17bc0ee1e |
| RTL | CLEAN | placement:18/34/88; SoC:2549; datapath:8003; pinned processor top:1918; source.diff; integrity receipts | R581-1 | bc89f84e6757f8fcddf21958e99f40f17bc0ee1e |
| Robustness | CLEAN | placement:51/63; recipe:154; gate:297/323; resource.log; independent-probes.log | R581-1 | bc89f84e6757f8fcddf21958e99f40f17bc0ee1e |
| Tests | CLEAN | placement selftest:55/73/156; both mutation drivers; OOC suite; checks.json; independent probe script | R581-1 | bc89f84e6757f8fcddf21958e99f40f17bc0ee1e |
| Docs | CLEAN | recipe document:183; plan:634; area budget:358; PR body; public author packet; documentation receipts | R581-1 | bc89f84e6757f8fcddf21958e99f40f17bc0ee1e |

R581-1-R1 | RESIDUE | Docs | PR #702 body, Status paragraph

Authority/evidence: the published PR still says, "No remote branch or review object was changed." That sentence describes the author's local handoff but reads as current PR status. Impact: narrative ambiguity only; no measurement, figure, verdict, test, generated artifact, conformance, clause or privacy claim changes. Required exact fix: replace that sentence with "The author completed this work locally before publication." Verification: inspect the published Status paragraph; no source or test change is needed. The manager may carry this to the residue checklist. It leaves Docs CLEAN.

Local execution used concurrent independent checks under one foreground runner, with at most four resource-mutation workers plus five other children. No background shell job, full parent/processor/builder bank, implementation run, hardware operation, shared install, source fix or GitHub write was performed. Full builder execution was explicitly prohibited; eight focused resource/shipping-image checks ran instead. Physical calibration was NOT RUN. The scoped HDL executable's identity was verified as 5.050; no new HDL simulation build was needed for this tooling-only diff.

| Executed check | Result | Raw receipt |
|---|---|---|
| Recipe self-test | PASS, including both census stages and every role reversal | receipts/recipe.log |
| Recipe enforcement removals | Control PASS; all 41 detected | receipts/recipe-mutants.log |
| Resource self-test | 260 arms and 500 cases at seed 234 PASS; split controls PASS | receipts/resource.log |
| Resource enforcement removals | Control PASS; all 180 detected | receipts/resource-mutants.log |
| OOC Tcl refusal suite | All 58 arms PASS (491.77 s) | receipts/ooc.log |
| Baseline policy validation | All three endpoints PASS | receipts/baseline.log |
| Hierarchy/report helpers | PASS | receipts/reports.log |
| Focused builder resource and image checks | Eight checks PASS, no skipped arm | receipts/builder-focused.log |
| Documentation and related source checks | Fourteen commands PASS | receipts/checks.json and named logs |
| Independent compatibility and adversarial probes | PASS | receipts/independent-probes.log |
| Whitespace and tracked integrity | PASS | receipts/diff-check.rc; integrity-before.json; integrity-after.json |

`scripts/run_checks.py` records every command, return code and elapsed time in `receipts/checks.json`; separate `.log` and `.rc` files retain raw results. Reproduce with `python3 scripts/run_checks.py <clone> <packet> <pinned-markdown-python>`, then `python3 scripts/independent_probes.py <clone> <packet>` and `python3 scripts/verify_integrity.py <clone>`. Set `TMPDIR=<packet>/scratch` and `PYTHONDONTWRITEBYTECODE=1` for the latter two commands. The mutation driver has no `--jobs` option; `-X cpu_count=4` bounds its workers. The runner joins every process before returning.

The accepted record is byte-identical to the base: 27,995 bytes, SHA-256 `cf2eec5ce8e41d50f5308264a8608d7341ba142d6d3a04058e5572e1a8a29e41`. Independent stored-record replay returns 0 for each endpoint, identically before and after this change. Report parsing, digest construction, figures, hierarchy scopes and synthetic route-status checks also match. Generated legacy integrated and standalone 1x1/8x8 recipe outputs match the base byte for byte in the probe fixtures.

| Unchanged stored endpoint | LUT | FF | Slices | RAMB36 / RAMB18 | DSP / CARRY4 | WNS / WHS ns | Record replay |
|---|---:|---:|---:|---|---|---|---|
| route-1x1 | 50,267 | 54,413 | 15,779 | 74 / 27 | 14 / 3,402 | +0.299 / +0.031 | 0 |
| ooc-1x1 | 23,179 | 19,779 | Not recorded | 16 / 3 | 8 / 1,494 | -3.562 / +0.159 | 0 |
| ooc-8x8 | 30,135 | 27,380 | Not recorded | 21 / 5 | 8 / 1,889 | -2.278 / +0.159 | 0 |

These are stored figures, not new measurements. Identities still name build 6511674, device `xc7a100tfgg484-2`, the recorded synthesis/implementation directives and worker settings, and 20.000 ns standalone clocks. The prior completed route and four timing corners are documented in `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:60`. Original full measurement directories were not supplied in this public packet, so this review does not claim a fresh parse of those route files or a repeated route. Unconstrained standalone setup slack establishes no integrated timing result.

The [public source evidence packet](https://github.com/kebag-logic/milan-fpga/tree/6aae6d5fcc382329791dd54395da2605e18e0f69/review-evidence/640-m0s-r1) contains the author's handoff and 28-command receipt inventory. All five downloaded files match its published manifest. It does not publish those 28 raw logs; their listed hashes are author evidence, not independently inspected raw execution. This packet supplies fresh raw receipts for the checks executed here. No manager source bank ran at this head, and none is inferred.

Independent verdict and ledger frozen before reading prior public findings. Audit follows in the final report.

Hosted checks remain in progress in the inspected exact-head snapshot. Final snapshot follows in REPORT.md; no hosted acceptance is asserted.

Tracked integrity was verified directly against committed blob bytes, file kinds and executable modes, and the full stage-zero index. The three required dependencies are registered submodules at `2ad2f845dd583f8310075fa2380cb60a04fd091a`, `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`, and `48ff7a7e2ef782cf778d47910cf85835c64b1bce`. Their tracked bytes, modes and indices also match. All disposable trees are under packet `scratch/` and excluded from publication. The unit memory ceiling is 12 GiB; the current sampled peak is below 2 GiB, with no out-of-memory event.

The manager still owns hosted/local-workflow acceptance, the second independent verdict and consolidated ledger, final current-dev candidate validation with builder/native banks, publication of those candidate receipts, and post-merge containment. Source base and supplied live dev were both `7c1b52bee26b497080ee22b1c1986109f80a5ee7`; candidate validation remains a separate merge-turn duty. This review supplies no merge authorization. Parent integration, actual split routes and firmware-memory reconciliation, service/physical qualification, and M9 acceptance re-recording remain future work. Issue #640's final 38,040-LUT acceptance is not met or closed by this PR.

R581-1 FINISHED
