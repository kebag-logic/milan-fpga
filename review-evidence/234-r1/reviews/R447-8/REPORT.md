[R447] NEGATIVE - exact head 68d26ea034789ce2519db22d0df4e4328bc1b0de

# R447-8: external review of issue #234 / PR #638, rounds 7 and 7b

- Role: external independent reviewer, cleared context.
- Head: `68d26ea034789ce2519db22d0df4e4328bc1b0de`, tree `4bc95158cc7e2b5f64051a100b770298ef194a70`.
- Delta reviewed: `d5f56313..68d26ea0`.
  - Merge `4d81e10d` of dev `54643724`.
  - `a89d0696` re-records the three endpoints.
  - `469d1620` updates the docs and states the re-baseline rule.
  - `aabdc283` states the merge-bank predecessor rule.
  - Merge `68d26ea0` of dev `5fabb46e`.
- Judged against: composition review R446-7 (F1 MAJOR), round-7 assignment 5972491855 (option (a)) and round-7b assignment 5973328289.
- The branch contains live dev `5fabb46e`, so the candidate tree equals the head tree.

## Verdict

NEGATIVE, on one MINOR finding (F1, Docs). It is in the PR body's current summary, not in the repository.

The re-baseline itself is correct:

- Both merges are clean `--no-ff` merges with the stated parents and no hand edits.
- The three re-recorded endpoints equal their published `record --write` receipts exactly, as JSON.
- Every tolerance, floor and ceiling is unchanged, field by field.
- `check` exits 0 on each new run, and `check-baseline` is green.
- The figures in AREA_BUDGET and on the findings page, and the delta attribution, add up against the record and the receipts.
- PR #634's own published build of the same image gives identical route figures.

R446-7 F1 is resolved.

F1 is this: the PR body still says that, at this head, B's route exits 1 and B's standalone deltas are +162 / -172. Against the record now committed, B's route exits 0 at -14 LUT, and its standalone deltas are +173 / -166. Those figures come from the executor's own round-7 receipts, and the body's own limitations section says the same. A wrong gate verdict and wrong figures are not wording only, so this is MINOR, not RESIDUE.

## Reconstruction, in order

1. AGENTS.md (sections 3 and 5 to 8) and the CONTRIBUTING precedence rule.
2. docs/README.md.
3. Issue #234: the body and acceptance criteria, then the public comments:
   - lane 5966260488;
   - rulings 5967852698 (gate in both places; criterion 1 at 50 MHz; tolerances accepted; B's rejection intended);
   - owner decision 5967924270 ("the #638 resource gate holds every resource at its recorded value");
   - round-7 assignment 5972491855 and REVIEW READY 5973319945;
   - round-7b assignment 5973328289 and REVIEW READY 5973356984.
4. Requirement NFR-RES-01 (60 % LUT).
5. Interface authorities: `docs/design/AREA_BUDGET.md` (policy table `:149-153`, rule `:189-195`, bank rule `:236-244`) and `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`.
6. Diff `1269cdaf..68d26ea0` and history, with the focus on `d5f56313..68d26ea0`.
7. Public evidence:
   - `review-evidence/234-r1` at `43ad8362` (round 1);
   - the round-7 packet on the same evidence branch at `22b292d3` (`author-r7/`), from which I read only the executor's packet;
   - PR #634's public body and comments, for the image figures it published at its merge.

I read prior reviews (R446-7, and my own R447-7) only after writing my verdict and ledger. They are dealt with in the last section.

## What I checked, with evidence

### Merges (round 7 item 1, round 7b item 1)

From `receipts/merge-structure.txt`:

- `4d81e10d` has parents `d5f56313dc5a…` and `546437243e87…`. Its tree `04a0c948` equals `git merge-tree --write-tree d5f56313 54643724`, which is also R446-7's candidate tree.
- `68d26ea0` has parents `aabdc283…` and `5fabb46e…`. Its tree `4bc95158` equals `git merge-tree --write-tree aabdc283 5fabb46e`.
- So nothing was hand-merged, not even the `docs/findings/README.md` rows.
- At the head, README differs from dev only by the PR's two rows. Against `aabdc283` it differs only by PR #646's `629_...` row.
- All five commits have one-line messages.
- `d5f56313` and `1269cdaf` are ancestors of the head, so there was no rebase.
- The remote branch is at `68d26ea0`, and remote dev is at `5fabb46e`.

### Re-recorded endpoints (round 7 item 2)

- **Record equals receipt.** `match_record_receipts.py` → `receipts/record-receipt-match.txt`. Each published `record-write-C-<endpoint>.log` (rc 0) holds the full record. Each is JSON-equal to the committed `endpoints.<endpoint>.record`, giving "ALL MATCH":
  - route: LUT 50,767, FF 59,634, SLICE 15,832, BRAM tiles 92.5, RAMB36 79, RAMB18 27, DSP 14, WNS +0.193, WHS +0.024, CARRY4 3,506;
  - ooc-1x1: 24,332 / 25,345;
  - ooc-8x8: 31,556 / 33,937.
- **Field-by-field comparison** of `4d81e10d` against the head (`compare_baseline.py` → `receipts/baseline-field-compare.txt`):
  - Only `record.*` and the `measured` note change.
  - Every `tolerance`, `floor` and `ceiling` field is unchanged at all three endpoints.
  - The schema, description, identity (tool, device, flow, standalone clock) and scope set are unchanged.
- **check exits 0 on each new run.** The published receipts show:
  - `real/check-C-*-worktree.rc` = 0, and `final-real/gate-check-C-{route,ooc-1x1,ooc-8x8}.rc` = 0 at `aabdc283`, every delta 0, route status complete;
  - before recording, `pre-check-C-route-1x1.rc` = 1, with LUT +639 (139 over) and FF +628 (28 over), and both standalone checks rc 0;
  - `vivado-chain.log`: the three runs strictly serial (21:06 → 21:45 → 22:04 → 22:28), with commit `a89d0696` at 22:29.
- **check-baseline green at this head:** `receipts/gates/resource-gate-check-baseline.log`, "baseline PASS: 3 endpoints".
- **Separate corroboration.** PR #634's public body publishes its merge image (`c1288648`):
  - LUT 50,767, FF 59,634, slices 15,832, WNS +0.193, WHS +0.024, 106,622 of 106,622 nets routed;
  - placed processor top 23,335 LUT / 23,435 FF, and meter 483 / 630.
  - These equal C's route record, including `u_pp` at 23,335 / 23,435.
- **The hand-edited `measured` notes.**
  - All three read "dev 54643724, after PR #634, processor 631eeb34, issue #234 re-baseline of 2026-10-03; first recorded at dev 1269cdaf".
  - The file is still in the exact byte form `record --write` emits (`receipts/baseline-canonical.txt`).
  - `record --write` replaces only `record` (`syn/ooc/pp_resource_gate.py:725-729`), so a hand edit is the only way to set the note. See S1.
- **The measured inputs are the head's.** From `receipts/delta-scope.txt` and `receipts/rtl-scope.txt`:
  - `4d81e10d..HEAD` touches only the baseline JSON and four Markdown pages.
  - Dev `54643724..5fabb46e` touches two Markdown pages.
  - No file under `hdl configs avdecc sw protocol-processor gptp-processor third_party external syn/yosys` differs between the lane's commits and their parents, or between the head and dev.
  - The gitlinks are identical at `1269cdaf`, `4d81e10d`, the head and dev.

### Delta attribution (round 7 item 2)

From `crosscheck_docs.py` → `receipts/crosscheck-docs.txt` (35 of 35 ok) and `receipts/attribution-sources.txt`:

- **The sums close.**
  - `milan_datapath` +673 = meter 483 + wrapper -33 + rest +223.
  - Its FFs: +629 = 630 + 2 - 3.
  - The rest's A and C figures, 17,590 / 17,813 LUT and 23,541 / 23,538 FF, follow from the table.
  - Whole image: +639 = 673 - 2 (CPU) - 10 (SoC top) - 22 (residual, as stated). FF +628 = 629 - 1.
  - The meter is 76 % of the LUT growth, and more than all of the FF growth.
- **Name entries.** `AEM_NAME_ENTRIES_C` goes from 38 to 39 (1x1) and from 99 to 107 (8x8) in the generated shape headers. It binds to `DESC_NAME_ENTRIES_P` at `hdl/milan/milan_datapath.sv:7681`.
  - No other `KL_pp_shadow` parameter binding line changed.
  - The new `AEM_N_CLKSRC_C` and `AEM_CLKSRC_*` constants are used only in `milan_datapath`.
  - So "the only wrapper parameter that moved" holds.
- **Meter.** `g_aaf_meter` elaborates when `AEM_N_AAF_CLKSRC_C != 0` (`milan_datapath.sv:5674`). The value is 1 at 1x1, so there is one instance.
- **Sub-block movements.** The movements on the page match the record diff:
  - route: `u_nvm` +19, `u_store` +9, `u_dyn` -83, `u_d3` +25, `u_notify` +14;
  - 1x1: `u_nvm` -11 / +1, `u_store` +7, `u_d3` -7;
  - 8x8: `u_nvm` -5 / +8, `u_store` -3.
- **PR #634's changed sources.** `milan_csr.sv`, `KL_media_nco.sv`, `KL_media_grid_align.sv` and `KL_mmcm_drp_servo.sv` are the files #634 changed (`git diff --stat 1269cdaf HEAD -- hdl`). That matches the four instances the page names as changed.

### Docs to the new tree (round 7 item 3)

- **AREA_BUDGET current-head table** (`docs/design/AREA_BUDGET.md:111-118`): each row recomputes from the record.
  - LUT 80.07 %, 12,727 over 38,040.
  - FF 47.03 %.
  - Slices 99.89 %, 18 free.
  - BRAM 68.52 %, 42.5 free.
  - DSP 5.83 %.
  - Timing +0.193 / +0.024.
- **Allocation figures:** wrapper 24,332 is 38.4 %, below the 11,177 target, so the cut is 12,727 LUT, 53 %. `milan_datapath` is 42,200 LUT, 66.6 %. The timing-fall figure of 0.163 ns is right.
- **The first record is kept as history:**
  - one dated sentence at `:122`;
  - `:169` "sized on the first record";
  - the B narrative in past tense at `:178-182`.
- **Findings page.**
  - The dated section "Re-baseline of 2026-10-03, after PR #634" comes first. The first-record sections follow it, introduced as history.
  - Its four C run-receipt rows equal `run-receipts.json` (rc, minutes, log, digest prefix, bytes).
  - The levers residual is 47,200 LUT, 74 %, with 9,100 over.
- **Index rows** (`docs/findings/README.md:23-24`) carry the new figures and the rule.
- **Stale figures:** `git grep` for the first record's figures finds them only where they are labelled A, `1269cdaf` or history.

### Rules (round 7 items 3 and 4)

- **Re-baseline rule** (`AREA_BUDGET.md:189-195`): "A merge that moves the shipping image records its own re-baseline…". It cites the ruling and links the findings section; the anchor resolves.
- **Merge-bank predecessor rule** (`:236-244`):
  - The trigger is the merge result's dev delta since the revision the `measured` note names, not the PR's own diff.
  - It covers RTL, the processor pin and the build recipe.
  - The predecessor's growth is recorded first as its own re-baseline.
  - It is stated as the bank's rule, with no new tooling.
- **Consistency with the tree:** the delta since `54643724` is docs only today (`receipts/rtl-scope.txt`), so the rule triggers nothing now. A stale note can only name an older revision, which widens the delta and makes the bank trigger more often, never less. That is why S1 is only a suggestion.

### Gates and probes at this head

- **Gates.** `run_gates.sh` ran 20 gates, 16 in parallel, under `receipts/gates/`. All exited 0:
  - the gate's self-test: 260 arms and 500 cases, digest `151eb3fc6a0d989c`, equal to the executor's;
  - mutants: 174 of 174 killed;
  - `check-baseline`;
  - `pp_baseline` self-test and mutants;
  - `ci_scope` and `ci_events`;
  - `docs_check` with and without git;
  - `gen_toc --check` and `--verify-anchors` (328 links);
  - `check_doc_paths` (901 paths);
  - `check_em_dash --base 5fabb46e`: 0 findings over 746 lines;
  - `check_doc_style`, `DOC_MAP --check`, `check_archive`, the module matrix, solution docs and feature status;
  - `git diff --check` against `5fabb46e`.
- **Fuzz.** The PR's own `--fuzz 20000` gave 0 failures, digest `0596f2c893188fb0` (`receipts/gates/resource-gate-fuzz-20000.log`).
- **Probes** (`probe_check_baseline.py` → `receipts/probe-check-baseline.txt`, on scratch copies of the baseline):
  - `check-baseline` exits 2 on route LUT tolerance 501, FF tolerance 599, ooc-8x8 LUT tolerance 315, WNS floor 0.02 and BRAM ceiling 122.
  - It also exits 2 on a record with WNS below its floor, on BRAM above its ceiling, and on a non-hex input digest.
  - So the unchanged policy is enforced by a hosted gate, not only asserted.
  - Removing the `measured` note still passes (S1).
- **Gate code unchanged.** The gate, its self-test and mutants, `pp_baseline*`, `ci_scope`, `ci_events`, `rtl-fast.yml`, the recipe and CI_WORKFLOWS are byte-identical to `d5f56313` (`receipts/gate-code-unchanged.txt`, empty diff).
- **Hosted snapshot** at the exact head, read-only (`receipts/hosted-check-runs.tsv`):
  - success: bdd-conformance, changes, docs-check-no-git, full-ci-gate, verilator-lint, wire-accountability and Yosys shards 0 to 3;
  - in progress at the snapshot: docs-check, elaborate, Verilator shards 0 to 4 and yosys-elaboration;
  - skipped: Physical gPTP. A skip is not an executed job.

## Findings

[R447] F1 MINOR Docs - PR #638 body, "Headline figures" block, paragraph "Gate on real data at this head" (live body line 60) - B's route verdict and B's standalone deltas are stale at this head

- **Authority and evidence:**
  - The paragraph says: "Gate on real data at this head: … B exits 1 on the route (+625 LUT over the 500-LUT tolerance; …) and 0 on both standalone endpoints (+162 / -172 LUT)."
  - At this head the committed record is C's. The executor's own round-7 receipts at `aabdc283`, whose gate code and record are identical to this head, show:
    - `final-real/gate-check-B-route.rc` = 0: LUT -14, FF -620, "RESULT: PASS";
    - `gate-check-B-ooc-1x1`: +173 LUT / +125 FF;
    - `gate-check-B-ooc-8x8`: -166 / -93.
  - The same body's "Known limitations" says "Against C's record, B's route passes at -14 LUTs". The body contradicts itself.
  - AGENTS.md §6, Docs lens: the PR must give a cold reviewer enough correct evidence.
- **Impact:** a reader of the current summary takes it that the committed gate rejects B at this head, and gets B's standalone deltas wrong. Criterion 4's real-data proof at this head is now C against the first record (`pre-check-C-route-1x1.rc` = 1), not B. The paragraph states a gate verdict and figures, so it is not wording only.
- **Required outcome:** the paragraph states the verdicts against the committed record:
  - A: three exit 0, with "re-baseline recommended" on the route;
  - B: route exit 0 at -14 LUT, only because B lacks PR #634's meter, and standalone exit 0 at +173 / -166;
  - optionally, B's first-record verdicts, labelled as against the first record.
- **Verification:** the live body's paragraph equals the `final-real/gate-check-{A,B}-*` receipts. The rest of the body is unchanged except where the residues below apply.

[R447] R1 RESIDUE Docs - `docs/design/AREA_BUDGET.md:184` - "Accepting B means recording its route as the new baseline, a reviewed decision."

- The sentence is in present tense. After round 7, B's measured route is a tree without PR #634. Its intent, that the adoption is measured again on its merge result, is already required by `:189-190`.
- Exact fix: "Accepting the next adoption means recording its route, measured again on its merge result, as the new baseline, a reviewed decision."

[R447] R2 RESIDUE Docs - PR #638 body, Status (line 22) and "How to get into the same state" (line 429) - the head is named as `aabdc2839a272631222c30a62e83218d893b40d2`

- The round-7b line already tells readers to read `68d26ea0` there.
- Exact fix: replace both occurrences with `68d26ea034789ce2519db22d0df4e4328bc1b0de`.

[R447] S1 SUGGESTION Robustness, Tests - `syn/ooc/pp_resource_gate.py:94,467,725-729` against `docs/design/AREA_BUDGET.md:193,238` - the `measured` note is now the bank trigger's input, but it is optional, free text and never written by `record --write`

- Evidence: in the probe `route-measured-note-removed`, `check-baseline` still exits 0 with the note removed.
- A stale note errs toward triggering more often, so nothing is required.
- Optional: have `check-baseline` require a `measured` note naming a dev revision, or have `record --write` take that revision as an argument.

[R447] S2 SUGGESTION Tests, Docs - `docs/design/AREA_BUDGET.md:111-123` and the findings page's current-record tables - the "current head" figures are not tied to the record by any gate

- My `crosscheck_docs.py` shows they agree at this head. A later re-baseline could leave them stale without any gate noticing.
- Optional: extend `check-baseline`, or a docs gate, to compare the budget table's figures with `route-1x1.record.figures`.

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #234 acceptance as ruled (5967852698, 5967924270); round-7 items 1 to 4 and round-7b items 1 and 2 against `receipts/merge-structure.txt`, `receipts/record-receipt-match.txt`, `receipts/baseline-field-compare.txt` (policy unchanged), published `pre-check`/`check`/`final-real` receipts (rc 1 against the first record, then rc 0), `receipts/gates/resource-gate-check-baseline.log`; WNS +0.193 ≥ +0.030 and WHS +0.024 ≥ 0 floors, BRAM 92.5 ≤ 121.5; NFR-RES-01 gap stated as not met | R447-8 | `68d26ea034789ce2519db22d0df4e4328bc1b0de` |
| RTL | CLEAN | No HDL, configuration, AEM, SoC, Yosys or gitlink change by the lane (`receipts/rtl-scope.txt`, `receipts/delta-scope.txt`). Attribution checked against the RTL: `hdl/milan/milan_datapath.sv:7681` (`DESC_NAME_ENTRIES_P`), `:5674` (`g_aaf_meter`, `AEM_N_AAF_CLKSRC_C` = 1), the wrapper's parameter bindings `:7658-7700` unchanged, shape headers 38→39 and 99→107 (`receipts/attribution-sources.txt`). Resource and timing effects quantified by the record and PR #634's independent build. | R447-8 | `68d26ea034789ce2519db22d0df4e4328bc1b0de` |
| Robustness | CLEAN (S1 optional) | `receipts/probe-check-baseline.txt` (8 policy and record mutations rejected with exit 2, control passes); `receipts/gates/resource-gate-fuzz-20000.log` (0 failures); the bank rule at `AREA_BUDGET.md:236-244`, judged against today's dev delta (docs only) and against a stale or missing note; `receipts/baseline-canonical.txt` | R447-8 | `68d26ea034789ce2519db22d0df4e4328bc1b0de` |
| Tests | CLEAN (S2 optional) | `receipts/gates/*.log` (20 of 20 rc 0: self-test with digest `151eb3fc6a0d989c`, 174 of 174 mutants, `pp_baseline` self-test and mutants, `ci_scope`, `ci_events`); gate and test code byte-identical to `d5f56313` (`receipts/gate-code-unchanged.txt`); `receipts/crosscheck-docs.txt` (35 of 35) | R447-8 | `68d26ea034789ce2519db22d0df4e4328bc1b0de` |
| Docs | UNCLEAN (F1 MINOR; R1 and R2 RESIDUE) | `docs/design/AREA_BUDGET.md:13,100-123,166-195,236-244`; `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:1-130,451-461`; `docs/findings/README.md:23-24`; docs gates in `receipts/gates/`; live PR body (F1 at line 60, R2 at lines 22 and 429) | R447-8 | `68d26ea034789ce2519db22d0df4e4328bc1b0de` |

## Prior findings at this head

I wrote this section after the verdict, findings and ledger above.

| Prior finding | State at `68d26ea0` | Evidence |
|---|---|---|
| R446-7 F1 (MAJOR Conformance, RTL, Robustness, Docs): the `1269cdaf` baseline predates #634 and already fails the composed image | **RESOLVED** by option (a) | See below. |
| R446-5 R1 (RESIDUE Docs, PR body): "run by `strict()` on every JSON the gate reads" | **Retained** as RESIDUE | The live body still has it at line 286 (`receipts/r446-5-r1-text.txt`). R446-5's exact fix stands: "run by `strict()` on every JSON that `check`, `record` and `check-baseline` read". |
| R447-7 S1 to S3 (retained from R447-6), R446-6 S1 and R446-5 S1 (SUGGESTION) | **Retained**, optional | The gate code is byte-identical to `d5f56313` (`receipts/gate-code-unchanged.txt`). |
| Every BLOCKER, MAJOR and MINOR of R446-1 to R446-6 and R447-1 to R447-7 | **Remain resolved** | The gate code, tests, recipe and CI docs are unchanged since `d5f56313`. The self-test, mutants and fuzz rerun green here. |

How option (a) resolves R446-7 F1:

- The merge-train tree was measured: C is `4d81e10d`, the same tree `04a0c948` that R446-7 judged.
- All three endpoints were recorded with `record --write`, every policy field unchanged.
- `check` on the C route exits 0, which is F1's own verification. It exited 1 against the old record, exactly as R446-7 predicted (139 / 28 over).
- `check-baseline` is green.
- The docs gates were rerun on this head.
- The docs no longer call the `1269cdaf` figures current:
  - `AREA_BUDGET.md:13,100-123` now gives dev `54643724`;
  - findings page `:456` now gives 18 left at C;
  - index rows updated.
- F1's Robustness half (no Vivado comparison at a non-RTL merge) is answered by the bank rule at `AREA_BUDGET.md:236-244`.

## Real limits

- **Vivado.** I ran none. The route and standalone figures rest on the executor's published receipts, and on PR #634's independent publication of the same route.
- **Raw reports.** The hierarchy, utilization and timing reports were not published, only their SHA-256 values. So the following are checked only for arithmetic consistency and against the RTL, not against reports I opened:
  - the per-instance split of the `milan_datapath` remainder (`aaf_latency_tap_bank` +68, and so on);
  - the critical-path endpoints and 39 logic levels;
  - the ROM's same-size, constants-only claim.
- **Input digests.** `inputs_sha256` was not recomputed, because the run directories are not public.
- **Make.** I did not run `make -C gptp-processor docs`, which is not touched by the delta. The host's GNU make is 4.4.1, and I did not run the gates under 4.3. None of the gates I ran invokes make.
- **Banks and hosted CI.** I ran no full parent, PP, gPTP, Yosys or builder bank, and no hosted workflow or act run.
- **Hardware.** Physical calibration was NOT RUN. Field skips are not hardware proof.

## Review clone restored

From `receipts/restore-verify.txt`:

- HEAD `68d26ea0`, tree `4bc95158`; the index tree equals it.
- `git diff-index HEAD`: 0 lines. `git status --porcelain --ignored`: 0 lines, after removing the Python byte caches the gates created.
- Gitlinks: `protocol-processor` `631eeb34`, `gptp-processor` `5dce647a`, `third_party/verilog-axis` `48ff7a7e`, `external` `efeb541a`.
- The only change to the clone's object store was fetching the public evidence commit `22b292d3`.

## Pending manager duties

- F1: correct the PR body paragraph, then re-review.
- Carry R1, R2 and R446-5 R1 to the residue checklist.
- Hosted and act acceptance of the exact head. Several contexts were still in progress at my snapshot.
- Build and validate the final current-dev candidate at the merge turn (source base `1269cdaf`, live dev `5fabb46e`).
- If dev moves with an image input before merge, apply the bank rule at `AREA_BUDGET.md:236-244`.
- Publish the raw C reports, or state why they stay private, if a later reviewer must check the per-instance attribution.

R447-8 FINISHED
