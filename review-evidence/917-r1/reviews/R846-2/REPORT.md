[R846] NEGATIVE - exact head 8f73ade54366cc832bad3386c8b6f3bbb12ca5e4

External independent delta review R846-2 of issue #917 / PR #918. Tree `ae584aff6a5a4e2dc9dde81b170c893cde65a2da`; source base `cec88385ad0a0ec0d61b91597640797766e45010`; previous reviewed head `3926c271aaf77420fb9093694be0ab9d511b898d`. Round two is one commit, 21 files, +525/-122. All five lenses were applied. One MINOR validation defect remains, plus one source-comment RESIDUE. No new shipped RTL or firmware defect was found.

Scope was reconstructed from the operating contract, documentation index, [issue #917](https://github.com/kebag-logic/milan-fpga/issues/917), its TAKEN and REVIEW READY comments, [the public ruling](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6894152131), [the owner decision](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6898289590), REQUIREMENTS section 1, FR_NFR sections 3.4.1/3.4.2, the mailbox contract/design and the supplied round-two allowance ruling. The full source-range diff/history established context; the delta received detailed review. Prior public findings were read after the independent diff pass. No private author material, other current-round review report or management source bank was consulted.

**R846-2-F1 - MINOR - Tests, Robustness - Commit-order validation remains incomplete.**

Artifacts: `tb/verilator/ctrl_service_budget/grade.py:195`, `tb/verilator/ctrl_service_budget/held.py:46`, `tb/verilator/ctrl_service_budget/selftest_held.py:27`; reviewer `probe_attribution.py` and `attribution.log`.

Authority/evidence: R846-1 F2 required attribution without accepting missing, duplicate or misordered commits; the assignment retains that requirement. The held record must commit first on its channel. The parser tracks a held frame for RXR, but the ordinary RXC branch never checks that state. Also, release() unpacks held_at but validates its cycle only against the last byte and upper allowance.

Two constructed histories pass the actual parser and grade.grade():

- A ends at 1059 and is held on channel 2 at 1070. B ends at 2059 and commits through `RXC 2070 2`, before A's `RXR 500100 2`. Both commits are credited; A's response row is measured and within_budget=true. B has overtaken A on the same channel.
- After `RXH 1070 2`, `RXR 1060 2` is accepted. The hold occurs ten clocks after its purported release; the measured row reports one clock of ingress.

These are synthetic observation histories, not CPU-system measurements or evidence that the shipped RTL generates these sequences. Positive attribution, wrong-channel/orphan/duplicate/late releases, missing probe release and release-before-hold in line order were checked separately. The old-attribution negative control is caught.

A positive other-channel commitment while AECP remains held is also measured correctly. The required ordering validation must retain this independence.

Impact: a broken observer or an ordering regression can yield a successful measurement from an impossible held-record history. The ordinary attribution and published measurements are repaired; the remaining validation weakness is MINOR, rather than retaining the former MAJOR severity for the fixed attribution error.

Required outcome: reject same-channel commitment that overtakes an outstanding held record, and a release timestamp that does not follow its hold. Preserve independent-channel activity and valid coincident observations. Add standing negative controls for these histories and a valid other-channel control. No production RTL change or budget relaxation is requested.

Verification: `python3 -B probe_attribution.py <checkout>` reproduces both accepted invalid histories. They must fail validation while the valid held/follower case remains measured. Removing either new ordering guard must fail a named self-test. This is the remaining ordering portion of prior F2, not unrelated scope expansion.

**R846-2-R1 - RESIDUE - Docs - New source comments contain bench labels.**

Artifact: `tb/verilator/mbx/suite.hpp:1648`, comment ending at line 1650.

Authority/evidence: the owner's source-comment rule excludes bench labels. The added comment contains (B7), (B8) and (B9).

Impact: comment wording only; no behavior, measurement, figure, verdict, generated artifact, clause claim or privacy property changes. This does not make a lens unclean.

Exact fix:

```cpp
// #917, what a held record leaves for the frames behind it: the free space
// past it, the frames the filter refuses behind it and a channel
// closed while it is held.
```

Verification: inspect added comment lines. Keep executable assertion names and the README's check identifiers.

**Prior findings disposed at this head.**

| Prior finding | Disposition and evidence |
|---|---|
| R845-1 F1, MINOR, Tests/Robustness/Docs | Resolved. suite.hpp:1652 adds the last-fitting-slot case, RX_DROP versus RATE_DROP, unread-byte comparisons and held delivery. mutants.py:679 plants space from the committed head for both adapters; both fail B7 by name. README.md:452 correctly describes the separate tail-guard mutant. |
| R845-1 F2, MINOR, Tests/Robustness | Resolved. suite.hpp:1694 offers a foreign target, a 22-byte cut and a 14-byte stub behind a hold, checking counters, ERR and held bytes. mutants.py:683 removes the identity guard and fails B8 by name. |
| R845-1 F3, MINOR, Tests/Robustness | Resolved. suite.hpp:1722 closes FILTER_EN after a hold, checks release at refill and no further accepted/counting activity. mutants.py:687 gates release on open and fails B9 by name. |
| R846-1 F1, MINOR, Conformance/Docs | Resolved. KL_mbx_rx.sv:38, MAILBOX_SPLIT.md:277, suite.hpp:393 and :1544, frames.hpp:297 and PR description/references distinguish the measured one-in-flight workload from permitted pipelining. Timeout/retry cite 9.3.2.6/9.3.6; B0 is next-refill delivery. |
| R846-1 F2, formerly MAJOR, Conformance/Tests/Docs | Allowances, margins, frame identity, held measurement and old-attribution control are resolved. Ordering remains R846-2-F1, MINOR, Tests/Robustness. Conformance and Docs portions are resolved. This reviewer assigns the remaining severity and lenses. |
| R845-1 R1 and R846-1 R1, RESIDUE, Docs | Resolved at the named source locations: issue-comment identifier removed, behavior/reason retained. R846-2-R1 is a different new comment instance. |
| R845-1 R2, RESIDUE, Docs | Resolved in MAILBOX_SPLIT.md:306: rate refusal applies to a passing frame that fits; filtering and insufficient space have their own outcomes. |
| R845-1 S1, SUGGESTION, Conformance/Docs | Adopted in MAILBOX_SPLIT.md:312 and PR limitations: second controllers, pipelined commands and controller responses share the bucket. Fifty unpaced commands are not promised. |

**Artifact-specific lens results.**

[R846] PASS Conformance - REQUIREMENTS.md:42; FR_NFR.md:422; mailbox_emit.py:217; MAILBOX_CONTRACT.md:874 - Token delivery retains 64 clocks / 1 ms. Held allowance is refill_ms + 1 ms, generated as ADP 11, ACMP 6, AECP 6, MAAP 21, SRP 3 ms. Complete-response margins correctly subtract ingress and egress: held ACMP 173 ms, AECP 213/223 ms, MVU 213 ms; at the 10 ms proposal, 183, 223/233 and 223 ms. No service/response bound moves. Parsed YAML equals the source base including rates, ABI and version; generator checks pass. One-in-flight acceptance is distinguished from pipelining. Three hardware walks remain owed, not a claimed pass.

[R846] PASS RTL - KL_mbx_rx.sv:458,598,608,738,775; published rtl-comment-only.txt; audit.log - Round-two production RTL changes are comments only. Independent token comparison agrees with the published identical lowered-output hash 50b2e99a4ba5ed57c8edd1c8c6c1527297ebfb94e1a3b1a93832250ede383836. Prior clean RTL coverage carries forward: write-head storage/free space preserves held records, committed-head guard rejects invalid tails, release spends the refill, and head visibility follows the registered header write. No clock/reset, CDC, FSM, width or firmware-image logic changed. Passive budget observers add no production ports. Prior route evidence remains applicable.

[R846] MINOR Robustness - suite.hpp:1652,1694,1722; held.py:40; grade.py:195; attribution.log - B7/B8/B9 close ring-space, malformed/filtered follower and close gaps on both adapters and the host model. Reset/refill/wrap coverage is unchanged. New grader rejection cases pass except the ordering holes in F1, leaving this lens unclean.

[R846] MINOR Tests - mailbox mutants.py:679; selftest_held.py:27; selftest_mutants.py:446; model.log; budget.log; attribution.log; receipts.log - New mailbox checks match their planted faults and run through the shared suite. The independent single-interface host-model run passes 542 checks. The old-attribution control fails for the intended defect. F1 remains despite passing standing tests.

[R846] PASS Docs - MAILBOX_SPLIT.md:273; FR_NFR.md:422; MAILBOX_CONTRACT.md:874; both READMEs; PR Round 2; source comments and public receipts - Changed allowances, margins and documented behavior agree. The false protocol restriction and wrong space-mutant description are corrected. R1 is residue only. The PR's claim that F2 is closed must follow the final ordering verification; this report explicitly retains that executable requirement.

**Published receipts versus execution here.**

Archive: [24755cf4, author-r2](https://github.com/kebag-logic/milan-fpga/tree/24755cf4fb9ea20dbede7ad298e7782957a619d8/review-evidence/917-r1/author-r2). audit.py verifies all 431 round-two and 423 retained round-one manifest entries against published SHA-256 values. The archive commit has no embedded signature and no detached signing material was supplied; this is byte-integrity verification, without a cryptographic signer-authentication claim.

check_receipts.py independently checks the receipt structure and values, recorded in receipts.log:

- Four mailbox controls pass; 242/242 mutants are caught. Both free-space arms fail B7, identity-guard removal fails B8 and open-gated release fails B9. The exact-head mailbox log records 622/667 single-interface checks, 629/674 two-interface checks, 547 model checks and 32 co-simulation checks without failures. The quick campaign records 13/13 catches.
- Firmware-control receipts record 699/699 catches. The workflow table has 139 zero exits and 226 explicit skips: 137 readable executed logs carry exact-head headers; two larger logs are represented by hashes/sizes plus exits. These are author-run steps, not a manager bank or hosted/replica acceptance verdict.
- Shard 1/4 initially has 16 passes and one timeout, milan_dp_render. Its fresh exact-head rerun passes; together the receipts support 17/17. The initial timeout is not counted as a pass. Unchanged earlier shards retain prior evidence.
- Both held groups bind last byte 100001422, hold 100001427 and release 100500065 to the probe, with both followers refused. Rows report 5.23609 ms at 1x1 and 5.11361 ms at 8x8/1if, including 4.98643 ms ingress against 6 ms, within 20 ms. Published old-attribution controls are caught.
- The 8x8/1if held run exits 1 for the same three stated-cost overruns as the ordinary AECP control: 120704/117875 against 101000 cycles and 95723 against 43000. Both have zero refusals and budget misses. As assigned, this is known #914 work, not a new finding or a green overall run.
- Regrade receipts report 94/94 grades and table byte equality for both recorded 1x1 populations, zero refusals and seven retained pre-existing misses. This is not a freshly executed population at this head or at 8x8/1if.
- All 46 fixture-image hash entries are byte-identical. Split firmware matches the base comparison: 1x1 bb04b69678bda6d7aa21458b5a39da1a611c3211efabd314ff590e06f6c76978, 145496 bytes; 8x8/1if 506a1ae4da57e1d71f22201f02f4e1df49d6cb110dfe677c5d1fba0e154ca8fb, 158176 bytes. ROM-bank and constraint hashes match. No firmware source changes this round.

Large CPU observation logs are published by digest/size and excerpts, so full regrading was not independently repeated. The held measurements and 94-group equality above are author receipts, not new CPU-system measurements. Physical calibration is NOT RUN; field skips are not hardware proof.

**Reviewer-owned ledger.** CLEAN means no open BLOCKER, MAJOR or MINOR under that lens. It does not complete hardware or merge duties.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue/ruling; REQUIREMENTS section 1; FR_NFR:422; mailbox_emit:217; generated channel table; YAML; held receipts | R846-2 | 8f73ade54366cc832bad3386c8b6f3bbb12ca5e4 |
| RTL | CLEAN | KL_mbx_rx:458,598,608,738,775; passive observers; token identity; lowered-output and inherited route receipts | R846-2, preserving unchanged R846-1 coverage | 8f73ade54366cc832bad3386c8b6f3bbb12ca5e4 |
| Robustness | UNCLEAN, F1 | suite.hpp B7-B9; shared model; held.py:40; grade.py:195; attribution.log | R846-2 applied; no clean round for changed grader | 8f73ade54366cc832bad3386c8b6f3bbb12ca5e4 |
| Tests | UNCLEAN, F1 | New mailbox mutants; selftest_held; old-attribution mutant; model/budget/attribution logs; campaigns | R846-2 applied; no clean covering round | 8f73ade54366cc832bad3386c8b6f3bbb12ca5e4 |
| Docs | CLEAN; R1 residue | Design hold section; FR_NFR margins; generated contract; READMEs; source comments; PR/evidence | R846-2 | 8f73ade54366cc832bad3386c8b6f3bbb12ca5e4 |

**Reproduction and limits.** run_checks.py takes checkout, packet and task (generator, model or budget). probe_attribution.py takes checkout. audit.py takes checkout and extracted evidence root; check_receipts.py takes evidence root. Scripts and raw receipts are listed in MANIFEST.sha256. Disposable outputs remain in scratch and are not published. Independent checks ran concurrently as foreground commands. No source edits, prohibited banks, hardware, shared installations, commits, pushes or GitHub writes were performed. The pinned simulator identity was checked; no RTL rebuild was needed for this delta.

Independent execution: generator check/crosscheck/selftest pass; the shared host-model suite passes 542 checks; the nine held-attribution self-checks pass and the old rule is caught. The broader budget self-test completed its baseline and caught 210 independent mutations before a deliberate time-bounded interruption (budget.log and budget.rc retain the interruption, not a successful exit). finish_budget.py ran a fresh passing baseline and the four remaining mutations in a new process; all four were caught, exit 0. Together the two logs cover 214/214 existing mutations, with no escaped mutation or baseline failure. This is not represented as a single uninterrupted successful campaign. Expected CONTROL ... ESCAPED lines inside the self-test exercise its rejection of invalid negative-control evidence; they are distinct from MUTANT ESCAPED, of which there are none. These passing existing controls do not detect F1.

Source integrity is proved against tree entries, not merely status: 1608 superproject blob bytes/modes and index, exact head/tree, and required submodule gitlinks plus tracked bytes/indexes. The optional external submodule remains deliberately uninitialized. The standard-clause correction follows the verified clause findings from R846-1; full standards text was not re-audited in this delta.

**Pending manager duties.** Arrange F1's correction/re-review and R1's residue checklist. Finish the other independent review. Build and validate the final candidate against current dev (assignment tip 6b66f66d89cf25d2717687bcc2c3bf617685a99a, distinct from source base cec88385). Builder/native banks, hosted/replica acceptance and published receipts belong to that merge turn; no manager source-head bank is claimed here. Record the selected timing directive; the retained selected-route receipt reports +0.203 ns setup / +0.036 ns hold. Complete three hardware descriptor walks, keeping or reopening #917 until evidence exists. Merge authorization, post-merge containment and final issue completion remain pending.

R846-2 FINISHED
