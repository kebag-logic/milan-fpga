[A710b] TAKEN
Branch: `818-wns-gate`, head `32f0d9b5` (PR #820); new commits on top, no rebase.
Authoritative references: this issue; the [A10] round-2 comment above; R748-1 (issuecomment-6529741002) F1, F2, F3, R1, S1; the ruling in #814 (issuecomment-6522621984, rule 1).
Interpreted scope: F1, the Mark II mapping procedure's `record` command in `docs/design/MARK_II_AREA_PLAN.md` takes the route-set form, proven by running it on a recorded set. F2, the fall WARNING prints whenever the fall exceeds the 0.25 ns column, also beside a floor REGRESSION; an arm for each combination and a mutant that suppresses it. F3, a set whose timing summary's worst WNS (and WHS) is below every corner report is refused; arms and the one-way mutant killed. R1, the PR body's mutant claim made exact; S1 if cheap. No other behaviour change.
Validation plan: `pp_resource_gate.py --selftest`, `pp_resource_gate_mutants.py`, `check-baseline`, the rtl-fast step that calls the gate, the docs gates, behave; the gate on dev `1e80128f`'s three recorded routes and #814's head routes.
Blockers: none
