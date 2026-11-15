[R838] POSITIVE - exact head 867faf1e7321e1260f86701f01d7de0c94e67490

R838-9 applied all five lenses to the two-commit documentation/comment delta from `234bc149ff888eb96659ecaaa5ce6e4fb27319d4`. The prior MINOR causes are resolved. No open BLOCKER, MAJOR or MINOR remains in this delta review. One citation RESIDUE below does not dirty coverage.

Tree: `639655730d2a898d963e195cfb95d35fef5ca715`. This is source-head review, not merge-candidate or hardware acceptance.

## Scope and authority

Reconstruction followed AGENTS.md / CONTRIBUTING.md, docs/README, #894's frozen acceptance and public decisions, REQUIREMENTS.md product ownership, FR_NFR 3.4.1, MAILBOX_SPLIT and MAILBOX_CONTRACT, then the full-base diff inventory/history and the narrow delta, then published evidence. The requested `66f713267f201d1a00d7f711e04b3a996d804dee..867faf1e` inventory includes imported work. The later-round instruction governs fresh examination: unchanged code was not re-reviewed.

Key public authorities: [1x1 merge scope](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6867393730), [contingent bounds](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6858269025), [last-notice amendment](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6862465874), [egress and pace](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6867990126), [configuration ruling](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6883864236), [SRP drain](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6886633874), [slice and item 5](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6888782796), and [round-14 REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6891277821).

Evidence paths below refer to [archive 1a095573](https://github.com/kebag-logic/milan-fpga/tree/1a0955730171f3fdc32387098b4beec60788c0ce/review-evidence/894-r1). I wrote my independent verdict and five-lens ledger before reading prior reviewer reports. Reconciliation then used the public [R837-7](https://github.com/kebag-logic/milan-fpga/pull/902#issuecomment-6890948441), [R838-7](https://github.com/kebag-logic/milan-fpga/pull/902#issuecomment-6890766701) and [R838-8](https://github.com/kebag-logic/milan-fpga/pull/902#issuecomment-6890858159) findings. No concurrent review, private author material or management checkout was read.

## Cause-level resolutions

| Prior ID; severity; lenses | Disposition and evidence at this head |
|---|---|
| R837-7-F1; MINOR; Docs | RESOLVED. `SPLIT_CONTROL_MEMORY.md:2197` states 735 us; `sw/firmware/ctrl/srp/README.md:238` states 33.38 ms at 950 us; `poll_grade.py:70` states 280/365 us. Section 13's changed narrative separates intermediate and current rows, loads, slice and TICK. FR_NFR:383 identifies the 48.23/188.41 results as then. Current rows and loads reproduce. The PR's two quantitative sites remain corrected. The off-by-one citation is R838-9-R1 below. |
| R838-7-F1; MINOR; Tests, Docs; retained cause of R838-6-F2 / R838-4-F1 | RESOLVED, preserving R838-8's correction. PR section 8 gives 0.516/0.512. Its R838-6-F2 row gives R4 13.10 and last notice 127.21 within 130 at 950 us; 13.05/132.71 are explicitly historical. Exact-head execution agrees. |
| R837-7-R1; RESIDUE; Docs | RESOLVED. `ctrl_loop.h:321` says the cut was measured at fe0cef5b, distinguishing the measurement image from the cut. Preprocessed bytes are identical. |
| R838-7-R1; RESIDUE; Docs | RESOLVED. `edit_rows.py:3` names “its SET_CONFIGURATION ruling, item 3” and retains #894. AST including positions is identical after excluding the module docstring. No new prohibited review/lane/comment-ID instance occurs in the changed source prose. |
| R837-7-S1; SUGGESTION; Docs, Robustness | TAKEN. `SPLIT_CONTROL_MEMORY.md:2509`, PR 14.3 and `author-r14/receipts/item5-no-late-completion.md` state the live-clock/out-of-reset precondition and that an independent datapath clock/reset reopens the proof. Source check described below. |
| R837-7-S3 / R838-7-S2 / earlier indexing suggestions; SUGGESTION; Docs | TAKEN for this packet. All 45 inner-index rows match published bytes; all 46 files match the outer manifest, without redaction. INDEX explicitly explains the earlier packets' original/published hash mapping. |
| R837-7-S2; SUGGESTION; Tests, Robustness | RETAINED, optional. `record_classes.py:134` can report an unanswered over-cost record without holding it. No executable change addresses this; the PR explicitly retains the limitation. Preserve the prior suggestion to hold/refuse that case with a control; no published misgraded span is claimed. |
| R838-8-S1; SUGGESTION; Docs | RETAINED, optional. The R838-6-F2 verification cell still names `receipts/model/*-3909588f.txt`. Suggested replacement: `author-r13/receipts/model/flip-1x1-ed0df35b.txt` and `load-check-ed0df35b.txt`. The printed exact-head commands are correct, and the reproduced rows/load validate them. |

The live PR body equals `author-r14/PR-BODY.md` byte-for-byte, SHA256 `f25a398c64340870686d03fd2f455e4a20db2c7aa16f168e52f25a426eaca741`. A final live read confirmed the same body and exact head. It contains Round 14, the R837-7/R838-7/R838-8 rows, the restored round-13 leg and validation tables, and “In round 12, nothing under sw/ changed after a47cd3f2.” That statement is now scoped to round 12.

## Figure sweep and independent checks

The author's search reproduced **64** token/path/line hits exactly: **36 historical, 28 unrelated**. I checked their classification in context and independently searched 725, 33.01, 900 us, 0.515, 0.511, 13.05 and 132.71 across the specified documents, READMEs and source files. Broader substring hits included a 1.725 percent quantity and a seed ending 0725; neither is a moved cost. No additional current stale moved figure was found. The search is a navigation aid, not an automatic proof of prose correctness.

Current statements agree: build of one **735 us**, TICK **55**, AECP timer slot **70**, LINK **155**, SRP drain **280**, slice **950**, loads **0.516 / 0.512**. Historical 725/50/65/150/250/900 and earlier rows remain historical or refer to other quantities. The old 900 us failure is explicitly at the design then built.

Own exact-head commands, both exit **0**:

- `python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 1x1/1if`
- `python3 -B tb/verilator/ctrl_service_budget/load_grade.py --check`

| Current row | Result, ms | Bound, ms |
|---|---:|---:|
| R4 | 13.10 | 20 |
| R4L | 188.48 | 238 |
| ACMP / ADP / MAAP | 28.95 / 27.30 / 27.42 | 30 each |
| First / last queued notice | 14.66 / 127.21 | 20 / 130 |
| R5 / R6 | 74.07 / 69.86 | 90 each |
| tx / txL | 33.38 / 48.43 | 49 each |

The flip output is byte-identical to the archived final round-13 receipt. Load is **0.516 / 0.512**, both under **0.70**. Pace **8 ms**, slice selection **950 us**, and **585/585** flip controls carry from verified published evidence and unchanged executable inputs; those controls and the full grid were not rerun here.

## No-code-change proof and item 5

`delta.diff` shows only six changed paths: three Markdown files, `ctrl_loop.h`, `poll_grade.py` and `edit_rows.py`. Independently:

- Header preprocessing preserves every emitted byte; SHA256 **13d2df1e0b8efa832734c6bd2c24fdf1b4e72788e07b6d3f573a24b8dd6a49e5**.
- The poll grader's AST, including positions, is identical.
- The edit grader's AST, including positions, is identical except its module docstring; no tracked reader of that docstring was found.
- Published image inventories have the same paths and **332/332** equal hashes at 234bc149, b25530f6 and 867faf1e: **8 ELFs, 8 binaries, 316 objects**. They also equal the round-13 inventory.
- All **14/14** relinked harness receipt rows say identical at both newer heads. Every hash agrees with the older published evidence: 13 in its harness list, arm A in its fixture image list; **10 distinct ELFs**.
- All **28** documentation gate summary exits are **0** and each summary agrees with its raw log. Their receipt states a clean clone before and after. These are verified author executions, not fresh reviewer executions.

This checks the published byte-identity evidence; I did not rebuild or directly hash unpublished binaries. It supports carrying round 13's measurements and test assessments without reopening unchanged code.

For the added precondition, `milan_soc.py:265,282,288` creates sys and milan outputs on the same PLL without overriding `with_reset`. The [pinned clock implementation](https://github.com/enjoy-digital/litex/blob/a1e1c3652ec2f1346ebaea7663d2867f393ae2c4/litex/soc/cores/clock/xilinx_common.py#L58) gives each its own `AsyncResetSynchronizer(cd, ~self.locked)`. Thus “together” describes their shared reset cause, not cycle-identical deassertion across different clocks. The claim is the supported operating product path, not reset-transient or stopped-clock fault tolerance. MAILBOX_CONTRACT:346 retains its 64-cycle acknowledgement requirement; the previously reviewed crossing/protocol proof is unchanged. No new late-completion cost measurement is claimed.

## Wording residue

**R838-9-R1 - RESIDUE - Docs - PR finding row points one line before the intended summary.**

- **Artifact:** PR #902 Findings table, R838-6-F2 row; `pr-body-excerpts.txt`, source line 371.
- **Authority/evidence:** the cell cites `SPLIT_CONTROL_MEMORY.md:2524`; the load/R4 paragraph is at **2525**. Line 2524 is the preceding hot-list bullet. R837-7-F1's requested citation was 2525.
- **Impact:** navigation only. The adjacent paragraph, exact-head commands and displayed figures are correct; no measurement, verdict, clause claim or privacy rule changes.
- **Exact required outcome:** change that citation from `:2524` to `:2525`.
- **Verification:** open the cited paragraph at this head. No executable test or rebuild is needed. This residue does not dirty a lens.

## Earlier dispositions carried at unchanged causes

These are retained public resolutions from R838-7/R838-8, not fresh code reviews. The six-file delta and compiled/AST identity establish that the relevant executable causes did not change.

| Prior IDs | Disposition and cause-level artifact |
|---|---|
| R837-6-F1 | Resolved: final compare receipts include E1; timer/LINK/build/TICK corrected and rows/rules rerun. |
| R838-6-F1 / R837-6-R2 | Resolved: per-image receipt and section 13 replace universal ROM growth. |
| R838-6-F2 / R838-4-F1 | Resolved in R838-8: current PR load and row figures now agree with exact-head checks. |
| R838-6-R1 / R837-6-R1 | Listed round/lane instances removed; R838-7-R1 is now resolved by the docstring-only change. |
| R838-6-R2 / R837-5-R1 | Resolved: historical-margin heading names round-30 measurements; misleading current-head wording removed. |
| R838-6-R3 | Resolved: PR says compiled firmware output, supported by identity evidence. |
| R837-6-S1 / R837-5-S1 / R838-5-S7 | Indexer checks readback after sanitizing; publisher redactions map through outer manifest. Publication-index suggestion resolved for this packet; older redactions remain mapped. |
| R837-6-S2 | Later-record case fixed and planted; gap/deferred-response limit remains optional S1. |
| R837-4-1 | Actual-array/domain assertion and floor retained in `aecp_maps.c`; map storage/indexing unchanged. |
| R838-4-F2 | Correct work-arm selection retained in `aecp_arms.py`. |
| R838-3-F1 / R837-3-1 / R838-2-F2 | Direct-index collision/work fixes retained; map algorithm unchanged. |
| R838-3-F2 / R837-3-2 / R838-2-F3 / R837-2-3 | Corrected bounds/references retained; current slice sites updated to 950. PR summary exception is resolved by R838-8. |
| R838-3-F3 | Historical aligned-ROM reconciliation retained; new arithmetic checked. |
| R837-2-1 / R837-2-2 | 49/238 egress bounds and whole-ms count retained in loop/pace/join artifacts; model checks pass. |
| R838-2-F1 | Horizon-free join classification/controls unchanged; new joins fit corrected bounds. |
| R838-1 F1 / R837-1-1 | Tier-1 rows, long-record storage/charges retained; recomputed rows pass. |
| R838-1 F2 / R837-1-2 | MRP budget, static assertion, tx/txL proof retained; 33.38/48.43 ms now. |
| R838-1 F3/F4 | Longer-notice-after-drain and ordinary-round-clear tests/plants unchanged in AECP/loop files. |
| R838-1 F5 / R837-1-3 | MAILBOX_SPLIT current slice correctly updated to 0.95 ms. |
| R838-1 F6/F7 / R837-1-5 | Rotating order and conditional Domain/VLAN claims retained; licence/resume/reset/gap causes unchanged. |
| R837-1-4 / R838-1 S5 | Reported 8x8/#910 scope retained; no passing flip inferred. |
| R838-1 RS1 / R837-1-6; R838-2-R1 / R837-2-4; R837-4-R1 | Original source-comment repairs retained; the new docstring residue is now resolved. |
| R838-2-R2 / R837-2-5; R838-3-R1 / R837-3-R1; R837-4-R2; R838-4-R1 / R838-4-S10 | Historical receipt/head/count/share repairs retained; no historical count promoted to fresh measurement. |

## Optional suggestions retained for one-pass absorption

All following items remain **SUGGESTION**, with their original IDs and lens attribution. They create no new merge requirement. Probe evidence mentioned here belongs to the earlier public reports; it was not rerun in this documentation review.

| ID; lenses; artifact | Evidence / impact | Suggested outcome / verification |
|---|---|---|
| R838-7-S1, retaining R837-6-S2; Tests, Robustness; `record_classes.py:102-112` | Naming ends at next record start, not measured span end. `audit_timing.py` demonstrates a span ending at 23,000 named by a response at 40,000 before next start 1,000,000, charged paced. No published run is shown misclassified. | Correlate deferred replies with request/sequence identity or use true spans where valid; preserve legitimate polled replies and add a gap control. |
| R838-5-S1; Docs; AECP README owed ordering | Later-response/earlier-notice order can expose an older cached value. | Add a two-controller example; compare response/notice order. |
| R838-5-S2; RTL; `aecp.c` counter reset | Earlier redundant defensive reset unchanged. | Explain invariant, or remove only with queue/retry verification. |
| R838-5-S3 / R837-1-8; Tests; `aecp_owed_notice_steps.py` | Offline scenario remains; native tests supply execution evidence. | Drive compiled behavior and require a behavioral plant failure. |
| R838-5-S4; Tests; measurement inventories | Widened survey improves coverage; sustained pressure/counts remain useful. | Publish counts/maxima and reconcile spans under longer expiry pressure. |
| R838-5-S5 / R837-1-7; Tests; `rows_tiers.least_margin` | Unsolved -1 can outrank solved scores below -1; passing choice unaffected. | Rank unsolved last; add mixed failed-search ordering control. |
| R838-5-S6; Tests; ACMP decline bound | Conservative prior bound unchanged. | Tighten only with source proof and mutation control. |
| R838-5-S8; Tests; `mrpdu_grade.py:84` | Callback-late and owed-centisecond origins differ. | Explain/align origins; test delayed callback. |
| R838-5-S9; Tests, Docs; H-81N receipt | Resolved: model-size exception distinguished from timing miss. | Retain distinction; no new action. |
| R838-5-S11 / R837-4-S1; Tests; `aecp_maps.c` first-coordinate guard | Earlier guard-removal plant survived admission; guard unchanged. | Add an admitted descriptor/edge case killing it. |
| R838-5-S12; Docs; floor discussion | Placement sensitivity remains; attribution improves explanation. | Explain remaining margin assumptions against measured counterfactuals. |
| R838-5-S13; Robustness, Docs; format/domain contract | Safety depends on admitted formats/fixed cluster widths. | State precondition; check generated keys when widths change. |
| R838-5-S14; Robustness, Docs; `struct edit` | Wide-table size is not full-call-chain stack proof. | Measure target peak stack before extending supported images. |
| R838-5-S15; Tests, Docs; historical item-2 provenance | Current carry has inventories; older subset attribution optional. | Retain run heads/input-identity spans beside historical probes. |
| R837-5-S2; Tests; undersized-table plant | Wider-domain refusal was probed, but lacks permanent wide plant. | Add floor-only 16x32 plant requiring assertion diagnostics. |

## Five-lens results and reviewer-owned ledger

[R838] PASS Conformance - `docs/reference/FR_NFR.md:383`, #894 public decisions, `flip-check.txt`, `load-check.txt` - current costs/rows preserve the frozen bounds and 1x1 scope; no normative requirement changes.

[R838] PASS RTL - `delta.diff`, `ctrl_loop.h:321`, `milan_soc.py:265,288`, pinned clock source:58-60 and `verification.txt` - no logic or architecture delta; the added reset precondition matches the shared PLL construction.

[R838] PASS Robustness - `SPLIT_CONTROL_MEMORY.md:2509`, item-5 receipt and unchanged control ASTs - supported-clock assumptions are explicit; independent reset/clock changes reopen the proof; failure paths and known 8x8 limits are not newly claimed clean.

[R838] PASS Tests - `verification.txt`, round-14 identity/gate receipts, carried round-13 receipts and the two own model checks - no executable test change, no weakened control, and quantitative expectations agree with execution.

[R838] PASS Docs - all six delta files, `stale-grep.txt`, `independent-grep.txt`, `figure-and-pr-audit.txt`, `pr-body-excerpts.txt` - stale-current causes fixed; historical figures distinguishable; only R838-9-R1 wording residue remains.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | FR_NFR:383; public scope decisions; flip/load outputs | R838-9 delta, carrying unchanged R838-7/R838-8 and R837-7 coverage | `867faf1e7321e1260f86701f01d7de0c94e67490` |
| RTL | CLEAN | Six-file diff; header preprocessing; PLL/reset source and pin | R838-9 delta, carrying unchanged R838-7/R837-7 coverage | `867faf1e7321e1260f86701f01d7de0c94e67490` |
| Robustness | CLEAN | Item-5 precondition; unchanged graders/controls; known-limit PR text | R838-9 delta, carrying unchanged R838-7/R837-7 coverage | `867faf1e7321e1260f86701f01d7de0c94e67490` |
| Tests | CLEAN | Image/harness/gate manifests and logs; AST checks; flip/load execution | R838-9 delta, carrying unchanged R838-7/R838-8 and R837-7 coverage | `867faf1e7321e1260f86701f01d7de0c94e67490` |
| Docs | CLEAN | Complete narrow diff; moved-figure sweep; live PR body; publication hashes | R838-9 | `867faf1e7321e1260f86701f01d7de0c94e67490` |

The carried source coverage is at `234bc149ff888eb96659ecaaa5ce6e4fb27319d4`; this round explicitly checked the intervening artifact changes before carrying it to the head above.

## Integrity, real limits and pending duties

`integrity-final.txt` independently verifies all **1,622** superproject tracked blobs, modes and index entries, and every tracked blob/mode/index in the five initialized dependency submodules, against their exact gitlinks. Checkout status is clean. No source bytes required restoration. All extraction is under this packet's unpublished `scratch/`.

The **46** round-14 files match the outer manifest; **45** indexed files match their inner byte counts and hashes. Four specifically carried round-13 receipts also match the outer manifest. The archive commit is **unsigned**, and no detached signature was supplied. This review verifies content integrity, not cryptographic signer authentication.

No full banks, harness rebuilds, campaigns, hardware operations or hosted jobs were executed here. No manager source bank exists at this head, and none is claimed. Source execution evidence is the author's published receipts, with the narrow own checks identified above. Executed jobs and skipped contexts are not interchangeable.

**Physical calibration NOT RUN.** Field skips are not hardware proof. The 8x8/1if failures, 8x8/2if load/build/row limits and the older optional suggestions remain in their publicly ruled follow-up scopes; this review does not infer a passing 8x8 flip.

The manager still owns:
- the current-dev merge candidate, using source base `66f713267f201d1a00d7f711e04b3a996d804dee` and then-live dev (assignment: `6b66f66d89cf25d2717687bcc2c3bf617685a99a`), builder/native validation and published receipts;
- hosted and local-replica acceptance, with executed versus skipped evidence identified;
- the second independent review, no review in flight, explicit merge authorization, post-merge containment and public issue/project state;
- the residue checklist and optional follow-ups.

No GitHub write, commit, push, merge, source fix or contact with the author occurred. `reproduce.py` recreates the focused checks from the exact checkout with the evidence commit fetched. Only MANIFEST.sha256-listed files and REPORT.md are publishable; scratch is excluded.

R838-9 FINISHED
