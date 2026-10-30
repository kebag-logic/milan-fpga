# HANDOFF: [A710] issue #818, the resource gate's WNS rule for adoptions

Status: **REVIEW READY** at `32f0d9b5`, every gate rc 0 (2026-10-30 15:1x CET)

Lane: branch `818-wns-gate` from dev `1e80128f0a467b58bf884b7d9bf62e013a2fb141` (the live remote dev tip
throughout); origin `https://github.com/kebag-logic/milan-fpga.git`; every submodule at dev's pin, each checked for
its own top level and origin before the clean clones read it. Head:
`32f0d9b5425a8526ac9d39e5913c01944c36e4d0` (two commits, nothing pushed).

| Commit | Subject |
|---|---|
| `6d9c03c9` | Judge the route endpoint on the recipe's three placement directives: select the best worst-corner WNS, name its directive, hold WNS and WHS to their floors at every signoff corner and print a fall from the record as a WARNING, with arms and killed mutants (#818) |
| `32f0d9b5` | Document the route-set rule in the area budget, BUILDING section 5, the recipe's gate commands and the Mark II gate row (#818) |

Assignment: the body of #818; ruling #814 issuecomment-6522621984, rule 1. TAKEN posted as issuecomment-6523496438;
REVIEW READY posted as issuecomment-6524843701 (text in `REVIEW-READY.md`).
No Vivado run, no RTL, no sweep (none needed: the existing routed reports were used).

## 1. What the ruling asked and what the gate now does

| #818 / ruling | Gate behaviour at the head |
|---|---|
| A route set passes when the best of the recipe's three directives meets the build floor (+0.030 ns, 0 ns) at every signoff corner | `route_set()` reads the shipping route and one `--comparison` per other directive; `best()` picks the highest worst-corner WNS; `verdict_for()` judges WNS_ns and WHS_ns of that route at every corner `signoff()` derives from the flow's `kl_timing_grade_configure` line, naming each corner below a floor |
| The checker takes the three routed reports, or a single one marked as the shipping selection, and names the directive it selected | `--comparison DIR` (twice) or `--shipping-selection`; neither or both is exit 2. Output line `directive <D> selected: the best worst-corner WNS, <x> ns` or `directive <D>: the one route, marked as the shipping selection`, plus a per-route WNS/WHS table for a set |
| The fall from the record is computed and printed as WARNING, with no failure | The figure row prints the delta as before; a fall beyond the existing 0.25 ns timing-fall column prints `WARNING: fell by more than 0.25 from the record` in the row and a summary `WARNING: <figures> fell from the record ...; reported, never gated (#818)`; exit unaffected |
| Every other tolerance unchanged: LUT, FF, slices, RAMB and DSP | Unchanged code and policy; judged on the selected route. BRAM tile ceiling unchanged too. No baseline JSON or policy-table change; `check-baseline` unchanged |
| The re-record stores the selected directive's figures and names the directive | `record --write` with a set writes the selected route's record; its identity flow carries `place_design -directive <D>`. The record shape is unchanged, so no hand edit of the JSON |

### Material assumptions (all public in the PR body; none changes a policy value)

1. **Path.** The issue names `scripts/pp_resource_gate.py`; the gate is `syn/ooc/pp_resource_gate.py` (no file of that name in `scripts/`).
2. **The mark is required.** A route endpoint named alone without `--shipping-selection` now exits 2 (the issue's "or a single one marked"). Every documented command was updated; the only CI callers (`--selftest`, the mutants, `check-baseline`) take no route.
3. **Selection** is by worst-corner WNS alone (the issue's "best worst-corner WNS"); a tie goes to the recipe's order, ExtraPostPlacementOpt, AltSpreadLogic_high, ExtraTimingOpt. Both floors are then judged on that one route.
4. **Every route of a set** is read whole: refusals (unreadable report, identity, population, corners) are exit 2 and an incomplete route status is exit 1 for any route, selected or not, as the existing "an incomplete route is a material regression" rule reads for every route the gate reads. Figures are judged on the selected route only.
5. **Warning threshold.** The WARNING fires above the existing 0.25 ns "Timing fall" column (kept in the policy table and JSON); a smaller fall prints its delta and `ok`.
6. **Corner consistency.** The signoff corner reports are written on the routed state `baseline_timing.rpt` then reads across every corner (`baseline_integrated.tcl` writes `kl_timing_grade_reports` after the last `phys_opt_design`, then `report_timing_summary`), so the gate refuses (2) corner reports whose worst WNS or WHS differs from the summary's: they are not one run's. True on all nine recorded routes.
7. **Directive in the identity.** The identity comparison writes each of the three recipe directives as one; any other placement directive is still a recipe change (2). The identical-inputs refusal now applies at the same directive only.
8. **Comparison binding.** A comparison directory must hold exactly the script the recipe's snippet writes from the shipping script (the shipping thread setting, `open_checkpoint` of that route's `alinx_ax7101_synth.dcp`, then the shipping commands after `# Add pre-optimize commands` with only the placement directive changed); its inputs digest is the shipping route's. Verified byte-exact on dev's two real comparison scripts before writing the rule.
9. **Split placements** (`--placement f0-f4|full-split`) are judged alone with `--shipping-selection`; a set is refused for them.

## 2. Changes (file:line at the head, and why)

| File:line | Change | Reason |
|---|---|---|
| `syn/ooc/pp_resource_gate.py:25-35` | Docstring paragraph on route sets; usage lines `:60-63` | The exit-code contract and the new arguments, in the gate's own text |
| `syn/ooc/pp_resource_gate.py:131-146` | `DIRECTIVES`, `PLACE`, `COMPARISON`, `TAIL`, `CHECKPOINT`, `THREADS`, `OPENS`, `GRADE`, `SIGNOFF` | The recipe's three directives (shipping first), the comparison script's shape, and the timing grade and signoff prefix the corners come from |
| `syn/ooc/pp_resource_gate.py:319-348` | `record()` now wraps `measure()`, which also returns a route's signoff corners and reads a comparison against its shipping route | One reader for shipping and comparison routes; a comparison's inputs are the shipping route's |
| `syn/ooc/pp_resource_gate.py:351-373` | `bound()` | Binds a comparison to its shipping route by the script the recipe writes; gives its flow at its own directive |
| `syn/ooc/pp_resource_gate.py:376-405` | `signoff()`, `corners()` | Every declared corner's `*_signoff_<model>_<T>C_timing.rpt`, through the existing `timing()` reader, with the consistency refusal |
| `syn/ooc/pp_resource_gate.py:433-457` | `route_set()` | Set or mark, standalone and split refusals, each directive once |
| `syn/ooc/pp_resource_gate.py:460-499` | `directive()`, `best()`, `selection()`, `across()`, `recipe()` | Name, select, report, collect per-route problems led by their directive, compare identities across the three directives |
| `syn/ooc/pp_resource_gate.py:502-560` | `judge()`: identity and identical inputs for every route of the set (`:517`, `:525`), corner table, WARNING summary (`:546`) | The set's other routes must be the same recipe; the selected route is judged |
| `syn/ooc/pp_resource_gate.py:566-581` | `verdict_for()`: floor at every corner (`:572`), fall is a WARNING (`:577`) | Rule 1 of the ruling |
| `syn/ooc/pp_resource_gate.py:815`, `:856-859` | Fuzz marks its route case and mutates the corner reports too | Keeps the generated exit-code test on every report the gate now reads |
| `syn/ooc/pp_resource_gate.py:914-917`, `:956-975` | `--comparison`, `--shipping-selection`; main reads the set, judges the selected route, records it | The CLI the issue asks for |
| `syn/ooc/pp_resource_gate_set_selftest.py` (new, 259 lines) | Corner fixture (`CORNERS`, `summary()`, `corner_reports()`, `slack()`), `timing_arms()` (21), the recipe's comparison fixture `comparisons()`, `set_arms_table()` (29), standalone refusals (2), `re_record()` | The new arms; a separate module because `pp_resource_gate_selftest.py` stands at the idiom gate's 1000-line module limit |
| `syn/ooc/pp_resource_gate_selftest.py:29,78,88,108,112` | Fixture writes the four corner reports and the comparison split line and signoff call | Fixture routes look like the recipe's |
| `syn/ooc/pp_resource_gate_selftest.py:477-482,510,526,554,885,904,975,983` | Planted exceptions in `corners` and `best`; `MARK`; multi-text needles; arms judge with corners; fuzz tokens and structure for corner reports; the new arms run | 11 timing arms moved to the new module and rewritten (995 lines, within the limit) |
| `syn/ooc/pp_placement_selftest.py:221,289,300,325,338` | Single routes marked; the WHS plant changes the summary and the Fast corners together | The placement controls keep their verdicts under the new reader |
| `syn/ooc/pp_resource_gate_mutants.py:22-35,109,131,142` | 11 mutants rewritten to the new text | Same enforcement points, new spelling |
| `syn/ooc/pp_resource_gate_mutants.py:303-361,399,417` | `SET_MUTANTS` (38) and the new module copied into each mutant's folder | Every new enforcement point has a mutant the self-test must kill |
| `docs/testing/PP_SHADOW_BASELINE_RECIPE.md:220,565-610,627-632` | Gate commands with the comparisons, the route-set rule, the new exit-2 reasons, the re-record | The documented commands would otherwise exit 2 |
| `docs/design/AREA_BUDGET.md:423,435-442,448-453,480` | The rule, its ruling, the floor as the bound, the re-record from the set | The policy page |
| `docs/integration/BUILDING.md:570-579,632-633,722-725` | Section 5: the gate enforces the thresholds on an adoption's route set; the build still does not | Section 5 said "not automatically enforced" without qualification |
| `docs/design/MARK_II_AREA_PLAN.md:56` | The "Gate comparison" row | It stated the fall limit as binding |

## 3. New checks: each planted case and the mutant it kills

The issue's four cases (route-set arms, through `main()`, fixture WNS 0.500 / 0.400 / 0.300):

| Issue case | Planted | Verdict | Words required |
|---|---|---|---|
| A set whose best directive misses the floor at one corner fails | shipping summary and Slow_85C to +0.020 (Slow_0C kept +0.500), both comparisons below it | exit 1 | `directive ExtraPostPlacementOpt selected`, `below the floor 0.03 at Slow_85C`, not `at Slow_0C` |
| A set whose shipping directive misses the floor but whose best meets it passes, and names the best | shipping summary and Slow corners to +0.020 | exit 0 | `directive AltSpreadLogic_high selected`, `RESULT: PASS`, no `REGRESSION` |
| A large fall passes with a WARNING | all three below the record by 0.4 ns or more, best +0.100 | exit 0 | `WARNING: WNS_ns fell from the record`, `RESULT: PASS`, no `REGRESSION` |
| A resource over tolerance still fails | LUT +11 (tolerance 10) on the selected route; and SLICE +6 on a selected comparison | exit 1 | `REGRESSION: grew by more than 10`; `directive AltSpreadLogic_high selected` and `grew by more than 5` |

Every mutant that is new or rewritten, with the self-test failure that kills it (receipt `receipts/after/mutant-words.tsv`, 49 of 49 killed; the campaign itself: control passes, all 230 mutants fail):

| Mutant (removed enforcement) | Failing words |
|---|---|
| timing floor (`if missed:` -> False) | route arm 'WNS below the floor': exit 0, wanted 1 naming 'below the floor 0.03 at Slow_0C, Slow_85C' |
| timing floor boundary (`<` -> `<=`) | route arm 'WNS at the floor': exit 1, wanted 0 |
| timing fall (warning check -> False) | 'WNS fell more than the timing fall: a warning, never a failure' lacks 'WARNING: fell by more than 0.25 from the record' |
| timing fall boundary (`>` -> `>=`) | 'WNS fell by exactly the timing fall' ... and not 'WARNING' |
| floor names its corners | 'WNS below the floor' lacks 'at Slow_0C, Slow_85C' |
| a fall never fails (True -> False) | 'WNS fell more than the timing fall...': exit 1, wanted 0 |
| fall warning summarized | lacks 'WARNING: WNS_ns fell from the record' |
| every junction endpoint read (85 C dropped) | 'WNS below the floor' names only Slow_0C |
| every corner model read (Fast dropped) | the fixture refuses: worst WHS_ns 0.2 against the summary's 0.1 |
| one timing grade / signoff report set required | 'a second timing grade' / 'signoff reports not written' lose their reason |
| corners agree with the summary / for both slacks | "a corner's WNS (WHS) below the summary's": exit 0, wanted 2 |
| corner refusals of every kind named / name their report | 'a corner slack too long to be finite' / 'a corner report without its summary' lose the report name |
| best worst-corner WNS selected (-> first route) | 'a set whose shipping directive misses the floor ...': exit 1, wanted 0 |
| tie to the recipe's first | 'a tie between the comparisons ...' lacks 'directive AltSpreadLogic_high selected' |
| a single route selected alone | 'check reads the kind from a standalone directory': exit 2, wanted 0 |
| a set holds the three directives | 'a set of one comparison': exit 0, wanted 2 |
| a set and a mark exclusive / a route needs a set or a mark | 'a route both in a set and marked' / 'a route neither in a set nor marked': exit 0, wanted 2 |
| a standalone synthesis takes neither | 'a standalone synthesis with --shipping-selection': exit 0, wanted 2 |
| a split placement judged alone | 'a set of a selected split placement' loses 'is judged alone' |
| comparison script bound / flow at its directive / inputs the shipping route's / corners its own | 'route set control': exit 2, wanted 0 |
| comparison opens the shipping checkpoint | 'a comparison opening another checkpoint': exit 0, wanted 2 |
| comparison thread setting | 'a comparison of another thread setting': exit 0, wanted 2 |
| shipping route of the recipe | 'a set whose shipping route is not at the shipping directive' loses its reason |
| every route's identity | 'a comparison of another tool build, not selected': exit 0, wanted 2 |
| every route's identical inputs | 'the shipping route not selected, measured differently from the record's inputs': exit 0, wanted 2 |
| identical inputs at the record's directive | 'route set control': exit 2, wanted 0 |
| directives compared as one / only the recipe's | "placement directive another of the recipe's": exit 2, wanted 0 / 'placement directive outside the recipe': exit 0, wanted 2 |
| every route's route status / population | 'an incomplete comparison route, not selected': exit 0, wanted 1 / 'a comparison with a wrong population': exit 0, wanted 2 |
| set problems led by their directive | lacks 'ROUTE INCOMPLETE: ExtraTimingOpt: 3 nets with routing errors' |
| selection named / marked route named | 'route set control' / 'a marked route names its directive' lose the directive line |
| selected route judged and recorded | 'a selected comparison is judged on its own resources': exit 0, wanted 1 |
| fuzz marks a route | a generated case broke the exit-code contract |
| (rewritten) identical-input refusal / figures; route status of a route; check reads the route status; kind from the directory; all-fabric population not read / judged in a printed record | the arms they killed before, words in the TSV |

## 4. Resource before/after and route timing (recorded routes, no new route)

No RTL changed, so no figure moves; what moves is which route the gate judges and how. Route timing per directive (worst-corner WNS / WHS, ns, from each route's own signoff corners; Slow holds the worst setup, Fast the worst hold at every route):

| Route set | ExtraPostPlacementOpt | AltSpreadLogic_high | ExtraTimingOpt | Selected | LUT / FF / SLICE / RAMB36 / RAMB18 / DSP of the selected route (record 52,012 / 53,707 / 15,780 / 74 / 27 / 13) |
|---|---|---|---|---|---|
| dev `1e80128f` (#814 round 1) | +0.303 / +0.028 | +0.230 / +0.014 | +0.106 / +0.054 | ExtraPostPlacementOpt, +0.303 | 51,801 / 53,760 / 15,834 / 74 / 27 / 13 |
| #814 head `8b28ebaf` | +0.128 / +0.030 | +0.039 / +0.029 | +0.010 / +0.029 | ExtraPostPlacementOpt, +0.128 | 51,827 / 54,022 / 15,764 / 74 / 27 / 13 |
| #814 control `c1` | +0.168 / +0.025 | +0.342 / +0.034 | +0.300 / +0.036 | AltSpreadLogic_high, +0.342 | 51,863 / 53,849 / 15,821 / 74 / 27 / 13 |

Gate verdicts, dev's gate (before) and the head's (after), on the same directories:

| Route set | Before (`check` of the shipping route) | After (`check` of the set) | Changed as the ruling intends? |
|---|---|---|---|
| dev `1e80128f` | 0 PASS (WNS fell 0.137) | 0 PASS, selects ExtraPostPlacementOpt +0.303 | unchanged (acceptance of #818) |
| #814 head `8b28ebaf` | 1 (WNS fell 0.312 > 0.25) | 0 PASS, WARNING (fell 0.312), floor met at every corner | yes: the fall no longer refuses |
| #814 control `c1` | 1 (WNS fell 0.272) | 0 PASS, selects AltSpreadLogic_high +0.342 (fell 0.098) | yes: judged on its best directive |
| Each comparison directory alone | 2 (holds no recipe script) | 2 (same) | unchanged |
| A shipping route alone, unmarked | 0 / 1 / 1 as above | 2 (needs `--shipping-selection` or the set) | the issue's interface |
| A shipping route alone, `--shipping-selection` | as above | dev 0; head 0 with WARNING; control 0 with WARNING | the fall rule alone |

The comparisons named in either order give the same verdicts; `record` of each set prints the selected route.

## 5. Gate table (every one rc 0, never piped)

| Gate | Where | Result |
|---|---|---|
| `python3 syn/ooc/pp_resource_gate.py --selftest` | lane and clean clone at head | rc 0: 304 arms and 500 generated cases PASS (dev: 260), placement gate controls PASS |
| `python3 syn/ooc/pp_resource_gate_mutants.py` | lane and clean clone at head | rc 0: control passes, all 230 mutants fail (dev: 192) |
| `python3 syn/ooc/pp_resource_gate.py check-baseline` | lane and clean clone at head | rc 0: baseline PASS: 3 endpoints |
| `--fuzz 3000 check <dev route> --endpoint route-1x1`, `--fuzz 1000` on #814's head | real routes, head gate | rc 0: 0 failures each |
| rtl-fast replica, jobs `changes`, `bdd-conformance`, `yosys-elaboration` (the job whose step 8 runs the three gate commands) | clean clone at head | rc 0: every step success; behave 14 features, 495 scenarios, 2,288 steps passed |
| `python3 scripts/check_py_idiom.py` | lane before commit, and in the docs replica at head (the new module tracked) | rc 0, within every ratchet |
| docs workflow replica (GNU Make 4.3): every gate step of `docs.yml` run literally | clean clone at head, base dev `1e80128f` | rc 0: 44 steps, 0 failed, 2 skipped by rule (the candidate act runner on the host; the step that deletes `.git`, whose two gates ran on a `git archive` export: `docs_check` rc 0, `check_feature_status` rc 0); builder leg 1 again with the LiteX interpreter rc 0; the five markdown gates on CPython 3.12.3 rc 0 (link health, added-line em-dash, concise audience, cited path, per-page contents); the Python idiom gate rc 0 over 517 modules, long module 10 <= 10 |

## 6. Receipts

Under `receipts/`, host paths replaced by placeholders; files over 200 KB are in `receipts/large.sha256` by digest
and size. `INDEX.md` lists every file present, generated from the files. `receipts/route-reports.tsv` holds the
sha256 and size of every report the gate read in each route set.

| Receipt | What it holds |
|---|---|
| `receipts/before/` | dev's gate on each recorded route directory (`*-check.log`, `rc.txt`), dev's self-test (260 arms) and mutant campaign (192) |
| `receipts/after/` | the head's gate on each route set: the set, the set in reversed order, the shipping route marked and unmarked, the printed record (`rc.txt`); the generated-case runs on real routes; `mutant-words.tsv` |
| `receipts/gates/` | the lane's self-test, mutant campaign, `check-baseline` and idiom gate logs before the commit |
| `receipts/rtlfast-32f0d9b5/` | the rtl-fast replica of jobs `changes`, `bdd-conformance`, `yosys-elaboration`; `behave-tally.txt`, `gate-step-tally.txt` |
| `receipts/docs-32f0d9b5/` | the docs replica: `all.out`, per-step logs and `receipts.json`, the LiteX leg, the markdown gates, the no-git gates |
| `receipts/route-reports.tsv` | bytes and sha256 of every report the gate read in each route set |

Drivers are in `scripts/`: `run_routes.sh` (old and new gate on the recorded routes), `mutant_words.py`,
`copy_receipts.py`, `gen_index.py`, and the docs and rtl-fast replicas (`docs_run.sh`, `docs_steps.py`,
`docs_steps_md312.py`, `rtlfast_run.sh`, `rtl_fast_steps.py`, `make_clone.sh`, `env.sh`, `fw_env.sh`), the last
adapted from earlier lanes' copies, paths only.

## 7. Open questions for review

- Whether a non-selected comparison route that is incomplete should fail the set (as now) or be left out of the
  selection with a warning. The ruling does not say; this lane kept the existing rule for every route read.
- Whether a route judged alone should keep working unmarked. The issue asks for a marked one, so unmarked is exit 2.
