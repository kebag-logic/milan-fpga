[R866] POSITIVE - exact head 732726660a88cd79a568d650d955d535fe79c720

External independent composition review, R866-1, of PR #945 onto `dev-soft-core` at `cb96336d`. The exact reviewed tree is `11d45104e6c71b7623cec24bcac27610c5a402be`. The independent diff pass and this verdict/ledger were written before checking the PR discussion for prior findings. That discussion contained only the two review-start notices: there are no prior PR #945 findings to resolve or retain.

No open BLOCKER, MAJOR or MINOR found in the composition scope. Two wording-only residues are recorded below.

Scope and authority: AGENTS.md sections 6–7, CONTRIBUTING.md, docs/README.md, issues #665, #871, #894, #917, #929, #919, #920, #923, #924, #925, #930, #936 and #927 and their public scope decisions, REQUIREMENTS.md, docs/reference/FR_NFR.md (NFR-SCOUT-01/02/03 and the restatement/row rules), docs/design/MAILBOX_SPLIT.md and SPLIT_CONTROL_MEMORY.md. The #665 composition ruling is [6939574513](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6939574513). The source PR implementations were not re-reviewed; this review covers their union, recorded conflict resolutions, composition fixes, measurements and release record.

Frozen source chain verified against public PR metadata and the actual two-parent merge commits:

| PR | Frozen head | Train merge | Public source review coverage |
|---|---|---|---|
| #881 | d3e61e37 | 43b954e6 | R821 at frozen head; R822 at d3566d44 |
| #914 | e1ecce20 | 877c99e4 | R843 at frozen head; R844 at d0a2a160 |
| #918 | 394612c5 | 9c0e1974 | R845 and R846 at frozen head |
| #935 | 37255683 | 22a82038 | R855 and R856 at frozen head |
| #933 | 1a1e6665 | 2078c438 | R851 and R852 at frozen head |
| #938 | 81c9a1a0 | 7c28f53f | R857 at frozen head; R858 at bd252db1 |
| #931 | d06ded5a | 6a8126e4 | R847 and R848 at frozen head |
| #932 | 0fdfdba7 | 31304b74 | R849 at frozen head; R850 at 5f625090 |
| #934 | 544fd72c | 8f6fbb84 | R853 at frozen head; R854 at 9aa55d3b |
| #944 | d1aa4c44 | 49f005b9 | R861 and R862 at frozen head |
| #939 | 0297a19a | 3e908539 | R863 and R864 at frozen head |

Every full frozen SHA equals its public PR head, is the merge's second parent and is an ancestor of the reviewed head (`public/frozen-heads.json`, `receipts/checks/history.log`). The table deliberately does not call an ancestor signature an exact-head signature. The five ancestor-covered pairs use #665's explicit [2026-11-16 ruling](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6939460730), which accepts that coverage when the other source reviewer covers the subsequent delta. The signatures and their public URLs are preserved in `public/source-signatures.json`.

Conflict resolutions: all tables in the five published author RESOLUTIONS records were compared with actual remerge diffs, retained in `receipts/history/`. Material resolutions were checked as follows:

| Merge(s) | Union checked | Defect-sensitive verification examined |
|---|---|---|
| 43b954e6 | REBOOT and GET_AS_PATH tests, plants and record-completeness rules both retained; GET_AS_PATH moved to B24 with its plant target updated | Accepted/refused REBOOT and answered-path controls, B24 response contents, public firmware shards |
| 877c99e4 | Shape-specific costs and completeness composed with REBOOT/path checks; TX under-statement plants now address shape rows | Both point flip checks; per-shape and mixed-point completeness controls |
| 9c0e1974 | Token-held, reboot, largest-notice and datapath groups/imports retained | Harness group inventory and refusal controls |
| 22a82038 | Listener and mailbox-entity test arms both scheduled | Firmware invocation inventory; source suite receipts |
| 2078c438, 7c28f53f | PHY, identity/refusal, reboot and saved-name context/ports preserved; journal and shape arguments composed | Boot/PHY tests, save-age and journal controls, regenerated coverage record |
| 6a8126e4 | GSI and EDIT windows both dispatched; `own_point` and the measured memory ledger retained | Wrong-symbol/point and half-tile refusal controls; edit/face plants. The removed product flag/refusals are explicitly ruled removals in #665 comment 6950343235 |
| 31304b74 | Listener-kind and listener-copy plants both included; latest-kind copy oracle brought into agreement with #925 | Independent reference/copy sequence comparison, SRP mutation campaign; ratchet remains full covered/total |
| 8f6fbb84 | Entry/participant and held-Talker observation both parsed; owner/opportunity MRP grading preserved; source-fixed twin expectations composed | MRP owner/opportunity controls; twin expected rows and plant inventory; no new gate waiver |
| 49f005b9 | Face and notice plants both spliced; build-dependent held-Talker and talker-notices groups both present; twin differences assigned to #943 | Firmware notice/face plants; talker-notice verdict controls; sixteen-plant twin contract |
| 3e908539 | README table/contents union only; no logic conflict | Actual remerge diff, unchanged CPU binaries and seven confirmation groups |

Composition fixes were inspected against both pre-change behavior and the union's measured failure. The map-edit cut (`aecp_maps.c:18,106,466`) retains the short descriptor/body guards, reads invariant port geometry once and extracts the same ten channel bits. The independent probe exhausts 262,144 type/channel combinations, with ignored bits populated. The PHY/store arbitration (`ctrl_plat_phy.c:295,326`; `nvm_store.c:893`) gives an owed centisecond save step priority; otherwise an owed PHY frame excludes the extra save step. The B12, L5 and L6 tests and all four new plants distinguish the prohibited alternatives, including durable save under perpetual failed probes. The plant compile correction retains `owes()` without changing the planted error.

The notice cut (`aecp.c:670`) tracks each working buffer's cached interface MAC through buffer swaps, caches port access within the walk and reads recipient values before writing the frame. The mailbox helper/inlining changes preserve submit/wait/error handling; T8 checks that a word-loop commit still proceeds after an earlier DMA error. The listener cut avoids only an unchanged boolean publication; the called `acmp_listener_registered()` has no additional observable operation on a valid unchanged binding. These cuts address union cost regressions; they do not alter the source PR protocols.

The claimed pure rewraps are AST-identical. The moved burst/MRP dictionaries and stream-info/PHY mutation rows are AST-identical after expanding their in-place module/function splices. The moved talker-notice verdict is identical after removing the self-import/module qualification. The shape argument fold was checked at every changed caller. Receipts: `history.log`, `refactors.log`, `format-hot.log`. The final hot list exactly equals the published ordered trace list after removing only `aecp owe` and `aecp owed_drain`: 268 traced, 266 retained, with the published 54-image filter and three trace hashes. No entry was hand-inserted or reordered.

Measured figures were recomputed using integer arithmetic at 100 MHz: `ceil(cycles × 1.05 / 100 / 5) × 5` microseconds. The survey rows were also parsed and their published rounded values independently recalculated.

| Restated cost | Measured cycles | Recomputed statement, us |
|---|---:|---:|
| 1x1/1if paced one-row edit | 29,331 | 310 |
| 8x8/1if poll base | 28,417 | 300 |
| 8x8/1if retained apply | 35,350 | 375 |
| 8x8/1if MAAP record | 16,682 | 180 |
| 8x8/1if SRP record/unit | 35,547 | 375 |
| 8x8/1if ADP record | 12,779 | 135 |
| 8x8/2if MAAP record | 14,770 | 160 |
| 8x8/2if fixed events | 4,069 | 45 |
| 8x8/2if AECP event | 11,404 | 120 |

At this head the locally recomputed 1x1/1if rows are last notice 137.97/140 ms, ACMP 29.93/30 ms and txL 48.89/49 ms; load at the pin is 0.522/0.70. Those narrow ACMP and txL margins are retained rather than rounded into a broader claim. The reported 8x8/2if load is 0.799 against its 0.70 flip ceiling, an existing held limitation, not a passing point.

Historical survey rows reporting ADP 130 as exceeded are superseded by the carried 135 restatement, not discarded evidence. Final local flip/load checks pass. At 8x8/1if, TX's 76.81 ms row is covered by 77 ms, still ≤80 ms, so the withdrawn Talker hold-off remains 8 cs. The 375-us unit is carried by the measured image; all four arm sets complete, the receipt reports no additional budget miss beyond the seven known held-egress misses, and 119 join intervals lie in 187.150–190.414 ms within 181–239 ms. Load is 0.744 ≤0.75. The existing 1x1/1if 0.70 ceiling, last notice 140 ms, ACMP 30 ms, txL 49 ms and other owner row bounds remain unchanged. The separate known 8x8/2if limits are not represented as passing supported-shape or hardware qualification.

Step 11 carry is supported by both required receipts: twelve full SHA256 image identities are equal before/after #939 and at 73272666; the confirmation diff is empty for 8x8/1if held-Talker, AECP, largest-notice and fanout, 1x1/1if largest-notice and fanout, and 8x8/2if fanout. Script/log identities and measured values are recorded in `receipts/published/regrade/confdiff-final.txt`. These are published receipt comparisons, not a claim that binary images absent from the archive were independently re-hashed.

The ROM ledger also follows the 2026-11-15 S14-debt rule. Rounding ROM and SRAM independently to 2,048-byte half-tile granules reproduces 44.5/45.5 RAMB36 at 1x1 with one/two interfaces, 58.0 at 8x8/1if and 62.5 at 8x8/2if. The 8x8/1if ROM is 137,472 bytes, 256 beyond its former capacity and 1,792 below its new capacity. The size fixture’s largest arm requires 60.5 tiles. Published platform-ledger controls catch all nine planted stale-key, over-budget and unlinked-override defects. These are named ROM debts, not fit or timing exceptions.

The split routes use the actual #818 floor, setup ≥0.030 ns and hold ≥0, best of three. At 1x1/1if the three setup/hold pairs are 0.141/0.033, 0.054/0.036 and 0.031/0.036 ns; at 8x8/1if they are 0.073/0.034, 0.064/0.027 and 0.006/0.036 ns. The best routes pass at both points. The losing 0.006-ns route is retained as a losing route, and the obsolete 0.030-ns hold reading in historical summaries is not the acceptance floor. #939 supplies the logic cut; no floor exception was taken.

The final commit changes only `syn/ooc/pp_resource_baseline.json`. Its entire routed-release record equals the published record-write JSON: 54,002 LUT, 55,203 FF, 15,849 slices, 71 RAMB36, 27 RAMB18 and 15 DSP, setup/hold 0.194/0.017 ns on the selected ExtraTimingOpt route. The three release routes are 0.115/0.033, 0.053/0.017 and 0.194/0.017 ns; selected-route resource and corner checks pass. The +541 LUT baseline increase is recorded debt. Same-directive attribution sums to +400 LUT/+262 FF: render crossing +121/+192 and −3 RAMB36/+128 LUTRAM, meter +41/−18, EDIT +96 FF, remaining variation +238/−8. This agrees with #665 comments 6979461559, 6979996755 and 6981065172.

The distributed-RAM render FIFO is shared by the release and 1x1 split images; it is not split-only. The 8x8/1if split has no render master. Raw cell, clock, exception, timing and CDC reports support the corrected premise: the relevant write-to-read clock pair has 201 Safe, zero Unsafe/Unknown endpoints; the render instance has CDC-15 Warning ×192 and the pre-existing pointer CDC-2 ×2/CDC-5 ×2, no CDC-26 or Critical path on this crossing. Its storage-to-register paths are covered by asynchronous clock groups. The synchronized pointer/empty-controlled read is the recorded stability argument; no waiver was added. This is report-based evidence, not physical calibration.

Published gate receipts cover all four firmware shards, the twin and plants, touched datapath suites, mailbox/DMA plants, meter plants (38/38), render controls (32 PASS), image/ledger checks and the completed harness self-test. Input-carry assertions are in `receipts/checks/gate-carry.log`: since the step-11 execution, only the resource record, the separately retested load statement and a trailing blank changed. The completed harness self-test at 4374cc27 has exactly the same harness bytes as this head. Larger published logs are explicitly hash/tail stubs. In particular, the twin stub exposes maps/no-edit results and the aggregate successful exit, not every individual earlier plant line. No stronger raw-log inspection is claimed.

Local evidence: `run_checks.py` passed docs, idiom, hygiene, both flip points, flip/load controls, load and resource-record checks; `check_history.py`, `check_refactors.py`, `audit_receipts.py`, `audit_gate_carry.py` and `probe_format.py` passed. The initial local `run.py --self-test` was stopped by the review runner's 500-second timeout after 55 caught mutants and no unexpected failure; its rc=124 is retained and is not presented as a full pass. Independent firmware execution results are recorded in `receipts/firmware/`. No manager source bank is claimed.

The local harness self-test subsequently completed through `resume_selftest.py --jobs 4`: unmutated checks passed, and the 55 completed mutants from the original run plus 240 remaining mutants cover all 295 names, all caught. All four continuation partitions returned zero (`run-resume.log`, `run-resume-0.log` through `run-resume-3.log` and their rc files). The continuation uses the repository's unchanged `checks()` and mutation contexts; it changes only scheduling and verifies name coverage.

Independent final-head firmware validation completed: all four invocations of `sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard INDEX/4`, with separate scratch build directories, returned zero and printed PASS. The general firmware campaign caught 797/797 mutants, including all four composition-specific PHY/store plants; the AECP and SRP mutation shards also completed without an escaped plant. The normal shard completed all 85 scheduled arms. Full raw logs, exit codes and the invocation summary are in `receipts/firmware/`. All started foreground drivers have completed.

Reviewer-owned coverage ledger:

[R866] PASS Conformance — receipts/checks/history.log, receipt-audit.log, flip1.log and flip8.log — frozen ancestry, restatements and owner bounds checked against the public #665 rulings and NFR-SCOUT requirements.

[R866] PASS RTL — receipts/history/3e908539.diff; receipts/published/regrade/fit-summary-p11.txt; receipts/published/step11/cdc/fcdc-summary.txt; syn/ooc/pp_resource_baseline.json — composition wiring, best-of-three floors, release record and scoped CDC findings checked against the accepted step-11 and release rulings.

[R866] PASS Robustness — sw/firmware/ctrl/plat/ctrl_plat_phy.c:326, sw/firmware/ctrl/aecp/aecp_maps.c:466, sw/firmware/ctrl/aecp/aecp.c:670 and receipts/firmware/ — owed-step/frame exclusion, malformed/boundary map handling, recipient/buffer identity and failure paths checked against preserved interface contracts and defect-sensitive campaigns.

[R866] PASS Tests — receipts/checks/refactors.log, run-resume.log, gate-carry.log; receipts/firmware/; receipts/published/r5-p11-render.log — mutation tables, invocation union, caught plants and evidence applicability checked against the no-weakened-check rule.

[R866] PASS Docs — docs/reference/FR_NFR.md:393, docs/design/SPLIT_CONTROL_MEMORY.md:675, public PR #945 and the published RESOLUTIONS tables — current figures, historical limits, release attribution and corrected shared-FIFO premise checked against measurements and public decisions; wording residues below do not change claims.

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #665 public scope rulings; eleven frozen source heads and merge parents; ctrl_loop.h; flip_grade.py/load_grade.py; published cost, image-hash and confirmation receipts | R866-1 | 732726660a88cd79a568d650d955d535fe79c720 |
| RTL | CLEAN | Every merge remerge-diff; step-11 README resolution; release resource record; split timing receipts; render FIFO CDC, cells, timing exceptions and hierarchy reports | R866-1 | 732726660a88cd79a568d650d955d535fe79c720 |
| Robustness | CLEAN | ctrl_plat_phy.c/nvm_store.c; aecp_maps.c; aecp.c fanout; mbx_dma.c/mbx.c; srp_listeners.cpp; source-head firmware and twin mutation receipts | R866-1 | 732726660a88cd79a568d650d955d535fe79c720 |
| Tests | CLEAN | Resolution test unions; mutation relocation AST comparisons; four published firmware shards; twin and touched datapath suite receipts; local flip/load controls and hygiene gates | R866-1 | 732726660a88cd79a568d650d955d535fe79c720 |
| Docs | CLEAN | docs/README.md; REQUIREMENTS.md and docs/reference/FR_NFR.md; MAILBOX_SPLIT.md; RESOLUTIONS tables; PR #945 frozen-step table and release/CDC record | R866-1 | 732726660a88cd79a568d650d955d535fe79c720 |

[R866] RESIDUE Docs — sw/firmware/ctrl/test/test_plat_boot.cpp:91,95,116,119 — R866-1-R1: bench labels in composition comment prose.

- Authority/evidence: the owner comment rule of 2026-10-15 forbids bench labels in source comments. The composition-renumbered GET_AS_PATH entry and added PHY inventory text carry B24, Phy.B11/Phy.B12/Phy.L1–L6 and L5/L6 labels.
- Impact: wording violates the source-comment convention. It changes no behavior, measurement, figure, verdict, clause claim or privacy rule.
- Required outcome / exact fix: remove the B24 prefix on line 91, the parenthetical label list on line 95 and the L5/L6 prefixes on lines 116/119; keep the behavioral descriptions and issue/requirement references. Do not rename executable tests or change assertions.
- Verification: inspect the comment-only diff; the relevant prose contains no bench identifiers and executable bytes are unchanged.

[R866] RESIDUE Docs — sw/firmware/ctrl/plat/ctrl_split_hot.txt:14,19 — R866-1-R2: issue-comment IDs in the hot-list header.

- Authority/evidence: the same owner rule forbids issue-comment IDs in source comments. The new hot-list header contains issuecomment-6959600243 and issuecomment-6967930396.
- Impact: wording violates the source-comment convention; list entries, ordering, hashes, measurements and acceptance rules are unaffected.
- Required outcome / exact fix: delete those two IDs and their adjacent separating commas as needed, keeping issue #665, ruling dates, item numbers and NFR-SCOUT-01.
- Verification: only header prose changes; all 266 ordered entries and three trace hashes remain byte-identical.

Limits: this is the source composition review, not current-dev merge-candidate acceptance. Source-PR metadata responses bundled source-review bodies; those bodies were not used as technical evidence for this composition verdict. Source signatures were extracted solely to verify the freeze contract. No other composition review report was used. Raw CDC summaries contain unrelated Critical paths; the clean statement applies only to the reviewed render crossing and its composition, not whole-design CDC closure. Some published large logs and timing reports are hash-and-tail stubs; no absent full log was claimed to have been read. No fresh route, physical calibration or hardware run was performed. Physical calibration was NOT RUN in the published evidence; field skips supply no hardware proof.

Pending manager duties: validate the final current-dev merge candidate against live dev `e275d7950ef3385753e6a15d2e191ba855b171ed`, run the required builder/native banks and link their receipts, accept the hosted/local-replication evidence while distinguishing executed from skipped contexts, obtain the other independent composition verdict, and satisfy the remaining merge/containment and hardware qualification obligations. The source base remains `cb96336d`; there is no manager source bank at this head. This review neither authorizes a merge nor substitutes for those duties. Carry R866-1-R1/R2 to the residue checklist; retain the existing #640 resource debt and S14 ROM debt.

Reproduction: from the detached candidate clone, run the portable scripts in `scripts/`. `prepare_evidence.py` rehydrates only the named public author receipts from archive commit `66fea879135dec78ecfb2410d5dc2115c1a29077` into `scratch/`; it reads no other reviewer report. Audit outputs and original execution logs are in `receipts/`. MANIFEST.sha256 lists the publishable packet; scratch builds and extractions are excluded. The tracked-byte/mode/index check verifies all required initialized submodules, not merely a clean status display.

R866-1 FINISHED
