[R467] POSITIVE - exact head 4742d2c02c109f7dd8e21d74905efb182b2dbca2

# R467-2: external independent review of issue #649 / PR #650, round 2

- **Exact head:** `4742d2c02c109f7dd8e21d74905efb182b2dbca2`, tree `7e247e4f65ef8a02d9834246af6329c888fca206`. Round-1 head `da0dbc37`, source base `241f9184`, live dev `fea346e7`.
- **Role:** external cleared-context reviewer. I reconstructed the task from these public sources:
  - AGENTS.md, CONTRIBUTING.md and docs/README.md.
  - Issue #649: the body, the lane assignment (5976977547), TAKEN, REVIEW READY (5978158007), the round-2 assignment and ruling (5978713464), and REVIEW READY round 2 (5980922096).
  - The PR #650 body and the manager's evidence comment (5980942776).
  - The diffs `241f9184..4742d2c0`, `da0dbc37..4742d2c0` and `fea346e7..4742d2c0`, with their history.
  - The public evidence: `review-evidence/649-r1` and `review-evidence/649-r2/author` on `649-review-evidence` at `67855cfa`.
- **Order of reading:** I read the prior public findings (R466-1 5978523295 and my own R467-1 5978705424) only after this independent pass was complete.
- **Verdict: POSITIVE.**
  - Every round-1 finding is resolved at this head (table below), each against a probe or re-run of my own.
  - No BLOCKER, MAJOR or MINOR finding is open.
  - Five RESIDUE wording items are recorded with exact fixes, plus three new suggestions; one round-1 suggestion (S4) stays open.
- **Still measurement only.** Against dev `fea346e7`, the lane touches exactly `syn/resmap/` (8 files), `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md` and one row of `docs/findings/README.md`.

## Focus items: what I verified at this head

| # | Claim | Result | Receipt |
|---|---|---|---|
| 1 | Tie set stated exactly: Partition is an identity; leaf LUT figures and sharing adjustments are read from the placed-cell census (218 rows); every named tie has an arm that fails when the tie is removed | **Holds.**<br>• Partition is stated as an identity on page `:58-79` (at `:62`) and in the docstring `resmap_map.py:13-56` (at `:19-22`).<br>• My own re-reading of the census, without the lane's code: all **218 of 218** rows' four LUT columns equal the distinct (slice, LUT letter) sites their cells occupy. Every parent's adjustment equals minus its census shared-site count.<br>• Disabling each tie or sub-check in turn: ancestry additive, ancestry LUT sign, census leaf cells, census LUT sites, stray owner, flat report, record totals, record scope columns and depth are all **killed** (12 to 14 of 15 arms pass). The two bookkeeping guards that the page calls implied survive, as stated.<br>• On the real published inputs, the census tie refuses two plants: a non-processor leaf's LUT changed from 3 to 5, and a census LUT cell moved to another LUT letter.<br>• Round 1's arm B, run verbatim, is caught: `census: top/leaf LUT counts 2 LUT sites, the report says 7` | `receipts/check_census_lut.log`, `receipts/probe_r2.log` |
| 2 | Generated LUT reconciliation: leaves 51,123; 17 adjustments totalling -356; image 50,767 | **Holds.**<br>• Independent derivation: leaf sum 51,123 (logic 48,891, LUTRAM 2,228, SRL 4).<br>• 17 non-zero adjustments summing to -356, all logic (LUTRAM 0, SRL 0).<br>• Every row of the page's `map-lut-sharing` block matches, including the shared-site column and the 50,767 image row | `receipts/check_census_lut.log`, `receipts/check_map_json.log` |
| 3 | Sub-linear growth wording everywhere | **Holds.**<br>• Page `:631` ("a little less than linear"), `:636`, `:681` and `:797` give the residual signs (Yosys -,+,- at N = 1, 2, 4; processor -,+,+,- at 1, 2, 4, 8) and the falling increments (10,780, then 5,632, then 5,229).<br>• The README row says "a falling cost per added stream"; the PR body says sub-linear.<br>• No "faster than linear" wording remains in the page, README, scripts or PR body | `receipts/wording-greps.log` |
| 4 | 59 points; one census rate | **Holds.**<br>• README: 59 points (52 guard-clean, 7 refused).<br>• One rate, 64 lines a second (12,248 lines in 190 s), at page `:1115` and `route_map.tcl:59`.<br>• Arithmetic: 12,248 / 190 = 64.5 lines a second, and 129,908 cells at that rate take 33.6 min, so "about 34 minutes" holds.<br>• The basis is stated in the published handoff (lines 285-286). The stopped run's partial files are not published (see limits) | `receipts/wording-greps.log` |
| 5 | Guard exclusion fails closed, with arms | **Holds.**<br>• `refusals()` raises `GuardError` on a missing record, a hard error, or a non-zero rc with no refusal (`resmap_models.py:148-156`). `build()` checks every point first (`:358-365`).<br>• On a copy of the real published `summary.json`, each of three plants stops the models with exit 1, naming the point: a deleted `streams-4` record, a planted hard error on `pp-rxslots-8`, and a bare rc 1 on `chans-2`.<br>• Self-test mutants all killed: a missing record read as clean; a hard error read as clean; a refused point kept in the stream fit, the processor fit, the TDM model or the calibration; a stale page reported as equal; a rank-deficient fit accepted | `receipts/failclosed-real.log`, `receipts/probe_r2.log`, `receipts/probe_selftests.log` |
| 6 | CPU count, L1 ways, L2, FPU and core prices; profile labels; tracked recipe unchanged; the two no-ops | **Holds.**<br>• Re-parsed each variant's published `synth_hierarchy.rpt` (top row, and the CPU row that `meta.json` names) without the lane's code. All 20 equal `soc_prices.json` and the page's `soc-variant-prices` rows.<br>• Every non-ship row is labelled "not buildable under the shipping software profile".<br>• Least squares re-derived:<br>&nbsp;&nbsp;– 1,484.4 LUT per core (residuals 2.1, -3.2, 1.1);<br>&nbsp;&nbsp;– 132.1 LUT and 3.50 BRAM per L1 way;<br>&nbsp;&nbsp;– L2 on the L1-cached core: -1.6 LUT/KiB, and 4 BRAM tiles per doubling.<br>• FPU ladder on the M core: M, then M+F (+2,569 LUT), then M+F+D (+3,548 LUT, +5 DSP). F and F+D on RV32I are recorded as not generated, with the generator's error.<br>• XLEN and the core choice are each priced at two bases.<br>• Both no-ops are measured: `rv64-fpu` equals `rv64`, and `l2-8k/16k/32k` equal `ship`.<br>• `pricing-copy.diff` removes exactly the head recipe's two `ap.error` refusals, verbatim.<br>• `git diff 241f9184..4742d2c0 -- sw/litex/` is empty; `milan_soc.py` is blob `3f8c332e` at the base, at dev and at the head | `receipts/check_soc_variants.log` |
| 7 | Cold re-run from `review-evidence/649-r2/author/` at `67855cfa`, census from `inputs/map_cells.tsv.xz` | **Reproduced** with the exact-head scripts.<br>• `resmap_map.py map` prints `TIED: 175 blocks, depth 5; LUT 50767, FF 59634, slices 15832.00, CARRY4 3506, RAMB36 79, RAMB18 27, DSP 14` (rc 0).<br>• `resmap_models.py` regenerates a `models.json` byte-equal to the published one.<br>• `resmap_tables.py ... --soc-variants ... --page` prints `page: every table equals a fresh generation` (rc 0), with both the published and the regenerated models.<br>• `map.json`, `blocks_ranked.md`, `partition.md`, `lut_sharing.md` and `tables.md` are byte-equal to the published outputs. All 26 page blocks equal the fresh `tables.md`.<br>• The decompressed census hashes to `b377ddec...`, round 1's census digest.<br>• Round 2's two reports equal round 1's recorded digests (`fbf802c4...`, `2e3c6b51...`) when only their Date line is changed (to 08:17:46 and 08:17:47). This confirms page `:1117` | `receipts/cold-rerun.log`, `receipts/check_receipts_and_tables.log`, `receipts/r1-reports-date-line.log` |
| 8 | The `--no-ff` merge of dev `fea346e7` is clean, and the diff against dev touches only `syn/resmap/` and the findings pages | **Holds.**<br>• `689a9010`'s parents are `da0dbc37` and `fea346e7`. Its tree `44fd4ada` equals a fresh `git merge-tree` of the two.<br>• The dev side changed 7 docs/testbench files, with no overlap with the lane.<br>• `fea346e7..4742d2c0` touches 10 files: 8 under `syn/resmap/`, the page, and the README row.<br>• Gitlinks are identical to dev's | `receipts/merge-and-scope.log` |

### Round-1 probes, run unchanged

Each script's sha256 equals the round-1 packet's copy.

- **`probe_partition.py`** stops at its arm-A assertion, because `partition_ties` no longer exists. The stated identity (page `:62`) answers that arm. Its arm B, run verbatim in `probe_r2.py` part 1, is caught.
- **`probe_stray_owner.sh`:** the mutant is killed (14 of 15 arms pass).
- **`probe_selftests.py`:**
  - Its three F7 mutants (stream fit, processor fit, stale page) are killed.
  - It then stops at the removed partition site, so its last two arms were run in `probe_r2.py` instead.
  - Ignoring the guard lines: killed.
  - Disabling only the first half of the sweep summary tie survives, as in round 1. Disabling both halves is killed (`receipts/probe_sweep_tie_pair.log`), so the tie is armed as a pair.
- **`check_map_json.py`:** all checks pass (175 leaves, 51 of 51 scopes, 17 adjustments). Round 2's `map.json` table, leaves and adjustments equal round 1's.
- **`check_receipts.py`:** all 59 rows match (247.9 min, the same 7 refused).
- **`check_receipts2.py`:** as in round 1, 59 of 59 points carry ROM digests and all five anchor rows match. Its "checkpoint digest not in #234 page" line is unchanged from round 1. That point was settled then against the #638 round-7 receipts.
- **`compare_tables.py`:** 26 of 26 page blocks equal.

## Findings

No BLOCKER, MAJOR or MINOR finding is open.

### RESIDUE (wording only)

None of these changes a figure, test, code, generated table or claim.

**RES-1. The self-test arm count.**
- Where: page `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:78` and PR body Round 2 item 1.
- Current wording: "15 arms, each caught by the tie that the arm names" (page) and "each with a self-test arm that only it satisfies (15 arms)" (PR body).
- Why it is wrong: 15 arms are counted (`resmap_map.py:627`), but one is the clean fixture, which must tie. Only 14 arms plant a wrong figure.
- Exact fix, page: "builds a small consistent image and requires it to tie (one arm), then plants a wrong figure in each of 14 more arms, each caught by the tie that the arm names."
- Exact fix, PR body: "(15 arms)" becomes "(14 planted arms and the clean fixture, 15 in all)".

**RES-2. Who carries the generator patch.**
- Where: page `:935`.
- Current wording: "The lane's VexiiRiscv SoC generator carries a local patch".
- Why it is wrong: the patch is the recipe's tracked `sw/litex/patches/0005-vexiiriscv-cacheless-litex.patch`, not a lane change. The current wording suggests the recipe was altered.
- Exact fix: "The recipe's VexiiRiscv SoC generator carries the tracked patch `sw/litex/patches/0005-vexiiriscv-cacheless-litex.patch`, which routes".

**RES-3. Where the census is published (page).**
- Where: page `:1217`.
- Current wording: "The census `map_cells.tsv`, 12.5 MB, is over the evidence's 200 KB file limit, so the manifest gives its digest".
- Why it is wrong: the census is published compressed (manager comment 5980942776).
- Exact fix: "The census `map_cells.tsv`, 12.5 MB, is over the evidence's 200 KB file limit, so it is published compressed as `inputs/map_cells.tsv.xz` (decompressed SHA-256 `b377ddec33c438bc`); the map and the table check both read it."

**RES-4. Where the census is published (PR body).**
- Where: PR body "How to validate", and Round 2 item 6.
- Current wording, "How to validate": "(decompress the two `.xz` files, and place the census `map_cells.tsv` in `inputs/map/`)".
- Exact fix: "(decompress the three `.xz` files, `models/models.json.xz`, `work/summary.json.xz` and `map_cells.tsv.xz`, and move `map_cells.tsv` into `inputs/map/`)".
- Current wording, item 6: "once published" and "kept for the manager to publish beside it".
- Exact fix: "published at `67855cfa`, the census as `inputs/map_cells.tsv.xz`".

**RES-5. Which receipts carry HEAD and a clean-tree record.**
- Where: PR body Description (`yosys_sweep.py` row: "records HEAD and a clean tree in every receipt") and Round 2 item 7 ("HEAD and a clean-tree check in every sweep receipt").
- Why it is wrong: the published round-1 receipts and guard records predate the change. None of the 59 carries a `tree` record.
- Exact fix: append "(receipts written from round 2 on; the published round-1 receipts predate it)".

### SUGGESTIONS

- **S6. A self-test arm for a missing recorded scope.** At `resmap_map.py:289-292`, the record tie's "scope not in the map" branch has no arm. With its `failures.append` deleted, the self-test still passes 15 of 15 (`receipts/probe_r2.log`). The tie itself is armed, and all 51 scopes are present on the real image. One more plant would cover the branch, for example a record scope `{"wrapper/absent": {"LUT": 1}}`.
- **S7. The L2 BRAM fit.** `soc-variant-fits` (page `:913`) fits L2 BRAM per KiB: 0.32, with residuals -0.57, +0.86 and -0.29 tiles that are not shown. The data, and page `:936`, grow by four tiles per doubling. Fit L2 per doubling, or show the BRAM residual. The prose is already correct.
- **S8. A stale guard record after a failed re-lint.** At `yosys_sweep.py:466-475`, a re-lint that fails before writing (for example, because it refuses a dirty checkout) leaves the previous `guards.json` in place for `summary` to read. The command does exit 1, but deleting the old record first would make the stale state impossible.
- **S4 (round 1, still open, as the lane states).** A talker-only or listener-only point would split the per-stream cost by direction.

## Prior public findings: resolution at this head

- I read these only after the pass above. "R466-1" is comment 5978523295, and "R467-1" is comment 5978705424.
- No other public finding exists on PR #650 or issue #649, and there is no PR review.

| Item | Disposition | My evidence at this head |
|---|---|---|
| R467-1 F1 = R466-1 F1 (tie set overclaims; Partition and stray owner unarmed; depth comment) | **Resolved.**<br>• The leaf-LUT reading is now independent: the census LUT tie over 218 rows.<br>• Partition is stated as an identity.<br>• The stray owner is armed.<br>• `route_map.tcl:22-24` describes the implemented check.<br>• Page, README row, PR body and both script headers agree | `receipts/check_census_lut.log`, `receipts/probe_r2.log`, `receipts/probe_stray_owner.log`, `receipts/probe_partition.log` |
| R467-1 F2 = R466-1 F4 (54 points; two census rates) | **Resolved:** the README says 59, and one rate is given | `receipts/wording-greps.log` |
| R467-1 F3 = R466-1 F6 (CPU, cache and L2 not costed) | **Resolved** under ruling 5978713464, option (b).<br>• The variants are priced from the scratch copy and labelled, each with three points or two-valued by nature.<br>• The tracked recipe is unchanged.<br>• The FPU's three points are on the M core because F needs M (the generator error is recorded). I read that as within the ruling, and it is stated publicly on page `:918-920` and in REVIEW READY | `receipts/check_soc_variants.log` |
| R467-1 F4 (no re-runnable receipts) | **Resolved:** the cold re-run reproduces TIED, a byte-equal `models.json`, and "every table equals a fresh generation" | `receipts/cold-rerun.log` |
| R467-1 F5 = R466-1 F2 (LUT columns do not partition; adjustments unpublished) | **Resolved:** the generated `map-lut-sharing` table, and "partition" qualified at page `:58-63`, `:291-295`, `:325` and docstring `:15-22` | `receipts/check_census_lut.log` |
| R467-1 F6 = R466-1 F3 (faster-than-linear wording) | **Resolved** | `receipts/wording-greps.log` |
| R467-1 F7 = R466-1 F5 (guard exclusion fails open; arms missing) | **Resolved** | `receipts/failclosed-real.log`, `receipts/probe_r2.log` |
| R467-1 RES-1 to RES-5 = R466-1 RES1 to RES4 | **Applied** as worded: page `:21`, `:258`, `:24`, `:17`, and the PR Status | page at head; PR body |
| R467-1 S2 = R466-1 S1 (HEAD and clean tree) | **Taken** in code (`yosys_sweep.py:271-285`, `:397`). Armed: the "tracked change read as clean" mutant is killed. RES-5 covers the PR wording | `receipts/probe_r2.log` |
| R467-1 S3 = R466-1 S2 (rank) | **Taken** (`resmap_models.py:134`), and armed | `receipts/probe_r2.log` |
| R467-1 S4 = R466-1 S3 (split by direction) | **Open**, as the lane states | - |
| R467-1 S5 = R466-1 S4 (`ship-8x8` guard record) | **Taken:** 59 of 59 guard records published, `ship-8x8` included, all Verilator 5.050, none with hard errors | `receipts/failclosed-real.log` |

## Lens results

Each line names the artifacts examined at the exact head.

- `[R467] PASS Conformance - issue #649 acceptance 1-4, ruling 5978713464, page :19-165, :289-325, :843-940, inputs/soc_prices.json, synth_hierarchy.rpt x20 - map totals tied to route-1x1; each block's LUT read twice (census tie, 218 rows); reconciliation 51,123 / -356 / 50,767; SoC variants priced per the ruling at three points or two-valued; recipe unchanged; no RTL, configuration or gate-baseline change against dev fea346e7`
- `[R467] PASS RTL - git diff fea346e7..4742d2c0 (no hdl/, configs/, constraints/, sw/ or gitlink change); recipe facts the page relies on: milan_soc.py:3666-3669 (the two refusals, matched verbatim by pricing-copy.diff), :2572-2580 (--with-fpu reaches only NaxRiscv), sw/litex/patches/0005-vexiiriscv-cacheless-litex.patch (no hub or L2 without an LSU L1); gitlinks 5dce647a / 631eeb34 / 48ff7a7e / efeb541a equal dev`
- `[R467] PASS Robustness - resmap_map.py:208-228 (an unknown primitive on a LUT BEL is refused), :299-322 (census LUT over every row; stray owner); resmap_models.py:134 (rank), :148-156 and :358-365 (fail closed on a missing, hard-error or rc-only record, shown on real inputs); yosys_sweep.py:271-285, :397, :466-499 (dirty checkout refused, per-point exception handling, exit 1); resmap_tables.py:248 (fewer than three points stated, not fitted)`. S6 and S8 are suggestions only.
- `[R467] PASS Tests - the five self-tests at head (map 15/15; sweep, soc, models and tables PASS); 24 mutants in probe_r2.py plus the round-1 probes: every tie, guard, rank and page-check mutant is killed. The only survivors are the two guards stated to be implied, the record tie's missing-scope branch (S6), and the redundant first half of the sweep tie, whose pair is killed. The census tie refuses the real-data plants`
- `[R467] PASS Docs - docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md (all 1,217 lines), docs/findings/README.md:25, the resmap_map.py and route_map.tcl headers, the soc_sweep.py and sweep_plan.json descriptions, the PR #650 body; docs_check 0 findings; check_em_dash 0 findings against fea346e7 (1,218 lines) and 241f9184 (1,312 lines); gen_toc --check OK; --verify-anchors 340 links; check_doc_paths OK (908 paths)`. RES-1 to RES-5 are wording only.

## Lens ledger (reviewer-owned)

I wrote this ledger before reading any prior finding text. It did not change after I resolved those findings.

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #649 scope and acceptance; rulings 5976977547 and 5978713464; page Method, map, LUT reconciliation and SoC variants; `soc_prices.json` and the 20 variant reports; `pricing-copy.diff` against `milan_soc.py`; the `pp_resource_baseline.json` route-1x1 record | R467-2 | 4742d2c02c109f7dd8e21d74905efb182b2dbca2 |
| RTL | CLEAN | diff `fea346e7..4742d2c0` (no RTL or recipe file); `milan_soc.py:2572-2580`, `:3666-3669`; patch 0005; gitlinks | R467-2 | 4742d2c02c109f7dd8e21d74905efb182b2dbca2 |
| Robustness | CLEAN | `resmap_map.py` input refusals and census tie; `resmap_models.py` fail-closed handling and rank check; `yosys_sweep.py` tree state and guard command; fail-closed plants on real inputs | R467-2 | 4742d2c02c109f7dd8e21d74905efb182b2dbca2 |
| Tests | CLEAN | five self-tests; `probe_r2.py` (24 mutants plus real-data plants); round-1 probes, unchanged; cold re-run; independent census and SoC re-derivations | R467-2 | 4742d2c02c109f7dd8e21d74905efb182b2dbca2 |
| Docs | CLEAN (RESIDUE carried) | page (1,217 lines), README row, script headers, PR body; docs gates | R467-2 | 4742d2c02c109f7dd8e21d74905efb182b2dbca2 |

## Real limits

- **Vivado was not run.** The route reopen, the four anchors and the 20 SoC variant syntheses are checked only through their published reports, receipts and digests.
  - The SoC variant logs (`ooc.log`) and the scratch generator outputs are published as digests, not files.
  - The claim at page `:126`, that the shipping variant gives the same top through the copy and through the tracked recipe, was not re-run.
- **The SoC exports were not regenerated.** That needs the recipe's LiteX environment, the SDK and the scratch generator copies.
- **No Yosys point or Verilator guard was re-run this round,** so the pinned Verilator was not invoked. The round-2 diff does not touch the mapping or the lint, the 59 guard records are now published, and round 1 reproduced all 59 guards and 19 Yosys points.
- **The census rate's source files are not published** (the stopped first reopen's partial census). The rate is checked only by arithmetic against the stated counts.
- **Path redaction.** The manager redacted paths in the published `route_map.log`, `tcl.sha256` and `soc_prices.json`. Their original digests in `MANIFEST.json` equal the ones the page gives (`51cc25fd...` for the log).
- **Physical calibration NOT RUN.** The page makes no hardware claim.
- **Hosted evidence at the exact head was inspected only,** at 14:25 UTC:
  - 10 contexts succeeded: `bdd-conformance`, `changes`, `docs-check-no-git`, `full-ci-gate`, `verilator-lint`, `wire-accountability`, and `Yosys shard 0/4` to `3/4`;
  - `Physical gPTP` was skipped;
  - 8 were still in progress: `docs-check`, `elaborate`, `yosys-elaboration`, and `Verilator shard 0/5` to `4/5`.
  - Hosted and local-replica acceptance belongs to the manager.

## Pending manager duties

- Carry RES-1 to RES-5 to the residue checklist.
- Confirm the in-progress hosted contexts at the exact head; hosted and act acceptance stay with the manager.
- Build and validate the current-dev candidate at the merge turn (source base `241f9184`, live dev `fea346e7`). The recorded merge `689a9010` is clean.
- Items the lane still has open:
  - The #229/#640 summary comment is unposted.
  - Three tooling findings need their own issues:
    - the Yosys flows ignore sv2v-converted elaboration guards;
    - the builder accepts 235 AEM names against the backend's 128;
    - `milan_soc.py --with-fpu` is a silent no-op on the VexiiRiscv path.
- CONTRIBUTING still requires a second positive review, the internal one.

## Clone restoration

- **State:** the clone is at the exact head. HEAD is `4742d2c0`, the index tree equals the head tree `7e247e4f`, and `git status --porcelain --ignored` is empty.
- **Blobs:** all 1,008 tracked blobs re-hash raw to their recorded ids, with matching modes.
- **Gitlinks:** at their pins (`gptp-processor 5dce647a`, `protocol-processor 631eeb34`, `third_party/verilog-axis 48ff7a7e`). `external` is uninitialized, as it was at start (`receipts/restore-check.log`).
- **How scripts ran:** every script ran either with `-B` from the clone, or from a git-archive copy under `scratch/`. Mutants were applied only to that copy and restored byte for byte.
- **GitHub:** no write was made.

R467-2 FINISHED
