[R844] POSITIVE - exact head d0a2a1605d7acc691936a61f9afaa0e67f4b46f2

External independent review R844-5, issue #894 / PR #914, round 13. Tree `200d73043aefc480fc11c6d00e2689c4757077ff`. All five lenses are CLEAN for this delta. R843-5-F1, R844-4-F1 and R844-4-F2 are resolved. No BLOCKER, MAJOR or MINOR remains. One new wording residue and four retained optional suggestions are recorded below.

The substantive review covers `8883d4998496c6d2e234143b43807731e8851b63..d0a2a1605d7acc691936a61f9afaa0e67f4b46f2`: three commits (`a840c14d`, `32a9242f`, `d0a2a160`), eleven files. The requested full source-base diff from `7398ec0aeea468d92ff642a03a06e291a0cd58d1` was obtained and indexed. Earlier implementation was not reviewed again; unchanged code retains its prior verdict unless this delta changes its dependencies. See `delta-history.log` and `round13.diff`.

Reconstruction followed AGENTS.md/CONTRIBUTING.md, docs/README, the issue body and public scope decisions, requirements/interface authorities, diff/history, then public evidence. The independent verdict and ledger were written before reading prior reviewer reports. Their findings were then reconciled at their causes. No private author material or unpublished reviewer material was used.

Binding decisions include the [shape scope](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6867393730), [held-egress acceptance](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6871343905), [reported rows and ledger rule](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6892938049), [composition](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6914952893), [#930 targets](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6918853411), [accepted measurements](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6934688411), and [plant/base-failure disposition](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6938589932). REQUIREMENTS.md section 1, FR_NFR 3.4.1, MAILBOX_SPLIT and the loop/SRP contracts supply the requirements. The [freeze decision](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6939574513) governs subsequent composition. This source verdict is not merge authorization.

**Named findings resolved at this head**

**R843-5-F1, Tests/Docs: resolved by option (a).** `flip_grade.py:74,81,454` calls `tx_statements` for reported 8x8/1if separately from ordinary row acceptance. `rows_grade.py:97,159,307` supplies the missing shape, reads its own poll costs, and derives its 40 pending notices from the configuration. `rows_tiers.py:126,183` selects its long-notice cost and the ruled nearest-point event costs. This is an in-tree derivation, not a mirrored 74.26 constant. In a disposable exact-head export, the actual CLI refuses 60, 69, 70 and 74 ms by name with exit 1; 75 and 76 ms exit 0. The gate's own 615 controls pass. Increasing the model's poll base by 100 us raises the derived tx row to 78.99 ms. See `transmit-probe.log`, `probe-tx-*.log` and `flip-selftest.log`.

**R844-4-F1, all five lenses: resolved.** `ctrl_loop.h:355` states 75 ms, the 74.26 ms row rounded up. `srp_mbx.c:36` derives `2000 + 19 + ceil(75/10) = 2027 cs`. The reviewed envelope leaves `20270 - 190 - 74.26 = 20005.74 ms`, above the two configured LeaveAllTime periods, 20000 ms, cited by IEEE 802.1Q-2018 35.2.2.8. The earlier 70 ms statement now fails the real CLI. Comments and SRP/harness documentation describe the guard and current values. This resolves the previously demonstrated model-envelope defect; it is not a physical wire measurement.

**R844-4-F2, Conformance/Docs: resolved.** `SPLIT_CONTROL_MEMORY.md:2765,2808,2813,2827,2838` separates historical measurements, the Listener-copy image, and the current in-tree derivation. The complete current row sequence independently reproduces R4 21.39, R5 136.64, R6 132.93, first 18.98, last 387.95, R4L 208.55, ACMP 52.76, ADP 52.64, MAAP 53.91, tx 74.26 and txL 159.82 ms. The largest-command load is 1.034; 0.969 and the older within-bound R4 conclusion are historical. The named `46cf2a7d` receipts substantiate 32936 SRP cycles, 2403014 retry rounds, last notice 25.625 ms, and two share-overrun passes with maximum 222434 cycles. MAILBOX_SPLIT:390 now states 0.9 ms at 1x1/1if, matching `ctrl_loop.h:339`. R4 remains openly reported debt under #872.

**Evidence and independent checks**

The immutable [public archive](https://github.com/kebag-logic/milan-fpga/tree/48b6c3a2475861387068bc762f423bb417dd6915/review-evidence/894b-r1) supplies the execution evidence. All 228 author-r13 files match the published manifest hashes. Three author-r10 receipts used for the corrected historical figures also match: 231 verified extracted files. The archive commit is unsigned and no detached signature is supplied in these author paths. This establishes hash/content integrity, not signer authentication.

`author-r13/receipts/images/qimg-{8883d499,d0a2a160}.txt` contains eight ELF/loadable hash pairs. Independent comparison confirms the six 1x1/1if, 1x1/2if and 8x8/2if pairs are identical. The two 8x8/1if pairs change. The published disassembly/content comparison identifies exactly `li a3,2026` to `li a3,2027`, at fixture address `9ef8` and platform address `9ed4`, with all other section bytes unchanged. Its same-image negative control fails as intended. `img_r13.py` checks disassembly and section contents. These are verified published build receipts, not an independent eight-image rebuild.

The final commit changes documentation and a printed table header only relative to `32a9242f`, so its measured image applies. The published comparison of the three Talker legs and eight transmit-aged control groups reports all eleven simulation logs byte-identical to `46cf2a7d`, and graded text unchanged. The sole grade difference is the separately stated reclaim limit, 4000 versus 3500 cycles. These groups end before their armed hold-off expires; their equality does not test an expiry they never reach. Existing timer tests and the SRP campaign provide separate evidence at their stated shapes. This review independently checks the changed shape's envelope and the published compiled-image immediate.

The three-positive-leg aggregate prints **RESULT: FAIL**, solely because it contains none of the seven held-egress ledger rows. This is disclosed in the PR and is not counted as a full acceptance pass. The earlier named `backlog-owed` measurement supplies those rows. Individual rerun legs exit 0 without STATED lines; the transmit-aged control is caught in eight of eight groups. The scoped aggregate reports SRP 10.869 ms, MRPDU 3.109 ms and Talker rows at most 189.638 ms, within their stated bounds.

| Public source evidence | Result and scope |
|---|---|
| Harness self-test | 931 checks / 259 caught mutants reported; explicitly abbreviated archive retains zero failures and rc 0 |
| Flip | Both 1x1/1if and 8x8/1if checks pass; 615/615 controls; 8x8/2if's failure remains disclosed |
| Load | 28/28 controls; 8x8/1if load 0.735 at the pin versus 0.75 |
| SRP campaign | 436 caught result lines, zero escaped result lines; retargeted readiness and Listener-copy plants present |
| Firmware-unit | Published step exit files are zero; srp_mbx.c line coverage 746/746, 100%; this is a line-coverage claim |
| Documentation | 61 executed steps, 34 NOT RUN with reasons, zero bad; local steps, not hosted job executions |
| Images and legs | Six fixed image pairs identical; two one-instruction changes; eleven group-log comparisons identical |

`evidence-audit.log` records the receipt checks and full image hashes. The firmware-unit post-run receipt reports untracked `dispatch-build/` test output, not changed tracked source. Campaigns not rerun at this head keep the PR's explicit prior-head attribution and reason. No manager source bank is asserted or inferred.

Independent execution passed the 1x1/1if flip check, 615-control flip self-test, load check and 28-control self-test, and all six CLI constant probes. `transmit-probe.log` records the full derived row table and tx terms. `diff-check.log` is clean. Probe setup initially lacked extracted descriptor sources and then used two incorrect inspection API names; these reviewer-script errors were corrected before the successful run and are not candidate failures. Mutation bytes were confined to the disposable export.

An additional full harness rerun was intentionally interrupted to avoid duplicating the published full campaign after the focused checks had completed. Its partial log (local paths normalized) and exit 130 are retained as `harness-selftest.log` and `.rc`, with counts in `harness-attempt-summary.log`: 931 passing checks, 52 caught mutants, zero failed checks or escaped mutants before interruption. `public-scrub.log` records raw and published hashes. It is **not** counted as a complete local pass or as a candidate failure. The complete 259-mutant result remains attributed to the author's public receipt.

**Prior findings reconciliation**

The latest public reports are [R843-5](https://github.com/kebag-logic/milan-fpga/pull/914#issuecomment-6940020752) and [R844-4](https://github.com/kebag-logic/milan-fpga/pull/914#issuecomment-6940102979). Their earlier-finding ledger was reconciled against this delta. Unchanged resolved causes are carried forward under the narrow-review instruction.

| Prior item | Disposition at this head |
|---|---|
| R843-5-R1 | Resolved: load_grade.py:567 names the donor measured-cost column and says the pin already carries #32; numbers/verdict unchanged |
| R843-5-R2 | Resolved for the successor packet: author-r13/INDEX.md says round 13; index.py derives its title from the originating directory |
| R843-4-R1 | Resolved: FR_NFR.md:393 identifies the current image and says the two named older images held at their own figures |
| R844-1-F1; R843-2-S1 | Held-egress growth/completeness guards remain resolved; egress_ledger.py is unchanged |
| R844-1-R1 / R843-1-R1 | Earlier source-comment cleanup retained; added comments introduce no prohibited lane/reviewer/issue-comment identifier (source-comment-scan.log) |
| R843-1-S1 | Declared charging-unit guard and main-arm contract agreement remain addressed; debug/wire remainder retained below |
| R843-2-S3 | Current manifest verification addresses content integrity; signature limitation remains explicit |
| R843-2-RES1/RES2/RES3; R844-2-R1/R2 | Earlier ledger, guard/include-scope and receipt wording dispositions retained; causes unchanged here |
| R844-3-R1 | Correct shape name in record_classes remains unchanged |
| R844-3-R2 / R843-3-R1 | Shape qualifier retained; current numerical slice corrected by this delta |
| R844-3-R3/R4 | Historical row/load labeling and survey-comparison correction retained |
| R843-3-F1 | Later recurrence was R844-4-F2; current rows and image attribution corrected above |
| R843-3-F2 | Mixed-point completeness fix unchanged; current packet includes its named refusal and 14/14 controls |
| R843-3-R2 | FR_NFR ledger link and recorded-miss distinction retained |
| R843-3-S1 | Retained-retry explanation and measurement attribution remain addressed; no cost rule changed |

**R844-5-R1 - RESIDUE - Docs - PR #914, Status and How to get into the same state.** Authority/evidence: the current public PR is at the reviewed head, but its body still says nothing has been pushed and publication must precede retrieval. Impact: stale publication-status prose only; no measurement, executable verdict or conformance claim changes. Exact fix: replace those sentences with “Published source head: `d0a2a1605d7acc691936a61f9afaa0e67f4b46f2`. The manager owns composition and merge.” Remove the obsolete prerequisite sentence before the fetch commands. Verification: compare the displayed head with the amended prose. Immutable handoff records need not be rewritten.

Retained optional suggestions, preserving their identities and attributable lenses:

- **R843-2-S2 / R843-3-S2 - SUGGESTION - RTL, Robustness - aecp_arms.py:114 and aecp_wire.py:133.** Authority/evidence: unchanged debug/wire arms retain a documented contract exception and measure no retry-round costs. Impact: optional coverage clarity; no timing defect demonstrated. Optional outcome: use each arm's interface contract or assert that it measures no round cost. Verification: generated contract/assertion and affected-arm receipts.
- **R843-4-S1 - SUGGESTION - Tests, Docs - public author-r7/scripts/f1_check.py.** Authority/evidence: substring checks do not bind figures to rows/images. Impact: optional checker weakness; actual current documentation was independently compared here. Optional outcome: structured row/image comparison. Verification: reject a swapped figure or wrong-image attribution.
- **R843-5-S1 - SUGGESTION - Tests - srp_listener_mutants.py:34, srp_mutants.py:93,225, srp_mbx.c:862.** Authority/evidence: readiness plants target the indication; the earlier review demonstrated equivalent walk-site plants are caught by the differential test. Sites and campaign table are unchanged. Impact: missing permanent regression plants, not untested behavior. Optional outcome: add both walk-site readiness plants. Verification: both fail by name at 1x1/1if and 8x8/1if.
- **R843-5-S2 - SUGGESTION - Tests - srp_listeners.cpp:331.** Authority/evidence: two fixed 3000-step seeds remain. Impact: optional sequence-space coverage. Optional outcome: an additional externally supplied seed printed on failure, retaining deterministic defaults. Verification: reproduce a chosen seed and identify it in the failure report.

**Reviewer-owned ledger**

Each PASS covers the delta and affected dependencies at this exact head. Optional suggestions and wording residue do not prevent clean coverage.

| Lens | CLEAN/UNCLEAN | Examined artifacts and PASS evidence | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | ctrl_loop.h:355; srp_mbx.c:36; FR_NFR 3.4.1; tx/hold-off derivation; corrected section-13 figures against named receipts | R844-5 | d0a2a1605d7acc691936a61f9afaa0e67f4b46f2 |
| RTL | CLEAN | round13.diff has no HDL/CDC/reset or ABI change; constant consumer traced; eight-image receipts and required gitlinks checked | R844-5 | d0a2a1605d7acc691936a61f9afaa0e67f4b46f2 |
| Robustness | CLEAN | flip_grade.py:74,81,454; rows_tiers.py:557; four understated constants rejected; two passing boundary controls; no-solution refusal inspected; reset notice count 40 | R844-5 | d0a2a1605d7acc691936a61f9afaa0e67f4b46f2 |
| Tests | CLEAN | Independent flip/load checks and fault probes; public harness/SRP/firmware receipts; image negative control; eleven-log comparison with incomplete aggregate explicitly identified | R844-5 | d0a2a1605d7acc691936a61f9afaa0e67f4b46f2 |
| Docs | CLEAN | SPLIT_CONTROL_MEMORY.md:2765,2808,2813,2827,2838; MAILBOX_SPLIT.md:390; FR_NFR.md:393; SRP README:227; harness README:205; load header and packet title | R844-5 | d0a2a1605d7acc691936a61f9afaa0e67f4b46f2 |

**Real limits and pending manager duties**

This is a source-head delta review. Published author execution supplies source-bank evidence; no manager source bank ran or is inferred. Image and large-log equality were checked through published receipts/comparison scripts, not an independent eight-image rebuild or retrieval of every raw simulation trace. No hardware, physical calibration, full parent/processor/synthesis/builder banks, hosted acceptance or local workflow replica was run by this reviewer. Physical calibration is **NOT RUN**; field skips and simulated/model timing are not hardware proof.

The known twin/twin-plants failure remains the base's stale row assigned to #935. Reported 8x8/1if every-source debt remains #872's, including R4 21.39 ms versus 20 ms and the separate 49 ms transmit service-bound miss. Correcting the hold-off's 75 ms input does not make those general rows pass. The timing floor remains #818's. None is relabeled as a new delta finding.

The manager must publish this packet, carry R844-5-R1 to the residue checklist, reconcile the other independent review, and freeze the source once both required verdicts permit it. Under the freeze decision, the composition lane merges frozen heads, resolves conflicts and measures the composed image. The manager must validate the actual current-dev candidate with required builder/native banks and hosted/local acceptance, distinguish executed jobs from skipped contexts, and link receipts on the PR. Source base `7398ec0aeea468d92ff642a03a06e291a0cd58d1` and supplied live dev `6b66f66d89cf25d2717687bcc2c3bf617685a99a` differ; check the live tip at the merge turn. No candidate result is claimed. Authorized merge, containment, documentation and issue/project completion remain pending manager duties.

Integrity receipts verify raw tracked bytes, executable/symlink modes, index entries and all five required initialized submodule gitlinks/bytes. The unchanged external gitlink is uninitialized and supplies no runtime evidence. Disposable trees remain under packet scratch/. No source fixes, commits, pushes, GitHub writes or changes to another checkout were made. MANIFEST.sha256 lists publishable receipts/scripts; scratch is excluded.

R844-5 FINISHED
