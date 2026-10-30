[A710]

## Contents

- **[Status](#status)** — REVIEW READY at the head below, every gate rc 0; `818-wns-gate` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — The task, the ruling it applies, and roles.
- **[Description](#description)** — The route-set rule, what each route of a set must be, and the verdicts on the recorded routes.
- **[Authoritative references](#authoritative-references)** — The ruling, the build floor and the recipe.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Checkout and submodules.
- **[How to validate](#how-to-validate)** — The gate's self-tests, its mutants, the baseline audit and a route-set check.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — The interpretations this lane made, and what it did not change.
- **[Definition of Done](#definition-of-done)** — The merge bar from CONTRIBUTING.md.

## Status

**REVIEW READY** at `32f0d9b5425a8526ac9d39e5913c01944c36e4d0`; `818-wns-gate` -> `dev` (`1e80128f`, the live tip).

- The gate's self-test: 304 arms and 500 generated cases PASS (dev: 260 arms), the placement controls PASS.
- Its mutant campaign: the control passes and all 230 mutants fail (dev: 192); each of the 38 new ones and the 11 rewritten ones is killed by the arm written for it.
- `check-baseline`: PASS, 3 endpoints. No baseline or policy-table change.
- The generated exit-code test on real routes: 3,000 cases on dev's shipping route, 1,000 on #814's head route, 0 failures.
- rtl-fast, the jobs this change reaches (`changes`, `bdd-conformance`, `yosys-elaboration`, whose step runs the three gate commands above), in a clean clone at the head: every step success; behave 495 scenarios.
- The docs workflow under GNU Make 4.3, in a clean clone at the head: 44 steps, 0 failed, 2 skipped by rule; the markdown gates on CPython 3.12.3 and the no-git gates also rc 0.
- The Python idiom gate: within every ratchet; `pp_resource_gate_selftest.py` stays within the 1000-line module limit.
- dev `1e80128f`'s three recorded routes from #814 round 1 pass and select ExtraPostPlacementOpt at +0.303 ns, the best worst-corner WNS of the three.

## Linked Issue / roles

Closes #818
Relates to #814, #76

Executor: `[A710]`
Internal cleared-context reviewer: `[R<n>]`
External reviewer: `[R<n>]`

## Description

The ruling on #814 (rule 1) changes the resource gate's WNS rule for adoptions. At 99.5 % slice use, unchanged logic moved 0.3 to 0.57 ns between routes, so a 0.25 ns limit on the best record measures placement, not the change. `syn/ooc/pp_resource_gate.py` (the issue names `scripts/`, which holds no such file) now judges the route endpoint on a route set:

| Rule | At the head |
|---|---|
| A set is the recipe's three placement directives | `check <shipping route> --endpoint route-1x1 --comparison <AltSpreadLogic_high route> --comparison <ExtraTimingOpt route>`; or one route marked `--shipping-selection`. Neither, or both, exits 2 |
| The gate selects the best directive and names it | The highest worst-corner WNS; a tie goes to ExtraPostPlacementOpt, then AltSpreadLogic_high. It prints each route's worst-corner WNS and WHS and `directive <D> selected: ...` |
| WNS and WHS meet the build floor at every signoff corner | +0.030 ns setup and 0 ns hold, the floors already in the policy, judged at each `*_signoff_<model>_<T>C_timing.rpt` the flow's timing grade declares; a miss names its corners and exits 1 |
| The fall from the record is a warning | Above the existing 0.25 ns timing-fall column: `WARNING: fell by more than 0.25 from the record`, never a failure |
| Every other tolerance is unchanged | LUT, FF, slice, RAMB36, RAMB18, DSP and the BRAM tile ceiling, judged on the selected route |
| The re-record names the directive | `record --write` of a set stores the selected route; its flow carries `place_design -directive <D>`. The record's shape is unchanged |

What each route of a set must be:

| Requirement | Refusal |
|---|---|
| A comparison holds exactly the script the recipe's snippet writes from the shipping script: the shipping thread setting, that route's synthesis checkpoint, then the shipping commands with only the directive changed | exit 2, naming the checkpoint, the thread setting or the script |
| The set holds each of the three directives once | exit 2 |
| Every route has the record's identity but for its directive, and its control population | exit 2 |
| Every route's signoff corners are one run's: their worst WNS and WHS are the timing summary's | exit 2 |
| Every route is completely routed | exit 1, led by its directive |

Comparisons take the shipping route's inputs, since they place its synthesis checkpoint; the identity comparison writes the three recipe directives as one, and any other directive is still a recipe change. The identical-inputs refusal applies at the same directive.

The recorded routes, before (dev's gate on the shipping route) and after (the set):

| Route set | Worst-corner WNS, ns: ExtraPostPlacementOpt / AltSpreadLogic_high / ExtraTimingOpt | Before | After |
|---|---|---|---|
| dev `1e80128f` | +0.303 / +0.230 / +0.106 | 0, fell 0.137 | 0, ExtraPostPlacementOpt selected, floor met at every corner |
| #814 head `8b28ebaf` | +0.128 / +0.039 / +0.010 | 1, fell 0.312 | 0, ExtraPostPlacementOpt selected, WARNING for the 0.312 fall |
| #814 control route | +0.168 / +0.342 / +0.300 | 1, fell 0.272 | 0, AltSpreadLogic_high selected, fell 0.098 |

The only verdict changes are the ruling's: a fall beyond 0.25 ns no longer refuses. A route named alone without the mark exits 2 by the new interface.

| File | Change |
|---|---|
| `syn/ooc/pp_resource_gate.py` | `route_set()`, `bound()`, `signoff()`, `corners()`, `best()`, `selection()`; `judge()` and `verdict_for()` apply the floors per corner and warn of a fall; `--comparison` and `--shipping-selection` |
| `syn/ooc/pp_resource_gate_set_selftest.py` (new) | 21 timing arms on one route's corners, 29 route-set arms through `main()` (the issue's four cases among them), 2 standalone refusals and the set's re-record |
| `syn/ooc/pp_resource_gate_selftest.py`, `syn/ooc/pp_placement_selftest.py` | Fixtures carry the four corner reports; single routes are marked; 11 timing arms moved to the new module and rewritten |
| `syn/ooc/pp_resource_gate_mutants.py` | 38 new mutants, 11 rewritten to the new code |
| `docs/design/AREA_BUDGET.md`, `docs/integration/BUILDING.md` section 5, `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`, `docs/design/MARK_II_AREA_PLAN.md` | The rule, its ruling, the gate's commands with the comparisons, and the stale "fall limit binds first" lines |

## Authoritative references

- The ruling on #814, rule 1: https://github.com/kebag-logic/milan-fpga/issues/814#issuecomment-6522621984 (amends the #708 ruling's "no fall exception" for this gate; the floor exception stays forbidden).
- The build floor: `docs/integration/BUILDING.md` section 5, the #395 margin decision (WNS >= +0.03 ns and WHS >= 0 at every declared corner); `sw/litex/platforms/ax7101_timing.py` declares the corners and `sw/litex/timing_grade.tcl` writes their reports.
- The recipe's three placement directives and the comparison snippet: `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`, "Integrated measurements".
- The gate's policy: `docs/design/AREA_BUDGET.md`, "The resource gate".

## How to get into the same state

```sh
git clone https://github.com/kebag-logic/milan-fpga.git
cd milan-fpga
git checkout 818-wns-gate
git submodule update --init protocol-processor gptp-processor third_party/verilog-axis
```

## How to validate

```sh
python3 syn/ooc/pp_resource_gate.py --selftest
python3 syn/ooc/pp_resource_gate_mutants.py
python3 syn/ooc/pp_resource_gate.py check-baseline
```

Expected result / pass criteria: each exits 0; the self-test ends `resource gate selftest: 304 arms and 500 generated cases PASS` and `placement gate: unchanged acceptance schema, record and policy PASS`; the campaign ends `resource gate mutants: control passes, all 230 mutants fail`; the audit prints `baseline PASS: 3 endpoints`.

On a recipe measurement (`$WORK` as the recipe sets it, the route and its two comparison directives already run):

```sh
python3 syn/ooc/pp_resource_gate.py check "$WORK/ax7101/gateware" --endpoint route-1x1 \
  --comparison "$WORK/ax7101-AltSpreadLogic_high" --comparison "$WORK/ax7101-ExtraTimingOpt"
```

On dev `1e80128f`'s three recorded routes this exits 0 with `directive ExtraPostPlacementOpt selected: the best worst-corner WNS, 0.303 ns`, every corner at or above both floors.

## Known limitations / out of scope

- Interpretations, each public here for review: the mark is required for a route judged alone; selection is by worst-corner WNS alone, both floors then judged on that route; a non-selected route that is incomplete still fails, as every route the gate reads always has; the WARNING threshold is the existing 0.25 ns column; corner reports that disagree with the timing summary are refused; a split placement is judged alone.
- No policy value, baseline record or recipe command changes. The record stays the twelfth record; #806 and #787 each re-record from their own merge route under the ruling.
- The build itself still does not enforce the floors; the shipping seed selection stays manual, now documented as the best worst-corner WNS directive.
- No RTL change and no new route: the routes cited are the ones #814 recorded.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
