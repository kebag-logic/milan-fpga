[R615] POSITIVE - exact head 169073fe9751b873d140b46d4363e02ad4f56b88

Issue #70 / PR #79, external independent review, round R615-2. All five lenses are CLEAN. No open BLOCKER, MAJOR, MINOR or RESIDUE remains. Two prior SUGGESTIONs are retained below; neither prevents acceptance.

Reviewed tree: `4396587d7017497d185c38d3c497ab3b7e04cb42`. Source base: `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`. The published PR head was re-read and matches. The diff comprises seven commits and fourteen files. [Public review start](https://github.com/Mister-M-alt/FPGA-gPTP/pull/79#issuecomment-6105615031).

The resumed directory contained a skeleton and passing focused receipts. This review retained those files, performed fresh focused validation, and completed the remaining work. The independent verdict and ledger were saved in `receipts/independent_verdict.md` before opening either prior public review report. No private author material, other checkout, management material or unpublished reviewer report was read. No source edit, commit, push, GitHub write or synthesis run was performed.

**Authority and scope.** There is no repository AGENTS.md or CONTRIBUTING.md at this head. The supplied workspace instructions apply. `docs/README.md` orders implementation and executable evidence above guides and historical records. `docs/INTEGRATION.md` defines the single `clk_i` domain, and both RTL top declarations retain that port. Acceptance comes from [issue #70](https://github.com/Mister-M-alt/FPGA-gPTP/issues/70), its [initial scope decision](https://github.com/Mister-M-alt/FPGA-gPTP/issues/70#issuecomment-6101768043), and its [round-two decision](https://github.com/Mister-M-alt/FPGA-gPTP/issues/70#issuecomment-6105265276). The latter requires effective binding, zero unclocked registers, critical-warning rejection, full-path identity and named negative controls. The ordering agrees with the [2026.1 non-project constraint flow](https://docs.amd.com/r/en-US/ug903-vivado-using-constraints/Non-Project-Flows).

This is a synthesis-recipe and measurement-documentation change. No protocol, PHC, parent interface, RTL or microcode behavior change is authorized or present. Parent adoption is outside this issue's source acceptance.

| Acceptance / public scope item | Disposition and artifact-specific evidence |
|---|---|
| Both tops receive the 10 ns constraint before synthesis | MET. `syn/ooc/engine_ooc.tcl:14` and `ucpu_ooc.tcl:14` read the repository XDC before `synth_design` at lines 22 and 16. `ooc_clock.xdc:9` defines `clk` on `clk_i`. Independent Tcl command traces confirm ordering and preserve top, part and generic arguments. These traces emulate commands; they are not synthesis runs. |
| Retain six reports | MET. Both scripts retain flat utilization, hierarchical utilization and timing reports, appending clock-source information to the existing timing file. Tcl traces verify all six filenames. The synthetic end-to-end positive control retains six reports and exits zero. The author separately reports an actual exact-head `make ooc` pass with six retained reports. |
| Remeasure constrained and unconstrained figures at the source baseline | MET on published source evidence. The author's exact-head issue receipt records both flows and their setup, and states normalized bodies match the first review head except for appended clock reports. Current guide tables agree. No independent remeasurement is claimed in this round. |
| Label quoted resource figures by flow | MET. `docs/HDL_DEVELOPER.md:174` and `docs/MANAGER.md:29` distinguish both flows; the latter labels the PR #76 delta unconstrained. Six historical pages add flow notes without changing figures. Historical Tcl recipes are unchanged from founding commit `c99f7a8` through the source base. Prototype notes disclose narrower historical evidence. Placed bench figures retain their separate recipe. |
| Named rejection when constraints arrive late or do not take effect | MET. Each top's late-read and foreign-file plants stop make before the synthesis sentinel. Independent log/report cases reject wrong period/source, extra clock, late parse, missing count/report/log, critical warnings and unclocked registers. Synthetic unclocked output for either top makes the actual shell/make flow fail by name. |
| Source gates and unchanged functional sources | MET on the evidence below. `hdl`, `tb`, `bench` and `scripts` have no base-to-head delta. Fresh local contract, lint and documentation gates pass. Full source simulation and actual synthesis are supported by the author's published exact-head receipts. |

The published measurement table agrees across both current guides:

| Top / flow | LUT | FF | BRAM tiles | DSP | WNS |
|---|---:|---:|---:|---:|---:|
| Engine, constrained | 4,852 | 3,652 | 1.5 | 4 | +1.773 ns |
| Engine, unconstrained | 4,853 | 3,652 | 1.5 | 4 | +1.773 ns |
| MicroCPU, constrained | 1,643 | 733 | 1.5 | 4 | +1.941 ns |
| MicroCPU, unconstrained | 1,643 | 733 | 1.5 | 4 | +1.941 ns |

Both flows use Vivado 2026.1, `xc7a100tfgg484-2`, out-of-context synthesis, the default directive, shipping ROM and 10 ns clock. The issue's older +2.249 ns engine figure predates PR #76. Unconstrained slack is a post-synthesis report, not evidence of timing-driven synthesis.

**Execution and public evidence.** The [pinned public bundle](https://github.com/kebag-logic/milan-fpga/tree/60da4bff912a59b5fec27c850893a333ed2cd2d4/review-evidence/g70-r1) contains author documents for the first review head, not raw exact-head logs. Fresh public downloads match both manifest hashes. It is historical corroboration. The [exact-head author receipt](https://github.com/Mister-M-alt/FPGA-gPTP/issues/70#issuecomment-6105533391) and current PR body report successful source gates and real synthesis controls, including both renamed-port cases, an 8 ns clock and a foreign same-basename file. These are author execution claims with excerpts, not reviewer executions.

| Reviewer execution at this head | Result | Receipt |
|---|---|---|
| Pinned compiler identity, checked before use | Verilator 5.050, revision v5.050 | `receipts/resumed_gates/compiler_identity.txt` |
| `make -j16 contract` | rc 0 | `receipts/resumed_gates/contract.log` and `.rc` |
| `make -j16 lint` | rc 0, engine and bench | `receipts/resumed_gates/lint.log` and `.rc` |
| `make -j16 docs` | rc 0; checks/self-tests pass; source evidence 20 exact, zero findings | `receipts/resumed_gates/docs.log` and `.rc` |
| Static clock check / unchanged self-test | PASS / PASS, 30 arms | `receipts/resumed_gates/ooc_static.log`; `receipts/probes/selftest_clean.log` |
| Independent focused probes | 34/34 expected outcomes: two Tcl traces, seven make controls, fourteen post-check cases, ten checker mutations, one clean self-test | `receipts/probes/results.json`; per-arm raw logs and return codes |
| Prior-finding follow-up probes | 7/7 expected outcomes: three synthetic integrations, one additional checker mutation, three retained-suggestion observations | `receipts/reconcile/results.json`; per-arm receipts |
| Regenerated shipping ROM | Byte-identical to tracked ROM | `receipts/rom_verification.json` |

All eleven checker mutants fail through named self-test diagnostics without crashes. The synthesis sentinel deliberately returns 37, so make rc 2 in the clean static-control arm proves it reached the sentinel. Fault arms return make rc 2 without reaching it. The synthetic end-to-end clean arm returns zero; each unclocked arm returns make rc 2 after post-check rejection. These synthetic outputs are not resource or timing measurements.

The first probe-driver run expected a later diagnostic for the foreign-path mutant. The checker correctly rejected it earlier. Only the review script's expectation was corrected; no source change was needed. Initial results and the correction note are retained in `receipts/probe_first_run_*` and `receipts/probe_harness_note.txt`.

The author reports exact-head `make tb` rc 0: microCPU 768/768, parser 268/268, engine 1,613/1,613 in three images, engine mutation arms 34/34, gaskets 81/81 plus 5/5, tsn-gen 288/288 plus 4/4, and bench tag PASS. The same receipt reports contract, lint, docs and actual `make ooc` rc 0. This reviewer did not rerun the prohibited full source bank.

**Prior findings, explicitly reconciled at this head.** Sources: [prior internal findings](https://github.com/Mister-M-alt/FPGA-gPTP/pull/79#issuecomment-6105254592) and [prior external findings](https://github.com/Mister-M-alt/FPGA-gPTP/pull/79#issuecomment-6105263432), opened after the independent verdict and ledger were saved.

| ID / severity / all attributable lenses | Location, authority and impact | Required or suggested outcome; verification and disposition |
|---|---|---|
| R614-1-F1 — MINOR — Conformance, Robustness, Tests, Docs | `check_ooc_clock.py:148`, `:170`; `run.sh:5`, `:39`. The round-two decision requires effective binding, not just parsing. Previously unclocked synthesis could be labelled constrained. | RESOLVED. Timing checks require the exact 10 ns summary, source `clk_i` and `no_clock` zero; log checks reject critical-warning lines and nonzero final counts. Both tops append `report_clocks`. Independent isolated faults and both synthetic unclocked make integrations fail by name; clean controls pass. Actual renamed-port synthesis failure is supported by the author receipt. Headers and guide claims match the checks. |
| R614-1-F2 — SUGGESTION — Tests | `check_ooc_clock.py:110`, `:184`, `:318`, `:320`. Prior mutation controls exposed missing independent coverage for duplicate clocks and a widened log-read search. | RESOLVED. The double-clock fixture names its count finding. The late-read fixture requires both findings, so accepting an echo anywhere now fails the self-test. Reviewer mutations `mutant_duplicate_xdc` and `echo_anywhere` are both killed by name. |
| R615-1-01 — RESIDUE — Docs | `docs/HDL_DEVELOPER.md:219`. The earlier sentence insufficiently scoped historical flow wording; no measurement changed. | RESOLVED with the exact requested replacement: "This repository's `syn/ooc` figures before #70 were unconstrained." Fresh docs gate passes. No residue remains to carry. |
| R615-1-02 — SUGGESTION — Conformance, Robustness, Tests | `check_ooc_clock.py:93`, `:188`. The round-two decision adopts full-path identity; basename matching could validate another file. | RESOLVED. Static matching requires the literal repository-relative argument; log matching requires the resolved full path. Foreign-file plants fail for both scripts; basename-widening mutations fail the named self-test. |
| R615-1-03 — SUGGESTION — Robustness, Tests | `check_ooc_clock.py:101`, `:113`, `:272`. The static parser permits additional non-`create_clock` XDC commands; malformed `10.0.0` raises `ValueError`; some missing-input guards lack built-in self-test arms. These are broader hardening/diagnostic gaps beyond the frozen clock rules. | RETAINED, narrowed by the new post-check: a second visible clock is rejected after synthesis. Extra-command static acceptance and malformed-period behavior are confirmed in `receipts/reconcile/retained_suggestion.json`. Suggested outcome: explicit allowed-command policy, named malformed-period finding and missing-input self-test arms. Verify those controls while retaining the clean 30-arm pass. No acceptance failure is established at this head. |
| R615-1-04 — SUGGESTION — Conformance, Docs | `hdl/ucpu/KL_gptp_ucpu.sv:11`. An unchanged historical comment describes the delta from another repository's 1,070-LUT anchor as arithmetic growth. The current recipe differs; its Tcl header already qualifies that comparison. | RETAINED. No-RTL-change scope leaves this comment untouched, and no current figure is shown wrong. Suggested outcome: a later scoped comment update pointing to `syn/ooc/ucpu_ooc.tcl`. Verify it distinguishes the original comparison flow and changes no RTL behavior. Manager decides follow-up ownership. |

**Reviewer-owned ledger.** Each row covers this round's exact head; earlier reviews are not substituted for current coverage.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue acceptance and both scope decisions; Tcl/XDC; six report destinations; issue/PR measurement tables and author source receipts; actual diff scope | R615-2 | 169073fe9751b873d140b46d4363e02ad4f56b88 |
| RTL | CLEAN | Unchanged `hdl/tb/bench/scripts`; both top clock declarations and engine 100 MHz default; synthesis arguments and shipping ROM identity; fresh lint and contract | R615-2 | 169073fe9751b873d140b46d4363e02ad4f56b88 |
| Robustness | CLEAN | Static and post-synthesis checks, path identity, critical-warning/timing parsing, shell failure propagation; negative controls for each top; retained suggestion 03 | R615-2 | 169073fe9751b873d140b46d4363e02ad4f56b88 |
| Tests | CLEAN | Built-in 30-arm self-test; 41 expected reviewer probe outcomes including eleven named mutation kills; author exact-head full-gate receipt; hosted state inspection | R615-2 | 169073fe9751b873d140b46d4363e02ad4f56b88 |
| Docs | CLEAN | HDL/manager flow tables; six archived notes; historical Tcl identity; PR/issue claims against source evidence; fresh docs checks; resolved residue and retained suggestion 04 | R615-2 | 169073fe9751b873d140b46d4363e02ad4f56b88 |

**Integrity and reproduction.** `verify_clone.py` independently hashes all 106 tracked blobs using Git blob framing, checks their modes, and compares every stage-zero index entry with the exact-head tree. All match. Status is empty, including ignored files. There are zero mode-160000 entries, so no required submodule gitlinks apply in this donor repository. The base-to-head diff passes whitespace checking. All disposable copies, generated data and temporary directories used by the new probes are under packet `scratch/`, excluded from publication.

Invoke the portable scripts with Python 3, in this order:

1. `run_focused.py --repo CLONE --packet PACKET --compiler PINNED_COMPILER --jobs 4`
2. `reconcile_probes.py --repo CLONE --packet PACKET --jobs 4`
3. `verify_clone.py --repo CLONE --output PACKET/receipts/verify_clone.json`

The driver waits in the foreground, with separate logs and return-code files, at most four probe processes concurrently, and `make -j16`. No heavy build or synthesis is involved. `MANIFEST.sha256` lists the publication set; unlisted resumed files and all scratch contents are excluded.

**Real limits.** Actual synthesis, placement, routing and full simulation were not rerun by this reviewer. Published synthesis excerpts and the source table support acceptance; their underlying six raw actual report bodies were not available in the specified public bundle for independent normalization. Synthetic fixtures test checker behavior and shell propagation only. The Tcl reader is a narrow format guard, not a general interpreter or proof against arbitrary adversarial rewrites.

Exact-head GitHub inspection found zero workflow runs, zero check runs, and a pending combined status with zero contexts. There are no executed or skipped hosted jobs to count as evidence. Absence of hosted execution is not a passing hosted gate. No manager source bank runs at this head, and none is claimed or inferred.

Physical calibration NOT RUN. No hardware was used. Field skips are not hardware proof, and OOC slack is not board timing qualification.

**Pending manager duties.** Obtain the other independent round-two disposition and apply the full completion bar. Build and validate the current-dev merge candidate with builder and native banks at the merge turn, using source base `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d` and live dev `ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5`, then link receipts on the PR. Source-head validation above does not validate that candidate. Hosted/act acceptance remains manager-owned. Decide follow-up ownership for the two retained suggestions and publish this packet. No residue item remains open from this review.

R615-2 FINISHED
