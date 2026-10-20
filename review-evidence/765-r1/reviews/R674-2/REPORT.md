[R674] POSITIVE - exact head d4a27e6334118c9eef1023aa27e9fd2b7de9f076

External independent review, R674-2, issue #765 / PR #769. Tree `a78b680bc9ffdbd43e25035ed8ece9e6b746d839`. All five lenses were applied to the round-two delta. R673-1-F1 and R673-1-F2 are resolved at their causes. R674-1-RES1 is resolved. No new BLOCKER, MAJOR, MINOR or RESIDUE was found. The three previously recorded optional suggestions remain open and do not prevent clean coverage. This is a source review verdict, not merge authorization or hardware qualification.

Scope and reconstruction

The review followed AGENTS.md and CONTRIBUTING.md, docs/README.md, [issue #765 and its public scope decisions](https://github.com/kebag-logic/milan-fpga/issues/765), the linked requirement and interface authorities, then the stacked comparison and history, then public execution evidence. The [round-two assignment](https://github.com/kebag-logic/milan-fpga/pull/769#issuecomment-6298037023) selects F2 option (a): retain the flat instrument's family comparison and explain its distinction from the device listener. It excludes S1-S3 and RTL logic changes.

The recorded comparison is `4191b098..d4a27e6334118c9eef1023aa27e9fd2b7de9f076`; the reviewed delta is `75db4b57cff47bb614d14dead084649a4c2aa2a3..d4a27e6334118c9eef1023aa27e9fd2b7de9f076`. Its three commits are `059ecec1e`, `11119970c` and `d4a27e633`. They change five files. Unchanged artifacts retain R674-1 coverage at `75db4b57cff47bb614d14dead084649a4c2aa2a3`. No earlier implementation findings were silently reopened as new delta work.

The independent conclusion and artifact-specific ledger were written in `independent-pass.md` before opening prior review findings. The subsequent reconciliation read the public R673-1 findings and R674-1 residue/ledger. No other round-two report was read. The PR has no additional review bodies or inline review comments in the fetched public snapshot.

Authorities used for this delta are FR-STR-03 (`docs/reference/FR_NFR.md:271`), the live compliance row (`docs/reference/MILAN_COMPLIANCE_MATRIX.md:190`), the architecture's media-path boundary and the integration contract. The unchanged clause interpretation is carried from R674-1: Milan v1.2 4.4.2.2, Tables 5.6/5.16 and 6.2; IEEE 1722-2016 7.3 and I.2.4/I.2.4.1. This round does not claim a fresh independent reading of the full standards PDFs. The frozen issue and assignment explicitly specify the current-format comparison, including channels; no new clause interpretation is introduced.

Prior findings and suggestions

| ID | Original severity and all recorded lenses | Disposition at this head |
|---|---|---|
| R673-1-F1 | MINOR; Docs, Tests, Conformance | RESOLVED. `tb/verilator/avtp_rxmon/reference/KL_avtp_rx_monitor_ctx_ref.sv:493` now states the subtype, encoding, rate, depth, full 10-bit channel comparison, nonzero count and nonsparse requirement. It cites #765 and Milan v1.2 4.4.2.2, Table 5.6 and Table 6.2. Lines 502-510 implement those terms; the claim that channels_per_frame is absent is removed. |
| R673-1-F2 | MINOR; Docs, Tests, Conformance | RESOLVED by assigned option (a). `hdl/ieee1722/avtp/KL_avtp_rx_monitor.sv:182`, `tb/verilator/avtp_rxmon/sim_main.cpp:246,433,460,472`, and `tb/verilator/tsn_fuzz/fuzz_aaf.py:141,175` distinguish intentional flat family acceptance from the device listener's current-format rejection. The section and five labels in `hdl/ieee1722/avtp/doc/TEST_RESULTS.md:29,96` follow the corrected generator. The current PR known-limitations paragraph makes the same distinction. No check or expectation was weakened. |
| R674-1-RES1 | RESIDUE; Docs | RESOLVED. The current PR Contents separators use ` - `; the entire fetched PR body contains no U+2014. Labels, links and purpose remain intact. |
| R673-1-S1 | SUGGESTION; Tests | RETAINED, optional and unassigned. Add a shipped-context subtype rejection case and its mutant if this follow-up is taken. |
| R673-1-S2 | SUGGESTION; Tests | RETAINED, optional and unassigned. Add the zero-count-current-format boundary and its mutant if this follow-up is taken. |
| R673-1-S3 | SUGGESTION; Tests | RETAINED, optional and unassigned. Align the shipping-shape acceptance stimulus length or accurately name the header-only check, and correct its stale diagnostic text if this follow-up is taken. |

The resolved findings' verification is substantive: the changed reference comment was checked against its comparator and the production comparator; the flat campaign's actual wrapper instantiates `KL_avtp_rx_monitor`; and the generated artifact's section/check identities match the campaign. Published exact-head lockstep results are 116/0 at N=1 and 119/0 at N=8, with 14/14 mutation controls. Flat results are 97/0, with AAF 164/0 and final-head freshness PASS. The published static/docs ledger includes `docs_check.py` at rc 0.

The retained suggestions preserve their original severity and lens; they are not downgraded findings. Their complete dispositions are:

- **R673-1-S1; SUGGESTION; Tests; `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:522`.** Authority/evidence: FR-STR-03 and issue #765 require current-format rejection; the prior public finding records that removing the subtype term survives the N=4 harness. Impact: that pre-existing term lacks an engine-level discriminating case. Optional required outcome: an AAF-input subtype mismatch case on the shipped context path, with a matching control. Verification: removing the subtype term must fail the named new assertion while the clean engine passes. The relevant sources are unchanged this round; the prior mutation was not rerun.
- **R673-1-S2; SUGGESTION; Tests; `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:521,527`.** Authority/evidence: the source explicitly rejects a zero channel count even against itself; the prior public finding records that deleting the nonzero term survives the existing harness. Impact: the zero-current-format boundary lacks discriminating coverage. Optional required outcome: test zero PDU count against zero current count. Verification: the clean engine rejects it and a removed nonzero guard fails the named assertion. Sources and existing tests are unchanged; the prior mutation was not rerun.
- **R673-1-S3; SUGGESTION; Tests; `tb/verilator/milan_dp/sim_main.cpp:1252,1371,1531`.** Authority/evidence: the shipping shape declares eight channels while this header-focused stimulus retains a 48-byte payload; the prior finding records the misleading whole-PDU label and stale two-channel diagnostic. Impact: the stimulus is useful for header acceptance but does not prove whole-sample-frame conformance. Optional required outcome: use a whole-frame payload or name the test for its actual scope, and correct the diagnostic. Verification: preserve the acceptance assertions and check the selected shape's payload geometry and printed description. This file is unchanged by the round-two delta.

No new source comment contains a bench label, lane name, review round, reviewer ID or issue-comment ID. Existing identifiers outside the delta were not relabelled as new residue.

Independent lens results

[R674] PASS Conformance - `tb/verilator/avtp_rxmon/reference/KL_avtp_rx_monitor_ctx_ref.sv:493`, `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:499`, FR-STR-03 and assignment item 1 - the new explanation matches the configured-format comparator, including both 10-bit slices. The flat instrument is explicitly distinguished at every assigned location; it is no longer offered as the device listener's Milan rule.

[R674] PASS RTL - `round2.diff`, `delta-check.log`, both changed `.sv` files - comment-stripped executable tokens are identical to the reviewed round-one head. Production context/CRF RTL, module interfaces, clocks, reset behavior, state transitions, parameter definitions and submodule gitlinks do not change. Prior RTL coverage therefore carries forward without a new route or broad bank.

[R674] PASS Robustness - `tb/verilator/avtp_rxmon/sim_main.cpp:460`, `sim_main_nx.cpp:902`, `format_mutants.py:40` - the flat zero-count rejection and family probes retain their expectations. The unchanged shipped-context cases retain matching acceptance, channel mismatch rejection/discard, the 264-versus-8 high-bit boundary, sequence recovery, LCTX reconfiguration and fmt0_i behavior. No delta changes the reset, malformed-input, ordering, backpressure or timeout machinery on which prior coverage depends.

[R674] PASS Tests - `check_delta.py`, `delta-check.log`, `published/author-r2/receipts/r2-rxmon/`, `r2-tsnfuzz/` - C++ stimulus/check expressions are unchanged after accounting for the single banner and check-label edits. Python AST comparison is identical after explicitly normalizing the renamed method, its docstring, the section title and label text. The call site uses the new method. Existing mutation expectations remain unchanged and the published exact-head runs pass. This round used bounded equivalence and receipt checks rather than repeating unchanged campaigns.

[R674] PASS Docs - all five files in `round2.diff`, the PR known limitations, `published/author-r2/receipts/r2-regen/`, `freshness-spotcheck.log` - F1/F2's misleading clause interpretation is removed. Generator output changes only the section title, five accepted-check labels and timestamp; 20 channel-section checks and 164 total passes remain unchanged. PR limitations agree with the source/campaign distinction. Prior house-style residue is corrected.

Public execution evidence and provenance

The immutable [publication at bf51200d](https://github.com/kebag-logic/milan-fpga/tree/bf51200d95edd1d371b269f6e3b459036dc2d891/review-evidence/765-r1) supplies the source-head evidence. `fetch_receipts.py` downloaded 70 selected execution receipts from `author-r2/receipts/r2-{rxmon,tsnfuzz,static,builder,regen}` and checked each against `MANIFEST.json`'s `published_sha256`, allowing the publication's declared path redaction. All 70 match. No private author notes or handoff were read.

| Published receipt group | Observed result and attribution |
|---|---|
| `r2-rxmon/HEAD.txt`, `rc`, `make_run.log` | Exact `d4a27e63`; rc 0; flat 97/0, NX 147/0, lockstep 116/0 and 119/0, lockstep mutation controls 14/14, format mutation controls 6/6. |
| `r2-tsnfuzz/HEAD.txt`, `rc`, `tsnfuzz.log` | Exact `d4a27e63`; CI oracle pin `deca300c9eb4863fa13383b45ba6cb6fd0828671`; rc 0; grader 54/0, AAF 164/0, gPTP 677/0, both freshness checks PASS, traceability 2/0. These are executed campaign receipts, not skipped contexts. |
| `r2-static/HEAD.txt`, `gates.tsv`, individual logs | Exact `d4a27e63`; 34 rows at rc 0, including docs and delta whitespace checks. |
| `r2-builder/HEAD.txt`, leg receipts and union | Author's exact-head bank; leg and union rc 0, 103 named gates accounted exactly once. Resource-calibration gate 11 has a NOT RUN arm because the historic report is absent. The union explicitly excludes that arm from its coverage. This is not a manager source bank or physical calibration proof. |
| `r2-regen/` | Generation occurred on `75db4b57` with the disclosed uncommitted round-two edits. The record was absent from the before-status modifications and present afterward. The AAF campaign produced 164/0; make returned 2 because freshness correctly rejected the old committed section/labels. Final-head `r2-tsnfuzz` then passed freshness with the new record committed. The initial refusal is not represented as a green gate. |

A signed-packet claim cannot be authenticated from this publication: the public commit-verification response says `verified: false`, `reason: unsigned`, with no signature or payload, and the manifest lists no detached signature. This review verifies immutable-publication hash consistency, not a signer identity. That evidence limitation does not create a source defect or replace any manager acceptance requirement.

The reviewer executed `check_delta.py`, `audit_evidence.py`, `verify_tree.py`, `git diff --check 75db4b57 HEAD`, and the repository freshness checker against the published exact-head campaign log and the checked-out artifact. All final checks passed. The freshness spot-check confirms internal consistency of the supplied log/artifact; it is not represented as a new simulated campaign or proof of the historical editing process. The generation receipts and final freshness run support the regeneration claim. No fault probe was necessary to resolve these text-only findings.

Reviewer-owned coverage ledger

Each row incorporates unchanged R674-1 coverage at `75db4b57cff47bb614d14dead084649a4c2aa2a3` and the delta application described above. F1/F2's affected lenses are re-covered at this head; no open MINOR is banked as clean.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | FR_NFR:271; compliance matrix:190; production context:499-528; reference:493-510; flat monitor:182-196; campaign:141-189; PR limitations | R674-2, incorporating unchanged R674-1 scope | d4a27e6334118c9eef1023aa27e9fd2b7de9f076 |
| RTL | CLEAN | Both changed SV files; `round2.diff`; unchanged production context/CRF and datapath interfaces; `delta-check.log`; `tree-verification.log` | R674-2, incorporating unchanged R674-1 scope | d4a27e6334118c9eef1023aa27e9fd2b7de9f076 |
| Robustness | CLEAN | flat harness:460-477; NX harness:902-999; format_mutants.py; unchanged reject/reset/boundary paths; published exact-head focused results | R674-2, incorporating unchanged R674-1 scope | d4a27e6334118c9eef1023aa27e9fd2b7de9f076 |
| Tests | CLEAN | C++/Python equivalence checks; r2-rxmon/r2-tsnfuzz receipts; campaign Makefile:201; cosim.py:135; freshness check; S1-S3 retained as optional | R674-2, incorporating unchanged R674-1 scope | d4a27e6334118c9eef1023aa27e9fd2b7de9f076 |
| Docs | CLEAN | all changed comments/banner/campaign text; generated TEST_RESULTS:29,96; public PR snapshot; r2-regen provenance; r2-static docs receipt | R674-2, incorporating unchanged R674-1 scope | d4a27e6334118c9eef1023aa27e9fd2b7de9f076 |

Integrity, reproduction and limits

`verify_tree.py` independently hashed raw tracked bytes and checked filesystem modes, every stage-zero index entry and pinned submodule identities, with replacement objects disabled. It passed for 1,423 superproject blobs and all five populated submodules. The four required pins are protocol-processor `2cbed0a987c1e68402658d69459ab7e5aa571adc`, gptp-processor `e4869fd0c42889b2ac806587cc5c78afb1c33461`, verilog-axis `48ff7a7e2ef782cf778d47910cf85835c64b1bce`, and tsn-c-stack `70936b77dc41981e192438388cd0aced69954f18`. Optional lwSRP was also checked; optional external remains uninitialized with its gitlink intact. No tracked source bytes were changed, so no restoration was necessary.

Portable checks: from the candidate clone, run `python3 <packet>/check_delta.py .`, `python3 <packet>/verify_tree.py .`, and `python3 <packet>/audit_evidence.py`. The latter reads only the included published receipts and snapshots. `fetch_receipts.py` can retrieve the same immutable public files again. The freshness command is `python3 scripts/check_results_fresh.py --log <packet>/published/author-r2/receipts/r2-tsnfuzz/tsnfuzz.log --artifact hdl/ieee1722/avtp/doc/TEST_RESULTS.md --label hdl/ieee1722/avtp/doc/TEST_RESULTS.md`. Receipt hashes and the report are enumerated in `MANIFEST.sha256`; `scratch/` is excluded.

No full parent, processor, gPTP, synthesis or builder bank was run by this reviewer. No route, hardware, Docker/local workflow replica, source fix, commit, push or GitHub write was performed. The scoped compiler identity was checked as 5.050, but no new compiled result is claimed. Physical calibration is NOT RUN, and field skips and desk simulation do not prove hardware compliance. Prior known limits remain: the pruned short-frame depacketizer window, input formats above zero supplied through LCTX, and samples_per_frame lacking a comparable PDU field.

The manager still owns hosted/local-workflow acceptance, including distinguishing executed jobs from skipped contexts; completion of the other independent round; final current-dev candidate construction and builder/native validation with published receipts; any current-base integration decision; and authorized merge plus post-merge containment. Source base `4191b098`, reviewed source head `d4a27e63`, and the final candidate are distinct. The assignment identifies live dev `78ca9bdf104819265588726bce4322696c38b8c2`; the manager must validate against the live tip at the merge turn. No manager source bank at this exact head is claimed or inferred. This report does not clear those pending duties or close the issue.

R674-2 FINISHED
