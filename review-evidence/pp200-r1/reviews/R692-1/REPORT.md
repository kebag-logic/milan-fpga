[R692] POSITIVE - exact head 33d3010cea8e053b1d2e83bcd9fa02f3f57d3f33

Issue #200 / PR #201, round R692-1. No findings: no open BLOCKER, MAJOR, MINOR, RESIDUE or SUGGESTION. All five lenses are clean for this source delta. This verdict is not final merge acceptance.

Reviewed base: 93fb0b2d736b36588ea7321e25fba2f8819ea41f. Reviewed tree: 1279c09f5b690c5e94969036baa57ccfa99eccf8. The published PR metadata and isolated checkout agree. One commit changes 19 paths. The final integrity check verifies all 704 tracked file blobs and executable modes, the index, HEAD and tree; the checkout is clean. This processor repository contains no submodule gitlinks. All probe edits and generated builds are confined to packet scratch directories.

The reconstruction followed the requested order: supplied AGENTS instructions and their referenced rules; repository contribution-instruction search (no tracked AGENTS.md or CONTRIBUTING.md); docs/README and repository/HDL guides; [issue #200](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/200) and its [assignment](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/200#issuecomment-6379943177); [issue #177](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/177), [PR #182](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/182), linked requirements and interface authorities; independent diff and history inspection; then the [published source evidence](https://github.com/kebag-logic/milan-fpga/tree/36defd6f727ac4de59d129e99c0f71188b3cdf42/review-evidence/pp200-r1). No private author material or another reviewer's report informed the independent verdict.

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #200 and assignment; #177/#182; IEEE 7.4.40, 9.3.5.3.3, Table 7-141; Milan 5.4.2.2/.9/.23; engine dispatch; V5 and boundary probes | R692-1 | 33d3010cea8e053b1d2e83bcd9fa02f3f57d3f33 |
| RTL | CLEAN | KL_aecp_engine.sv; E_NSUPPE/E_NOTIMPL/E_GAVB; command model; base/head ROM generation; sole executable change check; published area receipts | R692-1 | 33d3010cea8e053b1d2e83bcd9fa02f3f57d3f33 |
| Robustness | CLEAN | Length/type/existence ordering; full-width type comparison; RX-slot echo path; ten dispatch mutants; 32 boundary probes | R692-1 | 33d3010cea8e053b1d2e83bcd9fa02f3f57d3f33 |
| Tests | CLEAN | make check; fresh decode sweeps and standing control; dispatch campaign; published source campaigns, suites and parent consumer receipts | R692-1 | 33d3010cea8e053b1d2e83bcd9fa02f3f57d3f33 |
| Docs | CLEAN | docs/README; compliance row 14; F06.14 regeneration; 06 §§6.10/8.1; 09 verification; both bench READMEs; PR body; changed source comments | R692-1 | 33d3010cea8e053b1d2e83bcd9fa02f3f57d3f33 |

Conformance evidence: the local IEEE 1722.1-2021 text was read at §7.4.40, §9.3.5.3.3 and Table 7-141, and Milan consolidated v1.2 at §5.4.2.2, §5.4.2.9 and §5.4.2.23. Table 7-141 distinguishes an unimplemented command type (1) from an implemented command with an unsupported target (11). Milan requires GET_AVB_INFO implementation; IEEE identifies AVB_INTERFACE as its target. The two Milan comparison clauses independently use NOT_SUPPORTED for unsupported targets of implemented commands. §9.3.5.3.3 does not turn this implemented command into an unimplemented command type. The resulting status agrees with the frozen acceptance. The command-length echo is the explicit issue/assignment requirement; it is not presented here as a new general interpretation of every error response format.

RTL evidence: hdl/aecp/KL_aecp_engine.sv:3454–3463 preserves length → full 16-bit type → existence ordering. At cdl < 16 it selects UPC_BADARG_C; a non-AVB_INTERFACE selects UPC_NSUPPE_C with echo_r=1; AVB_INTERFACE selects UPC_GAVB_C with echo_r=0. E_GAVB's unchanged locate determines whether that interface index exists. hdl/aecp/ucode/gen_ucode.py:1131 uses the existing status-11/header/send/end program, without descriptor lookup, writes or gathers. The residual gavb_r routing is therefore unused in this refusal. The frame builder at engine:2602 reads echo bytes from the retained RX slot, and engine:2715 avoids sealing an unused response-memory payload.

The independent executable-text comparison, after removing comments and whitespace, proves the sole HDL change is UPC_NOTIMPL_C → UPC_NSUPPE_C in this arm. No ports, parameters, layouts or state were added. Independently generated base/head ROMs are both 26,624 bytes, 2,048 words, 92 programs, SHA-256 1f78804e448c385d633ed4355b7d84100ec13b12c77305c3bc11986653a80a8e. See source-identity.json and verify-source.py.

Robustness evidence: committed V5 covers existing and absent non-interface targets, an absent CLOCK_DOMAIN index, both adjacent type values and high-byte aliases 0x0109/0x8009. V1/V1b retain successful interface responses, V3 retains NO_SUCH_DESCRIPTOR, and V4 retains the short-command floor. All ten focused dispatch mutants were killed with the documented failing-check counts:

| Mutation | Failing checks |
|---|---:|
| Message-type guard removed | 14 |
| Wrong type reverted to NOT_IMPLEMENTED | 13 |
| Echo disabled | 13 |
| Fixed response body substituted | 13 |
| Type gate dropped | 13 |
| Only low type byte compared | 2 |
| Type gate inverted | 16 |
| Interface locate miss ignored | 1 |
| Padding rejected | 2 |
| Length floor reduced to 14 | 1 |

The unmodified dispatch control passed 1,008 checks. A separate disposable test copy added 32 byte-exact cases: cdl 12–15 with AVB_INTERFACE/0xFFFF partial bodies, and wrong types 0x0109/0xFFFF with index 0xFFFF at cdl 16, 17, 18, 19, 20, 100, 255, 256, 257, 511, 523 and 524. All passed, including patterned echoed padding; the augmented target passed 1,040 checks. This probes the first-failure order and length boundaries without changing RTL. See boundary-probe.patch, boundary-probe.log and run-boundaries.py.

Tests evidence from reviewer execution:

| Check | Result | Receipt |
|---|---|---|
| Full make -j16 check | rc 0 | make-check.log/.rc |
| Ten GET_AVB_INFO dispatch controls, --jobs 2 | One golden PASS; all ten KILLED; campaign rc 0 | dispatch-controls/results.json and raw arm logs |
| Standing gavb-other-type-not-implemented, --jobs 1 | Golden/restored PASS; mutant detected by the missing NSUPPE dispatch diagnostic | decode-control/results.json and raw build/sweep/run logs |
| Fresh decode sweeps | Each completed 617,916 trials, zero timeouts; golden/restored 176/176 checks | decode-control/*-sweep.log and *-run.log |
| Additional boundary stimulus | 32 additional cases pass, target rc 0 | boundary-probe.log/.rc |
| F06.14 regeneration in disposable exact-head copy | Current; no tracked diff | generated-docs.log |
| Source identity and independent ROM regeneration | PASS, exact bytes and modes | source-identity.json, tracked-blobs.txt |

The scoped simulator identity was verified as 5.050 before execution. Independent suites/campaigns ran concurrently under one foreground coordinator, with separate logs and rc files, explicit campaign --jobs and make -j16. Compiler parallelism was bounded to three workers per build; at most four builds overlapped. All foreground children completed. No full processor/parent/builder banks, synthesis bank, hardware run, source fix, commit, push or GitHub write was performed.

Docs evidence: hdl/aecp/ucode/aecp_commands.json:313/317 changes the status set and dispatch entries consistently. tb/aecp_cmds/decode.json:159 records NSUPPE, status 11, echo, cdl 16–100; its other semantic rows are unchanged. F06.14 at docs/architecture/06_aecp_engine.md:276 is generator-current. Sections 6.10 and 8.1, the verification standing-control description, both bench READMEs and the PR body match the implementation and measured mutation counts. Changed source comments describe behavior and clauses, with no newly introduced bench-lane/reviewer/round labels. Existing historical wording outside the added delta is not promoted into a new finding.

The acceptance's “section 8, item 12” is a stale locator: at both base and head, GET_AVB_INFO is row 14 at docs/00_MILAN_COMPLIANCE_REVIEW.md:598; row 12 concerns SET_CONFIGURATION notifications. Updating the existing GET_AVB_INFO row is the correct semantic outcome. The PR explicitly explains this discrepancy and includes every requested clause group. No renumbering of unrelated decisions is needed.

Published execution evidence was checked separately from reviewer execution. The selected downloaded receipts match the evidence commit's published SHA-256 manifest (public-receipt-verification.json). Source suite receipts report 1,030,399 checks with zero failures. Published source campaigns report decode 17/17, dispatch 74/74, deadline/hazard 67/67, counters 18/18, GSI 23 detected, name-write killed, ACMP 65/65, notifications 137/137, D3 110/110, elaboration controls 160/160 and name-state 16 killed. Notification and D3 comparisons were not run at the base; their head runs are present. Aborted/void receipts are not counted as passing evidence.

The published parent STATE receipt identifies dev a032c6d6e3775f145349d5a495c1e1ad12294936, the committed scratch pin 33d3010c, matching ROM ledger entries, and the other parent submodule pins. Public base-tree metadata independently agrees with the original processor, external and gPTP pins. The published milan_dp summary and rc report success at both pins: 11,630 [ok], 1,127 [PASS], zero [FAIL], and identical normalized check-line hashes. The two full parent logs are listed only by size/hash in EXTERNAL-RECORDS.csv; they are not present in this published bundle and were not independently inspected or rerun.

The published default-parameter protocol_processor_top area is 57,221 → 57,168 LUT: −53 (−0.09%), with LUTRAM, FF, BRAM, DSP and CARRY4 unchanged. This satisfies “about 0.” The parent wrapper's separately parameterized result is 58,039 → 58,506 LUT: +467 (+0.80%), with the other resource counts unchanged. Its constant-only control reproduces the head figure. The scratch measurement-row patch is published. These are attributed source receipts, not independent synthesis or hardware measurements; the wrapper increase is not hidden by the default-parameter figure.

Prior-review reconciliation: INDEPENDENT-VERDICT.md and its ledger were written before querying prior review FINDINGS. The subsequent PR review and review-thread lists were empty, and the refreshed PR conversation contained only the two review-start notices. There are no prior public findings on PR #201 to resolve or retain in this snapshot. Issue comments contained the assignment, acknowledgment and review-ready head. See prior-review-check.json.

Real limits and pending manager duties:

- The exact-head hosted snapshot shows successful docs-gates and portability jobs, with suites still in progress. The simulator build step was skipped after a cache hit; that is not a skipped test verdict. Pending suite/campaign steps are not counted as passed. Hosted/act acceptance remains the manager's responsibility.
- No manager source bank at this head is claimed or inferred. The source gate evidence above is the author's published evidence plus the focused reviewer runs.
- The manager must validate and publish builder/native-bank receipts for the final current-dev merge candidate, using live dev a032c6d6e3775f145349d5a495c1e1ad12294936 and this reviewed processor source, and satisfy the remaining completion bar and independent-review requirement.
- Physical calibration is NOT RUN. Field skips provide no hardware proof. No physical timing, board calibration, field behavior or controller interoperability was established here.
- The PR explicitly discloses possible rejection of this command-sized status-11 echo by a controller that expects the full GET_AVB_INFO response body for non-success statuses. The frozen requirement deliberately selects the echo, and the fixed-body mutant verifies that selection. This review does not claim universal controller compatibility.

Portable reproduction: run run-validation.py with the source checkout and scoped simulator paths, then run-boundaries.py with the source checkout, and verify-source.py with the source checkout. The scripts create their own trees under scratch/. Only REPORT.md and MANIFEST.sha256-listed artifacts are publishable; scratch/ is excluded.

R692-1 FINISHED
