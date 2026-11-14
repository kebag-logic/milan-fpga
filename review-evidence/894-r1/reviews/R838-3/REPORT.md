[R838] NEGATIVE - exact head dd01b0afef87037ec485cd49b40a26b542854bdd

R838-3 applied all five lenses to the delta from `8a3791e44533d6b1cc26d486d0b18e7d83470dc1`. One MAJOR and two MINOR findings remain. The 1x1/1if rows pass, the egress and pace corrections hold, and the former join-horizon defect is resolved. The map-work guarantee remains conditional on geometry that the build does not enforce. This review demonstrates excess lookup work on accepted commands, not a measured target deadline violation.

The source tree is `4d7787fe81c9a90177d98e1afff98f216cb3b140`. The repository contract, documentation map, frozen issue and public decisions, requirements and relevant interfaces were reconstructed before implementation and evidence were examined. The requested `66f713267f201d1a00d7f711e04b3a996d804dee..dd01b0af` comparison was distinguished from this round's 29-file delta. Unchanged code retains its prior assessment unless a changed dependency affects it. There are nine commits in the latter range, not eleven.

The independent verdict and ledger were recorded in `independent-pass.txt` before reading prior public review findings. No other current-round report or private author material was used.

Authority: [round-8 ruling, items 1–6 and STOP conditions](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6867990126), [contingent bounds](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6858269025), [queued-bound amendment](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6862465874), and [1x1 merge scope and follow-up duties](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6867393730), alongside REQUIREMENTS product ownership, FR_NFR 3.4.1 and mailbox/AECP/SRP interface documents. Public decisions amend the original both-point acceptance; 8x8 failure is not silently counted as passing.

Published evidence means [archive 183cd03d, author-r8](https://github.com/kebag-logic/milan-fpga/tree/183cd03d60e9d51dd8e251bbd38ffe5b3c01ee66/review-evidence/894-r1/author-r8), plus [REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6870102413) and the current PR body. Author paths below identify that archive. All 66 author-r8 files match the root manifest's published SHA-256 values. This establishes content integrity against the manifest: the archive commit is unsigned, and no cryptographic signature was available to verify.

**R838-3-F1 — MAJOR — Conformance, RTL, Robustness, Tests, Docs — legal key collisions still defeat the map-work bound.**

- Artifacts: `sw/firmware/ctrl/aecp/aecp_maps.c:127–143,186–211,350–415`; `sw/firmware/ctrl/aecp/README.md:199–215`; `sw/firmware/ctrl/test/test_aecp.cpp:2619`; `sw/builder/endstation_builder.py:1463–1473`; `sw/firmware/ctrl/aecp/aecp_entity.py:19`; `aecp_shape.py:24`. Receipts: `maps-probe.log`, `hash-geometry.txt`; probes: `probe_maps.py`, `audit_hash_geometry.py`.
- Authority/evidence: ruling item 3 and the retained #904 contract require bounded linear work for accepted and refused legal-length edits, preserving behavior. `place()` linearly probes `(stream_or_cluster + 9 * channel) & 255`. The comment and README depend on distinct legal keys having distinct hashes, then say every configuration has that property. The static assertion checks table/index capacity only. Neither configuration validation nor descriptor/storage generation enforces hash injectivity.
- The five checked-in configurations have no aliased keys in their generated current dynamic-port geometry (`hash-geometry.txt`). That is a property of these configurations, not a proof over every accepted legal key set. The builder and entity generator accept a configuration derived from the existing 8x8 configuration with 16 dynamic outputs, four channels each. Output keys `(stream 0, channel 1)` and `(stream 9, channel 0)` collide at slot 9. No firmware source is changed by the probe.
- The native probe submits generated-geometry-valid commands to the exact head. Success status, number added and complete removal all hold. Only the existing counting contract fails:

| Mappings | ADD visits / bound `2(n+R)` | REMOVE visits / bound `2(n+R)` |
|---:|---:|---:|
| 8 | 8 / 16 | 40 / 48 |
| 16 | 16 / 32 | 80 / 96 |
| 32 | **144 / 64** | **496 / 192** |
| 63 | **714 / 126** | **2,268 / 378** |

For ADD the map starts empty. REMOVE reads the populated map twice, so `R=2n`. The 63-mapping request fits the 550-byte legal frame envelope. This is a distinct-key collision family; the new one-key value-chain controls do not cover it. The two-key functional collision test checks correctness, not work.

- Impact: R838-2-F2's original repeated-value cause is repaired, but the general work guarantee retains an unguarded collision path. Current-configuration timing cannot establish the broader claim. This finding does not invalidate the reproduced 1x1 model arithmetic or demonstrate that its 975 us record cost was exceeded.
- Required outcome: establish the ruled bound for every accepted geometry within its supported scope, with a falsifiable distinct-key collision control. A proof restricted to particular geometry needs a public scope decision and enforceable generation/build validation; a comment alone is insufficient. Preserve behavior and the unchanged definition oracle. Re-measure affected images/costs and recompute rows if implementation changes.
- Verification: run the supplied accepted-key probe, existing 8/16/32/63 counting controls and quadratic plants, and unchanged definition test. Enumerate accepted key domains or demonstrate the approved guard's refusal with a negative configuration control. The counterexample must be covered by a corrected proof or an explicitly approved, enforced scope.

**R838-3-F2 — MINOR — Conformance, Docs — current timing prose retains pre-egress bounds.**

- Artifacts: `tb/verilator/ctrl_service_budget/README.md:183`; `docs/design/SPLIT_CONTROL_MEMORY.md:2464`.
- Authority/evidence: ruling item 1 and `paced_rows.PACED_BOUNDS` hold paced R4L at 238 ms; `CTRL_LOOP_TX_BOUND_MS` holds MRPDU at 49 ms. The service README still calls R4L's bound the 240 ms response time and directly identifies `PACED_BOUNDS`. It also links the 30 ms decision to the owner question rather than the ruling. The memory document's current THE TIERS bullet still derives 50 ms without egress, immediately before identifying the following three bullets as historical. Its new section above correctly states 49/238.
- Impact: readers obtain inconsistent current numeric contracts. These are bound/clause claims, not wording-only residue. The original R838-2-F3/R837-2-3 sites were substantially corrected, but the same class of discrepancy remains in dependent text.
- Required outcome: state 238 ms at commit for R4L, derived from the 240 ms wire endpoint less both allowances; state 49 ms after 190 ms plus the 1 ms egress allowance for MRPDU. Link the 30 ms decision to ruling 6844175391, optionally confirmation 6844947317. Keep historical values explicitly historical.
- Verification: compare these passages with FR_NFR 3.4.1 and `model-audit.txt`; run documentation checks after editing.

**R838-3-F3 — MINOR — Tests, Docs — universal +176 B image growth contradicts its receipt.**

- Artifacts: author `receipts/images/every-image-final.txt:2,10–11`; `HANDOFF-r8.md`, item 3 and image summary; REVIEW READY's image paragraph. Reviewer receipt: `receipt-audit.txt`.
- Authority/evidence: reproducible image-cap evidence is required. The receipt gives the 1x1/1if fixture as 110,584 B at the head and 110,400 B at the starting head: **184 B**, not 176 B. The other seven pairs differ by 176 B. The receipt comment and public summary say every image gains 176 B.
- Impact: growth/attribution figures disagree, although the listed cap comparison remains passing: 110,584 of 110,592 B leaves eight bytes in that ROM granule. No cap failure is alleged. Correcting a stated measurement delta is not RESIDUE under this round's rule.
- Required outcome: reconcile endpoints and growth. If both endpoints are correct, identify the fixture's +184 B separately and explain the additional eight bytes if attributing all growth to the rewrite. Preserve historical receipts and publish a correction as needed.
- Verification: subtract each matching pair and check the summary, ROM/SRAM needs and tile totals. Rebuild only if an endpoint is disputed.

**R838-3-R1 — RESIDUE — Docs — inaccurate public delta count.**

- Artifact: PR Status and REVIEW READY opening: “11 commits on round 7's `8a3791e4`”.
- Evidence: `git rev-list --count 8a3791e4..dd01b0af` returns nine; `delta-history.txt` lists them.
- Impact: history/navigation wording only; no source, measurement, timing bound or verdict changes.
- Exact fix: replace the phrase with “the delta from `8a3791e4` to `dd01b0af`”.
- Verification: preserve the exact endpoints and compare the public history. Non-blocking residue.

**Prior findings reconciled at this head.** Prior findings were opened after the independent pass: [R838-2](https://github.com/kebag-logic/milan-fpga/pull/902#issuecomment-6867751113), [R837-2](https://github.com/kebag-logic/milan-fpga/pull/902#issuecomment-6867959154).

| Prior finding | Disposition and cause-level evidence |
|---|---|
| R837-2-1, egress | Resolved. `ctrl_loop.h:336–360` derives 49 ms; `paced_rows.py:43` derives 238; `join_grade.py:28–34` derives 181–239. FR_NFR:373,381,424–426 accounts for allowances. The egress-free derivation is planted. F2 concerns remaining prose, not this corrected derivation. |
| R837-2-2, pace count | Resolved. `paced_rows.edits`, `gate_most`, `count_findings` exercise the whole-millisecond bound. The old rule is refused; own `model-audit.txt` confirms P=7 is smallest. |
| R838-2-F1, silent join horizon | Resolved. `mrpdu_grade.resolve` searches without a time horizon and classifies all five outcomes. `join_grade.held`/`run.stated_misses` fail late/absent outcomes. Own `join-probe.log` catches 291/500 ms and the old-horizon mutation while preserving empty, unresolved and owed-frame cases. Published regrading covers intervals and timer-to-MRPDU rows. |
| R838-2-F2, map work | Original same-key chain and invalid-geometry rescans resolved; **overall guarantee retained as F1**. Four native tests pass unchanged: definition, work, collision correctness and restored ownership (`maps-baseline.log`). Published plants catch n(n+1)/2 at 8/16/32/63. Distinct-key collisions remain unbounded by the stated contract. |
| R838-2-F3; R837-2-3 | Original FR_NFR SRP row, AECP 130 ms, mailbox 0.9 ms, header queued bound, stale R4 and principal 30 ms citations corrected. Remaining dependent contradictions are F2. FR_NFR now states 950–1050 ms periodic and 9.96–15.04 s LeaveAll spans. |
| R838-2-R1; R837-2-4 | Identified additions corrected to dated rulings. The added-source scan found no new issue-comment or review-round identifiers. Existing #746 material was not reopened. |
| R838-2-R2; R837-2-5 | Resolved by the new public explanation without rewriting history: round-7 `rows-1x1-final.txt` is identified as pre-restatement and the final receipt is named. Current counts distinguish 54 unplanted intervals from 57 including C-R1's three. |
| R838-1 F1; R837-1-1 | Prior resolution retained: all tier-1 channels have rows; 552-byte slots cover legal notices; R4L/txL charge the large notice. This delta's bound/cost consequences were rechecked. |
| R838-1 F2; R837-1-2 | Prior model/compile-time resolution retained; this round resolves egress. `ctrl_loop.c:203–204`, tx/txL and flip controls remain. |
| R838-1 F3/F4 | Prior native test/mutant resolution retained. Longer-notice test `test_aecp.cpp:1724`, ordinary-round test `test_port_loop.cpp:1674`, and clear at `ctrl_loop.c:332` are behaviorally unchanged. |
| R838-1 F5; R837-1-3 | Original stale slice resolved at 0.9 ms in MAILBOX_SPLIT:390. |
| R838-1 F6/F7; R837-1-5 | Prior order and Domain/VLAN resolution retained. `MAILBOX_SPLIT:385–394`, `srp/README:235–241`, `srp_mbx.cpp:1598,1635` and licensing/resume logic remain consistent. |
| R837-1-4; R838-1 S5 | Scope resolution retained: 8x8/2if is reported, its build cost explicitly refuted, and #910/#872 duties retained. |
| R838-1 RS1; R837-1-6 | Original comment cleanup retained; no new equivalent instance found in this delta. |

**Passing evidence and its limits.**

The reviewer reran `flip_grade.py --check --point 1x1/1if`: all eleven rows pass. The reviewer reran `--selftest`: 555/555 controls refused. See `flip-check.log`, `flip-selftest.log` and their return-code files.

| Row | Every-source ms | Bound ms |
|---|---:|---:|
| R4 | 12.82 | 20 |
| R4L | 173.37 | 238 |
| ACMP / ADP / MAAP | 28.35 / 26.76 / 26.88 | 30 each |
| First queued notice | 14.50 | 20 |
| R5 / R6 | 72.71 / 68.62 | 90 each |
| Last queued notice | 125.84 | 130 |
| tx / txL | 29.78 / 47.98 | 49 each |

`model-audit.txt` reproduces the pace table: P=6 gives txL 53.86; P=7 gives 47.98 with R4L 173.37; P=11 gives 45.65/233.37; P=12 fails R4L. No search beyond 11 is needed here, although the generic model allows 13. The slice is 900 us, join timer 19 cs and queued-bound derivation has no mismatch. Published load is 0.513 at the pin and 0.509 in the second column, below 0.70; relevant load arithmetic is unchanged by this delta.

`long_notice.refused_edits` adds 550-byte collision/conflict commands, expected BAD_ARGUMENTS, to record-cost measurements. Published exact-head maxima are 92,766 cycles for REMOVE, 86,504 for ADD, and 23,014–79,281 for refused cases. The collision pass is 96,142 against THE SHARE's 200,000 cycles. At 100 MHz, padding 92,766 cycles by 5% and rounding upward to 5 us gives 975 us. The exact-head largest-notice item is 34,370 cycles, giving 365 us. These conversions were checked; target runs were not repeated. F1 exercises different geometry.

Published round-7 regrading reports 57 intervals, 185.645–190.025 ms, none late/absent/unresolved, and timer-to-MRPDU rows 1.29242, 2.24512 and 3.440 ms. The exact-head receipt independently sums to **57 intervals across 14 runs**, **54 across 13 unplanted runs**, range **185.468–190.059 ms**. All are inside 181–239. The planted run is not represented as an independent clean campaign. These are published measured summaries, not reviewer re-execution of target traces.

Image receipts list fixture totals 40.5/41.5/54.0/59.0 and platform totals 42.5/43.5/56.0/60.0 RAMB36 for 1x1/1if, 1x1/2if, 8x8/1if and 8x8/2if respectively. Every listed ROM/SRAM need and tile total fits its applicable allocation/cap. The 1x1/1if fixture has eight ROM bytes remaining in its current block, not eight bytes below the overall 56-tile cap. The 8x8/1if platform occupies its 56.0-tile cap with 1,864 ROM bytes inside its allocation. F3 concerns growth attribution only.

Author source receipts report four sweep shards passing, 65 suites and 2,713,040 checks; native/mutation campaigns passing, including 269 AECP plants; tier controls 971/971 and 246 harness mutants caught. The workflow inventory contains **138 initial zero exits, one initial BAD 92/UNKNOWN, and 226 NOT RUN entries with reasons**. These are locally executed job steps, not hosted contexts. The first standalone simulation aggregate reports seven passes and `test_soc_timing_cuts` timing out at 900 s. The separate rerun receipt names the same clean head and 900 s setting, with eight passes. It clears that step's execution gap as published evidence; the first UNKNOWN is neither a pass nor a functional failure. Load as its cause remains the author's attribution. No manager source bank is claimed or inferred.

**Optional findings carried forward for one author pass.** Each is SUGGESTION and does not independently prevent coverage.

| ID / lenses / artifact | Evidence and impact | Optional outcome and verification |
|---|---|---|
| R838-3-S1; Docs; `aecp/README.md` owed ordering (R838-2-S1) | Accepted ordering permits a later response before an earlier notice, potentially exposing an older value afterward. No new protocol breach asserted. | Explain the consequence beside the contract; check a two-controller example. |
| R838-3-S2; RTL; `aecp.c:708` (R838-2-S2) | Redundant `counter_event` reset remains; removal is not required by this delta. | Retain with rationale or remove after proving the invariant; verify queue/retry tests. |
| R838-3-S3; Tests; `tests/steps/aecp_owed_notice_steps.py` (R838-2-S3/R837-1-8) | Scenario layer remains an offline model with string anchors; native tests supply execution evidence. | Optionally connect a scenario to compiled behavior and show a behavioral mutation fails. |
| R838-3-S4; Tests; cost/sample inventories and `long_notice.py` (R838-2-S4/R837-2-S3) | Refused inputs broaden coverage, but three join intervals per 1x1 group remain a small sample; no complete per-term maximum/sample inventory is published. | Publish counts/maxima and longer tier-1 pressure across expiries; check padding against raw records. F1 separately covers the blocking proof. |
| R838-3-S5; Tests; `rows_tiers.py:686` (R838-2-S5/R837-1-7) | An unsolved row scores -1 and can rank above a solved row worse than -1. Current passing selection is unaffected. | Before relying on such a mixed search, rank unsolved below solved rows and add an ordering control. |
| R838-3-S6; Tests; `acmp_mbx.c:122–175`, `rows_grade.acmp_items` (R837-2-S1) | A tighter decline bound may return margin; the retained bound is conservative. | Tighten only with source-derived proof and a mutation control; current acceptance does not depend on this. |
| R838-3-S7; Docs; author `INDEX.md` (R837-2-S2) | It lists absent `A10-RULING.md`; the two indexed scripts differ from their listed hashes. All published files match the root manifest, so integrity was verifiable. | Generate the index from published bytes, or explain redaction and name the root manifest as final authority; verify every indexed file/hash. |

**Reviewer-owned completion ledger.** Every lens was applied; none is clean while F1 remains open. Prior coverage is not used to clear changed map code or its dependencies.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN: F1, F2 | Issue/rulings; FR_NFR:365–450; `ctrl_loop.h:328–360`; `aecp_mbx.h:38–64`; `aecp_maps.c:86–415`; bound/pace audit and legal-key probe | R838-3 | dd01b0afef87037ec485cd49b40a26b542854bdd |
| RTL | UNCLEAN: F1 | No HDL/submodule delta; map termination, byte indexes, counts, linked values, validation order/atomicity; loop static checks; wrap-safe pace gate; generated geometry and image receipts | R838-3 | dd01b0afef87037ec485cd49b40a26b542854bdd |
| Robustness | UNCLEAN: F1 | Accepted/refused legal-length commands; same/distinct-key collisions; semantic oracle; join boundary/empty/late/absent/unresolved/owed-frame controls; retained reset/backpressure paths | R838-3 | dd01b0afef87037ec485cd49b40a26b542854bdd |
| Tests | UNCLEAN: F1, F3 | `test_aecp.cpp`, map mutants/work arm; `long_notice.py`; join/pace controls; 555-control run; native counterexample/baseline; archive and arithmetic audit | R838-3 | dd01b0afef87037ec485cd49b40a26b542854bdd |
| Docs | UNCLEAN: F1, F2, F3 | AECP/SRP READMEs; MAILBOX_SPLIT; SPLIT_CONTROL_MEMORY section 13; service README:151–190; FR_NFR 3.4.1; PR/REVIEW READY; packet/index and source-comment delta | R838-3 | dd01b0afef87037ec485cd49b40a26b542854bdd |

**Real limits and pending manager duties.**

- No source fixes, commits, pushes, GitHub writes, author contact, other-checkout edits or full validation banks were performed. All disposable test/config/build material is under `scratch/`. Source remained untouched. `tree-verification.txt` independently hashes tracked blob bytes, checks modes/index entries and verifies five required initialized submodules against gitlinks. The external submodule remains intentionally uninitialized.
- Native probes measure behavior and operation counts, not target execution time. The five-config audit covers generated current formats, not all accepted configurations or future format changes. The accepted counterexample refutes the universal claim; existing configurations' lack of aliases does not enforce the property at build time.
- Target campaigns, raw target trace regrading and every image were not rebuilt here. Published author receipts were hash-checked, read by section and spot-checked arithmetically. Previously assessed costs carry forward only where dependencies are unchanged. This is not a fresh maximum-plus-5% inventory for every term.
- Hosted CI does not execute on split PRs; no hosted skip counts as execution. The manager owns hosted/local acceptance. No manager source bank exists at this head.
- Physical calibration is **NOT RUN**. Field skips and simulation are not hardware proof. S12b still owes its first-ten-minute per-participant wire capture at 180–240 ms; a miss stops the campaign.
- Resolve F1–F3 and obtain fresh independent verdicts on affected artifacts before merge. Carry R1 to the residue checklist; suggestions remain optional. This report grants no approval.
- The manager must validate the actual current-dev merge candidate, including builder/native banks, recording both parents and its tree. Source base: `66f713267f201d1a00d7f711e04b3a996d804dee`; supplied live dev: `b7d692952305e4e0e132abb8f99c339eeb17a873`, to be refreshed at the merge turn. Source receipts are not candidate validation. Finish review, obtain explicit merge authorization and prove post-merge containment.
- Keep #894 open for the authorized 8x8/1if follow-up. It takes 49/238 ms, re-measures its command pass and checks 1x1 byte identity against the merged head. Keep #910's 8x8/2if 1,550 us build explicitly refuted and its relationship to #890 intact. Keep #908 open until the last notice is within 125 ms and txL within 40 ms at 20 cs. None of these deferred duties is counted as resolved here.

`REPRODUCE.md` gives commands. `MANIFEST.sha256` lists publishable scripts and receipts; `scratch/` is excluded. The map counterexample intentionally exits 1. All reviewer execution checks completed; no job remains running.

R838-3 FINISHED
