[R447] NEGATIVE - exact head 2a765a6c3868400c20ede2e357876f28a811c811

# R447-1 external review: issue #234 / PR #638

Head `2a765a6c3868400c20ede2e357876f28a811c811`, tree `09d124d8f8ec3598bfc74572c97a0dfec5273ec4`, base dev `1269cdafb4bb964c757baae0f0c5a932d43f540b`.
Five one-line commits, 11 files, no RTL, no gitlink change.
Verdict NEGATIVE: four open MINOR findings (Robustness, Tests, Docs).
Conformance and RTL are covered clean.
The measured figures, the ranking and the CI wiring hold up; the gate's own refusal and test surface does not yet meet the bar this round was asked to apply.

## Inputs, in order

AGENTS.md, CONTRIBUTING.md, docs/README.md; issue #234 body, the lane assignment (5966260488), the takeover (5966304381), REVIEW READY (5967818534) and the rulings (5967852698); NFR-RES-01 (`docs/reference/FR_NFR.md:317`), BUILDING.md section 5, the #231 baseline page and recipe; `git diff 1269cdaf..2a765a6c` and its history; the public packet at `43ad8362` `review-evidence/234-r1` (records, rankings, cones, mapping TSVs, receipts); hosted exact-head check runs.
No other reviewer's report was read.
PR #638 carries no earlier review findings: its only comments are the withdrawn start and the R446-1 / R447-1 start notices, so nothing is to be resolved or retained.

## Findings

```text
[R447] MINOR Robustness, Tests - syn/ooc/pp_resource_gate.py:219, :225, :243, :253, :283, :292, :311 - malformed baseline entries and a wrong-shape image manifest exit 1 by traceback
Requirement/evidence: the gate's contract (pp_resource_gate.py:21-22; PP_SHADOW_BASELINE_RECIPE.md:458) reserves 1 for a material regression and gives 2 for not comparable or unreadable; check-baseline returns 2 for a defective baseline (:315). receipts/probe_cli.log, through the CLI: baseline_images.json shaped ["a"] -> exit 1 (TypeError, not in the :219 except tuple); baseline endpoint without "record" -> exit 1 (KeyError, :225); baseline file not JSON -> exit 1 (:311); gated figure without tolerance -> exit 1 (KeyError, :253); ceiling naming no figure -> exit 1 (KeyError, :243); check-baseline with the ooc-1x1 record removed -> exit 1 (KeyError, :283) instead of its documented problem report and 2.
Impact: fail-closed (never a false pass), but an unreadable measurement or broken baseline is reported with the regression status; a bank or CI reader that keys on 1 versus 2 misroutes it, against the issue's scope item that CI output distinguish mapping changes from true regressions.
Required change: every malformed or missing baseline entry and every unreadable measurement exits with a documented non-regression status (2) and a named reason; check-baseline lists a missing record or an unknown ceiling figure as a problem; self-test arms drive these through the CLI.
Verification: probe_cli.py reports 54 of 54 as documented; a mutant removing the new guard is killed.
```

```text
[R447] MINOR Tests - syn/ooc/pp_resource_gate_selftest.py:143-153 and :203-238, syn/ooc/pp_resource_gate_mutants.py:13-52 - the self-test does not detect several disabled checks
Requirement/evidence: AGENTS section 6 Tests lens (each test can fail for the defect it claims; boundary behaviour). receipts/extra_mutants.log: control passes; 14 of 18 reviewer mutants survive the shipped 51-arm self-test. Disabled checks that survive: (a) RAMB36 removed from GATED["ooc"] and (b) DSP removed from GATED["ooc"] (AREA_BUDGET.md:145-146 documents +0 each for both standalone endpoints; no OOC arm plants RAMB36 or DSP); (c) main's refusal path (:322-324) returning 0 instead of 2, so the CLI the bank runs would pass every unreadable, missing or not-comparable measurement; (d) main reading every directory as "route" instead of kind_of() (:321). Boundary mutants that survive: timing floor "<" -> "<=" (BUILDING.md section 5 says "at least"), ceiling ">" -> ">=", timing fall ">" -> ">=". The shipped code is correct at all of these points (probe_cli.log: WHS 0.000 passes, WNS fall of exactly 0.25 passes, 121.5 tiles passes, 122 fails, standalone RAMB36/DSP +1 exit 1).
Impact: the hosted rtl-fast run is the only automated protection of the gate's logic; an edit that disables any of (a)-(d) stays green there, and the bank would then accept a standalone block-RAM or DSP growth, or exit 0 on an unreadable measurement.
Required change: arms that fail when each of (a)-(d) is removed and when the floor and ceiling boundaries move, and matching entries in the mutant campaign.
Verification: extra_mutants.py reports those mutants KILLED; the shipped campaign still passes its control.
```

```text
[R447] MINOR Robustness - syn/ooc/pp_resource_gate.py:207-220 and :48 - the route endpoint never reads routing completion
Requirement/evidence: the route endpoint is documented as "the fit itself" (AREA_BUDGET.md:161) and judges the shipping route for criterion 4; the recipe omits bitstream generation (PP_SHADOW_BASELINE_RECIPE.md:126), whose checks are the flow's usual refusal of unrouted nets; each route directory holds the build's alinx_ax7101_route_status.rpt (run-receipts.json:44, :100), and completion was checked by hand (findings :82). receipts/probe_route_status.log: the same measurement exits 0 "RESULT: PASS" with a clean status report and with one reporting 37 unrouted nets; the gate has no reference to route status.
Impact: at 99.78 % slices (35 free) an incomplete route is a plausible next failure; a candidate whose route does not complete passes the gate when its counts and its timing summary sit within tolerance, and only a later bitstream build refuses it.
Required change: the route endpoint refuses, with a documented status, a measurement whose route status reports unrouted nets or routing errors or is missing, with a planted arm.
Verification: probe_route_status.py exits non-zero for the 37-net case and 0 for the clean case.
```

```text
[R447] MINOR Docs - docs/findings/234_PP_SHADOW_AREA_BASELINE.md:134-135, docs/design/AREA_BUDGET.md:156 - the "blocks B did not change" movement figures mix partitions
Requirement/evidence: receipts/partition_check.log, from the published A/B 1x1 records, u_pp/u_nvm_port excluded: leaf scopes give net +101 LUT, absolute 365 LUT, net -11 FF; u_pp's direct children give net +95 LUT, absolute 309 LUT, net -12 FF; the complete own-logic partition gives net +79 LUT, absolute 391, net +93 FF. The findings page pairs "net 101" with "sum to 309"; AREA_BUDGET pairs "net 101 LUTs" with "95 FFs", which only appears when the processor top's own +107 FFs (findings :136) are added, a scope the LUT figure leaves out.
Impact: the tolerance rationale (AREA_BUDGET.md:153-159) quotes figures no single reading of the published records reproduces. The 250-LUT tolerance still covers every reading, so no verdict changes.
Required change: name one partition and give its net and absolute LUT and FF movement in both pages, with the processor top's own +107 FFs stated separately if kept.
Verification: partition_check.py output equals the prose in both pages.
```

```text
[R447] RESIDUE Docs - docs/design/AREA_BUDGET.md:114, :182, :185 - wording predates ruling 5967852698
Exact fix: :114 "proposed reserve: 13.5 tiles (10 %)" -> "reserve: 13.5 tiles (10 %), the 121.5-tile ceiling, accepted (manager ruling)". :182 "The proposal is one run per merge candidate that moves the processor pin, `KL_pp_shadow`, the shipping configuration or the build flow." -> "The manager's merge bank runs it for every PR that changes RTL, the processor pin or the build recipe (manager ruling)." :185 "Making it part of the merge bar is an owner decision; CONTRIBUTING is unchanged here." -> "That bank run is the local half of #234's fourth criterion (manager ruling); CONTRIBUTING is unchanged here."
```

```text
[R447] RESIDUE Docs - PR #638 body, "Decisions needed" items 1-3 and "Known limitations" bullet 2 - wording predates ruling 5967852698
Exact fix: item 1 -> "NFR-RES-01 ... The allocation needs the owner's ruling; the 121.5-tile ceiling and the gate tolerances are accepted as working policy (manager ruling)."; item 2 -> "Criterion 1 is judged at the declared 50 MHz shipping clock and is met (manager ruling)."; item 3 and the limitations bullet -> "The Vivado half of the gate runs in the manager's merge bank for every PR that changes RTL, the processor pin or the build recipe (manager ruling)."
```

```text
[R447] SUGGESTION Robustness - syn/ooc/pp_resource_gate.py:279-294 - check-baseline accepts a weakened policy
Requirement/evidence: receipts/probe_cli.log: the real baseline with the route ceiling removed, or with the route LUT tolerance at 10**9, gives "baseline PASS: 3 endpoints". Floors are required, ceilings are not, and nothing ties the JSON to AREA_BUDGET.md:142-146.
Suggested change: require the route ceiling, bound the tolerances, or check the AREA_BUDGET table against the JSON.
```

```text
[R447] SUGGESTION Tests - syn/ooc/pp_resource_gate_selftest.py - identity and parser guards without an arm
Requirement/evidence: receipts/extra_mutants.log: unbinding the identity's design name or design state, and relaxing the header-uniqueness, single-timing-summary, timing-value-row and single-generated-top guards, all survive. The route probe "design state changed" exits 2 correctly at this head.
Suggested change: one arm per guard.
```

## Clean lenses

```text
[R447] PASS Conformance - issue #234 acceptance with ruling 5967852698; docs/findings/234_PP_SHADOW_AREA_BASELINE.md:77, :263, :324, :337, :353; syn/ooc/pp_resource_baseline.json; .github/workflows/rtl-fast.yml:209-211; hosted job 111176191131 step 9 - criterion 1 as ruled: A route WNS +0.063 / WHS +0.036 ns at 20 ns, judged on the multi-corner summary (sw/litex/timing_grade.tcl:67-72 restores both corners before the recipe's report), meeting BUILDING.md section 5; criterion 2 is reported as not met at A and stays with #232/#230/#639 under "Relates to", so the PR closes nothing; criterion 3: tolerances, floors and the 121.5-tile ceiling documented, the allocation an owner decision, not a defect here; criterion 4: the hosted half is wired and executed at the exact head (51 arms, 25 mutants, baseline PASS) and the bank half documented; ranking levers 1-3 and 5 match RTL at protocol-processor 631eeb34 (KL_aecp_notify.sv:329 ram_style distributed 16 x 128, read at :337, :541-544, :551-552; :392 ctr_last_r 6 x 32 at 1x1, reset :934, compared :1034-1037; KL_srp_top.sv:947 tf_ram_r 2 x 32 x 47, written :959-968; protocol_processor_top.sv:2921 armq_r 8 x 4 x 47), the cone evidence (2,048 FF / 2,292 LUT; 2,304 FF / 648 LUT / 288 MUXF; 1,153 FF / 1,178 write LUT; 192 FF) and the totals (5,590 FF, 3,570 LUT, about 46,558 LUT left); savings are labelled estimates.
[R447] PASS RTL - git diff --name-status 1269cdaf..2a765a6c (11 files, none under hdl/, gitlinks unchanged at 631eeb34 / 5dce647a / 48ff7a7e) - no RTL or interface change to judge; the cited processor lines were read at the pinned revision (above); combination B material is absent: no C8/P2 patch path, no rom_digests.tsv row, no gitlink move, ddb3119d only named in findings prose.
```

## What was verified

- **Figures against the records.** `pp_resource_baseline.json` endpoint records equal the published `A-record-{route-1x1,ooc-1x1,ooc-8x8}.json` exactly. All 49 table groups re-derive from the published records with no mismatch: route, standalone, both sub-block tables, per-context table (`receipts/check_tables.log`). The ranking TSVs, from the hierarchy reports through a different parser, agree: 1x1 logic LUT 23,101 + LUT-as-memory 1,242 = 24,343. Every Yosys reconciliation sum and difference holds (1x1 gap 26,235; 8x8 gap 61,664; mapping TSV sums 50,198 / 27,254 and 93,892 / 35,333). The #231 step holds (+2,020 LUT, +812 FF, +3 DSP), as do the percentages and the NFR-RES-01 arithmetic. The installed tool reports SW Build 6511674, matching every record (`receipts/vivado_version.log`).
- **Gate on the real records.** Replaying all seven published records through the head's comparator reproduces the published gate logs: A 0, 0, 0; B route 1 (+625 LUT over 500); B standalone 0, 0; A at 10 ns 2 (`receipts/replay_records.log`).
- **Gate through its CLI, real policy.** Every resource at and one over its tolerance, every ceiling, floor and fall boundary, tool, device, flow, thread, state and standalone-clock changes, and missing or malformed reports behave as documented. The six exceptions are the first finding (`receipts/probe_cli.log`).
- **Touched gates.** 27 commands, all rc 0 (`receipts/gates/`): gate self-test 51 arms; gate mutants control plus 25 failing; check-baseline; `pp_baseline` self-test and 32 mutants; the reports self-test; `dp_srcs` self-test and tops; `ooc_tcl` 58 arms; `ci_events --check/--selftest`; `ci_scope`; docs_check; em-dash over 541 added lines; doc style; DOC_MAP; solution docs; feature status; module matrix; doc paths; archive; TOC and anchors; Python idiom; hygiene; TODO; fail-fast; test evidence; `git diff --check`. `make -C gptp-processor docs` ran under GNU Make 4.3, built from the verified release tarball, rc 0 (`receipts/make43_docs.log`).
- **CI wiring.** The three commands sit in the existing rtl-fast OOC step and its `ci_events.py` pin (`:2328-2330`). No new job, runner or tool is added. The hosted exact-head run executed them (`receipts/hosted_ooc_step_excerpt.log`). Nothing new needs Vivado on a hosted runner.
- **Clone restored.** HEAD and tree are exact. The index is equal to the HEAD tree (mode, blob, path). There are no untracked or ignored leftovers; the run's `__pycache__` was removed. Submodules sit at their gitlinks, clean (`receipts/restore_check.log`).

## Ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #234 criteria with ruling 5967852698; findings tables and ranking; baseline JSON; rtl-fast step and hosted job 111176191131; RTL lines at 631eeb34 | R447-1 | 2a765a6c3868400c20ede2e357876f28a811c811 |
| RTL | CLEAN | diff name-status and gitlinks; cited processor RTL at 631eeb34 | R447-1 | 2a765a6c3868400c20ede2e357876f28a811c811 |
| Robustness | UNCLEAN | pp_resource_gate.py through its CLI (54 probes), route-status probe | R447-1 | 2a765a6c3868400c20ede2e357876f28a811c811 |
| Tests | UNCLEAN | gate self-test and 25 mutants, 18 reviewer mutants, pp_baseline self-test and 32 mutants, 27 touched gates | R447-1 | 2a765a6c3868400c20ede2e357876f28a811c811 |
| Docs | UNCLEAN | findings page, AREA_BUDGET section, recipe section, PR body against records and rulings | R447-1 | 2a765a6c3868400c20ede2e357876f28a811c811 |

## Real limits

- **Records versus raw reports.** The raw reports are not public, so the step from them to the records cannot be re-derived. The packet publishes the gate's records and SHA-256 digests of `baseline_utilization.rpt`, `baseline_timing.rpt`, `baseline_hierarchy.rpt` and `baseline_cells.tsv`, but not the reports. The records were checked for exact equality with the baseline JSON and against independent public artifacts and the installed tool build.
- **No reproduction run.** No Vivado measurement or Yosys mapping was rerun: the export needs the builder environment and banks outside this review's allowance. So host-to-host determinism and the gate's verdict on a fresh measurement of this head (claimed exit 0) are untested. Several prose figures rest on unpublished reports: integrated synthesis 52,807 / 53,209, critical paths, `Synth 8-7186`, `milan_datapath` 41,527.
- **Hosted contexts.** At 09:55Z, docs-check, elaborate and Verilator shards 1, 2 and 4 were still in progress, and Physical gPTP was skipped. Skipped contexts are not evidence.
- **Physical calibration.** NOT RUN. No bitstream, hardware or field result exists, and field skips are not hardware proof.

## Pending manager duties

- Carry the two RESIDUE items to the residue checklist if they are not fixed.
- Publish the raw A route and A 1x1 standalone utilization, hierarchy, timing and route-status reports whose digests sit in `run-receipts.json`, so a later round can re-derive the records.
- Re-review the fix head under all five lenses, since a gate change un-covers Robustness and Tests and a docs change un-covers Docs.
- Hosted and act acceptance of the exact head, including the in-progress contexts.
- The internal review.
- Candidate-merge validation at live dev `1269cdaf` and post-merge containment.

R447-1 FINISHED
