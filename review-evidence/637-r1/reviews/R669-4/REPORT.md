[R669] POSITIVE - exact head 4ff3642e8fe9a0bd48d28374350390cde553bc32

R669-4 is the internal cleared-context review of issue #637 / PR #768, round 4, a narrow composition review. The head tree is `62626aefcfd7c4ff0b53f3a5413f700477bb9611`. The previously reviewed head is `1e914414557874648ac5041aff88b96908e0e053` (R669-3, POSITIVE). The source base is `e9cbb676`. The delta has two commits: the merge commit `d26fca65`, which merges dev `78ca9bdf` (PR #767 for #761/#762, on top of PR #766 already in the lane), and `4ff3642e`, which changes only the milan_dp README. It answers the composition assignment, PR #768 comment 6298729116. Live dev is `59740e3c` (PR #769).

**Verdict.** No BLOCKER, MAJOR or MINOR is open, and every lens is covered clean at this head. All three conflicted files keep both sides. `obj_dynmap` runs `[DYNMAP]`, then #767's `[762-DP]` case on its own fresh boot, then `[MAPREC]` over an erased window, and each section keeps its own counts. My probes show that neither case affects the other: each section's output is byte-identical to its own parent's run. The auto-merged `milan_datapath.sv` is an exact union of the two parents' changes. This round adds one SUGGESTION and two RESIDUE items. Every prior finding is reconciled below.

## What the delta is

| Artifact | Evidence | Result |
|---|---|---|
| Non-conflicted files | `receipts/merge-tree.txt`: I recomputed the automatic merge of `1e914414` and `78ca9bdf` (`git merge-tree`, tree `ef7e7d37`) and compared it with `d26fca65` | `d26fca65` differs from git's automatic merge only in the three conflicted files. Every other file, including `milan_datapath.sv` and the four auto-merged docs, is git's own merge result |
| `hdl/milan/milan_datapath.sv` | `receipts/merge-composition.txt` | Merge minus the lane parent equals dev's own change (`e26f1816..78ca9bdf`). Merge minus the dev parent equals the lane's own change (`e26f1816..1e914414`). Both are EQUAL on the +/- lines. #767's `stopped_i` is at `:7300` and the CRF-return restart (`tkd_crflk_q_r ^ crf_locked_w`) is at `:3305`. The lane's `amr_*` map writer and restore are byte-equal to `1e914414`'s change |
| `tb/verilator/milan_dp/dynmap_probes.vlt` | resolution diff vs `ef7e7d37` | Union of both sides: the lane's `#637` opens at `:26-45` and dev's `#762` elaborated-parameter opens at `:47-64`. Nothing was dropped; only the markers were removed |
| `tb/verilator/milan_dp/sim_nxn.cpp` | resolution diff; `receipts/merge-tree.txt` ("762 function body ... IDENTICAL") | The tail at `:3122-3128` calls `dynmap_power_on_and_adaptation_section()`, then `stopped_input_law_on_the_shipping_geometry()`, then `dynmap_map_records_section()`. The #762 function at `:4673` is byte-identical to dev's and sits in the `#ifdef DYNMAP_DEFAULT_TB` block (`:4427-4724`). `[MAPREC]` opens with `maprec_first_boot()` (`:4956`): a reset, then `load_the_saved_state_window(..., {})`, which is an erased window, then the boot walk |
| `tb/verilator/milan_dp/README.md` | resolution diff; `d26fca65..4ff3642e` diff | The leg row (`:84`), the #658 section intro (`:780-784`) and the `[762-DP]` paragraph (`:1359-1361`) state the order `[DYNMAP]`, `[762-DP]`, `[MAPREC]`. The 63-row campaign table (`:842-904`) is re-measured from "of 649" to "of 686" |
| Gitlinks | `receipts/merge-tree.txt` | No gitlink changes in `e9cbb676..4ff3642e`. The processor pin is `2cbed0a9` |

## Own probes (exact head unless stated; pinned Verilator 5.050, identity verified)

| Run | Result (`receipts/probes/sections-summary.txt`) |
|---|---|
| `obj_dynmap` at `4ff3642e` | 686/0. Preamble 52, `[DYNMAP]` 110, `[762-DP]` case 37, `[MAPREC]` 487 |
| `obj_dynmap` at dev `78ca9bdf` | 199/0 (52 + 110 + 37). Its `[DYNMAP]` and `[762-DP]` sections are byte-identical to the head's (`receipts/probes/762-section-dev-vs-head.diff` is empty; DYNMAP diff empty) |
| `[MAPREC]`, lane `1e914414` vs merge | The published lane log (`author-r3c/receipts/round3/legs/leg-dynmap.log`) and the merged log (`round3c/milan-dp/leg-dynmap.log`) match on all 608 section lines except one absolute-clock `[i]` line. That line's spacing is unchanged (`receipts/maprec-section-lane1e914414-vs-merge-published-logs.diff`) |
| Mutant: #762 `stopped_i` tied to `'0` at `:7300` | 686/2. Only `[762-DP] 2 stopped gap` and `[762-DP] 3 stopped silence` fail. `[MAPREC]` stays 487/0. This reproduces the author's m1 |
| Mutant: campaign row 15 (the restore refuses every framed record) | 686/83, all 83 in `[MAPREC]` (the table's "83 of 686"). `[762-DP]` stays 37/0 and `[DYNMAP]` 110/0 |
| `obj_maprec8`, `obj_maprec4` at head | 219/0, 137/0 |
| `obj_dynmap` on the live-dev test merge (tree `803f7b24`, from `4ff3642e` + `59740e3c`; text merge clean) | 688/0. `[762-DP]` case 39 (+2 from #769), `[MAPREC]` 487/0. See S1 |
| Docs gates at head (`receipts/probes/docs-*.log`) | `check_doc_paths` OK (1043 paths), `check_doc_style` OK, `docs_check` 0 findings. `check_em_dash` and `gen_toc` could not run here because the pinned Markdown renderer is not installed and no shared install is allowed. Their exact-head author receipts are rc 0 (`round3c/docs/d0-13`, `d0-48-*`) |

## Published evidence checked

- Evidence commit `1980192f`: all 844 `author-r3c/` files match `MANIFEST.json` (0 mismatches, 0 missing, 0 unlisted; `receipts/evidence-manifest-author-r3c.txt`). The host API reports the commit as unsigned, so integrity rests on the commit id and the manifest.
- The campaign at `d26fca65` (byte-identical to the head except the README): 68/68 PASS, 63/63 caught, five clean legs (`round3c/campaign/campaign-d26fca65.verdicts.txt`). All 63 README rows match it on mutant name, failure count and leg total (`receipts/readme-table-vs-campaign-d26fca65.txt`). Every row's verdict, name and failure count is unchanged from round 3's `600565b4` campaign (`receipts/campaign-600565b4-vs-d26fca65.txt`). So none of the 54 dynmap plants moves a `[762-DP]` check.
- The #767 wiring mutants at `d26fca65` (`round3c/wiring/`): m0 686/0. m1 and m2 fail exactly `[762-DP]` 2 and 3. m3 fails exactly `[762-DP] 4`. `[MAPREC]` is 487/0 in each.
- The milan_dp suite at `4ff3642e` is 12,892/0 over 17 tallies (`round3c/milan-dp/suite-tally.txt`, `leg-tallies.tsv`). The sweep has four shards at `4ff3642e`: 16+17+15+15 = 63 suites; 40,202 + 1,554,195 + 388,423 + 205,626 = 2,188,446 checks, 0 failures, 0 timed out, the four declared `tsn_fuzz` skips. Docs: 95/95 rc 0 at `4ff3642e`. Builder: both legs rc 0, with gate 11 declared NOT RUN. route-1x1 at `4ff3642e`: route complete, 0 routing errors, WNS +0.155 ns, WHS +0.036 ns, every resource verdict ok. ooc carry: 0 of `KL_pp_shadow`'s 50 sources changed since `887b6bf2`.
- Hosted checks at the exact head, snapshot 2026-10-21T02:07Z (`receipts/hosted-checks-snapshot.json`): 24 success, 1 skipped (Physical gPTP), 23 still queued or in progress, none failed. rtl-fast and verilator-lint succeeded. The manager owns hosted acceptance.

## Prior findings, reconciled at this head (read after my own pass)

| Finding | Disposition | Evidence at `4ff3642e` |
|---|---|---|
| R669-1, R670-1, R669-2-F1, R669-2-F2, R670-2-F1 (all MINOR or above) | RESOLVED (at R669-3/R670-3); not reopened | The lane-side RTL and tests they depend on are byte-equal to `1e914414`'s change (merge-composition EQUAL). `[MAPREC]` output is identical to the lane's, and the campaign is 63/63 with unchanged counts |
| R670-2-R1, R670-2-R2; R669-2 RES-1, RES-2, RES-3 (comment provenance) | RETAINED for the merge checklist (tracked by #746) | Still present, and only line numbers moved: `milan_datapath.sv:4926`, `:4930`; `sim_nxn.cpp:5628`; `dynmap_mutants.py:29`, `:35`, `:154`, `:168`, `:316`, `:345`, `:386-387`. README row 54 still says "the round-1 ordering" (the mutant name). The delta adds no new instance (scan of all lines added by the resolution and `4ff3642e`) |
| R669-2 RES-4 (docstring 19 vs 23) | RETAINED | `dynmap_mutants.py:29-38` unchanged |
| R669-2 RES-5 ("refused before the port is touched") | RETAINED | Now at `milan_datapath.sv:5495` |
| R669-2 S1, S2, S3; R669-1 S3 | Optional, unchanged | The artifacts they name (`amr_*` arms, `milan_dp/Makefile`) are not changed by the delta |
| R669-3-S1 (length-only record case) | Optional, unchanged | `[MAPREC]` lone-record section unchanged |
| R669-3-RES-1 (PR body roles "round 3 to be assigned") | RESOLVED | PR body lines 25-26 now read "round 3 assigned, notice 6298509526 / 6298519097, POSITIVE at `1e914414`" |
| R669-3-RES-2 ("(tb, hdl equal to the head)") | RETAINED | Now in the republished `author-r3c/HANDOFF.md:193` |
| R669-3-RES-3 ("So at the head: 60 of 60 caught ...") | RETAINED | `author-r3c/HANDOFF.md:304` |
| R669-3-RES-4 (round-3 validation rows cite no receipt) | RETAINED | PR body lines 106-110; the same gap recurs for round 3c (R669-4-RES-1) |

## Findings this round

### R669-4-S1 SUGGESTION - Tests, Docs - `tb/verilator/milan_dp/README.md:842-904` (the "of 686" denominators); the live-dev candidate - the leg total moves once #769 composes

- **Evidence.** The test merge of this head with live dev `59740e3c` is clean as text (tree `803f7b24`). On that tree `obj_dynmap` runs 688/0, and the `[762-DP]` case grows from 37 to 39 because #769 adds `[765]` checks in the shared stimulus (`receipts/probes/testmerge-sections.txt`). `[MAPREC]` stays 487/0. The README table's 54 dynmap rows state "N of 686", and the PR body and HANDOFF give 686 as the leg total. Under the candidate, those totals become stale. The per-mutant failure counts there are not measured.
- **Authority.** The README presents the table as measured. The figures are correct at this head, so this does not affect any lens here.
- **Optional outcome.** At the merge turn, either re-measure the table on the candidate or state that the table was measured at `d26fca65`. The table's date line already partly does this.
- **Verification.** The candidate bank's `obj_dynmap` total, and the campaign denominators if it is re-run.

### Residue (wording only; no lens left unclean; for the merge checklist)

| ID | Artifact | Defect | Exact fix |
|---|---|---|---|
| R669-4-RES-1 | PR #768 body, "Validation account (round 3c)" table (rows for milan_dp, campaign, wiring mutants, docs, builder, route-1x1, sweep) | The rows cite no receipt, although the receipts are published under `1980192f.../review-evidence/637-r1/author-r3c/receipts/round3c/` | Link `round3c/milan-dp/`, `round3c/campaign/campaign-d26fca65.verdicts.txt`, `round3c/wiring/wiring.log`, `round3c/docs/rc.tsv`, `round3c/builder/rc.tsv`, `round3c/route/route-1x1-check.log` and `round3c/sweep/` on their rows |
| R669-4-RES-2 | Issue #637 comment 6305925321 ("Commit: ... (branch `637-map-records`, local, not pushed)"); PR body lines 25-26 ("the round-3c head is not yet reviewed") | `4ff3642e` is now the published PR head, and round-4 reviews have started (notice 6305957530). Both statements are stale | Replace "local, not pushed" with "pushed as the PR head". On each role line, replace "the round-3c head is not yet reviewed" with "round 4 assigned, notice <id>, <verdict> at `4ff3642e`, comment <id>" once each verdict is published |

Comment rule (owner 2026-10-15): the delta's new source comments are clean. These are `sim_nxn.cpp:3123-3125`; the `dynmap_probes.vlt` lines are carried from the parents. They state behaviour with issue IDs, and none names a bench lane, lane, review round, reviewer or comment ID.

## Clean results by lens

- `[R669] PASS Conformance - hdl/milan/milan_datapath.sv:7300, :3305; receipts/merge-composition.txt; tb/verilator/milan_dp/sim_nxn.cpp:3122-3128; receipts/probes/sections-summary.txt - the merged RTL holds #767's 5.3.8.7 stopped_i wiring and the 4.4.4.3 CRF-return restart alongside this PR's map writer and restore (each side's change reproduced exactly). The Milan 5.3.9.1/5.3.10.1 save-and-restore behaviour is graded unchanged ([MAPREC] 487/0, byte-identical to the lane), and #762 is graded unchanged ([762-DP] identical to dev). Issue acceptance is unchanged from round 3. The on-board cold cycle is not claimed.`
- `[R669] PASS RTL - git diff 1e914414..4ff3642e -- hdl (dev's change only, EQUAL); receipts/merge-tree.txt (no gitlink change, auto-merge equals d26fca65 outside three tb files); author-r3c/receipts/round3c/route/route-1x1-check.log (route complete, WNS +0.155, WHS +0.036); hosted verilator-lint success at exact head - no lane RTL byte changed. The merged datapath is the exact union. The R669-2/R669-3 RTL verdict on amr_fsm, the PP_STAT composition and the arbiter carries forward, because nothing it depends on changed.`
- `[R669] PASS Robustness - receipts/probes/mutrestore.*, mut762wire.*; receipts/maprec-section-lane1e914414-vs-merge-published-logs.diff - the two cases are isolated by a fresh reset and an erased window. A total restore failure (83 MAPREC failures) leaves [762-DP] 37/0, and a broken #762 wiring leaves [MAPREC] 487/0. The torn, lone-record, deadline, failing-write and roll-back arms produce the lane's exact output after the #762 case has run.`
- `[R669] PASS Tests - receipts/probes/head.*, headmp8.*, headmp4.*, dev78ca9bdf.*; receipts/readme-table-vs-campaign-d26fca65.txt; receipts/campaign-600565b4-vs-d26fca65.txt; author-r3c/receipts/round3c/{campaign,wiring,milan-dp,sweep} - 686/0, 219/0 and 137/0 are reproduced at the head. 63/63 controls are caught at d26fca65 with failure counts unchanged from round 3. The #767 wiring controls still fire only on [762-DP]. The vacuity guard is still 59. The suite is 12,892/0, and the sweep is 63 suites, 2,188,446 checks, 0 failures.`
- `[R669] PASS Docs - tb/verilator/milan_dp/README.md:84, :780-784, :836-904, :1359-1361; PR body "Round 3c" section; author-r3c/receipts/round3c/docs/rc.tsv (95/95 rc 0 at 4ff3642e); receipts/probes/docs-check_doc_paths.py.log, docs-check_doc_style.py.log, docs-docs_check.py.log - the run order, per-section counts (52/110/37/487) and re-measured table match the executed leg and the verdicts. Wording residue is R669-4-RES-1 and RES-2. S1 is optional.`

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `milan_datapath.sv:3305`, `:7300`, `amr_*` (composition EQUAL); `sim_nxn.cpp:3122-3128`; own leg runs; issue acceptance (unchanged) | R669-4 | `4ff3642e8fe9a0bd48d28374350390cde553bc32` |
| RTL | CLEAN | merge composition of `milan_datapath.sv`; recomputed auto-merge; gitlinks; route-1x1 receipt at head; hosted lint at head | R669-4 | `4ff3642e8fe9a0bd48d28374350390cde553bc32` |
| Robustness | CLEAN | isolation probes (`mutrestore`, `mut762wire`); `[MAPREC]` section lane-vs-merge diff; `maprec_first_boot` erased window | R669-4 | `4ff3642e8fe9a0bd48d28374350390cde553bc32` |
| Tests | CLEAN | own `obj_dynmap`/`maprec8`/`maprec4` and dev-parent runs; campaign verdicts and README table cross-check; wiring receipts; suite and sweep receipts | R669-4 | `4ff3642e8fe9a0bd48d28374350390cde553bc32` |
| Docs | CLEAN | milan_dp README `:84`, `:780-784`, `:836-904`, `:1359-1361`; PR body round 3c; docs receipts; own doc path/style/docs_check runs | R669-4 | `4ff3642e8fe9a0bd48d28374350390cde553bc32` |

## Real limits

- I did not re-run the full milan_dp make, the sweep, the builder legs, route-1x1, the campaign, Yosys, xvlog or the firmware steps. Those rest on the author's exact-head (or `d26fca65`, README-only different) receipts, which I verified against the published manifest and spot-checked. I ran the four `obj_dynmap` variants, `maprec8` and `maprec4`, and three docs gates.
- `check_em_dash` and `gen_toc` were not reproduced (the renderer is not installed here). Their exact-head author receipts are rc 0.
- No manager source bank runs at this head, and none is claimed or inferred. The evidence commit is unsigned. Physical calibration and the on-board cold cycle are NOT RUN, and the field skips are not hardware proof.
- Hosted gates were still running at the snapshot. None had failed.

## Pending manager duties

- Build and validate the current-dev merge candidate (base `e9cbb676` to live dev `59740e3c`) with the builder and native banks, and link the receipts. My test merge is clean as text, and its `obj_dynmap` is 688/0 (S1). The candidate's milan_dp, avtp_rxmon and crf_rx suites carry #769's own changes.
- Decide S1: re-measure or qualify the README's "of 686" totals for the candidate.
- Accept the exact-head hosted `verilator-suites` and `yosys-portability` results once they complete.
- Carry R669-4-RES-1/RES-2 and the retained residue (R670-2-R1/R2, R669-2 RES-1 to RES-5, R669-3-RES-2 to RES-4) to the merge checklist.
- Merge only on explicit maintainer authorization, with two independent positive reviews.

R669-4 FINISHED
