[R850] POSITIVE - exact head 5f625090bbd09a67f01080aeaa1f05e9d9a79cdd

External independent review, round R850-2, issue #925 / PR #932. All five lenses are CLEAN. Both prior MAJOR findings and both prior MINOR findings are resolved at their causes. The prior suggestion and residue are addressed. Two new wording residues below do not affect the verdict. This approves the reviewed source; physical acceptance and current-dev candidate validation remain pending.

Tree: `84cd6032a8efac1563ae09d11a40ba206674373c`. Examined the complete `16ba667d..5f625090` delta and concentrated on the six commits after `09a948d4`. Thirteen files change. No HDL, mailbox contract, SRP timer/bound or submodule pin changes. Only the coverage record differs from `7a2def7c`.

Reconstructed AGENTS.md, CONTRIBUTING.md, docs/README.md, the public issue/scope decisions, requirements and interfaces before examining the diff and executable evidence. Read prior public findings after the independent code pass. No other current-round report, private author material or management checkout was read. No source edit, commit, push, GitHub write, hardware operation or merge occurred.

## Prior findings

| Prior finding | Disposition at this head | Evidence |
|---|---|---|
| R850-1 F1, MAJOR, all five lenses: trailing message loses transmission work | RESOLVED | `srp_mbx.c:399-402` retains work with `hold(i)` when the filter changes desired. `hold` at :122 only marks scheduler work; it neither reenters the library nor emits intermediate declarations. The previous reproduction and no-trailer controls, 200 phase/direction cases and 216 ordered-event traces pass at each interface count. |
| R850-1 F2, MAJOR, all five lenses: final unbind loses registration order | RESOLVED | `srp_mbx.c:209-247,630-698,910-924,1091-1110` and `srp_mbx.h:108-166`: the last unbind stores the interface/StreamID's latest kind while both registrations remain; a bind consumes it; either registration ending or interface reset releases it. The prior rebind reproduction retains Ready and Advertise feedback. The exception test/plant is replaced. |
| R849-1 F1, MINOR, Conformance/Docs: clauses and omitted departure/leave difference | RESOLVED | Public [scope ruling](https://github.com/kebag-logic/milan-fpga/issues/925#issuecomment-6930043105); `srp_mbx.c:194-203`; `srp/README.md:246-276,496-503`; test comments and PR body. These cite 35.1.2.1, distinguish JoinIn/JoinMt replacement from New, disclose the informative 35.2.6 NOTE and normative Milan 5.3.8.5 ruling, and record processor unregister-on-either-leave versus split fallback. |
| R849-1 F2, MINOR, Tests: repeated New from a two-kind state untested | RESOLVED | `srp_mbx.cpp:1902-1914,2085-2095`; `srp_kind_mutants.py:71-76`: repeated Failed New after Advertise New must decide again. Published exact `r849-renew-not-recorded` catches at both counts and the production campaign plant support the regression. |
| R849-1 F3, SUGGESTION, Tests: in-place rebind | ADDRESSED | `srp_mbx.cpp:1950-1977` replaces the same stream's destination in place and back. Exact `r849-bind-copy-skipped-for-self` is caught at both counts. |
| R849-1 F4, RESIDUE, Docs: report-local label | RESOLVED | `srp_mbx.cpp:1891` now begins `// #925: the talker`, replacing the report-local finding label. |

## Findings for this round

**R850-2-F1 - RESIDUE - Docs - new source comment contains a lane name.**

- Artifact: `sw/litex/ctrl_memory.py:250`, newly added comment text `as debt owed to S14`.
- Authority/evidence: the owner's 2026-10-15 source-comment rule excludes lane names and requires behavior/reason with issue or requirement IDs. This is a new comment occurrence, not an unchanged instance assigned to #746.
- Impact: wording hygiene only; no measurement, bound, test, generated artifact or conformance claim changes.
- Exact required fix: on this comment line replace `as debt owed to S14` with `as debt owed to the hybrid XIP work`. Keep the surrounding `#665` authority.
- Verification: inspect the added comment and confirm executable ledger values are unchanged. Carry to the residue checklist; Docs remains CLEAN.

**R850-2-F2 - RESIDUE - Docs - PR status retains pre-publication wording.**

- Artifact: PR #932 body, Status paragraph: `Six commits since reviewed head 09a948d4; nothing pushed in this round.`
- Authority/evidence: the public PR and review-start comment identify published head `5f625090`; the sentence retains the pre-publication handoff wording.
- Impact: stale publication prose only; no execution or acceptance claim changes.
- Exact required fix: replace that sentence with `Six commits since reviewed head 09a948d4; this head is published for review.`
- Verification: read back the PR body and confirm the SHA remains unchanged. Carry to the residue checklist; Docs remains CLEAN.

No open BLOCKER, MAJOR or MINOR; no additional suggestion.

## Reviewer-owned lens ledger

The RTL lens includes firmware architecture, storage lifetime and scheduling. Every row covers the current head and dependencies affected by the delta.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #925 body/ruling 6930043105; `srp_mbx.c:194-247,386-433,630-698`; pinned `mrp_mad.c:990-1067`; release `KL_srp_listener_fsm.sv:472-525`; wire reproduction receipts | R850-2 | 5f625090bbd09a67f01080aeaa1f05e9d9a79cdd |
| RTL | CLEAN | `srp_mbx.h:30-39,108-166`; `srp_mbx.c:122-128,209-247,630-698,935-968,1091-1110,1306-1354`; `MAILBOX_SPLIT.md:369-414`; memory-ledger diff, image receipts and unchanged gitlinks | R850-2 | 5f625090bbd09a67f01080aeaa1f05e9d9a79cdd |
| Robustness | CLEAN | `srp_mbx.cpp:1917-1948,1984-2125`; `srp_feedback.hpp:140-200` and existing withdrawal/reset/refusal tests; rerun phase/order/rebind probes; two-interface held-entry isolation | R850-2 | 5f625090bbd09a67f01080aeaa1f05e9d9a79cdd |
| Tests | CLEAN | `srp_kind_mutants.py:1-123`; `srp_mbx.cpp:1385-1435,1808-2125`; `srp_feedback.hpp:78-103,174-200`; `coverage.ratchet:36`; archived campaign/coverage and four independent spot-check logs | R850-2 | 5f625090bbd09a67f01080aeaa1f05e9d9a79cdd |
| Docs | CLEAN | `srp/README.md:246-276,493-503`; `SPLIT_CONTROL_MEMORY.md:135-147`; `ctrl/plat/README.md:110,135`; memory ledger/tests; PR body, public decisions and author-r3 receipts; F1/F2 are residue only | R850-2 | 5f625090bbd09a67f01080aeaa1f05e9d9a79cdd |

The receive fix retains transmission work even when a following message is unchanged or ignored. It observes copied indication state and sets pending work, preserving the serialized callback contract. Atomic replacement remains continuous; a genuine withdrawal stays retained for composition; only the final declaration is transmitted.

Ordering now survives local binding lifetime. All bindings of a StreamID carry its latest kind even with different destinations. The registrar walk refreshes `stream_kinds` separately from destination/VID eligibility. Consecutive replacements copy that state before replacing the old binding. The table uses full StreamID plus interface; swap-delete and descending reset traversal preserve other interfaces' entries.

The storage bound is conservative. Each held entry requires two distinct live attributes. `mrp_attr_inst` in pinned `mrp_mad.c:62-79` contains two 48-byte arrays before its other fields, exceeding the 64-byte small pool class. Each attribute consumes one medium or large block, so half those blocks bounds the held population; other allocations only reduce capacity. The count assertion guards width. Full-table fallback is a defensive white-box case, not an accepted exception in reachable operation. Storage is fixed and mailbox access contracts are unchanged.

## Independent execution

`run_spotcheck.py --repo <clone>` ran two independent native workers, eight compilation jobs each, with every process awaited. It appends unchanged published prior probes to disposable copies of the head's tests and compiles the head's firmware.

- One interface: 15 adapter/walk/probe tests and 23 composed feedback tests; all PASS, rc 0.
- Two interfaces: 16 adapter/walk/probe tests and 23 composed feedback tests; all PASS, rc 0.
- Both replacement directions, with and without the trailing Domain, first emit the matching declaration at model delay 0 ms. The composed GET_RX_STATE probe agrees.
- Each count passes 200 phase/direction cases, 216 three-event traces, the prior final-unbind reproduction, and new idle-timer/ignored-message, final-state-only, either-leave/expiry/reset, identity-change and in-place-rebind regressions.
- `git diff --check 16ba667d HEAD`: rc 0.

Raw receipts: `spot-if1-srp_mbx.cpp.log`, `spot-if2-srp_mbx.cpp.log`, `spot-if1-test_acmp_mbx.cpp.log`, `spot-if2-test_acmp_mbx.cpp.log`, each with its `.rc`. These are host tests, not fresh CPU measurements or physical timing proof.

## Published evidence audit

`audit_evidence.py` verifies all 234 author-r3 files against the SHA-256 manifest at immutable archive [22239840](https://github.com/kebag-logic/milan-fpga/tree/22239840693f38be230410d189dc9f4d16303feb/review-evidence/925-r1/author-r3). All match, including the complete file population. `evidence-integrity.json` records each hash. The archive commit has no embedded signature and no detached signature was supplied: this verifies the published hash packet, not cryptographic signer authentication. Published scrubbed receipts are distinguished from original-log hashes; original logs absent from the archive were not claimed verified.

Examined source receipts in that archive:

- `firmware/cov-check.log`: exact-head rc 0, 39 files PASS. `srp_mbx.c`: 768/768 lines, 695/698 raw branches, 100% after three unchanged standing exclusions; ratchet 695/695 counted branches agrees.
- `firmware/fw0.log` through `fw3.part2.log`: final-head receipts support 79 suite arms, 716 control, 299 AECP and 465 SRP catches, zero escaped production plants. Of 23 latest-kind plants, 21 run at both counts and two isolation plants at two interfaces.
- `plants/feedback-and-held-latest-if*.log` and `reviewers/r849-1/mutants-if*.log`: filter-hold, retained-order, repeated-New and in-place-copy defects are caught by named assertions. The obsolete `r849-unknown-withdraws` selection names the removed fallback test and reports an escape; its identical production mutation is caught by `feedback-latest-unknown-withdraws` on the new full-table guard. The legacy run is not counted as entirely successful.
- `reviewers/r850-1/`: all eight published reproduction/phase/order/rebind receipts pass. Their causes were independently checked above. Receipts at `7a2def7c` apply because the later commit changes only coverage counts.
- `workflows/docs-verify.md`, `rtl-fast-firmware-unit-and-changes.md`, `elaborate-verify.md` and selected step logs: executed steps succeed. Setup/hosted-only steps marked NOT RUN are not execution evidence. Elaborate records 10 executed steps, 36 not run with reasons. The old 65-suite sweep remains evidence at `09a948d4`, not a new sweep at this head.

## Budget, storage and image evidence

`audit_budget.py` checks all 16 cost rows per shape against measurement plus 5%, rounded upward to 5 us, and checks all eight SRP/transmit maxima per shape. `budget-audit.json` retains selected detailed rows and classifies raw STATED lines. Source cost statements and approved bounds are unchanged.

| Published measurement | 1x1/1if | 8x8/1if |
|---|---:|---:|
| Recorded rc / groups | 0 / 96 | 1 / 95 |
| Work passes / share overruns | 137,530 / 0 | 247,150 / 0 |
| Refusals | 0 | 0 |
| SRP record apply, us, bound 280 | 237.99 | 222.20 |
| SRP held, ms, bound 20 | 8.07806 | 9.04504 |
| SRP last service, ms, bound 20 | 9.78783 | 10.51546 |
| Timer-driven MRPDU response, ms, measured-row bound 20 | 1.87123 | 2.62353 |
| Join interval, ms, approved 181-239 | 189.053-190.070 | 188.316-190.122 |

Both points have zero late, absent or unresolved transmit work; the lateness test retains its 49 ms bound. Both retain the same seven pre-existing backlog-owed misses. The 8x8 rc 1 comprises 81 polls-base, two ACMP-item and four declined-offer statement records assigned to #914. Their rounded figures are 285/70/25 us versus existing 225/55/20 us statements. No new missed path or SRP/transmit failure appears. These are author source measurements, not a manager source bank.

`images/final-budget-image-identity.txt` records identical relinks of both measured `7a2def7c` budget ELFs at `5f625090`. `images/release-identity.txt` records identical release BIOS and stripped ELF at both shapes versus `16ba667d`. These hash receipts were checked; images were not independently rebuilt.

`ledger/plat_ledger-final.log` and its controls agree with the changed code: `ctrl_plat` sizes 17,728 / 19,392 / 18,624 / 21,248 B; ROM 118,128 / 119,712 / 130,752 / 132,304 B; planned RAMB36 43 / 44 / 56 / 61. Only 8x8/2if grows, from 60.5 to 61. Its entry follows the public [2026-11-15 ruling](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6892332745), with boundary controls rejecting 61.5. These are planned allocations, not newly routed area.

No fresh route is claimed. Earlier routes remain the assigned #927 base misses. The supplied #818 floor is +0.030 ns setup and 0 ns hold; positive hold below +0.030 ns is not a new finding. This budget round used the usage fallback. None of this constitutes physical calibration.

## Integrity, limits and manager duties

`verify_integrity.py` checks raw bytes/modes against Git blobs and the complete stage-zero index against the tree, bypassing status shortcuts. `integrity.json`: 1,627 superproject blobs and 1,238 blobs across five required initialized submodules match, with matching gitlinks/HEADs and no errors. The external gitlink is unchanged and intentionally uninitialized. No source restoration was needed. All disposable tests, builds and extracted evidence are under packet `scratch/`, excluded from publication.

Reproduce from this packet:

```sh
python3 -B run_spotcheck.py --repo <clone>
python3 -B audit_evidence.py --repo <clone>
python3 -B audit_budget.py --repo <clone>
python3 -B verify_integrity.py --repo <clone>
```

The original `run_reproduce.py`, `run_probes.py`, `run_rebind.py` and their additions are also included. Each accepts `--repo <clone> --interfaces 1` or `2`; the combined spot-check applies their same assertions with fewer compilations.

Full coverage, CPU banks, broad parent/processor/synthesis/builder banks and hosted jobs were not rerun. No workflow container or host orchestrator ran. Clause corrections were checked against the supplied public normative ruling, local contracts, pinned library and processor behavior; no fresh licensed-standards inspection is claimed.

Physical calibration NOT RUN. Field skips and host-model delays are not hardware proof. Listener Ready within one second on the bench remains pending. There is no manager source bank at this head. The manager owns exact-head hosted/act acceptance and must distinguish executed jobs from skipped contexts.

The PR targets `dev-soft-core`, recorded base `70f4056f`; that does not validate the future current-dev candidate. At merge turn the manager must construct the candidate against live dev (supplied tip `6b66f66d89cf25d2717687bcc2c3bf617685a99a`), run builder/native banks, publish receipts, complete bench acceptance and the independent-review bar, obtain merge authorization, and perform post-merge containment before closing the issue. Carry F1/F2 to the residue checklist. This report neither validates that future candidate nor authorizes merge.

R850-2 FINISHED
