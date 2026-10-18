[R645] POSITIVE - exact head 26ddcba423a204e75238d737ef41e6cb6e30ebc3

Tree `c3f5e8f17caa9dcb64093b01b6ac988c11fe9400`. Processor PR #183, Refs #176. All five lenses are CLEAN for this source review. Both external round-1 findings and both named internal round-1 items are closed. No BLOCKER, MAJOR or MINOR remains. One PR-history wording residue is recorded below; it does not change the verdict. This is not final parent-candidate acceptance.

**Scope and independence**

The processor checkout has no AGENTS.md or CONTRIBUTING.md. The supplied operating instruction, processor README, docs/README, issue body and public scope decisions were examined before the diff. REQ-AEM-009, architecture 01/02/06/07/09 and the HDL consumption contract supplied the relevant interface and behavior authorities. The public parent operating documents at `e9cbb676` were consulted later for parent adoption and publication rules; this was a supplemental read, not the initial processor reconstruction.

The independent pass covered `77cf6fb4..26ddcba4`, the author delta `e59804d8..bee33ff2`, and merge history. The independent verdict and five-lens ledger were written in `receipts/independent-verdict.md` before reading either prior public FINDINGS report. Only then were the [external findings](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/183#issuecomment-6243715823) and [internal findings](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/183#issuecomment-6244122972) reconciled. No current-round report from another reviewer was read. No private author material or management source bank was accessed.

The frozen authority is [issue #176](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/176), its [original assignment](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/176#issuecomment-6236134563), the [length ruling](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/176#issuecomment-6243713960), and the [round-2 assignment](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/183#issuecomment-6244127636). The exact-length rule is explicit project acceptance. Its cited clause baseline is IEEE 1722.1-2021 7.4.15.1 / Figure 7-40, IEEE 1722.1-2013 Figure 7.46, and Milan v1.2 5.4.2.9. The final copyrighted specification PDFs are absent from the checkout. This review does not claim a new verbatim examination of those PDFs or the compatibility NOTE.

**Behavior and merge findings: clean**

`hdl/aecp/KL_aecp_engine.sv:803`, `:1562`, `:1570`, `:3624`: both recognition predicates require SET_STREAM_INFO, exact cdl, and exact available payload length. Only 60/48 and 96/84 qualify. Every other shape reaching this command handler selects SIBAD and disables echo before type, streaming, flags or latency are judged. `hdl/aecp/ucode/gen_ucode.py:2356` builds status BAD_ARGUMENTS, cdl 96, with type/index over an otherwise zero body. It has no write, persistence-mark or notification instruction.

The accepted forms share their existing semantics and order: output direction, streaming refusal, MSRP_ACC_LAT_VALID alone, latency bit 31 refusal, then lock and descriptor existence. `A_RUN` at engine `:3775` lengthens only the legacy echo; `frame_byte` at `:2585` zeroes only its bytes @70..@107. The 2021 IP fields remain byte-exact. The latency capture settles before either accepted payload walk completes. The new predicates are combinational; no port, public parameter, register map, clock/reset domain or state register changes. Command discrimination confines the shared response-mux change. Upstream rejection of incomplete transport frames remains unchanged; the all-other-length rule concerns commands delivered to this handler.

The merged GET_AVB_INFO block at engine `:3423` and SET_CONFIGURATION block at `:3547` are byte-identical to processor main `77cf6fb4`. SET_STREAM_INFO's dispatch block is byte-identical to author head `bee33ff2`. The microprogram generator's executable syntax tree is identical to `77cf6fb4`; changes there are comments. The merge re-resolution has one conflict only, in `tb/aecp_cmds/decode.json`'s engine digest. The #177 NOT_IMPLEMENTED record change is inherited from main, not a conflict repair or a SET_STREAM_INFO change. The exact-head executable sweep agrees with the merged record, including both command families. See `receipts/artifact-audit.json`, `merge-resolution.diff`, and `aecp_cmds-run.log`.

**Prior findings: closed at this head**

| ID / original severity | All attributable lenses | Cause, required outcome and closure evidence |
|---|---|---|
| R645-1-F1 (original report R645-F1), MAJOR | Conformance, RTL, Robustness, Tests, Docs | CLOSED. The former lower-bound-only recognition is replaced by the exact predicates above. The public ruling requires rejection of every other length at cdl 96 without applying the offset. Independent exact-head probes below verify both boundaries and longer bodies, including write/mark/notification silence. W24n/W24n1 and W24o/W24o1 at `tb/pp_top/sim_main.cpp:8367` cover valid-flag cdl 97/140 with byte-exact refusals and unchanged published offset. M45 changes both `si21_w` comparisons to >=; its published result fails those four checks by name, with seven total failures. `decode.json:87`, `tb/aecp_cmds/sim_main.cpp:311`, architecture 06 `:261`, `:493`, `:1260`, and the PR's What changes/Acceptance now state the same contract. The previous oversized success and oversized response impact is removed. |
| R645-1-F2 (original report R645-F2), RESIDUE | Docs | CLOSED. The exact comment-anchor correction is present at engine `:803`, `:1562`, `:2582`, `:3603`, `:3773` and top bench `:8176`, `:8297`, `:8367`, `:8447`. New behavioral anchors carry issue #176 and REQ-AEM-009, and newly introduced row-navigation prefixes are removed. Executable names and assertion strings remain. The added-source-comment audit found no forbidden navigation/review labels. This was comment-only residue and never independently dirtied a lens. |
| R644-1-F1, MINOR | Tests | CLOSED. `tb/pp_top/sim_main.cpp:8231` fills payload bytes 46..83, corresponding to PDU @70..@107, with a nonzero pattern and compares the complete 2021 response byte-for-byte (W24a3). The exact-head focused run passes it. M46 widens `si13_pad_w` from `si13_w` to `ssinfo_r`; the published result fails W24a3 alone, one failure in 10,004 checks. M45/M46 are recorded beside M38-M44 at `tb/pp_top/README.md:1051`. Their patches apply to this exact head without alteration. The formerly surviving widened-padding error is now detected. |
| R644-1-R1, RESIDUE | Docs | CLOSED. `docs/architecture/09_verification.md:184` now says W24h-W24m, including the legacy input refusal. This is the requested exact coverage-label correction; no check or measurement changed. |

The M45/M46 failure evidence is author execution at `bee33ff2`, not a new reviewer mutation campaign at `26ddcba4`. The mutant sites and affected assertions survive the merge unchanged, both patches pass exact-head applicability checks, and the exact-head positive controls passed. That is sufficient to retain the published mutation evidence without repeating the campaign.

**Independent executable receipts**

The scoped compiler identity was verified as release 5.050 before use. Two bounded builds ran concurrently in a foreground orchestrator, with eight inner workers each and `make -j16`. All disposable sources and builds remained under this packet's `scratch/`; the original checkout was untouched. No full processor/parent bank, hardware run, shared installation or remote write was performed.

| Check | Result / receipt |
|---|---|
| Existing W24 on a booted, stopped-output fixture | Setup plus W24: 29 checks, zero failures. Includes both forms, legacy refusals, nonzero 2021 IP echo and cdl 97/140 refusals. `receipts/pp_top-run.log` |
| Independent boundary/effect probe | Nine lengths below; complete frame equality, offset state and rejected-command write/mark/notification silence all pass. Same receipt; probe source in `scripts/run_focus.py` and `receipts/focus-bench.diff` |
| GET_AVB_INFO dispatch cases | Existing `AvbInfoPhase::dispatch_cases()` runs after the boundary probe; final focused result zero failures. Same receipt |
| Exact-head command sweep | 617,908 trials, zero timeouts; 176/176 checks pass. `receipts/aecp_cmds-run.log`, `observed.json` |
| Command/doc consistency | 31 commands, 84 entries, F06.14 41 rows, pass. `receipts/command-doc-check.log` |
| Command/doc negative controls | 231 planted defects, all caught by name. `receipts/command-doc-selftest.log` |
| Dispatch/microprogram map | 61 engine constants, 90 entry points, pass. `receipts/upc-check.log` |

| Input cdl | Status | Response cdl | Offset after command | Dynamic writes |
|---|---|---|---|---|
| 59 | BAD_ARGUMENTS | 96 | 1000000 | 0 |
| 60 | SUCCESS | 96 | 600060 | 1 |
| 61 | BAD_ARGUMENTS | 96 | 600060 | 0 |
| 95 | BAD_ARGUMENTS | 96 | 600060 | 0 |
| 96 | SUCCESS | 96 | 600096 | 1 |
| 97 | BAD_ARGUMENTS | 96 | 600096 | 0 |
| 100 | BAD_ARGUMENTS | 96 | 600096 | 0 |
| 140 | BAD_ARGUMENTS | 96 | 600096 | 0 |
| 511 | BAD_ARGUMENTS | 96 | 600096 | 0 |

The first disposable probe build failed on an unqualified helper in the reviewer-added entry point. Qualifying that helper corrected the harness; no product source changed. The final build and execution receipts are rc 0. Host-specific build transcripts are excluded from publication; `build-provenance.json` records their hashes. Runtime receipts are unfiltered. Reproduction: `python3 scripts/run_focus.py <exact-head-clone> <packet-directory>`, then `python3 scripts/audit.py <exact-head-clone> <packet-directory>`.

**Published evidence and its limits**

The [public evidence package](https://github.com/kebag-logic/milan-fpga/tree/3f760c40cce2aa4b6d4478237376722483eebac5/review-evidence/pp176-r1) was read after the independent diff pass. All 27 author-r2 files match MANIFEST.json's published SHA-256 values. The boundary probe, both new mutant patches, named failure lists and source/parent gate tables were inspected by section. The source index contains 611 records; selected return-code hashes agree with the reported zero results and known parent pin-documentation failure. Digest indexes and summarized receipts are not a substitute for unavailable complete logs, so no byte-identical full-bank-log claim is made.

The package is hash-verifiable, but no cryptographic signature envelope is supplied. The public API marks both the evidence commit and reviewed source commit unsigned (`receipts/evidence-provenance.json`). Thus no claim of verified signing is made.

Author source-gate evidence is for merged author base `e59804d8` and author head `bee33ff2`: 1,029,982 / 1,029,987 suite checks, no failures; 41 lint targets; documentation and matrix gates; portability; and published relevant mutation campaigns. This is author evidence, not a manager source bank at the published merge head. The reviewer executions above cover the exact published head. The public issue/PR snapshots contain the scope rulings, assignments and review starts; no manager exact-head source-bank receipt was present or inferred.

At 2026-10-18 10:49:46 UTC, exact-head hosted runs [39120107221](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/actions/runs/39120107221) and [39120103675](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/actions/runs/39120103675) each had completed successful docs-gates and portability jobs, with suites still in progress. No listed job was skipped. This is a snapshot, not all-green hosted acceptance. `receipts/hosted-summary.json` preserves the job/step distinction. Hosted and local workflow acceptance belongs to the manager.

**Parent adoption**

The unchanged `parent-adoption-milan_dp-67.patch` hashes to `e142e2e7d7aec88fdc0bb7b6443d296f671f06391712b214339a50b84acc66d3` and applies to public parent `e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f`. Its only file is `tb/verilator/milan_dp/sim_nxn.cpp`, section #67: send the already-stored 750000 in the legacy command and expect SUCCESS at cdl 96. The following offset-preservation assertion remains meaningful. This is the sole issue-176 parent behavioral patch.

The author also applied the inherited PR #180 evidence-classification patch in the scratch parent. Its three classified readers came from processor main; it is not another #176 behavior change. Published removal controls identify exactly which checks need each patch: without #67, the legacy-status and following offset rows fail; without classification, three unexplained reader entries fail. With both, 22/23 consumer gates are reported rc 0 at both author revisions; pin documentation remains the known failure. The builder report retains one NOT RUN gate. These are source-consumer receipts, not validation of the manager's final candidate.

Carry the previously identified parent prose cleanup into adoption: `tests/steps/aecp_engine_steps.py:189` still describes the legacy body as truncated, and `tb/verilator/milan_dp/sim_nxn.cpp:6862` still says Milan refuses it. Replace those inherited explanations with the accepted-two-length contract and the unchanged cdl-96 refusal of the sweep's cdl-20 input. They are outside this processor delta; they must not be silently treated as current behavior after the parent pin moves.

**Remaining finding**

R645-2-R1 | RESIDUE | Docs | PR #183 opening branch-history paragraph.

Evidence: the current body still introduces “three commits on main f0b1b9d8” and ends its opening list at bee33ff2. The published review head now also includes merge 26ddcba4 from main 77cf6fb4. This is a stale introductory history description; the detailed author gate tables correctly name their author revisions and must retain those names.

Impact: readers must reconstruct the additional merge from the commit list. No measured result, code, test, generated artifact, clause claim or acceptance verdict changes. Exact correction: introduce the three listed commits as the author revision through bee33ff2, then add: “Published review head 26ddcba423a204e75238d737ef41e6cb6e30ebc3 merges processor main 77cf6fb4; the author gate receipts below remain scoped to e59804d8 and bee33ff2.” Verification: compare that prose with the public commit parents, without relabeling any receipt as an execution at 26ddcba4. The manager may carry this to the residue checklist.

**Reviewer-owned final ledger**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Frozen issue/ruling; REQ-AEM-009; engine :1562/:1570/:3624; 06 :261/:493/:1260; byte-exact boundary receipts. Exact lengths, fixed response and field semantics agree. | R645-2; unaffected R645-1 scrutiny retained | 26ddcba423a204e75238d737ef41e6cb6e30ebc3 |
| RTL | CLEAN | Engine recognition, payload walk, frame_byte :2585, A_RUN :3775; SIBAD/SINFO; merged GET_AVB_INFO and SET_CONFIGURATION arms; executable generator equality; map gate. No new sequential/interface change. | R645-2; unaffected R645-1 scrutiny retained | 26ddcba423a204e75238d737ef41e6cb6e30ebc3 |
| Robustness | CLEAN | Exact-head boundary/effect probes 59..511; cdl 12..100 observed record; legacy tail isolation; published streaming, invalid-value and missing-target checks. Upper lengths cannot enter the setter. | R645-2; unchanged reset/stall/ordering scrutiny retained from R645-1 | 26ddcba423a204e75238d737ef41e6cb6e30ebc3 |
| Tests | CLEAN | W24a3/W24n/o; M45/M46 patches and named failures; M38-M44 retained controls; exact-head sweep and W24 execution; 231 command/doc controls. Both previously missing falsifiers are present. | R645-2; unchanged controls retained from R645-1 | 26ddcba423a204e75238d737ef41e6cb6e30ebc3 |
| Docs | CLEAN | docs README; 06/09 changed contracts; command/field registries; bench READMEs; PR acceptance; source-comment scan. Prior residues corrected; R645-2-R1 is nonblocking history wording only. | R645-2; unaffected R645-1 scrutiny retained | 26ddcba423a204e75238d737ef41e6cb6e30ebc3 |

**Limits and pending manager duties**

No full source bank was rerun by this reviewer. Unchanged reset, backpressure, timeout, lock and streaming coverage keeps its earlier reviewed basis; the delta and its dependencies were rechecked. Physical calibration: NOT RUN. Field skips and simulated/hosted successes are not hardware proof.

The manager must obtain both independent positive source reviews, finish hosted/local-workflow acceptance, build the final current-dev candidate, run builder and native candidate banks, and publish those receipts on the PR. Source base is `77cf6fb4`; the stated live parent dev is `e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f`. Parent pin adoption must include #67, inherited classification, current pin documentation/diagram and the inherited prose cleanup above. This source verdict does not close #176 by itself.

Final checkout audit verifies all 632 tracked entries against raw committed blob bytes, file modes and the stage-zero index. HEAD/tree match exactly; status is clean. This standalone processor has no submodule gitlinks, so there are no nested required pins to restore; no parent checkout or pin was edited. MANIFEST.sha256 lists every publishable receipt and script. Scratch content is excluded.

R645-2 FINISHED
