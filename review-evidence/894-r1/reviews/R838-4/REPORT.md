[R838] NEGATIVE - exact head 5b264bf26416108add32d7fe5abca5252ffde2cb

R838-4 applied all five lenses to the seven-commit, thirteen-file delta from `dd01b0afef87037ec485cd49b40a26b542854bdd`. The map-index defect is resolved, and the revised 1x1/1if model passes. Two MINOR findings remain: stale current-row figures in the design document, and a public validation command that selects fewer tests than claimed. Neither demonstrates a firmware deadline or functional failure. One wording-only RESIDUE is also recorded.

The source tree is `2d2fa3312e4bf54ac42f71af967c83711a45bc36`. Reconstruction followed the repository contract, documentation map, issue/public decisions, requirements/interfaces, diff/history, and public executable evidence. The requested `66f713267f201d1a00d7f711e04b3a996d804dee..5b264bf2` inventory includes imported changes; this review judges the later delta and dependencies it changes. Untouched behavior retains its prior assessment. `independent-verdict.md` records the independent verdict and ledger before prior public findings were opened. No other current-round report was read.

Authority: [round-9 ruling](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6870437042), items 1-5 and STOP conditions; [egress ruling](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6867990126); [1x1 acceptance scope](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6867393730); [contingent bounds](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6858269025) and [queued-bound amendment](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6862465874). Requirements/interfaces examined include REQUIREMENTS product ownership, FR_NFR 3.4.1, ARCHITECTURE_HW_SW_SPLIT ownership/verification boundaries, the AECP contract, descriptor generation, and the loop/pace interfaces. The rulings amend the original both-point acceptance: 8x8/2if is reported, and 8x8/1if remains the follow-up lane's responsibility.

Evidence below means [author-r9 at archive fa3f0a8c](https://github.com/kebag-logic/milan-fpga/tree/fa3f0a8cdcf3cb801cb2d97977b6df00585621ac/review-evidence/894-r1/author-r9), [REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6872978311), and the PR body. All **75** published author-r9 files match the root manifest's SHA-256 values. The archive commit is unsigned: content integrity was verified, but no cryptographic signature was available to authenticate. `archive-integrity.txt` and `audit.log` record the distinction.

**R838-4-F1 - MINOR - Docs - current built-design rows retain superseded values.**

- Artifact: `docs/design/SPLIT_CONTROL_MEMORY.md:2342-2345,2481`; changed dependency `tb/verilator/ctrl_service_budget/rows_tiers.py:99`; reviewer `flip-1x1.log`.
- Authority/evidence: ruling item 4 requires recomputing every row after restating costs; item 5 and the Docs lens require consistent current figures. The paragraph introduces “The rows by every source (`rows_tiers.py`, the built design)” and its 1x1 row still gives R4 12.82, R5 72.71, R6 68.62, first 14.50 and last 125.84 ms. At this head they are **12.85, 72.91, 68.80, 14.51 and 126.46 ms**. Line 2481's current summary also retains R4 12.82. The progression table at line 2367 is correct.
- Impact: two sets of current results describe the same build. The AMAP_LIVE_WRITE change invalidates these dependent figures even though the old table itself was not edited. Every affected row still passes. This changes figures and cannot use the wording-only exception.
- Required outcome: update the current table/summary, or explicitly identify them as a snapshot of a named earlier head and point to the current table. Preserve historical data as history.
- Verification: compare all five entries and the summary with `python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 1x1/1if`; run applicable documentation checks.

**R838-4-F2 - MINOR - Tests, Docs - the thirteen-test claim has an eight-test command.**

- Artifact: PR #902 “How to validate” core command and expected result; author `receipts/item1/core-arm-head.txt`; reviewer `map-core.log`, `map-core-wide.log`.
- Authority/evidence: reproducible validation is part of the public contract. The PR documents `--core --filter 'Core.Map*:Core.Every*'`, then says the filter passes thirteen tests. That command runs **eight**, all passing. It omits `StaticMapsPreventOrphaningFormats`, `OutputMappingsHaveOneGlobalOwner`, `OutputPartitionGeometryUsesAllAdvertisedWidths`, `BootMapFaultsCannotPartlyReplaceTheSet`, and `RestoredOutputMapsHaveOneGlobalOwner`, present in the thirteen-test receipt.
- Impact: following the instructions does not reproduce the advertised format-safety, ownership, partition and boot coverage. The receipt is not disproved; the implementation's tests do not fail.
- Required outcome: use **`'Core.*Map*:Core.Every*'`**, or accurately state the narrower scope and separately provide the broader command. The wider selection was executed on the same exact-head binary: thirteen tests pass.
- Verification: `run_focused.py` reproduces the eight-test selection; `verify_filter.py` reproduces thirteen. Both return zero. Changing the command changes the tests executed, so this is not wording-only RESIDUE.

**R838-4-R1 - RESIDUE - Docs - “last REMOVE” should say “first REMOVE”.**

- Artifact: PR #902 “Measured”, `Core.EveryAcceptedMapKeyIsItsOwn` bullet.
- Evidence: the PR says the last 16x32 REMOVE has 1,165 visits against 2,078. Both the published key receipt and reviewer `map-keys.log` give this pair for the **first** REMOVE, which reads 976 rows. The last has 251 visits against 314.
- Impact: ordering wording only; the quoted measurement/bound are valid and every command passes.
- Exact fix: replace “the last REMOVE is 1,165 visits against 2,078” with “the first REMOVE is 1,165 visits against 2,078”. No measurement, test or verdict changes.
- Verification: inspect the eight consecutive 16x32 REMOVE lines. Non-blocking residue.

**Implementation and timing assessment.**

The direct index is sound for the generated domain. `aecp_shape.py:19-59` reads descriptor bytes, including every STREAM_OUTPUT's current/advertised formats and input-port cluster widths across configurations. `aecp_entity.py:39-44` emits the constants while allowing the map unit to exclude tables. `aecp_maps.c:156-163,201-210` uses `first * MAP_CHANNELS + channel`, with both maxima covering the input/output domains. Quotient/remainder uniqueness proves injectivity for `channel < MAP_CHANNELS`. The actual table definition covers the product, with the 256-slot floor; assertions cover both advertised domains and the byte-sized mapping index. Slots may exceed 256; their values, not slot indexes, are mapping-index-plus-one in a byte.

`aecp_maps.c:377-385` evaluates descriptor legality before `place()`, and forms a table address only after a valid position. The conditional expression in `place()` does not evaluate the multiplication for an out-of-domain key. `look()` treats an outside stored row as absent. The existing ILLEGAL turn preserves BAD_ARGUMENTS precedence, earlier port reads and atomicity. Lock/length/resource outcomes and duplicate-removal multiplicity are unchanged. The product format path retains its supported-format verdict (`aecp_face.c:210-218`); cluster widths are fixed. This delta changes no HDL, CDC, reset, queue ownership or submodule pin.

Independent enumeration (`domain-audit.log`) covers the five configurations and both extra geometries, all advertised formats and every dynamic port: **75 ports, 51 nonempty and 24 empty domains**, with no collision or outside key. The native key arm passes at all seven geometries, adding/removing keys in 63-mapping commands under `2(n+R)`. The 16x32 case has 488 accepted output keys and 544 slots. This proves functional/work behavior there, not target timing or a whole-call-stack bound.

The unchanged R838-3 probe has SHA-256 `81d2efaff1c9d808d7e2d9e35ff7b008b57dda7a9787262b2e4cd1cf0c576c39`. Its own run gives:

| Mappings | ADD visits / bound | REMOVE visits / bound |
|---:|---:|---:|
| 8 | 8 / 16 | 40 / 48 |
| 16 | 16 / 32 | 80 / 96 |
| 32 | 32 / 64 | 160 / 192 |
| 63 | 63 / 126 | 315 / 378 |

The definition-test body is byte-identical to `dd01b0af` (`audit.log`) and passes. The work test retains 8/16/32/63, accepted/refused cases and quadratic controls. The six new plants target channel loss, stream/cluster loss, short stride, the domain edge, an outside row matching a slot, and a table scan. Published subset/word receipts show each caught by the intended assertion. These subset receipts precede the final pace change; the relevant map/test source is unchanged, and the exact-head workflow receipt reports the complete 273-plant AECP campaign passing. Mutation campaigns were inspected, not rerun.

The **256-slot floor is a sound, disclosed choice for this measured candidate**, with a limited claim. It retains the former table size at the gated point and five checked-in shapes; it does not newly spend 192 bytes relative to round 8. Relative to the proposed 64-slot table it spends those bytes to preserve stack/cache placement. Receipts compare 98,720 cycles with 91,625 and disclose the unfavorable 8x8 increase to 156,716. That cost is restated, not hidden. At the widest tested geometry the table grows from 256 to 544 slots, another 288 stack bytes, without target timing or call-chain stack proof here.

The floor does not solve [#909](https://github.com/kebag-logic/milan-fpga/issues/909). Future frame, state-layout or linker changes can invalidate timing without changing the algorithm. Exact-image remeasurement and merge-candidate validation remain necessary. The published comparison supports the choice; this review did not independently reproduce the cache-only attribution from target traces or prove worst-case arbitrary cache states.

At 100 MHz the padding arithmetic is correct: 91,625 cycles becomes 965 us after 5% and upward 5-us rounding, so 975 remains as the larger cost; 98,720 becomes 1,040; 156,716 becomes 1,650; AMAP's 2,551 cycles becomes 30 us. Final 1x1 AVB/AS_PATH/AMAP maxima are 30.55/31.57/25.51 us within 35/35/30. The former 25.32-us AMAP measurement was already understated and is openly corrected. The 8x8 values 35.76/32.79/22.65 fit 40/40/25.

The independent audit confirms **P=8 is smallest**: P=7 gives txL 49.69 ms; P=8 gives 48.09 and R4L 188.39; P=12 fails R4L at 248.39. All eleven 1x1 rows pass:

| Row | Every-source ms | Bound ms |
|---|---:|---:|
| R4 | 12.85 | 20 |
| R4L | 188.39 | 238 |
| ACMP / ADP / MAAP | 28.44 / 26.83 / 26.95 | 30 each |
| First queued notice | 14.51 | 20 |
| R5 / R6 | 72.91 / 68.80 | 90 each |
| Last queued notice | 126.46 | 130 |
| tx / txL | 29.86 / 48.09 | 49 each |

Own load check gives 0.513 at the pin and 0.509 in the second column. The published grid gives 18 of 420 holding, the selected 900-us slice, and 0.692 with every command largest. The 64-slot counterfactual gives 0.705. Its older pace table uses AMAP=25; with current AMAP=30, the independently evaluated 1,040-us counterfactual still first holds at P=9 (txL 47.74). This does not change the floor decision.

**Execution evidence and image reconciliation.**

- Exact-head sweep receipts sum to **65 suites, 2,713,040 checks, zero failures/timeouts**. The workflow inventory has **139 zero-exit steps, 226 NOT RUN entries with reasons, zero bad**. These are local workflow executions, not hosted jobs or evidence that skipped contexts ran. No manager source bank is claimed or inferred.
- Lane evidence reports rows controls 971/971, flip 555/555, load 25/25, and 246 harness mutants caught with none escaped. Own flip self-test independently refuses 555/555. Full banks and target harness legs were not rerun.
- Harness summaries sum to **57 join intervals in 14 runs, 54 in 13 unplanted runs**, range **185.485-190.040 ms**, inside 181-239. Run-outs total 126 released and 69 empty; none is listed late, absent or unresolved. C-R1's three intervals are not a separate clean campaign. These are commit-side simulation measurements, not wire proof.
- At 1x1, the accepted REMOVE's published longest pass is 149,490 of 200,000 cycles, with record 91,625. The 8x8 record/share increases remain reported. The 8x8/2if SRP leg fails its understated build-of-one cost under #910; 8x8/1if failures remain follow-up work. Neither point is recast as passing.
- R838-3-F3 is reconciled: **+180 B `.text` everywhere**, plus 4 B alignment in the 1x1/1if fixture gives **+184 B ROM**; removal of 4 B alignment in the other seven gives **+176 B ROM**. This round's ROM deltas are zero/-8 B; SRAM/tile counts are unchanged. Section arithmetic was checked; ELF endpoints were not rebuilt.
- Every listed image fits. The 1x1/1if fixture has **16 ROM bytes inside its current block**, not sixteen bytes below the overall tile cap. The 8x8/1if platform uses its 56.0-tile cap with **1,872 ROM bytes inside its allocation**. Wider geometries were not measured as full platform images by this review.

**Prior findings reconciled.** Prior findings were opened after the independent verdict/ledger: [R838-3](https://github.com/kebag-logic/milan-fpga/pull/902#issuecomment-6870395150) and [R837-3](https://github.com/kebag-logic/milan-fpga/pull/902#issuecomment-6870427229).

| Prior finding | Disposition and cause-level evidence |
|---|---|
| R838-3-F1 / R837-3-1 | Resolved across all attributed lenses. Generated direct index, guards/assertions, own prior probe, seven-geometry native arm and advertised-domain audit remove dependence on hash injectivity. |
| R838-3-F2 / R837-3-2 | Resolved at every named site. Service README:183,185 and SPLIT_CONTROL_MEMORY:2351,2355,2376,2475,2481 now give 238/49, both pace conditions, current 0.792/0.752 and 0.513/0.509 loads, and ruling 6844175391. F1 above is a newly invalidated dependent row table. |
| R838-3-F3 | Resolved, Tests and Docs: +180 code and +184/+176 ROM reconciled in the section receipt, PR and REVIEW READY. |
| R838-3-R1 | Resolved: exact public endpoints and seven-commit history. |
| R837-3-R1 | Resolved: `long_notice.py:19-23` describes the first illegal index and row's own value correctly. |
| R837-2-1 / R837-2-2 | Retain resolution: derived 49/238 and 181-239; whole-ms `ceil((W+1)/P)`. New cost/P=8 consequences rechecked. |
| R838-2-F1 | Retain resolution: no-horizon resolver and five outcomes unchanged; new join receipt audited. |
| R838-2-F2 | Fully resolved by direct indexing beyond the earlier same-key-chain repair; definition/counting controls retained. |
| R838-2-F3 / R837-2-3 | Corrected numeric-contract sites retain resolution; new dependent discrepancy is F1 above. |
| R838-2-R1/R2 / R837-2-4/5 | Retain resolution: no new prohibited source labels; historic receipts remain historic and planted/unplanted counts distinct. |
| R838-1 F1-F7 / R837-1-1,2,3,5 | Prior tier-row, legal-notice sizing, model/compile checks, native controls, slice, ordering and Domain/VLAN resolutions retained where unchanged; affected map/timing dependencies reapplied. |
| R837-1-4 / R838-1 S5 | Scope resolution retained: 8x8/2if reported and #910/#872 duties open. |
| R838-1 RS1 / R837-1-6 | Comment cleanup retained; no equivalent new instance found. Existing #746 material not reopened. |

**Optional suggestions, retained for one author pass.** None independently prevents coverage.

| ID / lenses / artifact | Evidence and impact | Optional outcome and verification |
|---|---|---|
| R838-4-S1; Docs; AECP README owed ordering (R838-3-S1) | Later response can precede an earlier notice; no new breach alleged. | Explain the consequence with a two-controller example. |
| R838-4-S2; RTL; `aecp.c` counter reset (R838-3-S2) | Redundant reset remains outside the delta. | Retain rationale or prove the invariant before removal; check queue/retry tests. |
| R838-4-S3; Tests; `aecp_owed_notice_steps.py` (R838-3-S3) | Offline scenario model/string anchors; native tests provide execution. | Optionally connect a scenario to compiled behavior and show a behavioral mutation fails. |
| R838-4-S4; Tests; input/sample inventories (R838-3-S4) | AMAP's underestimate reinforces complete inventory value; join samples remain small. | Retain maxima/counts for every stated term; extend tier-1 pressure across expiries and compare raw records. |
| R838-4-S5; Tests; `rows_tiers.py` ranking (R838-3-S5) | Unsolved -1 can outrank a solved score below -1; current selection unaffected. | Before relying on a mixed failed search, rank unsolved last and add an ordering control. |
| R838-4-S6; Tests; ACMP decline bound (R838-3-S6 / R837-3-S3) | Bound remains conservative. | Tighten only with source proof and a mutation control; acceptance does not need it. |
| R838-4-S7; Docs; author INDEX (R838-3-S7 / R837-3-S1) | Publication still omits indexed A10-RULING.md and redacts scripts/index.py, changing its hash. Root manifest matches all published files. | Generate from published bytes or explicitly make root manifest authoritative after omission/redaction; verify entries. |
| R838-4-S8; Tests; `mrpdu_grade.py:84` (R837-3-S2) | Late classification starts at callback; row starts at owed centisecond. Existing rows stay within budget. | Align origins or state the distinction, with delayed-callback control. |
| R838-4-S9; Tests, Docs; H-81N (R837-3-S4) | rc=1 still lacks a diagnostic; point is outside this gate. | Include the reason to distinguish build failure from measured miss. |
| R838-4-S10; Tests, Docs; final measured-input receipt / REVIEW READY | Final H-L1L heaviest passes include 93,346 and 95,503; older remeasurement has 93,335 and 93,813. Summary still quotes 93,813 for refused edits. Receipt lacks per-record attribution, so this review does not infer which is refused. Overall maximum remains 149,490. | Publish final record/pass attribution and refresh the refused-edit maximum if needed. This is an evidence request, not a demonstrated share violation. |

**Reviewer-owned completion ledger.** All lenses were applied; Tests and Docs remain unclean for the public-validation defects above.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Rulings/FR_NFR 3.4.1; `aecp_shape.py:19-59`; `aecp_maps.c:139-163,201-225,367-431`; domain/probe/flip/model receipts; derived 49/238 | R838-4 | 5b264bf26416108add32d7fe5abca5252ffde2cb |
| RTL | CLEAN | No HDL/pin delta; direct-index arithmetic, byte values, guards and layout; `aecp_mbx.h:42-54`; descriptor and image receipts | R838-4 | 5b264bf26416108add32d7fe5abca5252ffde2cb |
| Robustness | CLEAN | Legal-length accepted/refused edits, edge/outside rows, semantic oracle, ownership/restore tests, wider geometries; retained join/reset/backpressure paths | R838-4 | 5b264bf26416108add32d7fe5abca5252ffde2cb |
| Tests | UNCLEAN: F2 | `test_aecp.cpp:2513,2632,2673,2701,2736`; key/work arms, six plants, own 555 controls, gate receipts and PR filter reproduction | R838-4 | 5b264bf26416108add32d7fe5abca5252ffde2cb |
| Docs | UNCLEAN: F1, F2 | SPLIT_CONTROL_MEMORY section 13, FR_NFR, AECP/service READMEs, comment delta, PR/REVIEW READY, index and measurement reconciliation | R838-4 | 5b264bf26416108add32d7fe5abca5252ffde2cb |

**Real limits and pending manager duties.**

- Source was never edited. Own execution comprised focused native selections, seven-geometry key arm, unchanged prior probe, flip/model/load checks, descriptor enumeration and receipt/identity audits. No full banks, target build, hardware, privileged action, GitHub write, source fix, commit, push or merge. No manager source bank exists at this head or is inferred.
- The identity receipt verifies the index tree, **1,619 parent tracked blobs/modes**, every gitlink, and initialized required dependencies' bytes/modes/indexes. The optional external pin is recorded; its absent checkout is not represented as checked. Disposable files are under `scratch/` and not publishable.
- Physical calibration was **NOT RUN**. Field skips are not hardware proof. The 180-240-ms wire capture remains S12b's; commit-side intervals do not discharge it.
- Correct F1/F2 and re-review their lenses; carry R1 to the residue checklist. Documentation-only changes need not invalidate unaffected code coverage, but changed artifacts require an updated reviewer-owned ledger.
- The manager owns the remaining independent verdict, hosted/local acceptance and current-dev merge-candidate validation, including builder/native banks and exact receipts. Source base: `66f713267f201d1a00d7f711e04b3a996d804dee`; supplied live dev: `b7d692952305e4e0e132abb8f99c339eeb17a873`, to be re-read at merge. Source-head receipts do not validate that future tree, especially layout-sensitive timing.
- Preserve #909, #908's original-bound restoration conditions, #910, and the 8x8/1if follow-up's shape-header consolidation, measurements and byte-identity duties. This report closes none of them and does not authorize merge. Post-merge containment and public issue/project completion remain pending.

`MANIFEST.sha256` names every publishable script and receipt; REPORT.md is also published. Scripts run from the candidate clone and write beside themselves. All launched checks finished before handoff.

R838-4 FINISHED
