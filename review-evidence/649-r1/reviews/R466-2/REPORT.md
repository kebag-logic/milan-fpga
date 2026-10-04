[R466] NEGATIVE - exact head 4742d2c02c109f7dd8e21d74905efb182b2dbca2

Round R466-2, internal cleared-context review of issue #649 / PR #650. Tree `7e247e4f65ef8a02d9834246af6329c888fca206`; source base `241f91845230ae410506dffb16b71937127fd175`; live dev `fea346e76c2a57ed5cd131af8fc68dfeff57f877`. All five lenses were applied.

Every round-1 finding from both reviewers (R466-1 F1 to F6, R467-1 F1 to F7) is resolved at this head, and every residue item was applied. The round-2 measurements reproduce or tie.

One new MINOR finding stays open, so the verdict is NEGATIVE. The page says the CPU, cache and L2 variants were synthesized "at the shipping synthesis directive". All 20 runs used Vivado's default directive, and the shipping build uses `AreaOptimized_high`. Three RESIDUE items and three SUGGESTIONs are listed separately.

## Basis

Read in this order:
- AGENTS.md and CONTRIBUTING.md;
- docs/README.md;
- issue #649: body, the lane assignment (5976977547), the round-2 assignment and ruling (5978713464), REVIEW READY round 2 (5980922096), and the evidence comment (5980942776);
- the PR #650 body at this head;
- the authorities the round-2 text cites: `sw/litex/milan_soc.py`, `sw/litex/build.sh`, `sw/litex/patches/0005-vexiiriscv-cacheless-litex.patch`, `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`, `syn/ooc/pp_resource_baseline.json`;
- `git diff 241f9184..4742d2c0`, with the round-2 delta `da0dbc37..4742d2c0` read line by line;
- the public evidence at `649-review-evidence` `67855cfa`, `review-evidence/649-r2/`.

Evidence integrity:
- 238 of 238 files hash to the top `MANIFEST.json`.
- The 81 entries where the author's `MANIFEST-all.sha256` differs are exactly the path-redacted files, and each matches its recorded original digest.
- The census `inputs/map_cells.tsv.xz` decompresses to `b377ddec…`.

My verdict and ledger were fixed before I read the round-1 external review (`receipts/pre_r467-1_verdict.txt`, sha256 `9f6ad16e…`). R467-1 was then read and resolved below; it changed nothing. The concurrent R467-2 report was not read.

## Round-1 probes, rerun unchanged at this head

The scripts are byte-identical to the round-1 published ones (`scripts/r1-unchanged/`, `receipts/r1-unchanged/script_digests.txt`).

| Probe | Round 1 (`da0dbc37`) | Now |
|---|---|---|
| `mutate_map_selftest.py` | 9 of 13 killed; `partition-off`, `census-stray-off`, `census-total-off`, `names-sum-off` survived | `ancestry-additive-off` and `ancestry-shared-off` killed, then the script stops: the `partition-off` site no longer exists, because Partition is no longer code. The adapted run is below. |
| `partition_identity_fuzz.py` | 0 Partition failures with Ancestry clean in 20,000 trees | Stops with `AttributeError: partition_ties`: the function is gone, and the page and docstring now call it an identity |
| `guard_exclusion_probe.py` | Exclusion-removal mutant survived (`models --selftest` PASS) | Mutant **killed** (`resmap_models self-test: FAIL`). A planted refusal is still excluded. |
| `check_page_tables.py`, against the round-2 `outputs/` | 21 of 21 blocks equal | 26 page blocks equal to `tables.md`; record tie in 7 columns; 51 of 51 scopes; leaf LUT sum 51,123 against 50,767; 17 adjustments −356; RESULT PASS |
| `pp_stream_fit.py`, against the published `summary.json` | slope 5,885.97, RMS 1,988.8, residual signs −,+,+,− | Identical. Increments are 10,780, then 5,632, then 5,229. |
| `refit_from_page.py` | All coefficients reproduced | Output byte-identical to round 1 |

R467-1's published probes, run unchanged on a disposable copy of the head (`receipts/r467-probes-unchanged/`):
- `probe_partition.py` stops at its arm-A assertion, because the stub target no longer exists. That is answered by the stated identity. Its arm B, a leaf inflated from 2 to 7 LUTs, is now self-test arm "a leaf's LUT figure outside the recorded scopes", and the census tie catches it.
- `probe_stray_owner.sh`: the mutant is killed (14 of 15).
- `probe_selftests.py`: its three guard and page mutants are caught, then it stops at the removed partition site.
- `check_map_json.py`, on my regenerated map: ALL CHECKS PASS.

Adapted round-2 probes (`scripts/`):
- **`mutate_map_r2.py`**, 27 mutants (`receipts/map_mutation_r2.log`):
  - 22 killed, including every tie-level removal and every new census-LUT mutant: off, leaves only, parents only, total column only, sub-columns only, kinds collapsed, site keyed by BEL, no ancestor climb.
  - 1 absent: `partition-off`.
  - 4 survive:
    - `census-total-off` and `names-sum-off`, the two guards the docstring and page name as implied;
    - `flat-slice-off` and `flat-lut-only`: the flat tie's FF, RAMB, DSP and slice columns have no arm of their own (S1);
    - `census-leaf-ff-only`: the census tie's RAMB and DSP columns have no arm of their own (S1).
- **`partition_identity_r2.py`** (`receipts/partition_identity_r2.log`):
  - On 20,000 random trees, the leaves plus the adjustments never differ from the top when Ancestry is clean. It is an identity.
  - On the real image (218 rows, 175 leaves, 43 parents), every ±1 LUT plant on every row is caught: 523 of 523. Of those, 335 are caught by the census LUT tie alone with Ancestry clean, the reading round 1 found missing.
- **`mutate_models_guards.py`** (`receipts/models_guard_mutation.log`):
  - Killed: the missing-record and hard-error paths, the stream, processor, calibration and TDM exclusions, and the rank check.
  - Survives: `build-upfront-check-off`. Its CLI still refuses each deleted record (`adp-if-1`, `no-crf`, `ship`, `pp-ship`, `ship-8x8`) through the final guard summary (`receipts/models_upfront_mutant_behaviour.log`), so the mutant changes no behaviour. Not a finding.
  - The unmodified CLI exits 1, naming the point, for a deleted record and for a planted hard error.
- **`check_receipt_rows.py`** (`receipts/receipt_rows_check.log`):
  - 59 of 59 page Yosys rows match `run-receipts.json`.
  - 59 of 59 guard records are published, `ship-8x8` included, and their 7 refusals equal the page's marks.
  - The round-2 reopen row `51cc25fd…` equals the manifest's original digest of `route_map.log`.

## Round-2 verification items

1. **Tie set.**
   - The page (:58-74), `resmap_map.py:13-56`, the README row, the PR body and the `route_map.tcl` header (:21-23) agree. Partition is stated as an identity. There are five ties: ancestry, census, flat, record and depth.
   - The census tie reads all 218 rows' four LUT columns as distinct LUT sites (`resmap_map.py:208-235`, `:309-314`). The map ties at this head.
   - Every tie has an arm that fails when the tie is removed, and the stray-owner check is armed (`PLANTS`, `:578-602`; 15 of 15).
2. **LUT reconciliation.** The generated table `map-lut-sharing` (page :139-162) gives leaves 51,123, 17 adjustments −356 (each equal to its census shared-site count) and image 50,767. It equals a fresh generation.
3. **Sub-linear wording** at page :631, :681-682 and :797, in the README row and in the PR body.
   - Residual signs: processor −,+,+,−; Yosys datapath −,+,− at N = 1, 2, 4.
   - ACMP talker: 6,390, then 2,166 per stream. Datapath own logic: 5,046, then 4,082 per stream. All recomputed (`receipts/datapath_growth.log`).
   - No "faster than linear" remains.
4. **59 points and one census rate.**
   - The README row says 59 (52 + 7).
   - There is one rate, 64 lines a second, at page :1115 and `route_map.tcl:59-60`.
   - Cross-check (`receipts/census_rate_check.log`): the stopped attempt's 868,352-byte partial census equals the header plus exactly 12,248 complete lines of the full census, plus 58 bytes of the next line. 12,248 / 190.4 s = 64.3 lines a second, and 129,908 cells take about 34 minutes.
5. **Guard exclusion fails closed.** `resmap_models.py:144-156` raises on a missing record or a hard error, and `:358-365` stops the build. `command_guards` catches failures per point (`yosys_sweep.py:494-499`). The arms are in `resmap_models.py:390-453` and in the page check at `resmap_tables.py:413-432`. All guard mutants except the redundant one are killed.
6. **CPU, cache and L2 prices** (`receipts/soc_variants_check.log`):
   - **Receipts.** For all 20 priced variants:
     - the published `synth_hierarchy.rpt` hashes to its receipt;
     - parsed with the repository's parser, it equals the receipt's totals and CPU row;
     - `meta.json` equals the receipt;
     - the run used the pricing copy and read the shipping ROM;
     - its argv differs from shipping only in the variant's flags.
   - **Fits.** CPU count is 1,484.4 LUT per core (RMS 2.3), L1 ways 132.1 LUT and 3.50 BRAM tiles per way, and L2 on the L1-cached core −1.6 LUT per KiB (RMS 22.2). Every page difference recomputes: M +426, F +2,569, D +3,548 and 5 DSP, XLEN +1,167 / +4,232, Nax +14,348, and the ratios 1.129 and 1.157.
   - **Points per parameter.**
     - Three points each: CPU count, L1 ways, and L2.
     - FPU: three points on the M core (none, F, F+D).
     - XLEN and core choice: each priced at two bases.
   - **Labels and recipe.** Every non-shipping variant is labelled "not buildable under the shipping software profile".
     - `pricing-copy.diff` removes exactly the two refusal blocks.
     - The recorded tracked-recipe digest `bae9e3d1…` equals `sw/litex/milan_soc.py` at this head.
     - `git diff 241f9184..HEAD -- sw/ configs/ hdl/ syn/ooc/ .github/` is empty (`receipts/tracked_recipe_unchanged.txt`).
   - **No-ops.** Both measured no-ops are stated (page :933, :935): `rv64-fpu` has the same CPU netlist name and source digest as `rv64`, and `l2-*` prices equal to `ship`.
   - The generation failures `fpu-f` and `fpu-fd` are recorded with their reason. See F1 for the directive.
7. **Cold re-run** from `review-evidence/649-r2/author/inputs/`, in a `git archive` of the head (`scripts/cold_rerun.sh`, `receipts/cold_rerun.log`):
   - `resmap_map.py map` prints `TIED: 175 blocks, depth 5; LUT 50767, FF 59634, slices 15832.00, CARRY4 3506, RAMB36 79, RAMB18 27, DSP 14`, rc 0.
   - The regenerated `models.json` is byte-equal to the published one.
   - `resmap_tables.py … --page` prints "every table equals a fresh generation", rc 0. It does so with the published models and again with my regenerated models.
   - My `map.json`, `partition.md`, `lut_sharing.md`, `blocks_ranked.md` and `tables.md` are byte-equal to the published `outputs/` (`receipts/cold_outputs_compare.log`).
8. **Merge.**
   - `git merge-tree --write-tree da0dbc37 fea346e7` gives a clean result, tree `44fd4ada…`, equal to merge commit `689a9010`'s tree.
   - dev `fea346e7` is an ancestor of the head, and live dev is still `fea346e7`.
   - `git diff fea346e7..HEAD` names only `syn/resmap/` (8 files) and the two findings pages.
   - All 12 lane commits are one line with no trailers.

Gates at the head (`scripts/run_gates.sh`, `receipts/gates/`), all rc 0:
- the five self-tests (map 15 of 15);
- `docs_check`, `check_doc_paths`, `gen_toc --check` and `--verify-anchors` (pinned renderer, scratch venv);
- `check_em_dash` against both bases;
- `check_py_idiom`;
- `git diff --check` against both bases.

## Findings

### F1 MINOR (Conformance, RTL, Docs): the SoC variant prices are described as synthesized at the shipping directive, but were run at the default directive

**Where:** `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:127`: "Vivado then synthesizes each exported SoC top out of context at the shipping synthesis directive".

**Evidence:**
- All 20 published `review-evidence/649-r2/author/inputs/soc-variants/*/soc_ooc.tcl` files are one script (sha256 `6da719ef…`). Its line 6 is `synth_design -directive default -mode out_of_context …`, and the published driver `scratch-scripts/price_variants.py:177` matches it.
- The shipping AX7101 build passes `--synth-directive AreaOptimized_high --opt-directive ExploreArea` (`sw/litex/build.sh:378-380`, `cfg_ax7101`).
- `docs/testing/PP_SHADOW_BASELINE_RECIPE.md:264` says the synthesis directive "remains `AreaOptimized_high`". The page's own :111 calls `AreaOptimized_high` "the shipping directives" for the datapath anchors.
- The published handoff's pricing-method note states `-directive default` correctly; only the page misstates it.

**Impact:**
- Every CPU, cache and L2 figure on the page (:931-938, the summary :27, the opportunities :1090 and the PR's headline SoC row) is a default-directive measurement presented as a shipping-directive one.
- The SoC calibration (1.13 for the SoC, 1.16 for the CPU, page :938) compares a default-directive synthesis with an `AreaOptimized_high` route. So the directive difference is folded silently into the factor the page offers for converting every variant's change.
- A #640 reader comparing these prices with the datapath anchors, which ran at `AreaOptimized_high`, is told the two share a directive, and they do not.

**Required outcome:** One of:
- the page states the directive actually used, and what that means for comparing these prices with the shipping image and with the datapath anchors (the calibration factor then absorbs a directive change as well as synthesis-to-route);
- the variants are re-priced at `AreaOptimized_high`.

Either way, the method text and the published receipts agree.

**Verification:**
- The page's method sentence names the directive in the published `soc_ooc.tcl`, or the re-run Tcl and its reports carry `AreaOptimized_high`.
- `resmap_tables.py --page` still passes.

## RESIDUE

Each item is wording only. No measurement, figure, test, code or generated artifact changes.

| ID | Where | Exact fix |
|---|---|---|
| RES1 | page :935 | "The lane's VexiiRiscv SoC generator carries a local patch that routes …" → "The recipe's VexiiRiscv SoC generator carries the repository's patch `sw/litex/patches/0005-vexiiriscv-cacheless-litex.patch`, which routes …". The patch is tracked (commit `ecf18de29`), not this lane's. |
| RES2 | page :1099 | "one after another inside one hold of the lock taken by a detached runner" → "one after another, in three holds of the lock taken by a detached runner (the first refused shipping attempt; the shipping variant, the route reopen and 16 variants; then the three L2 points on the L1-cached core)". The published `runs/chain_held.log`, `chain_held2.log` and `chain_held3.log` each take and release the lock. |
| RES3 | page :1217; PR body "How to validate" | page: "so the manifest gives its digest, `b377ddec33c438bc`" → "so it is published compressed as `inputs/map_cells.tsv.xz`, with its digest `b377ddec33c438bc` in the manifest". PR body: "decompress the two `.xz` files, and place the census `map_cells.tsv` in `inputs/map/`" → "decompress the three `.xz` files, the census into `inputs/map/map_cells.tsv`". |

## SUGGESTION

- **S1.** Give the flat tie's FF, RAMB, DSP and slice comparisons, and the census tie's per-leaf RAMB and DSP comparisons, an arm each. Three column-level mutants survive (`flat-slice-off`, `flat-lut-only`, `census-leaf-ff-only`). Every tie as a whole is armed, as the page says, so this does not contradict a claim.
- **S2.** The handoff's digest for the stopped attempt's partial census, `56763a0be20f3053…`, looks mistyped. The full census's first 868,352 bytes hash to `6763a0be20f30539…`, the same digits shifted by one. Only the handoff carries it; it is not in the repository.
- **S3** (carried from R466-1 S3 = R467-1 S4, listed open by the lane). A talker-only or listener-only point would split the per-stream cost by direction for #640.

## Prior public findings: resolution at this head

| Item | Disposition | My evidence |
|---|---|---|
| R466-1 F1 = R467-1 F1 (tie set; stray owner; depth comment) | **Resolved.** Partition stated as an identity; census LUT tie as a second reading of every leaf and parent; stray owner armed; depth comment fixed; all five statements agree | `map_mutation_r2.log`, `partition_identity_r2.log`, R467-1 probes |
| R466-1 F2 = R467-1 F5 (LUT sum) | **Resolved.** Generated reconciliation table; "partition" qualified | cold re-run; `r1-unchanged/page_tables_check.log` |
| R466-1 F3 = R467-1 F6 (curvature) | **Resolved** | `r1-unchanged/pp_stream_fit.log`, `datapath_growth.log` |
| R466-1 F4 = R467-1 F2 (59 points; one rate) | **Resolved** | README row; `census_rate_check.log` |
| R466-1 F5 = R467-1 F7 (guards fail open) | **Resolved** | `r1-unchanged/guard_exclusion_probe.log`, `models_guard_mutation.log`, `r467-probes-unchanged/probe_selftests.log` |
| R466-1 F6 = R467-1 F3 (CPU, cache, L2 uncosted) | **Resolved** by the maintainer ruling (b): measured. The method statement is the new F1 | `soc_variants_check.log` |
| R467-1 F4 (no re-runnable receipts) | **Resolved** | `cold_rerun.log`, `cold_outputs_compare.log` |
| R466-1 RES1 to RES4; R467-1 RES-1 to RES-5 | **Applied** as worded (page :21, :24, :17, :258; PR Status) | page diff |
| R466-1 S1, S2, S4 (= R467-1 S2, S3, S5) | **Taken:** clean-tree receipts (with an arm), the rank check (killed mutant), the `ship-8x8` record published | `receipt_rows_check.log`, `models_guard_mutation.log` |
| R466-1 S3 (= R467-1 S4) | Open by statement; retained as S3 | PR body Round 2 item 7 |

## Lens results (exact head 4742d2c02c109f7dd8e21d74905efb182b2dbca2)

```text
[R466] MINOR Conformance - docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:127; inputs/soc-variants/*/soc_ooc.tcl:6; sw/litex/build.sh:378-380 - SoC variants said to be at the shipping directive, run at default (F1)
[R466] MINOR RTL - same artifacts - synthesis-directive effect on the priced resources misstated, and folded into the 1.13/1.16 factor (F1)
[R466] PASS Robustness - resmap_map.py:125-136,:208-235 (unknown LUT-BEL primitive refused),:299-322; resmap_models.py:125-156,:355-366; yosys_sweep.py:271-286,:370-397,:466-499,:653-668; resmap_tables.py:226-282 - fail-closed guards, rank refusal, clean-tree refusal, per-point guard failures, fewer-than-three-points SoC axes; probes in models_guard_mutation.log
[R466] PASS Tests - resmap_map.py:578-629 (15 arms), resmap_models.py:390-485, resmap_tables.py:386-432, yosys_sweep.py:771-786 - 22 of 27 map mutants and 7 of 8 guard mutants killed; every survivor is a documented implied guard, a redundant path or column-level (S1); cold re-run reproduces every table
[R466] MINOR Docs - docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:127 - method sentence contradicts the receipts and the recipe (F1)
```

**Conformance.** Apart from F1, these were checked and found sound:
- the route-1x1 record tie and the 51 scopes on the regenerated map;
- the 17 adjustments against the census shared sites;
- every CPU, cache and L2 price, difference and fit, from the published reports;
- the ruling's conditions: scratch-only copy, recipe unchanged, labels, the generation failures with their reason, and no STOP needed (FPU has three points on the M core);
- the curvature statements;
- the census rate.

**RTL.**
- No `hdl/`, `configs/`, `sw/` or `syn/ooc/` change against the source base.
- The round-2 `route_map.tcl` change is two comment hunks only.
- `datapath_ooc.tcl` is unchanged since round 1.
- Black-box set for the SoC runs: `KL_gptp_gmii_launch`, `KL_mac_rmon_events`, `milan_datapath`.
- The `Opt 31-30` reason for comparing after synthesis is stated.
- The generator patch's no-L2 behaviour is confirmed in the tracked patch (`0005-…:20-22`, `:62-73`).
- The open defect is F1.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | issue #649 acceptance 1-4 and ruling 5978713464; page :58-74, :127, :139-162, :631, :681, :797, :880-938, :1095-1217; `soc_prices.json` and 20 `synth_hierarchy.rpt`; `pricing-copy.diff`; `prepare.json`; `pp_resource_baseline.json` route-1x1; regenerated `map.json` | R466-2 (not clean) | 4742d2c02c109f7dd8e21d74905efb182b2dbca2 |
| RTL | UNCLEAN (F1) | diff scope against base and dev; `route_map.tcl` round-2 hunks; `datapath_ooc.tcl`; 20 `soc_ooc.tcl` (one digest); `sw/litex/build.sh:378-380`; `milan_soc.py:3632-3670,:3860-3880`; `0005-vexiiriscv-cacheless-litex.patch` | R466-2 (not clean) | 4742d2c02c109f7dd8e21d74905efb182b2dbca2 |
| Robustness | CLEAN | `resmap_map.py`, `resmap_models.py`, `resmap_tables.py`, `yosys_sweep.py` refusal and fail-closed paths at the lines above; CLI probes with a deleted record and a hard error | R466-2 | 4742d2c02c109f7dd8e21d74905efb182b2dbca2 |
| Tests | CLEAN | five self-tests; 27 map mutants; 8 models mutants; real-image LUT plants (523); R467-1 probes; cold re-run with byte-equal outputs | R466-2 | 4742d2c02c109f7dd8e21d74905efb182b2dbca2 |
| Docs | UNCLEAN (F1) | the page in full at the round-2 hunks; `docs/findings/README.md:25`; `resmap_map.py:4-68`; `route_map.tcl:1-23,:56-60`; `soc_sweep.py:8-16`; `sweep_plan.json:71`; PR body; docs gates | R466-2 (not clean) | 4742d2c02c109f7dd8e21d74905efb182b2dbca2 |

## Real limits

- **No Vivado or LiteX was run.**
  - The SoC exports and the 20 syntheses were checked from their published reports, `meta.json`, Tcl and receipts, not re-run. The scratch exports and tops are published as digests only.
  - So "identical apart from the module name" (`l2-*`) and "the same top, comments aside" (shipping through the copy) are taken from equal prices and the handoff.
  - The effect of the directive in F1 is not quantified.
- **Yosys points were not re-run in this round.** Round 1 reproduced 7 points byte-equal, and the round-2 sweep changes touch receipts only.
- **The route reopen was not re-run.** The census and reports are the published ones, and their digests tie to the page and manifest.
- **Physical calibration NOT RUN**; nothing here is hardware evidence.
- **Hosted checks were read only** (snapshot `receipts/hosted_checks_snapshot.txt`):
  - succeeded: `rtl-fast`, `verilator-lint`, `yosys-elaboration`, the four Yosys shards, Verilator shard 3, `full-ci-gate`, `bdd-conformance`, `wire-accountability`, `docs-check-no-git`;
  - in progress: `docs-check`, `elaborate`, Verilator shards 0, 1, 2 and 4;
  - skipped: the physical gPTP context.

  Acceptance of hosted and act results is the manager's.
- **Clone restored and verified** (`receipts/clone_restore_check.txt`):
  - HEAD and index tree are exact;
  - 1,008 tracked blobs re-hash raw with matching modes;
  - the three required gitlinks are at their pins (`gptp-processor 5dce647a`, `protocol-processor 631eeb34`, `third_party/verilog-axis 48ff7a7e`), with `external` uninitialized as at start;
  - the Python caches my runs created were removed, and status (ignored files included) is empty.

## Pending manager duties

- Route F1 to the executor; re-review at the fixing head. F1 touches only the page, or the page plus re-priced receipts, so Conformance, RTL and Docs must be covered again there.
- Carry RES1 to RES3 to the residue checklist.
- Still open from round 1:
  - file the two tooling findings (sv2v-converted guards not enforced in Yosys; the builder accepts 235 names), and add a third: `milan_soc.py --with-fpu` is a no-op on the VexiiRiscv path;
  - post, or delegate, the #229 and #640 summary comment.
- Hosted, act and exact-head long-gate acceptance; build and validate the candidate on current dev (base `241f9184`, live dev `fea346e7`); post-merge containment.

R466-2 FINISHED
