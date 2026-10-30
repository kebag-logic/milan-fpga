[A710] REVIEW READY
Commit: `32f0d9b5425a8526ac9d39e5913c01944c36e4d0` (branch `818-wns-gate`, two commits on dev `1e80128f`, the live tip; not pushed by this lane)
Changed:
- `syn/ooc/pp_resource_gate.py` (the issue's `scripts/` path holds no such file): a route endpoint is judged on the recipe's three placement directives (`--comparison` for each of AltSpreadLogic_high and ExtraTimingOpt beside the shipping route) or on one route marked `--shipping-selection`; neither or both exits 2. The gate selects the best worst-corner WNS (a tie goes to the recipe's order), prints each route's worst-corner WNS and WHS, names the selected directive, and judges that route's WNS and WHS against +0.030 ns / 0 ns at every signoff corner the flow's timing grade declares, naming each corner below a floor. A fall from the record beyond the existing 0.25 ns column prints a WARNING and never fails. LUT, FF, slice, RAMB36, RAMB18, DSP and the BRAM tile ceiling are unchanged and judged on the selected route. `record --write` of a set stores the selected route, its flow naming its directive; the record's shape, the baseline and the policy table are unchanged.
- Each comparison must hold exactly the script the recipe's snippet writes from the shipping script, and takes the shipping route's inputs; every route of a set is judged on its identity (the three recipe directives compared as one), population, signoff corners (their worst must be the timing summary's) and route status.
- Arms: `syn/ooc/pp_resource_gate_set_selftest.py` (new: 21 timing arms, 29 route-set arms through `main()` including the issue's four cases, 2 standalone refusals, the set's re-record); fixtures carry the four corner reports. Mutants: 38 new, 11 rewritten.
- Docs: `docs/design/AREA_BUDGET.md`, `docs/integration/BUILDING.md` section 5, the gate commands in `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`, and the stale gate row of `docs/design/MARK_II_AREA_PLAN.md`.
Validation (each rc 0):
- `python3 syn/ooc/pp_resource_gate.py --selftest`: 304 arms and 500 generated cases PASS (dev 260), placement controls PASS.
- `python3 syn/ooc/pp_resource_gate_mutants.py`: control passes, all 230 mutants fail (dev 192); each new or rewritten mutant killed by its own arm.
- `python3 syn/ooc/pp_resource_gate.py check-baseline`: baseline PASS, 3 endpoints.
- rtl-fast replica in a clean clone at the head, jobs `changes`, `bdd-conformance`, `yosys-elaboration` (its step runs the three commands above): every step success; behave 495 scenarios, 2,288 steps.
- Docs workflow replica in a clean clone at the head: 44 steps, 0 failed, 2 skipped by rule; markdown gates on CPython 3.12.3 and the no-git gates rc 0; Python idiom gate within every ratchet.
- Generated exit-code cases on real routes: 3,000 on dev's shipping route and 1,000 on #814's head route, 0 failures.
Acceptance criteria:
- The self-test passes, each of the four cases planted with its expected verdict: met.
- dev `1e80128f`'s three recorded routes from #814 round 1 pass and select ExtraPostPlacementOpt (+0.303 ns; AltSpreadLogic_high +0.230, ExtraTimingOpt +0.106): met, exit 0, every corner at or above both floors.
- The docs gates pass: met.
- Verdicts on the recorded routes change only as the ruling intends: #814's head set goes from 1 (fell 0.312) to 0 with a WARNING, the #814 control set from 1 (fell 0.272) to 0 on AltSpreadLogic_high (+0.342); dev's stays 0.
Open risks/questions:
- A non-selected comparison route that is incomplete still fails the set (exit 1), as every route the gate reads always has; leaving it out of the selection instead would be a policy choice the ruling does not make.
- A route named alone without `--shipping-selection` now exits 2 (the issue's "a single one marked"); the documented commands are updated and no CI caller passes a route.
