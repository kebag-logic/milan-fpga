[A738d] REVIEW READY
Commit: 853ca25ae00fe26b09e019fbfe70893666617fc1
Changed: on top of `bf6c5a67`, three commits, no synthesis input. `syn/ooc/pp_resource_baseline.json`: `route-1x1`, `ooc-1x1` and `ooc-8x8` re-recorded through `pp_resource_gate.py record --write`, and their `measured` notes; no tolerance, floor or ceiling moved. `docs/design/AREA_BUDGET.md`, `docs/reference/SUBMODULES.md` and `CHANGELOG.md` state the maintainer decision (issuecomment-6689114981), keeping the figures, the three directives and the 15 slices. `docs/findings/234_PP_SHADOW_AREA_BASELINE.md`, its index and `docs/design/MARK_II_AREA_PLAN.md` carry the thirteenth record, because each states the current record. `docs/DOCUMENTATION_AUDIT.md` through its generator.
Validation:
- Against the twelfth record, `check` exits 1 on all three: `route-1x1` (ExtraTimingOpt selected, WNS +0.373 ns; LUT 52,529, +517 of +500; FF 54,582, +875 of +600), `ooc-1x1` (LUT 24,996, +650 of +250; FF 20,934, +530 of +250), `ooc-8x8` (LUT 36,864, +2,708 of +316; FF 32,036, +2,254 of +339).
- At this head, on a clean clone: `check` exits 0 on `route-1x1`, `ooc-1x1` and `ooc-8x8`; `check-baseline` exits 0. The route and `ooc-1x1` are measured at `b16f0175`, `ooc-8x8` at `bf6c5a67`, out of context only.
- `.github/workflows/docs.yml` at this head, clean clones: 72 `run:` steps exit 0, 24 not run with a reason on record, 0 bad.
- `docs_inventory.py --check` rc 0; `git diff --check 87e9d03a HEAD` rc 0; privacy check rc 0, 0 private lines.
- No full sweep, as assigned: the sweep, firmware self-test, builder and behave results remain those at `519d9c2b`.
Acceptance criteria: met as written, with those results at `519d9c2b`. All four items of the round 3 ruling are done; `Closes #845` stays.
Open risks/questions:
- New finding, not fixed: a re-export does not reproduce the record's `inputs_sha256`. The generated top's module-tree block comment changes order between exports of one commit, and the gate strips only `//` comments. With that comment removed, all three endpoints' inputs at this head equal the measured exports. No result here depends on it; it needs a new Issue.
- The `ooc-8x8` growth is nearly all the SRP listener, +2,279 LUTs and +2,239 FFs. 8x8 is not the shipping image the decision names; the ruling orders all three endpoints re-baselined.
- The selected route leaves 15 of 15,850 slices free. The integrated image with every lab fix is not measured here.
- The deltas include dev's movement since `f65c8ff7`. This adoption's share of the standalone growth is not measured.
