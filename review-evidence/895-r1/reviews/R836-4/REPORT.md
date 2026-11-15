[R836] NEGATIVE - exact head 056d619ddba179edb0dd2914e14a4b1d51988dd8

R836-4 external independent delta review, issue #895 / PR #901.

All five lenses were applied. One MAJOR evidence defect remains: the cost survey silently omits paced records and one held ordinary-record path, so the complete cost claim is not established. One MINOR documentation finding also remains: passages carried through the sync still present earlier images and figures as current. Conformance, Tests and Docs are UNCLEAN; RTL and Robustness are CLEAN. The three named prior defects are corrected at their original causes; the wider all-cost verification requested by R835-3-F1 remains incomplete under F2. One wording residue and the optional suggestions are collected below.

## Scope and authority

Reviewed head `056d619ddba179edb0dd2914e14a4b1d51988dd8`, tree `0e61c5c5587c826d696c205cf70295f7c1c82a9a`; source base `cec88385ad0a0ec0d61b91597640797766e45010`; preceding reviewed head `62298ab5cbfeb7056e4567f70e69d578201c75e0`. The base-to-head diff established scope; the later-round delta and dependencies received the detailed review. Unchanged code keeps its preceding coverage unless a changed dependency affects it. The #902 syncs were examined for this lane's resolutions, costs and figures, not as a replacement for #902's review. `659d7687` and `07ed787e` have the same tree, `697298a1c8a5552b7ecd7f5790ccfbfeaa16cf13`.

Context order was operating contract, contribution rules, documentation index, public acceptance/rulings, requirements/interfaces, diff/history, then executable evidence. Prior public findings were reconciled after the independent diff pass. No current-round peer report, private author notes or management source bank was used. No source edit, commit, push, GitHub write, hardware operation or merge was performed.

Authorities: #895 acceptance 1-5; [amendment 6840463408](https://github.com/kebag-logic/milan-fpga/issues/895#issuecomment-6840463408); the subsequent A10 rulings including [6886630886](https://github.com/kebag-logic/milan-fpga/issues/895#issuecomment-6886630886), [6892130675](https://github.com/kebag-logic/milan-fpga/issues/895#issuecomment-6892130675), and [6895331865](https://github.com/kebag-logic/milan-fpga/issues/895#issuecomment-6895331865); Milan v1.2 4.3.3.1/5.3.7.4; IEEE 802.1Q-2018 35.2.2.8/Table 10-7; REQUIREMENTS.md; FR_NFR 3.4.1; MAILBOX_CONTRACT.md publication ordering. Acceptance 6 is excluded: it is a bench item. The owner's later overflow rule records S14 debt rather than imposing a stop; no reviewed image exceeds its current entry.

Evidence archive: [50e931db](https://github.com/kebag-logic/milan-fpga/tree/50e931db5cbf079abcbe76519669641774c84c36/review-evidence/895-r1), selected author-r6 through author-r9 only. Below, `r8/` and `r9/` mean their `receipts/` directories. SHA-256 validation uses the archive MANIFEST's **published** hashes, not its pre-redaction hashes. The archive commit has signature status `N`: it is unsigned. All 1,507 selected published files match; the local INDEX checks also pass (160/384/203/670 entries for rounds 6/7/8/9). Hash integrity is verified; signer authentication is not claimed.

## Findings

### R836-4-F1 | MINOR | Docs | remaining current-head statements describe earlier images and figures

**Artifacts and evidence:**

| Artifact | Statement still present | Exact-head evidence / required correction |
|---|---|---|
| `docs/design/SPLIT_CONTROL_MEMORY.md:519` and table at 523-530 | “At this branch's head” introduces the round-6 images: platform 8x8/1if 129,928 B / ctrl_plat 18,176 B; platform 8x8/2if 131,464 B with 1,656 B left; fixture 126,320 B; answering arm 348 B left. | `r9/ledger-final/summary.md` and `plat_ledger.log`: respectively 130,200 / 18,240; 131,752 with 1,368 left; fixture 126,608; answering arm 60 B left. Either explicitly bind the whole table and following size/margin claims to the historical round-6 commit, or use the final-head table. Section 13's newer table is correct. |
| `docs/design/SPLIT_CONTROL_MEMORY.md:2551` | “33.38 ms at the head's 950 us slice”; CTRL_LOOP_TX_MS is “a figure only a static assertion reads”. | The built slice is 900 us and tx is 34.00 ms. `srp_mbx.c:35` reads this macro to derive the hold-off; the authorized two-interface change alters executable bytes. Identify these statements as #894's historical image and its reader set before composition, or replace them with this head's facts. |
| `docs/design/SPLIT_CONTROL_MEMORY.md:2682` | “At the head, round 13's legs, on images byte-identical to the head's” introduces #894's 140,032 one-interface passes and a two-interface exit on #910. | This lane's carried round-8 arm A has 130,341 one-interface passes, and its images include the Talker code. The round-9 carry proof is 73388996 -> 663b519b -> 449d29d2 -> 056d619d, not byte identity to #894's round-13 image. Qualify the earlier claim with its actual #894 head and retain this lane's current evidence separately. |
| `docs/design/SPLIT_CONTROL_MEMORY.md:2688` and `docs/reference/FR_NFR.md:390` | Current tier first-notice figures 14.66 ms / 20.93 ms (FR_NFR repeats 20.93). | Current rows are 14.72 / 21.11 ms. Use these, or explicitly attribute the old pair to the historical #894 image. |
| `docs/design/SPLIT_CONTROL_MEMORY.md:2689` | Under the tiers, tx is 33.38 ms and CTRL_LOOP_TX_MS is 99 at two interfaces. | This head's tx is 34.00 / 104.25 ms; statements are 34 / 105 ms. These newly carried numeric assertions contradict the ruling implemented at `ctrl_loop.h:377` and the page's section 13. |

**Authority:** the Docs lens requires authoritative figures and evidence attribution to agree with the reviewed head; the user's rule excludes measurement, figure and verdict errors from RESIDUE. These are the lane's sync/composition claims, not findings against #902's own code.

**Impact:** the same authoritative page reports incompatible current memory margins, timing constants and image provenance. A cold reader cannot use its closing claims to identify the validated image. The correct code and detailed receipts remain available; no functional or physical failure is inferred from this finding.

**Required outcome:** reconcile every listed current-head assertion in one documentation pass. Preserve legitimate historical measurements with an explicit historical subject, and point current-head claims to the final rows and images. Do not change measurements merely to match older prose.

**Verification:** compare all listed passages to `flip-1x1.log`, `probe.log`, `r9/ledger-final/summary.md`, `r8/legs/summary-1x1.txt`, and the image-identity chain. Re-review the documentation at its resulting head. A firmware bank rerun is not needed for a prose-only repair.

### R836-4-F2 | MAJOR | Conformance, Tests, Docs | the claimed complete cost survey silently omits paced records and SET_STREAM_INFO

**Artifacts:** published `author-r8/scripts/costs_vs_stated.py:142-144,182-183`; `author-r8/receipts/survey/survey-1x1-head-f93317cb.txt:67` and the corresponding 8x8 receipt; exact-head `tb/verilator/ctrl_service_budget/record_classes.py:134-139,149-168`; PR #901 “Every stated cost against the legs”.

**Authority/evidence:** acceptance 4 and ruling 6892130675 item 7 require the final image's cost survey; R835-3-F1 explicitly required every stated table, not only load_grade. The source class grader classifies an accepted/paced edit or SET_CONFIGURATION as **`paced`**. The published survey stores `classes.paced` but its EDIT_RECORD_US lookup returns **`classes.edit`**, which can never match. Its final receipts therefore report the paced statement (300 us at 1x1/1if, 595 at 8x8/2if) as zero measured, “not staged”, and still print UNDER 0. This is not a valid check of that class.

Separately, the survey calls `record_classes.held(leg, group, kind)` without `r.command`. For an answering-ports `aecp-fanout` SET_STREAM_INFO, the head deliberately holds that ordinary path only when it receives the command argument. Omitting it excludes the path from the `classes.other` maximum. The independent CLI in record_classes passes the command and checks required accepted commands, but no real-leg class-grader result was found in the selected r8/r9 receipts. A passing synthetic class self-test does not grade those real records.

`class_probe.py` uses the head's synthetic complete legs, raises its accepted SET_CONFIGURATION to 40,000 cycles, and calls the survey's actual extracted lookup function. The head's class grader refuses **420 us against 300**. The survey collected `classes.paced: 40000`, but its lookup found no measurement and reports “not staged”, contributing no UNDER. The same probe shows SET_STREAM_INFO held=True when its command is supplied, False with the survey's call. See `class-probe.log`.

**Impact:** UNDER 0 cannot establish that every input to the one-interface row/slice calculation covers its measured cost. The 300 us paced input and the ordinary accepted stream-info path are not proved by this audit, while the tight row margins and selected slice depend on those costs. This is an evidence/test weakness, not a demonstrated actual firmware overrun; no new runtime or RTL defect is asserted. Published hash integrity and other checked cost rows remain valid.

**Required outcome:** select the paced class under its actual key and preserve the command-sensitive held predicate. Run the head's full real-leg class grader over every required arm/group, including accepted SET_CONFIGURATION and SET_STREAM_INFO, and publish the measured maxima and verdicts. Reuse the preserved raw logs if complete; new full banks are unnecessary merely to correct this audit. If measurements exceed the statements, apply the stated rounding rule and recompute the rows, load, pace and slice under the existing rulings. Correct the complete-survey claim to match the actual coverage.

**Verification:** a planted over-cost paced record and an over-cost held SET_STREAM_INFO must each fail the same evidence path used for the real pass; the real receipts must show both class maxima, not a zero “not staged” cell. Re-review the resulting source/evidence head. R835-3-F1's original base cost is fixed, but its requested wider audit is not complete until this passes.

### R836-4-RS1 | RESIDUE | Docs | PR roles still identify the preceding round

**Artifact:** live PR #901, “Linked Issue / roles”: internal R835-3 and external R836-3, while the two public review-start comments identify R835-4 and R836-4.

**Authority/evidence:** public starts 6899719764 and 6899726363. This is only the current review label; it changes no result, measurement, figure or acceptance claim.

**Impact:** stale navigation to the active reviews. **Exact fix:** name R835-4 and R836-4 and link their current start comments; retain prior-round links in the findings history. **Verification:** role lines agree with the public starts. Non-blocking residue; it does not independently unclean Docs.

## Prior findings: closed or retained at their causes

| Prior ID / severity | Disposition at this head | Cause and verification |
|---|---|---|
| R835-3-F1 MAJOR, Conformance/RTL/Tests/Docs | Base defect CLOSED; broader audit RETAINED as F2 | `poll_grade.py:99` and `load_grade.py` now use 225 us, covering 21,094 cycles by the 5%-then-5-us rule. Rebuilt legs and the public STOP/ruling sequence resolve the old 205/215 discrepancy. The broader all-table check has the separate F2 hole. The rule now selects the built 900 us at the authorized 140 ms bound. Independent flip, grid and 1,033-control runs agree. |
| R835-3-F2 MINOR, Conformance/Tests | CLOSED | `rows_tiers.py:101` states AMAP_LIVE_WRITE at 30 us for 8x8/2if; the rebuilt receipt is 2,465 cycles, 30 us by the rule. The reported rows were recomputed. |
| R836-3-F1 MINOR, Docs | CLOSED | `SPLIT_CONTROL_MEMORY.md:2693` now states R4 13.25 ms, agreeing with this head's grader. F1 above concerns different remaining passages. |
| R836-3-RS1 RESIDUE, size versus byte identity | CLOSED | The old pace/tx wording at `SPLIT_CONTROL_MEMORY.md:528` now explicitly says linked ROM/SRAM **sizes**. The current PR separately explains the changed instruction and the actual identity chain. |
| R835-3-RS1 RESIDUE, unassigned roles | CLOSED as originally filed | Named reviewer roles replace “to be assigned”. RS1 above is the later-round label drift. |
| R835-3-S1 SUGGESTION, Robustness, first opening after a changed SID | RETAINED | `maap_mbx.c` startup's written mark is unchanged. The platform stream ID remains its fixed entity identity plus source number. Optional invariant comment/test is still useful; no newly supported dynamic first-opening operation is claimed. |
| R835-3-S2 SUGGESTION, Tests, audit every stated cost table | PARTLY TAKEN; F2 remains | r6-r8 survey scripts/receipts cover all nine table groups. `survey-check.log` confirms all 126 published row values and arithmetic against this head, but F2 proves that the paced row is falsely unmeasured and SET_STREAM_INFO is excluded. This audit has not established complete cost coverage. |
| R835-3-S3 SUGGESTION, Docs, base attribution | CLOSED for its original comparison | `SPLIT_CONTROL_MEMORY.md:528` identifies the round-4 comparison against 5b264bf2 and separately the round-5-to-round-6 delta. F1 above records the stale “head” attribution remaining over the later table. |
| R835-2-S2 = R836-3-S5 SUGGESTION, Docs, index after scrub | CHECKED on the current packets | `audit.log` records the manifest and local INDEX checks. Older packets are historical; current evidence uses published hashes. |
| R836-3-S1 / R836-1-S2 SUGGESTION, Conformance/Robustness | RETAINED | `srp_mbx.c:639` still compares the recorded destination; D -> E -> D during a hold-off can conservatively wait. Optional last-declared identity tracking and a timed D/E/D test remain useful. The shortcut compares both base and validity and does not change this behavior. |
| R836-3-S2 / R836-1-S3 SUGGESTION, Tests | RETAINED | `srp_talker.cpp:361` still refuses all allocation during the admission swap. Optional selective replacement-join refusal with transmission available would independently expose leave-before-join on the wire. |
| R836-3-S3 / R835-1-S1 / R835-2-S3 SUGGESTION, Tests | RETAINED | `srp_mbx.c:130` expiry wake-up is unchanged; other work at 8x8/2if can wake transmission. Optional isolated missing-wake control remains distinct from the existing never-ends plant. |
| R836-3-S4 / R835-2-S1 SUGGESTION, Robustness | RETAINED | Refused Leave and licence ordering at `srp_mbx.c:296`, the poll predicate and sliced transmit remain unchanged. Optional explicit validity gating/invariant and a Listener-registered refusal test remain useful. No new reopening path was introduced by the cached gate. |

Earlier mandatory findings closed before round 5 remain closed: acceptance wording was publicly amended; first declaration is gated; refused withdrawal retains ownership and retries before starting its hold-off; publication-count tests and the bounds comment remain; the old plant count is replaced by 35 Talker plants at each interface count; the configured LeaveAllTime interpretation is explicit. The source comment scan found no newly added prohibited lane/reviewer/comment identifiers in the reviewed delta. Optional suggestions above are not promoted into requirements.

## Applied lenses and executable evidence

**Conformance and RTL/architecture.** `srp_mbx.c:639-684` caches only the successfully processed masked gate and full base. Initialization zeros the cache; only initialization and this entry write the gate/source destinations. Reset/rebuild paths retain those values, and a repeat call does not clear already owed declarations. Invalid interface and reentry checks precede the shortcut, and it releases `busy` on return. Base changes with the same mask and validity loss/reacquisition still take the reconciliation path. The new base-sensitive plant targets that distinction. The added fields' memory effects are measured in the ledger, including the 64 B change at 8x8/1if.

The head has no HDL or submodule-gitlink change from the source base. Existing mailbox, clocks, resets and CDC contracts therefore carry; the firmware scheduling and state changes were nevertheless checked against them. The header derivation is 2,000 + 19 + ceil(tx/10): **2,023 cs at one interface, 2,030 cs at two**. `srp_talker.cpp:55` derives its horizon from the headers, while the wire assertion independently requires at least 20,000 ms after the Leave. The public ruling's extra 10 ms is on the conservative side of the configured minimum. No second independently typed hold-off term was introduced.

**Robustness and Tests.** Repeated calls, changed base, changing validity mask, reset/rebuild, refused entry, and retained owed work were checked at the shortcut's cause. The retained declaration/refusal tests cover valid startup, lapse, unchanged/changed destinations, reallocation, probe expiry, Listener demand and admission swaps. The head's published SRP campaign has 415 rows, including 70 Talker rows, and catches the new repeat-ignores-base plant at both interface counts. The two-interface transmit-statement controls now plant 104 under 104.25, while the one-interface control plants 33 under 34. The notice self-test pins (140,62), checks 141 as a miss, and still distinguishes the first notice's bounds; the direct queue probe returns (0,1,1,0,1,1).

**Image carry.** Recomputed comparisons of the four published hash lists have the same 552 names. Round-8 image 73388996 -> sync 663b519b: none change. Sync -> 449d29d2: exactly 12 names change, six `srp_mbx.o` objects and their six two-interface images; none are one-interface. The published full instruction/section comparisons show only `7ed00693` -> `7ee00693`, `li a3,2029` -> `li a3,2030`. 449d29d2 -> exact head: none change. The comparison script includes every linked object and each ELF's loadable binary; the section comparisons cover more than just instruction text.

Thus the earlier legs carry for the unchanged executable paths; this is not a claim that the changed hold-off has identical behavior. Its affected arms were rerun: 11 one-interface Talker tests, 11 two-interface Talker tests, seven two-interface gate tests and 76 SRP/ACMP tests pass. The 8x8/2if valid-destinations rerun reports two groups, zero refusals/misses, zero of 3,052 passes over share, and 49 joins at 185.605-190.228 ms. The two raw measured logs are reported byte-identical to round 8; result changes are the restated costs/build identity. Binary comparison receipts were audited; no independent firmware relink was performed here.

**Rows, headroom and load.** Independent `flip-1x1.log` reproduces every row:

| Row | Head ms | Bound ms |
|---|---:|---:|
| R4 | 13.25 | 20 |
| R5 | 75.84 | 90 |
| R6 | 73.36 | 90 |
| First queued notice | 14.72 | 20 |
| Last queued notice | 136.65 | 140 |
| R4L | 203.57 | 238 |
| ACMP | 29.63 | 30 |
| ADP | 27.86 | 30 |
| MAAP | 27.96 | 30 |
| tx | 34.00 | 49 |
| txL | 48.58 | 49 |

At the committed cost tables, the grid selects built slice 900 us, least relative margin +0.0086. F2 must be resolved before those tables can be called fully surveyed. At pass-own cost 260 us (225+35), every row passes. The independent in-memory probe changes both relevant table entries: at 278 us every row still passes (last 137.93, txL 49.00); at 279, last 141.36 and txL 49.02 fail. This proves the stated 18 us headroom without editing the source tree. ACMP's 0.37 ms and txL's 0.42 ms margins remain small.

The 126 published survey rows are independently matched to live tables and rounded again, including poll costs and datapath events (F2 limits their coverage): 21,094 cycles -> 225 us base at one interface; 32,705 -> 345 base at two; 66,481 -> 700 long-notice poll; 3,437 -> 40 fixed events; 2,465 -> 30 AMAP; earlier 21,120 -> 225 MAAP timer. Both columns retain the larger applicable statement. The ordinary AECP comparison uses classes rather than comparing 235 us to a largest-command record, but F2 shows it omits the held SET_STREAM_INFO path and never selects the paced-class measurements. Other not-staged entries remain explicitly not staged, not measurement passes.

`probe.log` derives load term by term from these audited costs and the header/contract rates; `load.log` reproduces about **0.517 / 0.514 at 1x1/1if**, within 0.70, and **0.798 / 0.756 at 8x8/2if**, reported, not a passing 0.75 flip. This is analytical long-window demand based on measured leg costs, not a directly measured wall-clock utilization. At 8x8/2if the first notice is 21.11 ms: within the separately stated measured 22 ms allowance, but above the analytical tier model’s 20 ms row bound. R4L fits 238 ms; several other rows do not. The original acceptance amendment and public decisions retain that distinction.

**Every ledger point.** The exact-head clean-clone receipts agree with the ledger:

| Point | Fixture ROM / SRAM B; tiles | Platform ROM / SRAM B; tiles |
|---|---|---|
| 1x1/1if | 112,424 / 55,200; 41.0 | 117,488 / 56,224; 43.0 |
| 1x1/2if | 113,984 / 57,376; 42.5 | 119,072 / 58,400; 44.0 |
| 8x8/1if | 125,088 / 96,304; 55.0 | 130,200 / 97,328; 56.0 |
| 8x8/2if | 126,608 / 113,248; 59.0 | 131,752 / 114,224; 60.5 |

Platform ctrl_plat sizes are 17,536 / 19,072 / **18,240** / 20,352 B. The corrected record is not linked into the firmware. The two 8x8/2if harness arms are 126,916 / 113,312 B and 126,776 / 113,248 B, each 59.0 tiles, with **60 / 200 B** ROM headroom. Platform ROM headroom is **1,368 B**; its debt against 56 is **4.5 tiles = 18,432 B**. `plat_ledger.py` passes all four platform points and the exact-head memory gate passes. No full builder or ledger link was repeated by this reviewer.

**Full source-head pass.** The published final-head lane receipts identify 056d619d and clean clones. There are 139 workflow-step return-code files, all zero, and 226 explicitly reasoned non-executed steps; these are the author's local execution of workflow commands, not 139 hosted jobs. The coverage-ratchet step has rc 0. Campaign receipts record control 716/716, AECP 299 and SRP 415, no escaped rows. Four sweep specifications and completions identify the exact head: 15+17+17+16 = 65 suites, zero failures/timeouts; check totals 361,003+2,046,229+284,233+21,575 = 2,713,040. The firmware jobs leave the disclosed untracked dispatch-build directory; that is not a tracked-source change. The first pass at c772b1e5 is kept separately and does not stand in for the final pass.

The seven held-egress misses at each point remain explicitly reported. At two interfaces, two answering-arm passes and two largest-notice passes exceed share; these are the reported #890 scope, not hidden by rc 0. All published round-8 joins (359 one-interface and 750 two-interface) lie within 181-239 ms. No physical calibration or field skip is treated as hardware proof.

The published harness transcript replaces only two ephemeral temporary-directory names; redactions.json records both hashes. Independent focused execution completed: flip check, load check, grid, 1,033-control rows self-test and the complete harness self-test all exited 0 (harness: zero failures). The additional synthetic class probe demonstrates F2 despite those passing checks.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F2 MAJOR) | #895 acceptance/rulings; `srp_mbx.c:35,639`; `ctrl_loop.h:282,377`; `aecp_mbx.h:75`; flip/load/grid and survey receipts; derived hold-off | R836-4 | 056d619ddba179edb0dd2914e14a4b1d51988dd8 |
| RTL | CLEAN | Base/delta file and gitlink lists; `srp_mbx.h:83`; cache initialization/writer/reset invariant; mailbox publication contract; scheduling constants and every memory point | R836-4 | 056d619ddba179edb0dd2914e14a4b1d51988dd8 |
| Robustness | CLEAN | `srp_mbx.c:639-684` and retained refusal/rebuild paths; `srp_talker.cpp`; `srp_gate.hpp`; new base-sensitive plant and both interface receipts | R836-4 | 056d619ddba179edb0dd2914e14a4b1d51988dd8 |
| Tests | UNCLEAN (F2 MAJOR) | `srp_talker_mutants.py:181`; `selftest_notice.py:81-94`; `rows_tiers.py` and `flip_grade.py` controls; 139 step rcs, campaigns, exact-head sweep, hash/section comparisons; independent probes | R836-4 | 056d619ddba179edb0dd2914e14a4b1d51988dd8 |
| Docs | UNCLEAN (F1 MINOR, F2 MAJOR) | `SPLIT_CONTROL_MEMORY.md:519,2551,2682,2688,2689,2693`; `FR_NFR.md:390`; correct section 13 and SRP README; current PR and public evidence | R836-4 | 056d619ddba179edb0dd2914e14a4b1d51988dd8 |

## Limits and pending manager duties

This review uses published links, disassembly comparisons, campaign and suite receipts, plus independent lightweight graders/probes. It does not claim a fresh firmware build, full bank, hardware run, or authenticated signature. The historical raw binaries were not rebuilt or re-disassembled here. Some costs are derived and unstaged, as explicitly recorded. The small one-interface timing margins and 60 B harness ROM margin remain real limits.

No manager source bank at this exact head is claimed or inferred. Hosted/act acceptance remains the manager's duty; this reviewer did not run or adjudicate it. The manager must validate the current-dev merge candidate (source base cec88385, supplied live dev `6b66f66d89cf25d2717687bcc2c3bf617685a99a`) with the required builder/native banks, publish its receipts, finish independent reviews, apply the merge integrity/containment rules, and obtain merge authorization. The identical #902 trees do not waive that candidate duty. Acceptance 6, calibration and physical evidence remain outside this review. #906/#907 remain pre-existing scope; #890/#908/#909 and S14 debt remain visible.

Resolve F2 by grading the actual measured records and restating/recomputing if needed; repair F1 in the same response and re-review. Carry RS1 to the residue checklist. Optional suggestions above remain optional. `integrity.log` verifies all tracked root/submodule bytes, modes, index and required gitlinks against their heads; the detached source tree is clean.

R836-4 FINISHED
