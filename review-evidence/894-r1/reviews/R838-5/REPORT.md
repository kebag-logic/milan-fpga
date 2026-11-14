[R838] POSITIVE - exact head 7398ec0aeea468d92ff642a03a06e291a0cd58d1

R838-5 independently applied Conformance, RTL, Robustness, Tests and Docs to the three-commit, six-file delta from `5b264bf26416108add32d7fe5abca5252ffde2cb`. All three prior MINOR findings and all three named RESIDUE items are resolved. No BLOCKER, MAJOR, MINOR or new RESIDUE remains from this review. Optional suggestions are consolidated below.

The reviewed tree is `2787f9fae40e581584d454e6cb476e68d1850487`. This is source-head review, not merge-candidate validation or hardware acceptance.

## Scope and reconstruction

Authority is [the round-10 assignment](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6873298790), read with the issue body and successive public decisions: [1x1 acceptance scope](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6867393730), [egress allowances](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6867990126), [direct-index ruling](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6870437042), and [queued-bound amendment](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6862465874). These amend the issue's initial both-point acceptance: this PR holds 1x1/1if; 8x8/1if is follow-up work and 8x8/2if remains reported.

Reconstruction followed AGENTS/CONTRIBUTING, the documentation index, issue/public decisions, REQUIREMENTS product ownership, FR_NFR 3.4.1, split architecture verification boundaries, mailbox/AECP interfaces, then diff/history and public evidence. The requested `66f713267f201d1a00d7f711e04b3a996d804dee..7398ec0a` inventory includes earlier imported work; this review applies the later-delta rule. Relevant dependencies include map validation/indexing, descriptor-derived geometry, actual slot storage, campaign build/diagnostic handling and current timing figures.

`independent-verdict.md` records my verdict and ledger before earlier public review findings were opened. No concurrent review report or private author material was read. Earlier findings were then reconciled below.

Evidence is [author-r10](https://github.com/kebag-logic/milan-fpga/tree/56e8f05bc2fa6d733d6b5c637bf1501d19dbe8dc/review-evidence/894-r1/author-r10), [author-r9](https://github.com/kebag-logic/milan-fpga/tree/56e8f05bc2fa6d733d6b5c637bf1501d19dbe8dc/review-evidence/894-r1/author-r9), [REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6874537343), and the live PR body. All **141 extracted published files** match the outer manifest's published SHA-256 values. The archive commit has **no signature**; content integrity was checked, but cryptographic signer authentication was unavailable. See `packet-audit.json` and `archive-identity.txt`.

## Named findings resolved at their causes

| ID / original severity / lenses | Artifact and authority | Resolution and verification |
|---|---|---|
| R837-4-1; MINOR; Conformance, RTL, Tests, Docs | `aecp_maps.c:158-191`, `aecp_map_mutants.py:58-64`, `aecp_mutants.py:885-950`; assignment item 1 | `MAP_DOMAIN` is `MAP_FIRSTS * MAP_CHANNELS`; `MAP_FLOOR` is separate. The assertion compares the **declared array's element count** with the shared-stride domain. My run catches the undersized-table plant on its own file and assertion words. Restoring the prior assertion lets it compile and makes the row escape with zero tests. `compile-row.log`, `compile-diagnostic.log`, `weak-assertion.log/json`. Both documents distinguish the safety bound from the layout floor. Resolved across every original lens; Robustness was also checked. |
| R838-4-F1; MINOR; Docs | `SPLIT_CONTROL_MEMORY.md:2342,2346,2347,2481`; assignment item 2 | All ten current cells equal independently executed flip checks, including refreshed 8x8/2if. Summary R4 is 12.85. Historical progression remains identified as historical. `docs-and-receipts.json`, both flip logs. |
| R838-4-F2; MINOR; Tests, Docs | PR #902, How to validate; assignment item 3 | Live command uses `Core.*Map*:Core.Every*`. My exact-head run passes **13 tests**, including the previously omitted ownership, format, partition and boot cases. `core-filter.log`. |
| R837-4-R1; RESIDUE; Docs | `aecp_arms.py:17-19`; source-comment rule | Comment now describes the geometry whose keys shared a slot under the former hash. Requested wording is present; no executable change. |
| R837-4-R2; RESIDUE; Docs | `SPLIT_CONTROL_MEMORY.md:2314,2322,2330` | Load table explicitly names the merge of `dev-soft-core` `0fb66211`, round 30's legs. Paragraph uses historical wording; figures are unchanged. Requested fixes and adjacent equivalent wording are present. |
| R838-4-R1; RESIDUE; Docs | PR current-state key-work bullet | Body now says **first REMOVE**, 1,165 visits against 2,078, preserving the measurement and correcting only its position. |
| R838-4-S10; SUGGESTION; Tests, Docs | PR share bullet; author-r9 `receipts/model/measured-inputs-final-pass.txt` | Resolved for the public claim: body reports supported overall maximum **149,490 of 200,000 cycles** and removes unsupported refused-edit attribution. Receipt lists maxima 93,346, 95,503, 138,064 and 149,490. No per-record attribution is inferred. |

The earlier reviews are [R838-4](https://github.com/kebag-logic/milan-fpga/pull/902#issuecomment-6873195590) and [R837-4](https://github.com/kebag-logic/milan-fpga/pull/902#issuecomment-6873294087). Their earlier resolutions remain valid where the delta changes neither implementation nor dependencies:

| Earlier IDs | Disposition at this head and cause-level artifact |
|---|---|
| R838-3-F1 / R837-3-1; R838-2-F2 | Retain resolution of collisions/quadratic work: direct indexing, range guards, validation-before-slot access, linked equal-key values and definition/counting tests are unchanged. The deficient compile guard is now resolved separately above. |
| R838-3-F2 / R837-3-2; R838-2-F3 / R837-2-3 | Retain corrected 49/238 bounds, both pace conditions, current named loads, 0.9 ms slice and ruling references at the previously named FR_NFR, service README, MAILBOX_SPLIT and section-13 sites. R838-4's dependent row discrepancy is resolved above. |
| R838-3-F3 | Retain image-growth reconciliation: earlier `.text` +180 B, ROM +184 B for 1x1/1if fixture and +176 B for seven other images due to alignment. Identity establishes zero further image change. |
| R838-3-R1 / R837-3-R1 | Retain corrected endpoints/count and collision description. Current delta is three commits; `long_notice.py` is unchanged. |
| R837-2-1 / R837-2-2 | Retain derived allowances and whole-ms `ceil((W+1)/P)` in `ctrl_loop.h`, `paced_rows.py`, `join_grade.py`. All are unchanged; current flip results pass. |
| R838-2-F1 | Retain horizon-free MRP run-out resolver with released, empty, late, absent and unresolved outcomes. `mrpdu_grade.py`, `join_grade.py` and controls are unchanged. |
| R838-2-R1/R2 / R837-2-4/5 | Retain dated source references, historical receipt attribution and separate planted/unplanted interval counts. No new prohibited source label occurs in this delta. |
| R838-1 F1 / R837-1-1 | Retain all tier-1 rows, 552-byte legal-notice storage, and largest-notice R4L/txL charges. Queue, model and harness code are unchanged. |
| R838-1 F2 / R837-1-2 | Retain public timing decisions, restored loop compile check and every-source tx/txL proof; later egress correction remains intact. |
| R838-1 F3/F4 | Retain native longer-notice-after-drain and ordinary-round-clear tests/mutants in `test_aecp.cpp`, `test_port_loop.cpp`, `aecp_owed_mutants.py`, `loop_step_mutants.py`. No related executable change. |
| R838-1 F5 / R837-1-3 | Retain corrected 0.9 ms slice in MAILBOX_SPLIT. |
| R838-1 F6/F7 / R837-1-5 | Retain rotating tier-1 order and conditional Domain/VLAN claim; SRP licensing, resume/reset and gap tests are unchanged. |
| R837-1-4 / R838-1 S5 | Retain scope resolution: 8x8/2if is reported, not undecided or passing. #910/#872 remain open duties. |
| R838-1 RS1 / R837-1-6 | Retain source-comment cleanup. Existing #746 material is not reopened. |

## Independent assessment and probes

The assertion now guards actual storage against the indexing domain. `place()` returns an index only for `first < MAP_FIRSTS` and `channel < MAP_CHANNELS`; its largest valid position is therefore below `MAP_DOMAIN`. The unsigned type and expansion of `MAP_SLOTS` remain equivalent to the prior definition. The floor stays 256; byte-sized slot **values** remain protected by `AECP_MAP_PAGE < 256`. Slot count and mapping-index width are distinct.

No runtime branch, validation precedence, atomicity, duplicate-removal multiplicity, queue, reset, CDC, clock, timer or backpressure behavior changes. Storage is still addressed only after geometry/range refusal. The floor is a measured layout choice under #909, not a timing theorem.

The campaign preserves its failure boundary: non-build rows require completed named test failures. A build row needs its own source basename and expected assertion words. Controls reject wrong words, another filename and a non-build row. BUILD is excluded from the claimed executable-test set. My weak-assertion probe proves the new control can fail, rather than crediting an arbitrary compile failure or zero-test execution.

The published seven-geometry probe covers five configurations, 16x4 and 16x32. Committed source compiles throughout; per-direction sizing is refused at the three geometries where it is too small; floor-only and an actually floor-sized array are refused at 16x32's 544-position domain. Those 35 compile outcomes were inspected, not rerun here. They supplement the independently executed 1x1 campaign and weak-assertion control.

Own foreground-supervised probes used at most eight concurrent compilation jobs, with disposable paths under packet `scratch/`:

| Probe | Result |
|---|---|
| Corrected core filter | 13 tests, zero failures, rc 0 |
| Campaign shard 257/274 | Undersized-table row caught, rc 0; compiler diagnostic retained |
| Prior assertion in disposable copy | Plant compiles; row escapes, campaign return 1; zero tests run |
| 1x1/1if flip | PASS, rc 0 |
| 8x8/2if flip | FAIL, expected rc 1; reported point only |
| Current table audit | Ten cells and summary R4 equal fresh checks |
| Published integrity | 141 outer-manifest hashes verified |

Current rows, milliseconds:

| Point | R4 | R5 | R6 | First queued | Last queued |
|---|---:|---:|---:|---:|---:|
| 1x1/1if | 12.85 | 72.91 | 68.80 | 14.51 | 126.46 |
| 8x8/2if, reported | 42.09 | 189.14 | 177.28 | 20.24 | 626.87 |

The fresh 1x1 check also confirms txL **48.09/49**, R4L **188.39/238**, tx **29.86/49**, and ACMP/ADP/MAAP **28.44/26.83/26.95**, each within 30. Last queued fits 130, not the original 125. Unchanged published loads are **0.513/0.509**, below 0.70.

## Sweep-skip evidence

The image inventories have identical paths and SHA-256 values for **332 files: 8 ELFs, 8 binaries and 316 objects**, covering fixture/platform at 1x1/1if, 1x1/2if, 8x8/1if and 8x8/2if. Comment headers are excluded from entry comparison. The recorded same-path baseline rebuild reproduces all entries. The floor-264 control changes 24 entries: eight ELFs, eight binaries and eight map objects. The build/hash scripts enumerate these outputs rather than one selected object.

The source delta supports that proof: only constant factoring/static assertion placement, tests and documentation change. Runtime operations, generated geometry, RTL, harness legs, timing graders and build inputs do not. The assignment's every-image condition is met by the published evidence, supporting carry-forward of round-9 measurements and skipping the four-shard sweep and harness legs. This is **receipt verification and source analysis**, not an independent image rebuild. Baseline-rebuild/control claims are summary receipts; separate control binaries and complete control hash inventories are not published in this packet.

Carried sweep receipts total **65 suites, 2,713,040 checks, zero failures/timeouts**. The exact-head workflow table counts **139 rc-0 steps, 226 NOT RUN entries with reasons, zero bad**. These are local workflow-step executions, not hosted jobs. Firmware receipts report the suite passing, coverage over 39 files, and 274/274 AECP plants caught. Published docs checks report zero findings; flip self-test reports 555/555 controls refused. No manager source bank is claimed or inferred. Hosted/act acceptance remains the manager's responsibility under split-PR policy.

All eight image-size receipts remain within caps. The 1x1/1if fixture retains 16 ROM bytes inside its allocation; the 8x8/1if platform remains at its 56.0-tile cap. Identity preserves this measured candidate; it does not protect a later merge from placement drift.

## Optional suggestions consolidated

Every row is SUGGESTION, with all attributable lenses. None prevents clean coverage. Unchanged optional items are retained rather than made new requirements.

| ID / lenses / artifact | Authority/evidence and impact | Optional outcome and verification |
|---|---|---|
| R838-5-S1, retaining R838-4-S1; Docs; AECP README owed ordering | Public decision permits a later response before an earlier notice; readers may miss the consequence. | Explain with two controllers editing one field; compare response/notice order. |
| R838-5-S2, retaining R838-4-S2; RTL; `aecp.c` counter reset | Prior redundant defensive reset is unchanged. | Explain the guard or remove only after proving the invariant; check queue/retry tests. |
| R838-5-S3, retaining R838-4-S3 / R837-1-8; Tests; `aecp_owed_notice_steps.py` | Offline model/string anchors remain; native tests supply execution evidence. | Drive compiled behavior from a scenario; show a behavioral plant fails. |
| R838-5-S4, retaining R838-4-S4; Tests; measured-input inventories | Complete counts/maxima and longer pressure samples would strengthen measured-cost reuse. | Publish per-term counts/maxima and longer expiry pressure; reconcile raw records and padding. |
| R838-5-S5, retaining R838-4-S5 / R837-1-7; Tests; `rows_tiers.py` ranking | Unsolved -1 can outrank a solved score below -1; current passing choice is unaffected. | Rank unsolved last before relying on mixed failed searches; add an ordering control. |
| R838-5-S6, retaining R838-4-S6; Tests; ACMP decline bound | Current bound remains conservative. | Tighten only with source-derived proof and a mutation control. |
| R838-5-S7, retaining R838-4-S7 / R837-4-S5; Docs; author-r10 `INDEX.md`, `scripts/index.py`, outer manifest | 64/65 inner rows match. Publication redaction changes only `scripts/index.py`: listed 1,212 bytes/hash `96a791f1...`; published 1,225/hash `4af1a900...`. Outer manifest correctly records both and `path_redacted: true`, so integrity remains verifiable. A10-RULING is now present. | Regenerate after redaction, or identify inner hashes as pre-publication and outer manifest as authoritative. Verify final sizes/hashes. Exact mismatch: `docs-and-receipts.json`. |
| R838-5-S8, retaining R838-4-S8; Tests; `mrpdu_grade.py:84` | Callback late-classification and owed-centisecond row origins differ; unchanged passing rows are not disproved. | Align origins or explain the distinction; add delayed-callback control. |
| R838-5-S9, retaining R838-4-S9; Tests, Docs; H-81N receipt | Outside this acceptance, rc-1 diagnostic would distinguish build failure from measured miss. | Publish reason and compare with the leg log. |
| R838-5-S11, retaining R837-4-S1; Tests; `place()` first-coordinate guard | Prior first-range-unchecked plant survived; product geometry makes it unreachable. | Add first-coordinate edge test with matching descriptor; show plant fails. |
| R838-5-S12, retaining remaining R837-4-S2; Docs; floor discussion | #909 citations are now resolved; optional margin explanation remains. | Explain placement-sensitive record margin and assumptions; compare load table/counterfactual. |
| R838-5-S13, retaining R837-4-S3; Robustness, Docs; `SPLIT_CONTROL_MEMORY.md:2461`, format verdict | Domain safety depends on product admission of declared output format and fixed cluster widths. | Name that precondition and widen domain when adaptation changes it; inspect format verdict/generated keys. |
| R838-5-S14, retaining R837-4-S4; Robustness, Docs; `struct edit` | Wide geometry grows table to 544 bytes; static-frame report is not whole-call-chain stack proof. | State integration limit and measure target call chain before wider image support. |
| R838-5-S15, retaining R837-4-S6; Tests, Docs; prior item-2 receipt headers | Earlier subset runs apply through unchanged map/test bytes; explicit provenance saves reconstruction. | Name run heads/source-identity span; compare blobs. |

## Reviewer-owned completion ledger

Each lens was applied to the delta and affected dependencies. Untouched behavior retains prior assessment under the assignment; no open MINOR or greater finding is carried as clean.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #894 assignment/amended FR_NFR 3.4.1; `aecp_maps.c:158-191,212-218,379-386`; both flip logs; image/cap evidence | R838-5 | 7398ec0aeea468d92ff642a03a06e291a0cd58d1 |
| RTL | CLEAN | `aecp_maps.c:158-218` array/count arithmetic and runtime guards; six-file delta with no HDL/pin change; 332 image hashes | R838-5 | 7398ec0aeea468d92ff642a03a06e291a0cd58d1 |
| Robustness | CLEAN | Actual-array bound; illegal/outside-key paths; native 13-test selection; published seven-geometry probe; own weak-assertion control | R838-5 | 7398ec0aeea468d92ff642a03a06e291a0cd58d1 |
| Tests | CLEAN | `aecp_map_mutants.py:58-64`; `aecp_mutants.py:885-950`; compiler diagnostic, control-failure and 13-test logs; firmware/workflow receipts | R838-5 | 7398ec0aeea468d92ff642a03a06e291a0cd58d1 |
| Docs | CLEAN | `SPLIT_CONTROL_MEMORY.md:2314,2346,2347,2461,2462,2481`; AECP README:213-242; `aecp_arms.py:17-19`; live PR body; ten-cell audit and finding dispositions | R838-5 | 7398ec0aeea468d92ff642a03a06e291a0cd58d1 |

## Limits, integrity and pending duties

- No full parent/processor/timing/synthesis/builder banks, target harness legs, hardware, Docker/act, privileged actions, GitHub writes, author contact, source fixes, commits, pushes or merges were performed. No sub-agents were used. The pinned simulator was not invoked. Source validation receipts are the author's; no manager source bank exists at this head.
- Physical calibration was NOT RUN. Field skips and commit-side simulation intervals are not hardware proof. S12b still owes the 180-240 ms wire capture on the final flip image before continuing its soak.
- #908 stays open until original 125 ms last-notice and 40 ms txL bounds at 20 cs can be restored. #909 placement sensitivity, 8x8/1if follow-up and 8x8/2if #910/#872 obligations remain. This verdict does not close them or authorize the default flip.
- Manager duties: obtain both independent current-head verdicts; ensure no round remains in flight; apply hosted/act policy; validate the **current-dev merge candidate**, including builder/native banks, at merge turn. Source base is `66f713267f201d1a00d7f711e04b3a996d804dee`; supplied live dev is `b7d692952305e4e0e132abb8f99c339eeb17a873`, subject to refresh. No candidate was constructed or validated here. After an authorized merge, containment and issue/project completion remain required.
- `checkout-integrity.json` hashes all 1,619 tracked parent blobs and verifies filesystem modes, exact index entries and absence of hidden index flags. All five populated submodules match pinned commits, blobs, modes and indexes; none has untracked files. Sixth gitlink `external` remains unpopulated as received, with index/tree pin verified. No checkout source was edited; plants/builds are under packet `scratch/`.
- Publish only REPORT.md and MANIFEST.sha256 entries. Portable scripts and raw focused receipts are listed there. `reproduce.sh CHECKOUT PACKET` reconstructs public extraction and focused checks; the evidence commit must be available in CHECKOUT. Disposable trees are excluded.

R838-5 FINISHED
