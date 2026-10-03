[R446] POSITIVE - exact head 68d26ea034789ce2519db22d0df4e4328bc1b0de

# R446-8: internal review of issue #234 / PR #638, rounds 7 and 7b

- Role: internal independent reviewer, cleared context, own detached clone.
- Exact head `68d26ea034789ce2519db22d0df4e4328bc1b0de`, tree `4bc95158cc7e2b5f64051a100b770298ef194a70`. The remote branch and `refs/pull/638/head` both resolve to this commit. It contains live dev `5fabb46e767c9308ab2580916237f43577698c6e`.
- Focus: the delta `d5f56313..68d26ea0`, which is two `--no-ff` merges of dev and three lane commits. Checked against the composition review R446-7 (F1 MAJOR), the round-7 assignment 5972491855 (re-baseline by option (a)) and the round-7b assignment 5973328289 (merge dev `5fabb46e`).

## Verdict

POSITIVE. R446-7 F1 is resolved by option (a):

- **The record and the published runs:** the three endpoints were measured again on the composed tree. The committed records equal the published `record --write` output field for field.
- **Gate results:** `check` exits 0 on all three runs and `check-baseline` is green.
- **Policy:** every tolerance, floor and ceiling is unchanged (21 of 21 fields).
- **Independent corroboration:** PR #634's own published build of the same image reports the same figures.
- **Merges:** both merges reproduce bit for bit with `git merge-tree`.
- **Docs:** brought to the new tree. The `1269cdaf` record is kept as dated history, and both new rules are stated.

No BLOCKER, MAJOR or MINOR is open. One new RESIDUE (R1, PR body) and one new SUGGESTION (S1, evidence packet) are recorded. R446-5 R1 (RESIDUE) and the earlier SUGGESTIONs are retained.

## Reconstruction

**Authorities and scope**
- Read: AGENTS.md, CONTRIBUTING.md (by reference from AGENTS.md), `docs/README.md`, and the #234 body.
- Scope and decisions on #234: lane 5966260488, rulings 5967852698, owner decision 5967924270, round-7 assignment 5972491855, round-7 REVIEW READY 5973319945, round-7b assignment 5973328289, round-7b REVIEW READY 5973356984.
- Requirement: NFR-RES-01 (`docs/reference/FR_NFR.md`). Interface authorities: `docs/design/AREA_BUDGET.md` and `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`.

**Diff and history**
- The diff and history `1269cdaf..68d26ea0`, focused on `d5f56313..68d26ea0`.
- The lane's own commits `4d81e10d..aabdc283` touch 4 files:
  - `syn/ooc/pp_resource_baseline.json`
  - `docs/design/AREA_BUDGET.md`
  - `docs/findings/234_PP_SHADOW_AREA_BASELINE.md`
  - `docs/findings/README.md`

**Public evidence**
- The round-1 archive `43ad8362:review-evidence/234-r1/author`.
- The round-7 author archive on `234-review-evidence`, commit `22b292d3ac9c3f80131e07d4e2a16e8afd068578`, path `review-evidence/234-r1/author-r7`: run receipts, pre-check and record-write logs, and `check` logs.
- PR #634's public evidence archive, `629-m2-review-evidence` at `ef8d033c`, `author-r4/receipts`. It holds the hierarchical utilization, route status and timing excerpt of the same image.
- The exact-head hosted check runs.

**Order of work**
- I read prior review reports only after writing `receipts/independent-verdict-before-prior-findings.txt`. That file was written before I opened any prior report.
- R446-7 is this reviewer's own earlier round.

## What was verified

**1. Merges (Conformance)** (`receipts/cross_checks.log` section 1, `receipts/readme_rows.log`)
- `4d81e10d`:
  - Its parents are `d5f56313` and `546437243e87`.
  - Its recorded tree `04a0c948` equals `git merge-tree --write-tree`'s.
- `68d26ea0`:
  - Its parents are `aabdc283` and `5fabb46e`.
  - Its recorded tree `4bc95158` equals `git merge-tree --write-tree`'s.
- Neither merge has any hand edit; the README rows were not hand-merged either.
- `docs/findings/README.md`:
  - It differs from live dev by exactly this PR's two rows.
  - It differs from `aabdc283` by exactly PR #646's `629_...` row.
- Dev's delta `54643724..5fabb46e` is two docs files.
- Against live dev, the PR has no build-input change.
- All four gitlinks are identical at `1269cdaf`, `54643724`, `5fabb46e` and the head.

**2. The re-recorded endpoints (Conformance, RTL)** (`scripts/check_record.py`, `receipts/check_record_vs_d5f56313.log`, 0 mismatches)
- Each committed endpoint record equals the JSON printed by the published `record-write-C-<endpoint>.log` (round-7 archive). That covers kind, identity, `inputs_sha256`, figures and every sub-block scope.
- Route: 50,767 LUT, 59,634 FF, 15,832 slices, WNS +0.193 ns, WHS +0.024 ns, RAMB36/RAMB18/DSP 79/27/14.
- `ooc-1x1`: 24,332 LUT and 25,345 FF. `ooc-8x8`: 31,556 LUT and 33,937 FF.
- The identity (tool, device, design, state, flow, clock) is unchanged from the first record.
- Each endpoint's `measured` note (`syn/ooc/pp_resource_baseline.json:450,917,1374`) is the only hand-edited field. Each names dev `54643724` and keeps "first recorded at dev 1269cdaf".
- Published `check` receipts exit 0 on all three runs (`final-real/gate-check-C-*.log`, rc 0, at `aabdc283`). The route prints "route status: complete".
- `pp_resource_baseline.json` is byte-identical between `a89d0696`, `aabdc283` and the head, so those receipts apply at the head.
- Pre-check against the first record: the route gives rc 1 (+639 LUT and +628 FF over 500 and 600), and both standalone endpoints give rc 0.
- The receipts table at `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:118-123` matches the published `run-receipts.json` exactly: log digests, bytes and minutes for all four runs.
- **Independent corroboration:** PR #634's own Vivado build of the same image is a separate run (`sw/litex/build.sh`, its archive `author-r4`). It gives:
  - totals of 50,767 LUT and 59,634 FF;
  - `milan_datapath` 42,200 LUT / 48,433 FF;
  - the SoC top's own logic 4,847 / 6,072, and the CPU 3,524 / 4,734;
  - `pp_shadow` 23,904 / 24,265, equal to the record's `wrapper` scope;
  - the meter 483 LUT (32 LUTRAM) / 630 FF;
  - 106,622 of 106,622 nets routed with 0 errors, and WNS/WHS 0.193/0.024.

  See `receipts/cross_checks.log` section 4.

**3. Policy unchanged (Conformance, Robustness)** (`receipts/check_record_vs_d5f56313.log`)
- Every policy field is unchanged against `d5f56313`, by value and type. That is 21 fields:
  - route tolerance: LUT 500, FF 600, SLICE 80, RAMB36/RAMB18/DSP 0, WNS/WHS fall 0.25;
  - route floors: WNS 0.03, WHS 0.0;
  - route ceiling: BRAM_TILE 121.5;
  - `ooc-1x1` tolerance: 250/250/0/0/0;
  - `ooc-8x8` tolerance: 316/339/0/0/0.
- The top-level `schema` and `description` are unchanged.
- Probe `scripts/probe_policy_plants.sh` (`receipts/probe_policy_plants.log`), run on a disposable copy:
  - Eleven single-field policy plants into the re-recorded baseline are each refused by `check-baseline` with rc 2, with the table cell named.
  - The control, a note-only edit and a record-figure edit pass.

**4. Delta attribution (Conformance, RTL, Docs)**
- **The meter** (`findings:76-78`, `AREA_BUDGET.md:123`): 483 LUT, 32 of them memory, and 630 FF. This equals PR #634's published hierarchical report. Its share is 76 % of the +639 LUT growth.
- **The rest of `milan_datapath`, +223 LUT, -3 FF** (`findings:72,81-85`):
  - The arithmetic is checked in `receipts/arith_check.log`.
  - The C-side instance figures equal PR #634's report: csr 3,073; media_nco 130; media_grid_align 373; mmcm_servo 899; aaf_latency_tap_bank 674; talker_diag 225; ctl_tx_mux 85; chan_map_capture 1,079.
  - "PR #634 changed the source of four of its moved instances" matches `git diff 1269cdaf 54643724 -- hdl`. The changed sources are `milan_csr.sv`, `KL_media_nco.sv`, `KL_media_grid_align.sv` and `KL_mmcm_drp_servo.sv`. The meter is new and `milan_datapath.sv` changed. No source of `aaf_latency_tap_bank`, `talker_diag`, `ctl_tx_mux` or `chan_map_capture` changed.
  - The remaining -22 LUT is reproduced.
- **`DESC_NAME_ENTRIES_P`** (`findings:41,44-48`): I regenerated both shapes at `1269cdaf` and at the head with the in-tree builder (`receipts/cross_checks.log` section 2).
  - `AEM_NAME_ENTRIES_C` is 38 to 39 at 1x1 and 99 to 107 at 8x8.
  - Every other constant bound to `KL_pp_shadow` (`milan_datapath.sv` instance, 20 parameters listed) is unchanged at both shapes.
  - `AEM_N_CLKSRC_C` moves (2 to 3, and 2 to 10), but it is not a wrapper parameter. The wrapper has no `` `include `` of a shape header.
  - The sub-block moves in `findings:87-89,102-108` equal the published pre-check logs:
    - route: `u_nvm` +19, `u_store` +9, `u_dyn` -83, `u_d3` +25, `u_notify` +14;
    - 1x1: `u_nvm` -11 / +1, `u_store` +7, `u_d3` -7;
    - 8x8: `u_nvm` -5 / +8, `u_store` -3.
- **The firmware ROM** (`findings:42`): the in-tree AEM image generator gives 7,352 bytes at `1269cdaf` and 7,512 at the head. The `1269cdaf` digest `9b077636…` equals the digest published on the earlier bench pages. The NVM record file gains one NAME record (53 to 54).

**5. Docs at the head (Docs)** (`scripts/arith_check.py`, `receipts/arith_check.log`, 50 checks, 0 mismatches)
- The `AREA_BUDGET.md` current table (`:111-118`): 80.07 % LUT, 12,727 over NFR-RES-01, 47.03 % FF, 99.89 % slices with 18 free, and +0.193 / +0.024 ns.
- Allocation (`:127-134`): 24,332 = 38.4 %; 42,200 = 66.6 %; wrapper 23,904; below 11,177; a 12,727 cut, 53 %.
- Timing fall (`:164`): the floor binds after 0.163 ns.
- Findings page (`:52-57`, `:66-74`, `:94-100`, `:456-461`): the C minus A rows, percentages and lever arithmetic are all reproduced.
- The old figures appear only in labelled A rows, one dated `AREA_BUDGET.md:122` sentence, and the history sections that the intro (`findings:3-6`) marks as history.
- The re-baseline rule is at `AREA_BUDGET.md:189-195`. The merge-bank predecessor catch is at `AREA_BUDGET.md:236-244`. It is stated as the bank's rule with no tooling, as the assignment's item 4 asks, and it names the `measured` note as the trigger revision.
- The index rows (`docs/findings/README.md:23-24`) carry the new figures and the rule.

**6. Gates at the exact head (Tests, Docs)** (`receipts/gates/*.log` and `.rc`, all rc 0)
- The gate's self-test: 260 arms and 500 generated cases, digest `151eb3fc6a0d989c`, the same as rounds 6 and 7.
- `pp_resource_gate_mutants.py`: control passes, all 174 mutants fail.
- `check-baseline`: "baseline PASS: 3 endpoints".
- `--fuzz 20000`: 0 failures, digest `0596f2c893188fb0`.
- `pp_baseline.py --selftest`, `pp_baseline_mutants.py`, `pp_baseline_reports_selftest.py`, `dp_srcs.py --selftest` and `ooc_tcl_selftest.py`.
- `ci_scope.py --selftest` and `ci_events.py --check`.
- `docs_check` (system Python and the pinned renderer), `gen_toc --check`, `gen_toc --verify-anchors`, `check_doc_paths`, `check_doc_style` and `DOC_MAP --check`.
- `check_em_dash --base 5fabb46e`: 0 findings over 746 added lines. Against `--base 54643724`: 0 over 1,355.
- `git diff --check 5fabb46e HEAD`.
- The four renderer-dependent gates first gave rc 2 because the host's system Python lacks the renderer. They were re-run with the existing pinned-renderer environment, whose name matches `tools/markdown/requirements.txt`'s digest prefix `40cdefe08ebda5e6` and whose pins match.
- The PR's gate code, self-test, mutants, recipe, CI workflow and classifier files are byte-identical to `d5f56313`.

## Findings

[R446] RESIDUE Docs - PR #638 body, "Status" paragraph ("Head `aabdc2839a272631222c30a62e83218d893b40d2`") and "How to get into the same state" (`git switch --detach aabdc2839a272631222c30a62e83218d893b40d2`) - the body still names round 7's head after round 7b
- **ID:** R1. Lenses: Docs.
- **Evidence:** the live PR body. The head is `68d26ea0`, the `--no-ff` merge of dev `5fabb46e` into `aabdc283`.
- **Why RESIDUE and not MINOR:** this is wording in a PR body only, unlike the precedent R447-6 F1, where following the body produced different counts.
  - The body's own Round 7 section already says: "Where this body names `aabdc283` as the head (Status, How to get into the same state), read `68d26ea0`".
  - At `aabdc283`, every validate command in the body gives the same output as at the head. The gate code, self-test, mutants and baseline JSON are byte-identical, and the only difference is PR #646's docs page and index row.
  - No measurement, figure, verdict, test or code changes.
- **Impact:** a reader who copies the checkout line without reading round 7b lands one merge behind the head.
- **Exact fix:**
  - In "Status", replace "Head `aabdc2839a272631222c30a62e83218d893b40d2` (the merge and three commits on round 6's `d5f56313`)" with "Head `68d26ea034789ce2519db22d0df4e4328bc1b0de` (round 7b's `--no-ff` merge of dev `5fabb46e` into round 7's `aabdc283`, the merge and three commits on round 6's `d5f56313`)".
  - In "How to get into the same state", replace `git switch --detach aabdc2839a272631222c30a62e83218d893b40d2` with `git switch --detach 68d26ea034789ce2519db22d0df4e4328bc1b0de`.
  - Then delete the sentence "Where this body names `aabdc283` as the head (Status, How to get into the same state), read `68d26ea0`."
- **Verification:** the body's checkout gives HEAD `68d26ea0` and tree `4bc95158`.

[R446] SUGGESTION Docs - round-7 author archive `234-review-evidence@22b292d3:review-evidence/234-r1/author-r7` - the A-side `milan_datapath` instance figures behind the delta attribution are not published
- **ID:** S1. Lenses: Docs.
- **Evidence:**
  - The round-7 REVIEW READY (5973319945) lists "evidence/round7/: C's records, the delta tables and the gate table" for publication. The archive holds only `HANDOFF.md`, `PR-BODY.md` and `receipts/`.
  - C's records are in the record-write logs, and the C-side hierarchy is corroborated by PR #634's archive.
  - The A-side (`1269cdaf`) instance values behind "csr +58, media_nco +9, media_grid_align +1, mmcm_servo -2, aaf_latency_tap_bank +68, talker_diag +61, ctl_tx_mux +54, chan_map_capture +33" (`findings:82-84`) appear in no public artifact. The A route's hierarchy report is published only as a digest.
- **Impact:** a cold reviewer can check those eight explanatory deltas on the C side only. No gated figure, verdict or conclusion rests on them. The page itself says the reports do not separate wiring from optimization.
- **Suggested outcome:** publish the round-7 delta tables named in the REVIEW READY, or A's and C's `baseline_hierarchy.rpt` (digest `01353be9…` for C, in `run-receipts.json`), with the next archive.
- **Verification:** the eight deltas recompute from the published tables.

## Prior findings at this head

I wrote this section after the verdict, findings and ledger above (see `receipts/independent-verdict-before-prior-findings.txt`). I read prior reports only after that.

| Prior finding | State at `68d26ea0` | Evidence |
|---|---|---|
| R446-7 F1 (MAJOR Conformance, RTL, Robustness, Docs): the `1269cdaf` baseline already fails the composed tree's image | **RESOLVED** by option (a) | The records are re-recorded at C and equal the published record-write output (section 2). The published `check` on the composed tree's three runs exits 0, and `check-baseline` passes at the head. The lines R446-7 cited now give C's figures or are dated history: `AREA_BUDGET.md:13` and `:107-123` (a `1269cdaf` sentence at `:122`), `findings:456`, and `README.md:23-24`. The standalone endpoints R446-7 did not measure are measured: -11/+1 and -6/+8. The Robustness half (no Vivado at a non-RTL merge) is answered by `AREA_BUDGET.md:236-244`. The docs gates rerun green at the head. |
| All BLOCKER, MAJOR and MINOR findings of R446-1 to R446-6 and R447-1 to R447-6 (last: R447-6 F1, MINOR Docs, PR body) | **Remain resolved** | Resolved at `d5f56313` per R446-6 and R447-7. The gate code, self-test, mutants, recipe and CI files are byte-identical to `d5f56313`, and the self-test, mutants, `check-baseline` and fuzz rerun green here (section 6). |
| R447-6 R1 and R446-6 R1 (RESIDUE Docs, PR body: round-6 assignment link; checkout naming round 5's head) | **Remain resolved** | The round-6 assignment link is still in the body ("Authoritative references"). The checkout line was later edited for round 7, and its new stale state is this round's R1, a separate item. |
| R446-5 R1 (RESIDUE Docs, PR body Round 5 row: "run by `strict()` on every JSON the gate reads") | **Retained** as RESIDUE | The live body still has the phrase in the Round 5 table row. R446-5's exact fix stands: "run by `strict()` on every JSON that `check`, `record` and `check-baseline` read". |
| R447-7 S1 to S3, R446-6 S1, R446-5 S1 (SUGGESTION) | **Retained**, optional | The code they concern is byte-identical to `d5f56313`. |

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Both merges recomputed (`receipts/cross_checks.log` s.1). `syn/ooc/pp_resource_baseline.json` records against `22b292d3:.../author-r7/receipts/real/record-write-C-*.log` and the policy against `d5f56313` (`receipts/check_record_vs_d5f56313.log`). Published C `check` logs at rc 0. #234 rulings 5967852698 and 5967924270 and assignments 5972491855 and 5973328289 item by item. PR #634's independent report (s.4). | R446-8 | `68d26ea034789ce2519db22d0df4e4328bc1b0de` |
| RTL | CLEAN | The PR changes no RTL against live dev (`receipts/cross_checks.log` s.1). The RTL-side claims of the delta: shape headers regenerated at `1269cdaf` and the head, the 20 `KL_pp_shadow` bindings at `hdl/milan/milan_datapath.sv` (`DESC_NAME_ENTRIES_P` at `:7681`), and no shape include in `hdl/milan/KL_pp_shadow.sv`. The HDL change set of `1269cdaf..54643724`. Instance figures from PR #634's hierarchical report. Route status 106,622 of 106,622 nets and WNS/WHS against the BUILDING.md section 5 floors. | R446-8 | `68d26ea034789ce2519db22d0df4e4328bc1b0de` |
| Robustness | CLEAN | `scripts/probe_policy_plants.sh` / `receipts/probe_policy_plants.log` (11 policy plants refused at rc 2; control, note and record edits pass). The predecessor and ordering case of R446-7 against `docs/design/AREA_BUDGET.md:189-195,236-244`. Configuration dependence: both shapes regenerated, and the 1x1 and 8x8 endpoints both re-recorded. `--fuzz 20000`: 0 failures. | R446-8 | `68d26ea034789ce2519db22d0df4e4328bc1b0de` |
| Tests | CLEAN | `receipts/gates/`: gate self-test (260 arms, 500 cases, digest `151eb3fc6a0d989c`), 174 of 174 mutants, `check-baseline`, fuzz, `pp_baseline` self-test, mutants and reports self-test, `dp_srcs` and `ooc_tcl` self-tests, `ci_scope --selftest` and `ci_events --check`, all rc 0. Test code byte-identical to `d5f56313`. No test reads a file the merges changed except the re-recorded JSON, which `check-baseline` validates. | R446-8 | `68d26ea034789ce2519db22d0df4e4328bc1b0de` |
| Docs | CLEAN (RESIDUE R1 and SUGGESTION S1 recorded; neither leaves the lens unclean) | `docs/design/AREA_BUDGET.md:13,111-134,164,189-195,236-245`; `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:1-123,456-461`; `docs/findings/README.md:23-24`. `receipts/arith_check.log`: 50 checks, 0 mismatches. `receipts/readme_rows.log`. Docs gates at the head in `receipts/gates/`. The PR body's Round 7 section and "How to validate". | R446-8 | `68d26ea034789ce2519db22d0df4e4328bc1b0de` |

## Real limits

- I ran no Vivado. The C figures are the author's published record-write output, independently corroborated by PR #634's separate build of the same image. The raw run directories of the round-7 runs were not read; they are lane storage.
- **Corroboration differences:** PR #634's hierarchical report is "Physopt postPlace", while the recorded route is "Physopt postRoute". Its totals, the wrapper, the meter, the route status and the timing summary all equal the record.
- **Not reproduced from public artifacts:**
  - the A-side instance values (S1);
  - C's critical path: 39 levels, `rows_r_reg[9][68]` to `slot_r_reg[0]`, 19.545 ns;
  - the claim that `alinx_ax7101_rom.init` stayed the same size. I did not compile firmware; only the AEM descriptor image sizes were regenerated.
- **Hosted snapshot** (`receipts/hosted-check-runs.txt`, taken during this review): 14 completed success and 1 skipped ("Physical gPTP (nightly and manual)", a nightly or manual context). Five were still in progress: `docs-check`, `elaborate`, and Verilator shards 1, 2 and 4 of 5. The job that runs the rtl-fast OOC step had not reported.
- **Not run:** any full parent, processor, gPTP, Yosys or builder bank; Docker or act; host `act_ci` or its self-test. The in-tree builder was run only to regenerate the two shape headers and the AEM image, in disposable extractions.
- Physical calibration NOT RUN; field skips are not hardware proof.

## Pending manager duties

- Hosted and act acceptance of the exact head. That includes the protected `rtl-fast` context (the OOC gate step), `verilator-suites` and `yosys-portability`, and the in-progress jobs listed above.
- Build and validate the final current-dev candidate at the merge turn. The source base is `1269cdaf` and live dev was `5fabb46e` during this review. If dev moves and touches RTL, the processor pin or the build recipe, the bank rule at `AREA_BUDGET.md:236-244` applies.
- Carry RESIDUE R1 (this round) and the retained RESIDUE R446-5 R1 to the residue checklist with their exact fixes.
- Consider S1: publish the round-7 delta tables or hierarchy reports.

## Clone integrity

- The review clone was never edited. Probes ran on `git archive` extractions under `scratch/`.
- Python bytecode directories that my gate runs created in the clone were removed.
- `scripts/verify_tree.sh` (`receipts/verify_tree.log`), run at the end, confirms:
  - HEAD, tree and index tree equal `68d26ea0` / `4bc95158`;
  - `git status --porcelain --ignored` is empty;
  - all 999 tracked regular files match their index blob and mode byte for byte;
  - the gitlinks match: `protocol-processor` `631eeb34`, `gptp-processor` `5dce647a`, `third_party/verilog-axis` `48ff7a7e`;
  - `external` `efeb541a` is uninitialized, as it was at the start.

R446-8 FINISHED
