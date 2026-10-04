[R466] NEGATIVE - exact head da0dbc37437b58ac591467cd1b8daa9c8896cf6e

Round R466-1, internal cleared-context review of issue #649 / PR #650. Tree `4ab5c8fffcffee036f0788d2302ee7d7d9a06c8c`, base and live dev `241f91845230ae410506dffb16b71937127fd175`. All five lenses applied. Six MINOR findings stay open, so the verdict is NEGATIVE. Four RESIDUE items and four SUGGESTIONs are listed separately.

The measurement itself holds up. Every figure checked recomputes or reproduces at this head. The open findings are in three places:
- what the map's tie set and the page claim about it;
- one wrong reading of a residual;
- the guard exclusion, which fails open and has no test;
- one acceptance item that needs a recorded decision.

## Basis

Read in order:
- AGENTS.md and CONTRIBUTING.md (sections 2, 6 and 6.1);
- docs/README.md;
- issue #649: body, the lane assignment (comment 5976977547), TAKEN and REVIEW READY;
- the PR #650 body;
- the authorities the page cites: `docs/design/AREA_BUDGET.md` (NFR-RES-01 gap, Tier 1), `docs/findings/234_PP_SHADOW_AREA_BASELINE.md`, `docs/reference/FR_NFR.md` (FR-CTRL-03), `syn/ooc/pp_resource_baseline.json` (`route-1x1`);
- the RTL lines the page cites;
- `git diff 241f9184..da0dbc37` and its five commits;
- the public evidence at `096998f8…/review-evidence/649-r1`: 73 of 73 files hash to its MANIFEST.json.

Scope of the diff: only `syn/resmap/` (8 files), `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md` and one row of `docs/findings/README.md`. There is no RTL, configuration, gate-baseline, workflow or existing-script change. Every commit message is one line with no trailers.

Prior public review findings on this PR: none existed when this round finished its own pass. The PR carries only the two review-start comments, no reviews and no review comments.

## Findings

### F1 MINOR (Tests, Docs): the map's tie set claims more checking than it does

**Where:**
- `syn/resmap/resmap_map.py:15-37`, `:47`, `:222-230` (`partition_ties`), `:265-267` (stray-owner check), `:490-504` (PLANTS);
- `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:59,64,71`;
- `syn/resmap/route_map.tcl:21-23`.

**Evidence:**

1. **The Partition tie can never fail on its own.** For the four LUT columns, the sharing adjustment is *defined* as parent minus its parts, so leaves plus adjustments equal the top by telescoping. For FF, RAMB and DSP, the sum is implied exactly once Ancestry passes. It is therefore not "two independent readings" (page :59, docstring :17).
   - The self-test has no Partition arm. The page says it "plants one wrong figure per tie" (:71, docstring :47, commit `3bc6528e1`).
   - Mutant `partition-off` survives 11/11 (`receipts/map_mutation.log`).
   - 20,000 random hierarchies gave 0 Partition failures with Ancestry clean (`receipts/partition_fuzz.log`).
2. **The stray-owner check has no arm.** This check (census cells owned by a parent that has no own row) can fail on real reports, but mutant `census-stray-off` survives. `census-total-off` and `names-sum-off` also survive; both are implied checks.
3. **A depth proof is described but not implemented.** The `route_map.tcl` header says the census "lets the parser prove the depth was not binding". The parser only tests `max depth < requested` (`resmap_map.py:309-311`) and never uses the census for depth.

**Impact:** The completion claim "one wrong figure per tie, each caught" is not true of the tie list as published. One of the seven ties is a derived identity, and one real check is untested.

**Required outcome:**
- Either state Partition as a derived identity and count six independent ties, or replace it with an independent reading.
- Add a planted arm for the stray-owner check.
- Make the `route_map.tcl` header describe the depth check that exists.

**Verification:** Re-run `scripts/mutate_map_selftest.py`. No surviving mutant should correspond to a check the page or docstring calls a tie, and the stray-owner mutant must be killed.

### F2 MINOR (Conformance, Docs): the LUT columns of the 175 blocks do not sum to the image

**Where:**
- page :52 ("The leaves partition the image."), :21 ("Every block, 175 in all, is tied"), :270 ("All 175 blocks") and the two partition tables (:175, :227);
- `syn/resmap/resmap_map.py:15` ("their sums are the image's totals").

**Evidence** (from the published `map.json`, `receipts/page_tables_check.log`):
- The 175 leaves sum to 51,123 LUT against the image's 50,767: +356, so the ranked table's "LUT % of image" column totals 100.70 %.
- 17 parents carry sharing adjustments totalling −356. The page shows two of them (image −39, `milan_datapath` −109). The other 15 (−208, including −156 inside `pp_shadow`) appear nowhere on the page.
- FF, RAMB36, RAMB18, DSP, CARRY4, slices and I/O-tile FFs do partition exactly.

**Impact:** Acceptance item 1 ("blocks sum to the routed totals, with the method stated") cannot be checked from the published page. A reader who sums the ranked table finds 356 LUTs the page does not reconcile, while the page says the leaves partition the image.

**Required outcome:**
- The page (generated, like its other tables) states the leaf LUT sum and every sharing adjustment, or their total by parent.
- "Partition" is qualified for the LUT columns in the page and the docstring.

**Verification:** Summing the ranked table's LUT column plus the published adjustments gives 50,767. `resmap_tables.py --page` still passes.

### F3 MINOR (Conformance, Docs): the processor's stream growth is slower than linear, not faster

**Where:** page :741 ("the residual (RMS 1,989) shows the growth is faster than linear"); the same reading at :626 ("the ACMP talker and the datapath's own logic grow faster than N").

**Evidence:** The reviewer reproduced `pp-ship`, `pp-si3`, `pp-si5` and `pp-si9`. Their `stat.json` digests are byte-equal to the receipts (`receipts/reproduction_digests.txt`), and refitting them with the committed code reproduces 5,885.97 LUT per unit, RMS 1,988.8 (`receipts/pp_stream_fit.log`).
- Per-stream increments are 10,780, then 5,632, then 5,229 LUT, and the residual signs are −,+,+,− at x = 1, 2, 4, 8. That is concave: the marginal stream gets cheaper, not dearer.
- The Yosys datapath fit shows the same shape (residuals −1,459, +2,432, −811 at N = 1, 2, 4; `receipts/refit_from_page.log`).
- The ACMP talker in the datapath grows +6,390 for the second stream, then about 2,166 per stream.
- The page's own Vivado reading (:576, :581) correctly says growth is "a little less than linear".

**Impact:** The most expensive parameter is described with the wrong curvature in the paragraph #640 will read for multi-stream scoping. The page also contradicts itself.

**Required outcome:** Say that the growth is sub-linear (a large first step, then a falling per-stream cost) in both places, consistent with the Vivado anchors.

**Verification:** The text agrees with the sign pattern of the published residuals.

### F4 MINOR (Docs): the findings index row gives the wrong point count

**Where:** `docs/findings/README.md:25` ("54 Yosys sweep points").

**Evidence:**
- `sweep_plan.json` has 59 points.
- The page (:996-1059) lists 59 runs, and the receipts hold 59 points.
- 54 is the plan's earlier size (the published executor handoff, section 3, "Plan: … 54 points" before "Final: 59 of 59").

**Impact:** The authoritative index states a figure that disagrees with the page and plan it indexes.

**Required outcome:** The row states 59 points, or 52 guard-clean plus 7 refused.

**Verification:** The row's count equals `len(sweep_plan.json["points"])`.

### F5 MINOR (Robustness, Tests): guard exclusion fails open on a missing record and has no test

**Where:**
- `syn/resmap/resmap_models.py:132-134` (`refusals` returns `[]` when no guard record exists), `:146`, `:233`;
- `resmap_models.py:350-352` (`unchecked` is computed and never enforced);
- `syn/resmap/resmap_tables.py:266-270` (renders "none" when nothing is refused);
- `resmap_models.py:361-387` (the self-test has no exclusion arm).

**Evidence** (`receipts/guard_exclusion_probe.log`):
- A point with no guard record is fitted exactly like a guard-clean point.
- A planted refusal is excluded.
- Removing the exclusion from both fits leaves `resmap_models.py --selftest` at PASS.

**Impact:** The sweep's defence against the sv2v guard gap the PR itself documents depends on an optional step. If `guards` is skipped or interrupted (`command_guards` has no per-point exception handling), refused shapes such as `streams-8` enter the stream fit, and the refusal table reads "none". The page's sentence "A point whose guard fires is … left out of every fit" holds only when every point was linted. At this head every fitted point was linted, so the published figures are not affected.

**Required outcome:**
- Models or tables refuse, or visibly flag, any point without a guard record.
- A self-test arm proves that a refused point leaves every fit and that a missing record is not treated as clean.

**Verification:** The exclusion-removal mutant is killed. A summary with one guard record deleted makes `resmap_models`/`resmap_tables` fail or flag that point.

### F6 MINOR (Conformance): the CPU, cache and L2 options are not costed, yet acceptance 2 is claimed met

**Where:** page :505-507, :789-790; PR body "Closes #649"; REVIEW READY "(2) … met".

**Evidence:**
- Issue #649's scope lists "the CPU and SoC configuration (core variant, caches, L2)". Acceptance 2 requires each parameter's per-unit cost "measured at three or more points or justified as linear".
- These options carry a recorded refusal (`milan_soc.py:3665-3670` refuses every variant), not a cost.
- The lane assignment says "STOP only if a measurement needs a change to the build recipe itself". The executor's published handoff decided not to treat this as a STOP. The interpretation is public, but no maintainer decision accepting it is recorded.

**Impact:** A listed acceptance item is closed by the executor's own reading of scope, which AGENTS.md section 2 says must be published as needing a decision.

**Required outcome:** One of:
- a public maintainer decision on #649 that the recorded refusal satisfies acceptance 2 for these options;
- the costs measured;
- the PR changed to "Relates to" for the unmeasured part.

**Verification:** That decision, or the measurement, is linked from the PR.

## RESIDUE

Each item is wording only. No figure, test, code or generated artifact changes.

| ID | Where | Exact fix |
|---|---|---|
| RES1 | page :21 | "Outside the processor, the gPTP plane…" → "In the rest of the datapath, the gPTP plane…". The CPU (3,524) and the SoC top's own logic (4,847) are outside the processor and larger than the CSR block. |
| RES2 | page :24 | "saves about 1,200 routed LUTs" → "could save up to about 1,200 routed LUTs", matching the opportunities section's "a saving is an estimate until a matched before-and-after route measures it". |
| RES3 | page :17 | "exit status, duration and log digest" → "exit status, duration and log or `stat.json` digest". The Yosys rows carry the `stat.json` digest. |
| RES4 | PR body, Status | "every table on the page equal to a fresh generation" → "every generated (`table:`-delimited) table on the page equal to a fresh generation". The tie, quantity, inventory, opportunity and run-receipt tables are hand-written. |

## SUGGESTION

- **S1.** `yosys_sweep.py run` reads sources from the working tree (through `dp_srcs.py` at `REPO`), while shapes come from the HEAD export. Record HEAD and a clean-tree check in each point receipt, or refuse a dirty checkout.
- **S2.** `fit()` stores `rank` but nothing asserts full rank. A missing stream point would silently produce a minimum-norm fit.
- **S3.** For #640, a talker-only or listener-only point would split the 3,828-LUT per-stream cost by direction. The issue's "talkers x listeners" admits it.
- **S4.** The published guard logs cover 58 of 59 points; `ship-8x8` is absent. The reviewer re-ran its lint with the pinned Verilator 5.050 and it is clean (`receipts/guards-ship-8x8.json`). Publish that record with the others.

## Lens results (exact head da0dbc37437b58ac591467cd1b8daa9c8896cf6e)

```text
[R466] MINOR Conformance - page :52/:21/:270, resmap_map.py:15 - 175-block LUT column sums to 51,123, 15 of 17 sharing adjustments unpublished (F2)
[R466] MINOR Conformance - page :741, :626 - stream growth called faster than linear; reproduced data are sub-linear (F3)
[R466] MINOR Conformance - page :505-507, :789-790; PR body Closes #649 - CPU/cache/L2 options uncosted, acceptance 2 claimed met without a decision (F6)
[R466] PASS RTL - diff 241f9184..da0dbc37 (no hdl/, configs/ or syn/ooc baseline file touched); syn/resmap/route_map.tcl and datapath_ooc.tcl (non-mutating reopen; OOC synth with AreaOptimized_high, ExploreArea, Synth 8-4445 promoted); hdl/milan/milan_datapath.sv:1636, :969-976; KL_pp_shadow binding in milan_datapath.sv (ACMP_SINKS_C/ACMP_SRC_C/AEM_* to the plan's KL_pp_shadow params); pp_pkg.sv:145 PP_N_CTRL_C=16; protocol_processor_top.sv:93-96, :1865 N_IF_P=1; KL_adp_engine.sv:67; ship-8x8 params against the tracked 8x8 builder argv (receipts/tracked_8x8_binding.txt)
[R466] MINOR Robustness - resmap_models.py:132-134,:350-352; resmap_tables.py:266-270 - missing guard record treated as clean (F5)
[R466] MINOR Tests - resmap_map.py:222-230,:265-267,:490-504 - Partition tie is an identity with no arm; stray-owner check unarmed (F1)
[R466] MINOR Tests - resmap_models.py:361-387 - guard exclusion untested; exclusion-removal mutant survives (F5)
[R466] MINOR Docs - page :59/:71, resmap_map.py:17,:47, route_map.tcl:21-23 - tie and depth-proof claims overstate the checks (F1)
[R466] MINOR Docs - page :52/:21, resmap_map.py:15 - "leaves partition the image" false for LUT columns (F2)
[R466] MINOR Docs - page :741, :626 - growth curvature misstated (F3)
[R466] MINOR Docs - docs/findings/README.md:25 - 54 points where the plan has 59 (F4)
```

Covered and found sound, by lens:

**Conformance.**
- Record tie from the published `map.json` against `pp_resource_baseline.json` `route-1x1`: LUT 50,767, FF 59,634, slices 15,832, RAMB36 79, RAMB18 27, DSP 14, CARRY4 3,506 all equal. All 51 processor scopes equal in LUT, FF, RAMB36, RAMB18, DSP and CARRY4.
- Route provenance: `4d81e10d..241f9184` changes only `.md` files and `syn/ooc/pp_resource_baseline.json`. The checkpoint digest `769a04bb733f2281` equals the #234 round-7 handoff on the `234-review-evidence` branch.
- Gap arithmetic: 50,767 − 38,040 = 12,727 (`AREA_BUDGET.md:113`). Ranks 4 to 6 come to 512 + 674 + 35 = 1,221 ≈ 1,200, which is 9.6 % of the gap. The redundancy sum is 7,100 LUT / 9,918 FF, 13.99 %.
- The eight-stream anchor is the tracked 8x8 configuration. Refused points are out of every published fit: 6 stream points; processor value lists without 32, 288, 512, 1152 or 235.

**Robustness.**
- Input refusals in `read_census`, `read_flat`, `requested_depth`, `patch_params` (exactly-once rule), `stage_roms` (ledger re-hash), `export_tree` (marker), `classify` (unpriced distributed RAM) and the Tcl property-length check. All were read and found sound.

**Tests.**
- The five self-tests pass at the head: map 11 of 11, sweep, soc, models, tables (`receipts/gates/*`).
- Map mutants killed: 9 of 13, covering ancestry additive and shared, flat, record totals and scopes, census per-leaf, I/O-tile split, slice-share normalisation and depth.

**Docs.**
- `docs_check` 0 findings; `check_doc_paths` OK; `gen_toc --check` and `--verify-anchors` OK; `check_em_dash --base 241f9184` 0 findings over 1,062 added lines (pinned renderer in a scratch venv); `git diff --check` clean.
- All 21 delimited table blocks on the page equal the published generated `tables.md`. `map-ranking` equals `blocks_ranked.md`; the three partition tables are verbatim in `partition.md` (`receipts/page_tables_check.log`).
- The page's 59 Yosys and 7 Vivado receipt rows equal `run-receipts.json` (`receipts/receipt_table_check.log`).
- Privacy: no home path, host, bench device or wiring in the diff. `J11.5` is a board connector already named in `FR_NFR.md` and `BUILDING.md`.

**Reproduction.**
- Seven Yosys points (`adp-if-1/2/4`, `pp-ship`, `pp-si3/5/9`) reproduce byte-equal `stat.json`.
- All nine variant shape headers reproduce byte-equal to the receipts. The builder accepts the 8x8 TDM8 variant at 235 names; the tracked 8x8 has 107.
- The committed `route_map.tcl` and `datapath_ooc.tcl` hash to the scripts the receipts record running.
- The Verilator 5.050 guard lint refuses `pp-names-235` and passes `ship-8x8`, `ship` and `pp-ship`.
- An independent least-squares refit of the page's tables reproduces every coefficient, RMS and largest residual. That covers the Vivado fit (3,827.9 / 2,911.1 / 1.5; RMS 393.6), the Yosys stream model, the processor parameters (3.45, 635.25, 215.18, 5,885.97, 58.61), the calibration ratios 0.447 / 0.422 / 0.402 / 0.355, route over OOC 0.9674, and the 4,739 / 4 = 1,185 slices claim (`receipts/refit_from_page.log`).

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F2, F3, F6) | issue #649 acceptance and lane comment; page map, sensitivity, opportunities; `pp_resource_baseline.json` route-1x1; `map.json`; `AREA_BUDGET.md`; `234_PP_SHADOW_AREA_BASELINE.md`; reproduced points | R466-1 (not clean) | da0dbc37437b58ac591467cd1b8daa9c8896cf6e |
| RTL | CLEAN | diff scope; `route_map.tcl`; `datapath_ooc.tcl`; `milan_datapath.sv:1636,:969-976` and the `KL_pp_shadow` instance; `pp_pkg.sv:145`; `protocol_processor_top.sv:93-96,:1865`; `KL_adp_engine.sv:67`; tracked 8x8 builder argv | R466-1 | da0dbc37437b58ac591467cd1b8daa9c8896cf6e |
| Robustness | UNCLEAN (F5) | `resmap_map.py`, `yosys_sweep.py`, `soc_sweep.py`, `resmap_models.py`, `resmap_tables.py` input and refusal paths; `guard_exclusion_probe` | R466-1 (not clean) | da0dbc37437b58ac591467cd1b8daa9c8896cf6e |
| Tests | UNCLEAN (F1, F5) | five self-tests; 13 map mutants; partition fuzz; models exclusion mutant; 7 Yosys reproductions; guard lint controls | R466-1 (not clean) | da0dbc37437b58ac591467cd1b8daa9c8896cf6e |
| Docs | UNCLEAN (F1, F2, F3, F4) | `649_RESOURCE_MAP_AND_SENSITIVITY.md`; `docs/findings/README.md:25`; script docstrings; PR body; docs gates | R466-1 (not clean) | da0dbc37437b58ac591467cd1b8daa9c8896cf6e |

## Real limits

- No Vivado was run. The routed checkpoint, the Vivado anchor reports, `summary.json`, `models.json` and the `route-map` directory are not in the public evidence. So:
  - the map tie and the table generation (`resmap_map.py map`, `resmap_tables.py --page`) were not re-executed end to end;
  - they were checked against the published `map.json`, `tables.md`, `blocks_ranked.md` and `partition.md`, and by reproducing 7 of 59 Yosys points and all 9 variant shapes.
- The Vivado refusal of `streams-8` (Synth 8-6058) is taken from the published handoff and run receipts. Its log is not published.
- The SoC exports and prices were not re-run, because they need the recipe's LiteX environment and SDK. The SoC tables were checked only against the published `tables.md`, `exports.json` and `prices.json`.
- Physical calibration was NOT RUN; nothing here is hardware evidence. Hosted checks were only read. Snapshot in `receipts/hosted_checks_snapshot.txt`: `rtl-fast`, `verilator-lint`, `yosys-elaboration`, four Yosys shards and Verilator shards 0 and 3 had succeeded; `docs-check`, `elaborate` and Verilator shards 1, 2 and 4 were in progress; the physical gPTP context was skipped. Acceptance of those checks is the manager's.

## Pending manager duties

- Rule on F6. File the two tooling findings: Yosys flows do not enforce sv2v-converted `$error` guards, and the builder accepts 235 names against the 128-record NAME block.
- Carry RES1 to RES4 to the residue checklist.
- Post, or delegate, the issue's summary comment on #229 and #640. Its draft is unposted in the executor's packet.
- Hosted, act and exact-head long-gate acceptance; the candidate merge on current dev; post-merge containment.
- Re-review after the fixes. F1, F2, F4 and F5 touch `syn/resmap/` or the page, so every lens they touch must be covered again at the new head.

R466-1 FINISHED
