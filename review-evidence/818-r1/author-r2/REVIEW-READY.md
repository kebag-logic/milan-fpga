[A710b] REVIEW READY
Commit: `50e5d08dda6e89cf010a740cea5cf4539807db01` (branch `818-wns-gate`, two commits on `32f0d9b5`, no rebase; not pushed by this lane)
Changed:
- F2: `syn/ooc/pp_resource_gate.py:572-578` reports the floor REGRESSION and the fall WARNING together (`REGRESSION: below the floor <F> at <corners>; WARNING: fell by more than 0.25 from the record`), the WARNING summary line follows (`:537`), exit still 1. Arms: WNS and WHS each below the floor with a fall beyond the timing fall (both printed) and within it (no WARNING). Mutants `fall warned beside a floor miss` and `fall warning summarized beside a floor miss`, each killed by the WNS "both reported" arm. `docs/design/AREA_BUDGET.md:442` and `docs/testing/PP_SHADOW_BASELINE_RECIPE.md:588` say so.
- F3: no gate change (the guard at `:401` is already two-way). Arms: the timing summary's WNS (0.010) and WHS (-0.050) below every corner report and under the floor exit 2 naming the disagreement. Mutant `corners agree in both directions` (`worst < figures[figure]`) killed by the WNS arm; `corners agree in the other direction` also added and killed.
- F1: `docs/design/MARK_II_AREA_PLAN.md:1340-1347` marks the mapping record `--shipping-selection` (the map reads one routed checkpoint).
- R1: the PR body's mutant sentence is exact: of 44 new and 11 rewritten mutants (9 changed edits; `timing fall` and `timing fall boundary` keep their edits under rewritten arms), 54 are killed by a named arm or check and `every corner model read` by the fixture record's refusal before the arms run.
- S1: two set arms for the BRAM tile ceiling (selected comparison over it fails; route not selected over it passes) and two killed mutants. The four `bound()` sub-conditions stay unarmed, each redundant with a later check; stated in the PR body.
Validation (each rc 0):
- `python3 syn/ooc/pp_resource_gate.py --selftest`: 312 arms and 500 generated cases PASS, placement controls PASS.
- `python3 syn/ooc/pp_resource_gate_mutants.py`: control passes, all 236 mutants fail; each round-2 mutant run alone is killed by its own arm.
- `python3 syn/ooc/pp_resource_gate.py check-baseline`: baseline PASS, 3 endpoints. `python3 scripts/check_py_idiom.py`: rc 0.
- rtl-fast replica in a clean clone at the head, jobs `changes`, `bdd-conformance`, `yosys-elaboration`: every job success; behave 495 scenarios, 2,288 steps.
- Docs workflow replica in a clean clone at the head: 44 steps, 0 failed, 2 skipped by rule; builder leg 1 with the LiteX interpreter, the five markdown gates on CPython 3.12.3 and the no-git gates rc 0.
- F1: the documented `cp` and `record` lines, run on dev `1e80128f`'s recorded shipping route: rc 0, ExtraPostPlacementOpt recorded at 0.303; a check against that scratch record passes. The map step needs Vivado and was not run.
Acceptance criteria:
- The self-test passes with the issue's four cases planted: met (unchanged arms).
- dev `1e80128f`'s three recorded routes pass and select ExtraPostPlacementOpt (+0.303 ns): met. All 15 recorded-route runs (the three sets, reversed, marked, unmarked, record) give output byte-identical to round 1's, so no recorded verdict changes in this round.
- The docs gates pass: met.
- R748-1's 28 real-route probes at the head: 28 PASS; the floor-miss probe now prints the REGRESSION and the WARNING and exits 1.
Open risks/questions: none
