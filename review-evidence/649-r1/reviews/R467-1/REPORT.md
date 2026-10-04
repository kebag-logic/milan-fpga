[R467] NEGATIVE - exact head da0dbc37437b58ac591467cd1b8daa9c8896cf6e

# R467-1: external independent review of issue #649 / PR #650

- Exact head: `da0dbc37437b58ac591467cd1b8daa9c8896cf6e`, tree `4ab5c8fffcffee036f0788d2302ee7d7d9a06c8c`; source base and live dev `241f91845230ae410506dffb16b71937127fd175`.
- Role: external cleared-context reviewer. Reconstructed from AGENTS.md, CONTRIBUTING.md, docs/README.md, issue #649 (body and the lane, TAKEN and REVIEW READY comments), the cited authorities (`docs/design/AREA_BUDGET.md`, `docs/findings/234_PP_SHADOW_AREA_BASELINE.md`, `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`, `syn/ooc/pp_resource_baseline.json`), the diff `241f9184..da0dbc37`, its five commits, and the public evidence tree `review-evidence/649-r1` at `096998f8`.
- Verdict: NEGATIVE. Seven MINOR findings are open. F1 to F4 came from my independent pass. F5 to F7 are prior public findings (round R466-1, published during this round) that I verified independently at this head and retain. The measured figures reproduce: every number I re-derived or re-ran matches the page. The open findings are about what the page claims its checks prove, one misread curvature, figure consistency, one acceptance item, a fail-open guard path, and evidence a cold reviewer can re-run.

## Scope check (measurement only)

`git diff --stat 241f9184..da0dbc37` touches exactly 10 files: `syn/resmap/` (8 new files), `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md` (new) and one added row in `docs/findings/README.md`. No RTL, configuration, workflow, gate baseline, existing script or gitlink changes. Between the routed commit `4d81e10d` and `241f9184`, only documentation and `syn/ooc/pp_resource_baseline.json` change (`git diff --name-only`), so the reused route is dev `241f9184`'s image, as the page says.

## Findings

### F1 MINOR - Conformance, Tests, Docs - the map's "seven independent ties" overstate what is tied

- Where: `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:59`, `:64`, `:71`, `:21` ("Every block, 175 in all, is tied to the recorded route"); `docs/findings/README.md:25` ("each tied to the `route-1x1` record"); `syn/resmap/resmap_map.py:17-18`, `:222-230`; `syn/resmap/route_map.tcl:22-24`.
- Evidence:
  - The Partition tie cannot fail. `ancestry_ties` sets each parent's LUT-column adjustment to exactly `parent - sum(children)` (`resmap_map.py:210`, `:218`), so "leaves plus every adjustment equals the top" is a telescoping identity, not a second reading. The FF, RAMB and DSP columns are already held exactly by Ancestry. Probe `scripts/probe_partition.py` (`receipts/probe_partition.log`): with `partition_ties` stubbed to return nothing, the self-test still passes 11 of 11 arms (arm A); on 2,000 random trees the LUT-column partition never fails (arm C). No self-test arm targets it. So the page's "plants one wrong figure per tie" and "each compares two independent readings" are false for this tie.
  - A leaf's LUT figure is tied only when the leaf is itself a recorded processor scope: 46 of the 175 leaves (independent count over the published `map.json`). For the other 129, a wrong LUT figure only makes the parent's sharing adjustment more negative, and that is accepted. Probe arm B: inflating a non-processor leaf from 2 to 7 LUTs in the self-test fixture ties clean, adjustment -6. So "Every block, 175 in all, is tied to the recorded route" overstates the check. Only the top, the 51 recorded scopes, and the FF, RAMB, DSP and CARRY4 census columns are tied.
  - `route_map.tcl:22-24` says the census "lets the parser prove the depth was not binding". `resmap_map.py:309-311` only compares the deepest reported row with the requested depth and does not use the census for it.
  - The real stray-owner check (`resmap_map.py:265-267`: census cells owned by a row that is not a leaf) has no self-test arm. With it disabled, the self-test still passes 11 of 11 (`receipts/probe_stray_owner.log`). This point was raised in R466-1 F1 and is verified here.
  - No published figure is wrong. My independent re-check of the published `map.json` against the record (`scripts/check_map_json.py`, `receipts/check_map_json.log`) passes every column, all 51 scopes and the slice shares. The finding is that the stated method, which acceptance item 1 requires, claims checks that do not exist.
- Impact: a reader of #640 scoping, or a future reuse of `resmap_map.py`, trusts a per-block LUT tie that does not exist for 129 blocks. The self-test's "one arm per tie" suggests coverage the tie set does not have.
- Required outcome: either make the leaf LUT columns independently checked (for example, bound or explain each sharing adjustment, or tie leaf LUTs to a second reading), or state exactly what is tied. That means: Partition is an identity given Ancestry; leaf LUT figures outside the recorded scopes are bounded only by the sign of their parent's adjustment; the self-test claim is corrected; the depth comment matches the implemented check. The page, the README row, the PR body and the two script headers must agree.
- Verification: rerun `scripts/probe_partition.py` against the new head. Either arm B is caught, or the page, README, PR and docstrings carry the stated limitation, and every tie named on the page has a self-test arm that fails when that tie is removed.

### F2 MINOR - Docs - figures inconsistent between artifacts

- Where: `docs/findings/README.md:25` says "54 Yosys sweep points". The page's run receipts (`:1000-1059`), `syn/resmap/sweep_plan.json` and the published `run-receipts.json` all hold 59 (independent count, `receipts/check_receipts.log`). `syn/resmap/route_map.tcl:59` says indexed census writing "measured about 35 lines a second, an hour of held lock"; page `:993` says "about 67 lines a second" for the same first attempt.
- Impact: the findings index misstates the sweep's size, and two committed artifacts give different measured rates for one event.
- Required outcome: the README row says 59 points (or explains what 54 counts). One measured rate, tied to its receipt, appears wherever the event is described, or an unmeasured rate is dropped.
- Verification: grep the head for both figures; each matches the receipts.

### F3 MINOR - Conformance, Docs - acceptance item 2 reported met for SoC parameters that carry no measured cost

- Where: issue #649 scope 2 ("the CPU and SoC configuration (core variant, caches, L2)") and acceptance 2 ("Each parameter's per-unit cost is measured at three or more points or justified as linear"). Page `:788-790` ("Each refusal is the measurement"). REVIEW READY comment 5978158007 ("(2) ... met"). PR body "Closes #649".
- Evidence: all six CPU, cache and L2 variants are refused by `milan_soc.py:3666-3669` under the baremetal profile, as recorded in `exports.json` and the soc-outcomes table. No cost is measured for any of them. The lane assignment (comment 5976977547) says "STOP only if a measurement needs a change to the build recipe itself", and the page says pricing these "needs a change to the build recipe". The executor recorded the refusals and reported the acceptance item met, rather than publishing the conflict for a decision (AGENTS.md section 2: "publish the conflict and mark the task as needing a decision rather than choosing an interpretation privately"; section 4: acceptance criteria are frozen).
- Impact: the issue closes with an in-scope parameter class unpriced, and with an executor reinterpretation of a frozen acceptance criterion that nobody else made public.
- Required outcome: one of the following. (a) A public maintainer decision on #649 that the recorded refusals satisfy acceptance 2 for the CPU, cache and L2 options, or that those options move to a named follow-up issue (with the PR's acceptance statement matching it). (b) A measurement that does not change the recipe, for example pricing the alternative CPU netlists out of context.
- Verification: the decision or follow-up link on #649, and the PR acceptance text agreeing with it.

### F4 MINOR - Tests, Docs - the table-equality check and the route-map tie have no re-runnable public receipt

- Where: PR body "How to validate" and Status ("every table on the page equal to a fresh generation"); page `:1061` ("The executor's packet holds every digest in full"); evidence tree `review-evidence/649-r1`.
- Evidence: the published evidence carries the outputs (`tables.md`, `map.json`, `blocks_ranked.*`, `exports.json`, `prices.json`, `run-receipts.json`). It has no log of `resmap_map.py map` or `resmap_tables.py --page`. It also has none of their small inputs: `map_hierarchy.rpt` (46,400 B), `map_utilization.rpt` (13,314 B), the eight Vivado `*_hierarchy.rpt` (about 25 KB each), `summary.json`, `models.json`, or per-point `guards.json`. Only their digests are published. The page names "the executor's packet", which a cold reader of dev cannot locate. I could verify that every page table equals the published `tables.md` (21 of 21, `receipts/compare_tables.log`), and I reproduced 19 of 59 Yosys points byte for byte. I could not re-run the generation the claim is about.
- Impact: acceptance 4 ("receipts ... published") and AGENTS.md section 1 ("all useful project state must be public") are met only as digests. The headline check of the page cannot be re-run by a cold reviewer.
- Required outcome: the small inputs above and the two check logs are published at a stable public location, and the page or PR names it, so that `resmap_map.py map` and `resmap_tables.py --page` can be re-run by a cold reviewer.
- Verification: from the published inputs, `resmap_map.py map` prints `TIED: 175 blocks, depth 5; ...`, and `resmap_tables.py ... --page` prints "every table equals a fresh generation" with exit 0.

### Prior public findings (R466-1, comment 5978523295): resolution at this head

I read R466-1 only after this report's verdict and ledger were first written (they then carried F1 to F4, with the guard fail-open as a suggestion). Each of its findings is resolved below against my own evidence at this head.

| R466-1 item | Disposition here | My evidence |
|---|---|---|
| F1 MINOR (tie set overclaims; stray-owner unarmed; depth comment) | Retained, merged into F1 | `receipts/probe_partition.log`, `receipts/probe_stray_owner.log` |
| F2 MINOR (175 leaf LUTs sum to 51,123; 15 of 17 adjustments unpublished) | Retained as F5 | `receipts/check_map_json.log` (17 non-zero adjustments, sum -356) |
| F3 MINOR (stream growth called faster than linear; data are sub-linear) | Retained as F6 | `receipts/curvature_check.log` |
| F4 MINOR (README "54" points) | Retained, merged into F2 | `receipts/check_receipts.log` |
| F5 MINOR (guard exclusion fails open; no test) | Retained as F7. My pass had rated it a suggestion. I raise it to MINOR because an interrupted `guards` run (no per-point exception handling at `yosys_sweep.py:470`) or a skipped one silently changes the published models | `receipts/probe_selftests.log` |
| F6 MINOR (CPU, cache, L2 uncosted; acceptance 2 claimed met) | Retained, same as F3 | `exports.json`, `milan_soc.py:3666-3669` |
| RES1, RES2 | Retained (same as RES-1, RES-3 below) | page `:21`, `:24` |
| RES3 (page `:17` "log digest"; Yosys rows carry `stat.json` digests) | Retained as RES-4 | page `:17`, `:1000-1059` |
| RES4 (PR Status "every table" means the generated tables) | Retained as RES-5 | the hand-written tables at page `:61-69` (ties), `:150-158` (quantities), `:460-510` (inventory), `:946-965` (opportunities), `:983-1059` (receipts) |
| S1 to S3 | Retained as suggestions (S2 to S4 below) | `yosys_sweep.py:145-157` (sources read from the working tree); `resmap_models.py:120-129` (rank not asserted) |
| S4 (published guard logs omit `ship-8x8`) | Retained as a suggestion. My 59-point reproduction lints `ship-8x8` clean | `receipts/repro-guards-summary.log` |

### F5 MINOR - Conformance, Docs - the 175 blocks' LUT columns do not partition the image, and most adjustments are unpublished

- Where: page `:52` ("The leaves partition the image."), `:21`, `:270` ("All 175 blocks"), partition tables `:175`, `:227`; `resmap_map.py:15` ("their sums are the image's totals").
- Evidence: over the published `map.json`, the 175 leaves sum to 51,123 LUT against the image's 50,767 (+356), so the ranked table's "LUT % of image" column totals about 100.7 %. 17 parents carry sharing adjustments summing to -356. The page shows two of them (image -39, `milan_datapath` -109); the other 15 appear nowhere on it. FF, RAMB36, RAMB18, DSP, CARRY4, slices and I/O-tile FFs do partition exactly (`receipts/check_map_json.log`).
- Impact: acceptance 1 ("blocks sum to the routed totals, with the method stated") cannot be checked from the page. A reader summing the ranked table finds 356 LUTs the page does not reconcile.
- Required outcome: the page states every sharing adjustment, or their totals by parent, as a generated table, and qualifies "partition" for the LUT columns in the page and in the docstring.
- Verification: the ranked LUT column plus the published adjustments sums to 50,767, and `resmap_tables.py --page` still passes.

### F6 MINOR - Conformance, Docs - stream growth is described as faster than linear; the measured growth is sub-linear

- Where: page `:626` ("the ACMP talker and the datapath's own logic grow faster than N") and `:741` ("the residual (RMS 1,989) shows the growth is faster than linear").
- Evidence: processor stream ports at x = 1, 2, 4, 8 give 57,386 / 68,166 / 79,430 / 100,345 Yosys LUT (three reproduced byte for byte here, `pp-si5` from the page's +22,044). The per-unit increments are 10,780, then 5,632, then 5,229, and the linear-fit residuals run -2,759, +2,135, +1,627, -1,002 (slope 5,885.97, RMS 1,988.8, equal to the page). That is concave. For the datapath at N = 1, 2, 4: 16,980, then 11,468 per stream. The ACMP talker adds 6,390 for the second stream, then 2,166 per stream. The datapath's own logic adds 5,046, then 4,082 per stream (`receipts/curvature_check.log`). The page's own Vivado reading (`:576`, "a little less than linear") agrees with the data, not with `:626` or `:741`.
- Impact: the most expensive parameter's scaling is described backwards in the paragraphs #640 will read for multi-stream scoping, and the page contradicts itself.
- Required outcome: both places say the growth is sub-linear (a large first step, then a falling per-stream cost), consistent with the residual signs.
- Verification: the text agrees with the sign pattern of the published residuals.

### F7 MINOR - Robustness, Tests - guard exclusion fails open; claim-critical paths lack self-test arms

- Where: `resmap_models.py:132-134`, `:146`, `:233`, `:350-352`; `yosys_sweep.py:462-474`; `resmap_tables.py:266-270`; self-tests `resmap_models.py:361-387`, `resmap_tables.py:276-298`; page check `resmap_tables.py:326`.
- Evidence: `refusals()` returns an empty list for a point with no `guards.json`, or whose lint hit a hard Verilator error, so the point is fitted as clean. `models.json` lists "unchecked" points, but nothing refuses or flags them, and the refusal table would read "none". `command_guards` calls `future.result()` with no per-point exception handling, so one failing point aborts the command and leaves other points without a record. Probes (`receipts/probe_selftests.log`): removing the refusal exclusion from the stream fit or from the processor fit, or forcing the `--page` comparison to report "equal", all leave the self-tests passing. At this head every point was linted (my 59-point reproduction finds the same seven refusals), so the published figures are unaffected.
- Impact: the defence against the sv2v guard gap the PR documents depends on a step whose absence is silent. A reproduction without the guard step publishes fits that include refused shapes such as `streams-8`.
- Required outcome: models or tables refuse, or visibly flag, any point without a clean guard record, and self-test arms prove that a refused point leaves every fit, that a missing record is not treated as clean, and that a stale page fails the check.
- Verification: the three probe mutants in `scripts/probe_selftests.py` are caught, and a summary with one guard record deleted makes `resmap_models.py` or `resmap_tables.py` fail or flag that point.

### SUGGESTIONS

- S2 (from R466-1 S1): `yosys_sweep.py run` reads sources through `dp_srcs.py` at the working tree while the shapes come from the HEAD export. Record HEAD and a clean-tree check in each receipt, or refuse a dirty checkout.
- S3 (from R466-1 S2): `fit()` records `rank` but nothing asserts full rank; a missing point would silently yield a minimum-norm fit.
- S4 (from R466-1 S3): a talker-only or listener-only point would split the per-stream cost by direction for #640.
- S5 (from R466-1 S4): publish the `ship-8x8` guard record with the others (clean in my reproduction).

### RESIDUE (wording only; exact fixes)

- RES-1, page `:21`: "Outside the processor, the gPTP plane (5,004) and the CSR block (3,073) are the two large blocks" should read "In the rest of the datapath, the gPTP plane (5,004) and the CSR block (3,073) are the two large blocks". The SoC top's own logic (4,847) and the CPU (3,524) are also outside the processor.
- RES-2, page `:237`: "Its recorded route lists 51 scopes inside `pp_shadow`" should read "Its recorded route lists 51 scopes, `pp_shadow` itself and 50 inside it". The record's 51 include `wrapper`.
- RES-3, page `:24`: "saves about 1,200 routed LUTs" should read "saves up to about 1,200 routed LUTs", matching the opportunities table's "up to the routed block" and the page's "A saving is an estimate".
- RES-4, page `:17`: "exit status, duration and log digest" should read "exit status, duration and log or `stat.json` digest".
- RES-5, PR body Status: "every table on the page equal to a fresh generation" should read "every generated (`table:`-delimited) table on the page equal to a fresh generation".

## What was verified (independent evidence, all at the exact head)

| Claim (focus item) | Result | Receipt |
|---|---|---|
| (1) Map tied to route-1x1: 50,767 LUT / 59,634 FF / 15,832 slices, CARRY4 3,506, RAMB36 79, RAMB18 27, DSP 14; 51 processor scopes equal | Holds on the published `map.json`: 175 leaves, depth 5, all 51 scopes equal in every recorded column, slice shares sum to 15,832, ancestry exact in every additive column, every LUT adjustment non-positive (17 non-zero, sum -356) | `receipts/check_map_json.log` |
| (1) Self-test plants one wrong figure per tie | 11 of 11 arms pass, but Partition has no arm and cannot fail (F1) | `receipts/selftest-resmap_map.log`, `receipts/probe_partition.log` |
| (1) Route reused is #638's round 7 | Checkpoint `769a04bb733f2281...` appears as `alinx_ax7101_route.dcp` in `review-evidence/234-r1/author-r7/receipts/run-receipts.json` on `234-review-evidence` | `receipts/route_dcp_digest_in_638_r7.log` |
| (2) Every point's inputs and ROM/shape digests recorded | 59 of 59 receipts carry design, shape-header (datapath), rewritten-source and ROM digests. Every ROM digest is in `syn/yosys/rom_digests.tsv`. All 26 datapath shape headers re-generated by the builder from a scratch export hash equal to the receipts | `receipts/check_receipts2.log`, `receipts/check_shape_digests.log`, `receipts/repro-shapes.log`, `receipts/repro-roms.log` |
| (2) Verilator guard check refuses 7 of 59 | Reproduced with the pinned Verilator 5.050 over all 59 points: the same 7 points, the same messages, no hard errors | `receipts/repro-guards.log`, `receipts/repro-guards-summary.log` |
| (2) Refused points out of every fit | Fit data rows (yosys-stream-data, processor-parameters values) exclude all seven. The marginal tables list refused points labelled "refused by a guard", which is not a fit. The exclusion fails open and has no self-test arm (F7) | page tables; `receipts/probe_selftests.log` |
| (2) Eight-stream anchor is the tracked 8x8 configuration | The builder's argv for `endstation_ax7101_8x8` differs from the shipping 1x1 argv in exactly the plan's `ship-8x8` changes (tdm32, render off, loopback off, probes off, taps off, 8 streams) | `receipts/anchor_8x8_argv_diff.log` |
| Yosys figures | 19 points re-run (3 ADP, 14 processor, `no-rxfilt`, `chans-2`): every `stat.json` byte-identical to the receipt digest. The recomputed marginals equal the page (`pp-ctrl-4` -6,818, `pp-si9` +42,959, `adp-if-2` +239, `no-rxfilt` -786 / -1,691, `chans-2` 97,577 ...) | `receipts/repro-digests.log`, `receipts/repro-summary.log` |
| (3) Per-stream 3,828 LUT / 2,911 FF / 1.5 BRAM, residuals | Least squares from the page's three anchors recomputed by hand: 3,827.9, 2,911.1 and 1.536, fixed 35.25 BRAM. Second stream 4,739, third and fourth 3,463.5 each | page arithmetic, re-derived |
| (3) Calibration 2.2 to 2.8x; out of context within 3.3 % of route | 97,607/43,622 = 2.24 and 170,266/60,454 = 2.82. Route over opt 42,200/43,622 = 0.967. Per block above 1,000 LUTs, 0.879 to 1.062 | page tables, re-derived |
| (3) Stream growth curvature | Sub-linear in Vivado, Yosys datapath and Yosys processor alike; the page's "faster than linear" at `:626` and `:741` is wrong (F6) | `receipts/curvature_check.log` |
| (3) Channels and TDM width free | FF identical across C = 2, 4, 8 at N = 1 and across C = 2, 8 at N = 4. LUT moves 30 and 779, inside the 1,227 RMS. TDM 8/16/32 with render pruned: within 7 LUT and 6 FF. The render-lane coupling is cited correctly (`milan_datapath.sv:969-976`) | page tables, RTL |
| (4) Opportunities: function cost each; second port measured only; ~1,200 and 12,727 | Every row names its function cost. Second port: a sum of 15 routed blocks = 7,100 LUT / 9,918 FF (14.0 %), nothing proposed. 512 + 674 + 35 = 1,221 ≈ 1,200 (9.6 % of the gap). 50,767 - 0.6 × 63,400 = 12,727 (`AREA_BUDGET.md:113`). #234 levers 1 to 5 at 3,600 LUT / 5,600 FF (`234_...:452`) | re-derived |
| (5) Page tables equal a fresh generation | 21 of 21 page blocks byte-equal to the published `tables.md`. The generation from inputs cannot be re-run from public evidence (F4) | `receipts/compare_tables.log` |
| (5) Self-tests run as the body states | All five exit 0: map "11 of 11 arms passed", sweep "PASS (0 problems)", soc, models and tables "PASS" | `receipts/selftest-*.log`, `receipts/selftest-rc.txt` |
| Run-receipt tables | 59 point rows match `run-receipts.json` (digest, seconds; 247.9 min total). Five anchor rows match rc, minutes, log digest and bytes | `receipts/check_receipts.log`, `receipts/check_receipts2.log` |
| Docs gates | `docs_check.py` 0 findings; `check_em_dash.py --base 241f9184` 0 over 1,062 added lines; `gen_toc.py --check` and `--verify-anchors` OK; `check_doc_paths.py` OK | `receipts/gate-*.log`, `receipts/gates-rc.txt` (em dash and TOC with the pinned renderer) |
| Privacy | No home paths, hostnames, addresses, serials or bench vendor names in the page, README row or scripts. `J11` is the board header already named in tracked configuration and docs | grep in this report's session; `docs_check.py` scrub 23/23 |

## Lens ledger (reviewer-owned)

First written before the R466-1 findings were read (Conformance F1, F3; Robustness CLEAN; Tests F1, F4; Docs F1 to F4). Updated after resolving them at this head as above.

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F3, F5, F6) | issue #649 scope and acceptance 1 to 4; lane comment 5976977547; page Method, Whole-image map, Sensitivity, Opportunities; `sweep_plan.json`; `exports.json`; `milan_soc.py:3666-3669`; `AREA_BUDGET.md:105-137`; `234_...:436-462`; `pp_resource_baseline.json` route-1x1 record | R467-1 | da0dbc37437b58ac591467cd1b8daa9c8896cf6e |
| RTL | CLEAN | diff has no RTL (10 files listed above); RTL facts the page relies on checked: `milan_datapath.sv:941` (TDM key lane 8), `:960-976` (render guards), `:1636` (talker-source guard), `:5596`/`:5940` (CRF blocks unconditional), `:6188` (LPF generate); `KL_nvm_backend.sv:288-290` (N_NAME_P guard); `protocol_processor_top.sv:1865` (`N_IF_P` bound to 1); gitlinks unchanged | R467-1 | da0dbc37437b58ac591467cd1b8daa9c8896cf6e |
| Robustness | UNCLEAN (F7) | `resmap_map.py` input refusals (`:101-133`, `:153-160`, `:303-311`); `yosys_sweep.py` exact-once rewrites (`:124-142`, `:276-290`), ROM re-hash (`:188-206`), export identity (`:233-258`), shape-source check (`:160-170`); `datapath_ooc.tcl` key refusals and `Synth 8-4445` promotion; `route_map.tcl` list-length check; `soc_sweep.py` expectation check (`:122-125`); guard fail-open (`resmap_models.py:132-153`, `yosys_sweep.py:462-474`) | R467-1 | da0dbc37437b58ac591467cd1b8daa9c8896cf6e |
| Tests | UNCLEAN (F1, F4, F7) | five self-tests run; mutation probes (`probe_partition.py`, `probe_selftests.py`, stray-owner probe); 19-point Yosys reproduction; 59-point guard reproduction; shape and ROM digest reproduction | R467-1 | da0dbc37437b58ac591467cd1b8daa9c8896cf6e |
| Docs | UNCLEAN (F1, F2, F3, F4, F5, F6) | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md` (all 1,061 lines); `docs/findings/README.md:25`; script headers; PR #650 body; docs gates above | R467-1 | da0dbc37437b58ac591467cd1b8daa9c8896cf6e |

## Real limits

- Vivado was not run: the route reopen, the four anchors and the refused 8x8 TDM8 anchor are taken from the published digests and the page. The route reports and Vivado hierarchy reports are not public (F4), so the route-map tie and the Vivado tables were checked only on the published outputs (`map.json`, `tables.md`) and by arithmetic.
- 40 of 59 Yosys points were not re-run (the remaining 25 datapath points need about 4 to 20 minutes each). The anchors' flattened runs were not re-run.
- The SoC exports and prices were not reproduced: that needs the recipe's LiteX environment and SDK.
- Physical calibration NOT RUN. The page makes no hardware claim, and none was tested.
- Hosted evidence was inspected only: at the exact head, `rtl-fast` and most contexts succeeded, `Verilator shard 1/5` and `4/5` were in progress, and `Physical gPTP` was skipped. Hosted and local-replica acceptance belongs to the manager.

## Pending manager duties

- File the two tooling findings as issues: Yosys flows ignore sv2v-converted elaboration guards (confirmed here by re-running `pp-ctrl-32` and `pp-names-235` in Yosys with rc 0; the receipts show rc 0 for the other five); the builder accepts `rm_ax7101_8x8_tdm8` with `AEM_NAME_ENTRIES_C = 235` against the backend's 128 (confirmed here: builder rc 0).
- The #229 and #640 summary comment is not posted (the PR says so).
- F4 can be resolved by publishing the inputs and check logs from the executor's packet.
- Build and validate the current-dev candidate at the merge turn; hosted exact-head contexts still in progress.
- Carry RES-1 to RES-3 to the residue checklist.

## Clone restoration

After the probes, the clone is at the exact head: `git diff` and the index are clean; the index tree is `4ab5c8ff...`; all 1,008 tracked blobs re-hash raw to their recorded ids with matching modes; the three required gitlinks are at their pins (`gptp-processor 5dce647a`, `protocol-processor 631eeb34`, `third_party/verilog-axis 48ff7a7e`; `external` uninitialized, as at start). The Python caches my runs created were removed (`receipts/restore-check.log`). Every disposable tree is under `scratch/`.

R467-1 FINISHED
