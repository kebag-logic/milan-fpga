[R549] POSITIVE - exact head 9c601b5983acfd60fb269b9a88c27b48cab7cf65

R549-4, external independent review of issue #686 / PR #695.
Tree: `d2337a496fb13813beb2f4a13aefcaca0e0a94db`.
Source base: `e21c1ca024d37ea188ad15b5c8f9c2dae18628df`.

All five lenses are CLEAN. R549-1-F4's remaining publication demand is resolved by the corrected public account and the available evidence. No manager source bank ran; this review neither claims nor infers one. No open MINOR, MAJOR or BLOCKER remains. Optional suggestions below remain optional.

This is a source review verdict. It does not declare the final merge candidate, hardware acceptance, or the whole issue complete.

Reconstruction and independence

I read AGENTS.md / CONTRIBUTING.md, docs/README.md, the issue and public scope decisions, requirements and interface authorities, then the requested diff and history, followed by public evidence. The requested range has 95 changed paths; comparison with imported dev `291710b1` isolates 20 lane paths. `48f12dc1..9c601b59` changes only `docs/design/MAAP_FABRIC.md`. Imported dev work was distinguished from the MAAP lane; this is not a fresh review of every imported firmware change.

The independent assessment and five-lens ledger were written to `independent-verdict.md` before reading earlier public review findings or another reviewer's report. Prior findings were then reconciled below. No private author material, management checkout, other review checkout, or author contact was used. R549-3's other dispositions stand, supplemented by the focused checks here.

The public contract is [issue #686](https://github.com/kebag-logic/milan-fpga/issues/686), including [the assignment](https://github.com/kebag-logic/milan-fpga/issues/686#issuecomment-6043036997) and [the round-2 scope decision](https://github.com/kebag-logic/milan-fpga/issues/686#issuecomment-6047563934). The assignment explicitly places bench interoperability after merge, with the manager. The clause authority remains IEEE 1722-2016 Annex B; this evidence reassessment does not replace the earlier direct standard-text review.

Disposition of the remaining finding

- ID: R549-1-F4, retained in part by R549-3.
- Previous severity: MAJOR. Lenses: Conformance, RTL, Tests, Docs.
- Artifacts: [manager correction 6052220964](https://github.com/kebag-logic/milan-fpga/pull/695#issuecomment-6052220964), [candidate evidence comment 6052017268](https://github.com/kebag-logic/milan-fpga/pull/695#issuecomment-6052017268), `author-r2/HANDOFF.md`, `author-r2/resource-receipts/`, and both candidate banks' results, completion and integrity records.
- Authority/evidence: AGENTS.md requires reconstructible public evidence; CONTRIBUTING.md requires source validation and current-dev candidate gates. Neither requires an additional manager-owned source bank on top of the author's source validation and the manager's candidate validation. The manager publicly withdraws the erroneous statement that such a source bank existed. The demand to publish its logs therefore has no remaining factual premise. The author source gate table, raw resource receipts, candidate bank logs and exact-head hosted execution are independently identifiable.
- Impact resolved: there is no longer an unaccounted-for claimed execution. Candidate evidence is not relabelled as source execution; absent logs are not treated as evidence of a failed or completed run.
- Required outcome: retain the correction and these distinct evidence populations publicly. No nonexistent log or additional source bank is required to clear this review finding.
- Verification: `evidence_audit.py` verifies candidate identities, 48/48 and 5/5 zero command statuses, all 53 numbered log objects, the 186-file repaired resource manifest, and equality of all three resource records with the reviewed head. Source gate applicability is checked by the documentation-only delta after `48f12dc1`. Result: RESOLVED across all four attributed lenses.

Evidence populations and results

| Population | Evidence examined | Result and boundary |
|---|---|---|
| Author source validation | [Archive 84add8ed, author-r2](https://github.com/kebag-logic/milan-fpga/tree/84add8ed571d376f8a1b39c3c6f71c4e80eed32a/review-evidence/686-r1/author-r2), final-head gate table; issue comment 6050832603 | Source execution is reported at `48f12dc1`, not as a new manager execution at `9c601b59`. Executable inputs are unchanged since that gate head. The public table reports MAAP suite/campaign/coverage, all five affected datapath suites, firmware/differential, lint, parser and docs gates passing. |
| Source resource measurements | Repaired archive `319f3567`, `author-r2/resource-receipts/r2-48f12dc1` | 186/186 checksum entries match. All three record objects equal the reviewed baseline, including identity, input digest, figures and scopes. Tolerances, floors and ceilings equal imported dev's policies. Earlier parser-regeneration results stand; no new synthesis or implementation run here. |
| Manager candidate validation | [Archive 319f3567, manager-candidate](https://github.com/kebag-logic/milan-fpga/tree/319f3567ed693bc5dffd422164a768c142485a2d/review-evidence/686-r1/manager-candidate) | Results/completion/integrity agree on commit `1351f398f9e0c246888b9ac5286db8370a3bc1f3`, tree `140c3b838ef3a1f72e2669744871a48b83911311`. Builder 48/48; native 5/5. Native logs cover parent suites, portability, both processor banks and behavior tests. These are inspected manager executions, not reviewer reruns. |
| Exact source head, focused reviewer execution | `focused-results.json`, six raw run logs and build/run status files | Clean harness: 130 checks, zero failures. Five selected defects built and exited 1 at the required named check. Compiler identity verified before execution. |
| Exact-head hosted snapshot | `hosted-checks.json`, `hosted-job-steps.json` | 22 successful contexts; Physical gPTP skipped. All five exhaustive simulation execution steps and all four portability execution steps succeeded. Aggregates were backed by executed shards. Manager retains hosted/local-replica acceptance. |
| Physical acceptance | Candidate builder `48.log`, `test_resource_calibration` gate 11; skipped physical context | Real calibration report absent: NOT RUN. Field skips and passing processes around skipped arms are not hardware proof. MAAP bench interoperability was NOT RUN here. |

Candidate base `b959830acd53a868febfe362974e33e144481aa7` is publicly identified as #654's candidate on live dev `99e4eb6c14462aafa84bb1ac597fd241abc1a240`. This round cross-checks published candidate receipts and the manager statement; it does not independently reconstruct that merge tree. Candidate evidence is distinct from source tree `d2337a49` and from any later final merge tree.

The source area receipt reports 515 LUT / 278 FF for MAAP against 637 / 268, meeting the +40/+40 budget. The source route record is 50,391 LUT, 54,263 FF and 15,788 slices; WNS +0.241 ns and WHS +0.029 ns meet the recorded floors, with complete routing. Standalone records are 23,179/19,779 and 30,135/27,380 LUT/FF. These are published source measurements, not new measurements of the final live-dev candidate.

Artifact-specific lens results

[R549] PASS Conformance - `hdl/ieee1722/maap/KL_maap.sv:114`, `:197`, `:365`; `REQUIREMENTS.md:91`, `:307`; issue acceptance and `clean.run.log` - The four frozen correction items retain clause-based behavior: CDL 16 and unicast DEFEND, strict timer bounds, requested-range ANNOUNCE comparison with the specified MAC ordering, and four PROBEs beginning immediately. Area/route evidence and the post-merge bench assignment remain separate. Declared exclusions are not called full Annex B compliance.

[R549] PASS RTL - `KL_maap.sv:138`, `:200`, `:222`, `:286`, `:370`; `hdl/milan/milan_datapath.sv:7065` - Checked nonzero reset seeding, timer widths, 17-bit range ends, state priority, destination/offset capture, backpressure and unchanged ports/state encoding. No new CDC or CSR interface. Seed documentation matches the shared reset path at `milan_datapath.sv:2465` and `hdl/common/csr/milan_csr.sv:1553`.

[R549] PASS Robustness - `tb/verilator/maap/sim_main.cpp:349`, `:419`, `:443`, `:481`, `:585`; `KL_maap.sv:292` - Applied zero-seed, adjacent/empty-range, unknown-message/version, disable/re-enable and stalled-frame checks. Focused zero-seed and mid-frame guard defects are caught. Live configuration inputs, unbounded transport stalls and incomplete malformed-input coverage remain explicit limits.

[R549] PASS Tests - `tb/verilator/maap/mutants.py:37`, `:99`; `sim_main.cpp:28`, `:571`; `sw/firmware/ctrl/test/test_maap_differential.cpp:115`; `tb/verilator/milan_dp/sim_crf_licence.cpp:842` - Expectations use clause numbers, wire bytes and observed intervals. Measurement budgets exceed graded timer bounds. Zero-seed variability excludes the initial phase transient. Compilation errors cannot count as kills. The consumer probes before allocation and still requires eventual allocation and the original refusal behavior. Source summaries and raw candidate executions retain their population labels.

[R549] PASS Docs - `docs/design/MAAP_FABRIC.md:64`, `:91`, `:134`, `:175`; `docs/design/AREA_BUDGET.md:99`; `docs/reference/FR_NFR.md:167`; `public-decisions.json` - Snapshot and supplied-seed bounds match implementation. Round-3 text distinguishes reset-time module seeding from shipping MAC programming after reset. The repaired manifest verifies; the source-bank correction is explicit. No protocol or measurement claim is waived as wording-only residue.

Prior findings, retaining every attributed lens

| Finding | Severity / lenses | Disposition and evidence at this head |
|---|---|---|
| R549-1-F4 remainder | MAJOR; Conformance, RTL, Tests, Docs | RESOLVED as above. Resource portion remains resolved; the claimed extra source execution is publicly withdrawn. |
| R549-1-F1 = R548-1-F3; former R548 R1 | MAJOR; all five | RESOLVED. `KL_maap.sv:292`, `sim_main.cpp:585`; zero-seed defect caught here. Manager's severity ruling retained. |
| R548-1-F1 | MINOR; Tests, Robustness | RESOLVED. `sim_main.cpp:419` and the guard-removal defect detect mid-frame rewriting; independently rerun here. |
| R548-1-F2 | MINOR; Conformance, Docs | RESOLVED. `MAAP_FABRIC.md:144` distinguishes repeated PROBEs one to three from the fourth's immediate ANNOUNCE and compare_MAC consequence. |
| R549-1-F2 = R548-1-F4; former R548 R2 | MINOR; Docs | RESOLVED. `KL_maap.sv:222`, `MAAP_FABRIC.md:64`, current PR body: source MAC and count remain live. |
| R549-1-F3 = R548-1-F5 | MINOR; Conformance, Docs | RESOLVED. `MAAP_FABRIC.md:50`, `:151`, module page and seed-selection arm distinguish clipped random blocks from unchecked supplied seeds. |
| R548-2-F1 | MINOR; Conformance, Docs | RESOLVED. `MAAP_FABRIC.md:91`, `:134`, `:175` matches reset/CSR wiring inspected here. R549-3's probe result stands. |
| R549-2-F1 = R548-2-E1 | MINOR; Tests, Docs | RESOLVED. 186 public checksums pass at archive `319f3567`; optional provenance annotation remains S3 below. |
| R548-1-S1, S3, S4 | SUGGESTION; Tests/Robustness, Tests, Docs respectively | RESOLVED. Own-empty-range check/control, supporting item 0 excluded from required-item coverage, and refreshed datapath comments remain unchanged. |

Remaining optional suggestions

These retain public severity and all attributed lenses. Their narrower probes were not rerun here.

| ID / severity / lenses | Artifact and authority/evidence | Impact | Required outcome if adopted / verification |
|---|---|---|---|
| R548-1-S2 / SUGGESTION / Tests, Robustness | `KL_maap.sv:353`; prior public truncated-PDU finding | Completion guard lacks comprehensive directed malformed-input evidence | Add truncated-PDU cases; require a guard-removal control to fail. |
| R548-2-S1 / SUGGESTION / Tests, Robustness | `sim_main.cpp:419`; prior public narrow-window probes | Present check covers a mid-frame stall, not every beat-zero/streaming window | Extend both windows; kill their corresponding narrow guard defects. |
| R548-2-S2 / SUGGESTION / Tests, Robustness | `sim_main.cpp:491`; prior state-specific probe | Own-empty-range check runs in PROBE | Repeat in ANNOUNCE, require no DEFEND, kill the state-specific defect. |
| R548-3-S1 / SUGGESTION / Docs | `MAAP_FABRIC.md:100`; public R548-3 | Timing reference point is implicit | Optional exact wording: "Stations differ only by how many axis_clk cycles after axis_resetn release their enable and sends fall." Check against the recurrence. |
| R548-3-S2 / SUGGESTION / Tests | `milan_datapath.sv:7065`, crflic harness; public R548-3 seed probe | Integration seed source is not pinned by a permanent check | Add the shadow-LFSR comparison in the seed-timing follow-up; reject the MAC-at-reset control. |
| R548-3-S3 / SUGGESTION / Docs | Archive `MANIFEST.json`, entry for `author-r2/resource-receipts/MANIFEST.sha256`; public R548-3 | Superseded hash is recoverable through history rather than an explicit correction annotation | Record the superseded hash or manager-correction note; verify provenance and retain passing published-byte checksums. |

Reviewer-owned completion ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue 686 frozen scope; REQUIREMENTS.md:91,307; KL_maap.sv:114,197,365; clean.run.log; source gate table and resource records; correction 6052220964 | R549-4 | 9c601b5983acfd60fb269b9a88c27b48cab7cf65 |
| RTL | CLEAN | KL_maap.sv:138,200,222,286,370; milan_datapath.sv:2465,7065; milan_csr.sv:1553; checkout-integrity.json; candidate integrity and resource records | R549-4 | 9c601b5983acfd60fb269b9a88c27b48cab7cf65 |
| Robustness | CLEAN | sim_main.cpp:349,419,443,481,585; clean and selected defect logs; KL_maap.sv:200,292; retained optional suggestions | R549-4 | 9c601b5983acfd60fb269b9a88c27b48cab7cf65 |
| Tests | CLEAN | mutants.py:37,99; sim_main.cpp:28,571; test_maap_differential.cpp:115; sim_crf_licence.cpp:842; focused-results.json; evidence-audit.json; hosted execution steps | R549-4 | 9c601b5983acfd60fb269b9a88c27b48cab7cf65 |
| Docs | CLEAN | MAAP_FABRIC.md:64,91,134,175; AREA_BUDGET.md:99; FR_NFR.md:167; public PR/decisions; repaired receipt manifest and source/candidate attribution | R549-4 | 9c601b5983acfd60fb269b9a88c27b48cab7cf65 |

Limits and pending manager duties

The focused campaign used four concurrent builds, four compiler jobs each, under the 16-job ceiling. Commands remained foreground executions. No full bank, synthesis, implementation, local workflow replica, hardware operation, source fix, commit, push, GitHub write or merge was performed. The original 26-case campaign, differential, coverage and round-3 integration probe were not all rerun; their prior results stand. Current raw focused receipts cover one clean control and five selected defects only.

The byte audit verifies 1,187 root blobs and 880 required-submodule blobs, modes and complete index entries against their commits. Required gitlinks are protocol processor `2ad2f845`, gPTP processor `5dce647a`, and stream library `48ff7a7e`. Source bytes were never edited, so no restoration was needed.

Scaled unit-clock results do not prove bounded wire timing under arbitrary backpressure. Existing frozen deviations remain: B.3.6.1 generator/seeding, the two other compare_MAC cells, DEFEND requested-field echo, PortOperational, busy-frame PROBE loss, tagged reception and supplied-seed validation.

The manager still owns final current-dev candidate gates and applicable resource re-baseline, exact-head hosted/local-replica acceptance, both independent reviews and absence of in-flight rounds, maintainer merge authorization, post-merge containment, public follow-up decisions and assigned bench interoperability. Physical calibration is NOT RUN; field skips do not clear hardware acceptance. This review closes F4's evidence demand, not these duties.

Portable reproduction and publication

```sh
python3 focused_checks.py <exact-head-checkout> <pinned-compiler> --jobs 16
python3 evidence_audit.py <exact-head-checkout>
python3 public_snapshot.py
python3 checkout_integrity.py <exact-head-checkout>
sha256sum -c MANIFEST.sha256
```

The evidence audit requires the two named public archive commits locally. The public snapshot uses read-only repository API calls. `MANIFEST.sha256` lists publishable scripts and receipts relative to this packet; REPORT.md is published alongside them. Scratch builds and unlisted material are excluded.

R549-4 FINISHED
