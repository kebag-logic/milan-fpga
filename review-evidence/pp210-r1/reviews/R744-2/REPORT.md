[R744] POSITIVE - exact head 0ea635ea22eeb6d97335c4e814eede1ac0d67ebc

Issue #210 / PR #211, round R744-2. Delta review from `18a4dc1fcf91528a52737d5ea830b5acd5d543c4`; original source base `a9e84b66d4cd0c331c8d6f2c1a71a62fcc824645`; exact tree `1833cde6be59abcfb24e1ba5b461c8fa8159fc2b`.

All five assigned factual findings are resolved at their causes. The new inventory derivations reject independently planted drift. No open BLOCKER, MAJOR or MINOR remains in this delta assessment. One wording residue and four previously published suggestions are recorded below. This verdict does not assert completion of hosted acceptance or authorize a merge.

**Scope and independence**

The supplied repository instructions were read first; the tracked tree has no AGENTS.md or CONTRIBUTING.md. Reconstruction then covered `docs/README.md`, [issue #210](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/210), the [parent plan](https://github.com/kebag-logic/milan-fpga/issues/797#issuecomment-6518880512), the public scope and [round-2 recurrence rule](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/210#issuecomment-6521384962), interface and requirement authorities, original-base diff/history, and the twelve-path delta. The six new commits preserve the round-1 head as an ancestor.

Before the independent verdict and five-lens ledger were saved, PR data was fetched only through the permitted metadata command. No PR comments, submitted reviews or inline reviews were fetched in that interval. The reviewer’s own round-1 report was read after the independent diff pass. Public author material was read only from the pinned published evidence directory. Other reviewers’ reports were first read after `INDEPENDENT-VERDICT.md`, its hash and timestamp were written. No private author files, management checkout, other review checkout or private scratchpad was accessed. Public reconciliation preserved the positive delta verdict.

**Prior findings: explicit disposition at this head**

| Prior ID and attributable lenses | Disposition and cause-level evidence |
|---|---|
| R744-1 F1 / R743-1 F4 — Conformance, Docs | **Resolved.** `docs/architecture/02_interfaces.md:283` now attributes the shaper’s operating value to IEEE 802.1Q-2014 §34.3(d), SRP ownership to §34.3.2 with §34.3(c), and per-stream bandwidth to §34.6.1. The nonexistent §34.6.1.1 is removed from the current page. The inventory’s evidence row now names this correction. Full adopted-edition clause-body access remains limited as stated below. |
| R744-1 F2 / R743-1 F5 — Conformance, RTL, Docs | **Resolved and gated.** `docs/architecture/06_aecp_engine.md:1427` says 30 operations; :1434 includes SHIFT_R and its 64-bit logical-right-shift semantics using `imm[5:0]`. These match `hdl/aecp/ucpu_pkg.sv:51` through the final enum member at :87 and `hdl/aecp/KL_aecp_ucpu.sv:681`. The new derivation checks both count and complete operation set. Retained round-1 construction evidence accounts for all 13 emitted opcode-29 words; generators and ROM bytes are unchanged. |
| R743-1 F1 — Docs | **Resolved by linking.** `README.md:28` links to the inventory’s Retired heading and states no count. The heading contains the three retired pages, each bannered. |
| R743-1 F2 — RTL, Docs | **Resolved.** `docs/architecture/02_interfaces.md:8` identifies the processor-owned identify-button synchronizer and its enable condition. `KL_aecp_notify.sv:1022` guards the implementation; :1031–1032 declare the two synchronization registers; :1096–1097 implement the stages. This agrees with §2 rule 3. |
| R743-1 F3 — Tests, Docs | **Resolved by linking.** `tb/nvm_port/README.md:6` describes suite bounds followed by randomized-harness bounds and links to the Makefile’s `BUILDS`. `tb/nvm_port/Makefile:41` derives seven builds, with the execution sequence at :45–53. The full figures campaign was not rerun; every README-derived input to it is unchanged across base, round 1 and this head. |
| R743-1 F6 — Conformance, Docs | **Requested disclosure alternative satisfied.** The prior finding explicitly allowed either correcting diagram 22 or listing it under the PR’s “Not fixed here.” The exact-head PR body now lists `docs/diagrams/22-aecp-descriptor-fetch.svg:155`, the invalid clause/budget claim, and a concrete replacement. The published handoff and issue’s round-2 ready comment also disclose it. The SVG itself is unchanged and still wrong; this is resolution by the prior finding’s explicit alternative within the Markdown/gate scope, not a corrected diagram or proof of that claim. It remains a follow-up obligation. |
| R743-1 RES1 — Docs wording | **Resolved.** The two lane parentheticals at `docs/00_MILAN_COMPLIANCE_REVIEW.md:577,588` and the `tb/pp_top/README.md:2728` heading are corrected. The additional lane reference at `tb/adp_engine/README.md:330` is also replaced with issue references. |
| R743-1 RES2 — Docs wording | **Resolved.** `docs/GLOSSARY.md:87` removes the copied clock count and retains the link to the owning guide. |

The source excerpts and independent mutation receipts support the table. The [prior public report](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/211#issuecomment-6521378606) was consulted only during reconciliation, including its precise alternative outcome for F6. No submitted or inline review findings were present at the final query.

**Remaining residue and suggestions**

**R744-2 RES1 — RESIDUE — Docs.** Artifact: `tb/adp_engine/README.md:330`, in the row edited this round. Its existing parenthetical “(review R406-1 F-1)” survives the lane-label removal. Authority: #210’s no-review-label rule, subject to the owner’s existing-label handling. Impact: provenance wording only; no measurement, clause, code, generated artifact or privacy change. Exact fix: delete that parenthetical after “clears the row,” retaining the behavior and the issue references later in the row. Verification: inspect that row and rerun the link gate. This is inherited residue, not a newly introduced label occurrence, and leaves Docs CLEAN.

A claim that all changed files or added diff lines are label-free would be false: unchanged review identifiers survive in edited mutation records. The occurrence comparison finds **no newly introduced workflow-label occurrence** from either the original base or round-1 head. The four targeted lane labels are removed. Existing source-comment labels remain outside this delta under #746; the disclosed mutation-record labels still prevent treating this PR as full closure of #210.

The following suggestions from the prior public review remain optional, with no current-tree contradiction demonstrated:

| ID / severity / lenses | Artifact and evidence | Impact, desired outcome and verification |
|---|---|---|
| R743-1 S1 / SUGGESTION / Robustness, Docs | `scripts/check-doc-inventory.py:30,131`; inventory row parsing records the displayed path without checking that its link resolves to that same file. Prior public probe passed with a link to another existing page. | Optional hardening: compare the normalized link target with the row path. Verify with a swapped valid destination. No present mismatched row is asserted. |
| R743-1 S2 / SUGGESTION / Robustness | `scripts/check-doc-inventory.py:40`; the file pathspec is lowercase `*.md`. | Optional support for uppercase Markdown extensions. Verify with an unlisted `NOTES.MD`. No such tracked file exists at this head. |
| R743-1 S3 / SUGGESTION / Robustness, Docs | `docs/INVENTORY.md:22` says stale evidence names a tracking issue; the gate checks that evidence is nonempty. | Optional enforcement of a tracking reference for stale rows. Verify with a stale fixture lacking one. No stale inventory row exists at this head. |
| R743-1 S4 / SUGGESTION / Conformance, Docs | `docs/GLOSSARY.md:17` and the existing precedence statements cite Milan §5.5.2.1; the prior clause review distinguishes its ACMP-specific rule from the general §4.2 rule. | Optional citation precision: cite §4.2 beside §5.5.2.1 for the general statement. Verify against the adopted Milan edition. The precedence principle itself was not contradicted; this review does not claim an independent reread of that clause. |

**Execution and artifact-specific evidence**

| Check | Result | Receipt |
|---|---|---|
| Exact-head documentation gates, `make -j16 check` | rc 0; includes the 25-case inventory selftest, 63-file inventory, link checks, figures, freshness, identifiers and command/matrix checks | `docs.log`, `docs.rc` |
| Add valid fake operation to the actual enum | make rc 2; derives 31 rather than 30 and reports the missing operation by name | `fake-op.log`, `.rc` |
| Drop `inventory` row from actual 09 §7 table | make rc 2; names the missing target | `drop-target-row.log`, `.rc` |
| Drop `inventory` prerequisite from actual `check:` rule | make rc 2; reports that the table names a target the rule no longer runs | `drop-check-prerequisite.log`, `.rc` |
| Restore old 29-operation heading and omit SHIFT_R | make rc 2; rejects count and missing operation | `old-uisa.log`, `.rc` |
| Clean controls before and after probes; links after restoration | rc 0 throughout | `inventory-clean.*`, `inventory-restored.*`, `links.*`, `probe-restored-diff.*` |
| NVM figures dependencies | Claim coverage, figure matches, measurement matches, waivers, arm table, matrix and size checks equal at all three revisions; coverage and size diagnostics empty | `nvm-derived-inputs.json` |
| Source construction and integrity | Only Markdown, Makefile and documentation checker changes; 754 tracked blobs/modes and exact index tree verified; no submodule gitlinks | `final-integrity.log`, `delta-audit.log` |

The derivations compare the µISA table to the source enum, including the documented aliases, and 09 §7 to the current Makefile’s check prerequisites. They are syntactic checks of those actual file forms, not general language parsers. Source-shape rejection, missing inputs and ordinary inventory failures are covered by the selftest; the independent probes above exercise the real file-to-gate wiring and specific manager-requested drift.

No hardware compilation or simulation was necessary for the delta. The retained reviewer-owned round-1 evidence includes documentation/static checks, RTL lint, five focused suites (76/211/586/1360/118 checks), and byte-identical regenerated ROMs. Eleven selected public round-1 artifacts were hash-verified against the pinned manifest (`retained-evidence-verification.log`). Their source, generators, suite recipes and execution inputs remain unchanged; those executions are not relabeled as new exact-head runs. All local commands stayed under a joined foreground process; documentation prerequisites used at most sixteen make jobs. No full bank or hardware run was started.

**Reviewer-owned ledger**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #210 acceptance/scope; docs conventions and requirements; corrected 02 clause attribution and published adopted-edition account; 06 instruction inventory; prior diagram finding’s explicit disclosure alternative | R744-1 unaffected evidence; R744-2 corrections and reconciliation | 0ea635ea22eeb6d97335c4e814eede1ac0d67ebc |
| RTL | CLEAN | Unchanged implementation/generator trees; enum, SHIFT_R execution, notify generate condition and synchronizer; retained ROM construction receipts | R744-1 construction; R744-2 source verification | 0ea635ea22eeb6d97335c4e814eede1ac0d67ebc |
| Robustness | CLEAN | Inventory derivations, parser refusal paths and selftest; four independent real-tree drift probes and restored controls; retained link-gate evidence | R744-2 derivations; R744-1 unchanged checker behavior | 0ea635ea22eeb6d97335c4e814eede1ac0d67ebc |
| Tests | CLEAN | Exact-head documentation gates; NVM recipe/build-count link and complete README-input equivalence; unchanged test/workflow sources; retained focused executions | R744-2 delta; R744-1 unchanged executions | 0ea635ea22eeb6d97335c4e814eede1ac0d67ebc |
| Docs | CLEAN | All twelve changed paths; retirement link, CDC exception, µISA table, NVM link, 09 gate description, inventory evidence, glossary and lane-label removals; residue and prior-findings reconciliation | R744-2; R744-1 unaffected pages | 0ea635ea22eeb6d97335c4e814eede1ac0d67ebc |

CLEAN means no unresolved defect within the applied delta scope; it does not certify unchanged deferred artifacts or pending executions.

**Public evidence, limits and manager duties**

The [pinned publication](https://github.com/kebag-logic/milan-fpga/tree/6c4944048d997343adecfdda2e43b2e0f4ba4b40/review-evidence/pp210-r1) contains the author’s round-2 handoff and PR-body narratives. Both match the published SHA-256 manifest. It does not contain raw round-2 gate logs or a detached signature. The publication commit’s verification metadata says **unsigned** (`evidence-publication.json`); a signed packet therefore could not be verified. Hash equality is verified, signature authenticity is not. Author-reported passes remain distinct from this review’s executed receipts.

At inspection, exact-head hosted runs [41049665225](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/actions/runs/41049665225) and [41049671908](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/actions/runs/41049671908) had successful documentation and portability jobs. Both suites jobs were still running lint/full-suite execution. Their traceability, mutation and NVM-figures steps were pending. The cached compiler-build steps were skipped, not the simulation jobs. `hosted-status.json` records job and step status; no pending or skipped context is counted as an executed pass.

Complete adopted-edition standard texts were not independently obtained this round. The clause correction is supported by the prior edition-specific evidence and the author’s published account of rereading §34.3(d), §34.3.2, §34.3(c) and §34.6.1, together with source/interface checks. No other edition was substituted. `authority-access.log` records this limitation. Unchanged normative statements keep the prior review’s coverage and limits; this is not an exhaustive new standards audit.

The unchanged diagram 22 clause/budget error, old source-comment clause references, µISA comments still saying 29, and existing workflow labels remain disclosed follow-ups. They must not be presented as corrected by this PR. The figure can be fixed using the replacement already published in the PR; the source comments and legacy labels need their assigned follow-up work.

No manager source bank exists or is inferred at this head. The public manager comments provide review starts, not execution receipts. The manager still owns hosted/act acceptance, the second independent positive review, the residue checklist, and validation of the actual current-dev merge candidate with builder and native banks at the merge turn (source base `a9e84b66`, supplied live dev `1e80128f0a467b58bf884b7d9bf62e013a2fb141`). No parent/processor/timing/synthesis/builder bank was run here. Physical calibration was **NOT RUN**; field skips and simulation evidence are not hardware proof.

Reproduction: `python3 probe-delta.py SOURCE PACKET` creates an exact-head disposable clone under `PACKET/scratch/`; `python3 run-docs.py DISPOSABLE_SOURCE PACKET` runs the documentation gates; `python3 verify-delta.py SOURCE PACKET` checks original-source integrity and NVM input equivalence. Only REPORT.md and files explicitly listed in MANIFEST.sha256 are publishable. Disposable trees and downloaded evidence remain under scratch and are excluded. The source checkout was never edited; probe-copy tracked bytes were restored, and original tracked bytes, executable modes, index, HEAD and absence of gitlinks were verified.

R744-2 FINISHED
