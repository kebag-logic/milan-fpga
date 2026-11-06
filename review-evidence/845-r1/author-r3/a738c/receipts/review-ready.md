[A738c] REVIEW READY
Commit: bf6c5a67778a5e5d479ae51b3b4377ad4f763801
Changed: on top of `b16f0175`, six commits, documentation and one comment, no synthesis input. F1: `docs/design/AREA_BUDGET.md`, the pin page and the CHANGELOG record the route figures, the gate state and the decision as pending. F2: the pin page, the CHANGELOG and the integration contract state what a registered settled input does at a link change (Milan v1.2 5.5.3.5.48, Table 5.5, 5.4.2.10.1 Table 5.9). F3: the `tb/verilator/pp_shadow/sim_main.cpp` group U comment states what row U states. F4: the prepared PR body names the measured head of each result. `docs/DOCUMENTATION_AUDIT.md` through its generator.
Validation:
- Resource gate in its own form, measured at `b16f0175`: `route-1x1` **exit 1** (ExtraTimingOpt selected, WNS +0.373 ns; LUT 52,529, +517 of +500; FF 54,582, +875 of +600). `ooc-1x1` **exit 1** (LUT 24,996, +650 of +250; FF 20,934, +530 of +250). No re-baseline; `check-baseline` rc 0. `ooc-8x8` not measured.
- `.github/workflows/docs.yml` at this head, clean clones: 72 `run:` steps exit 0, 24 not run with a reason on record, 0 bad.
- `docs_inventory.py --check` after `--write` rc 0; `git diff --check 87e9d03a HEAD` rc 0; privacy check rc 0, 0 private lines.
- `make -C tb/verilator/pp_shadow run` rc 0 at `bf0d7d10`, the last change to that file: 719, 317, 759 and 719 checks, 0 failures.
- No full sweep this round, as assigned: the sweep, firmware self-test, builder and behave results remain those at `519d9c2b`.
Acceptance criteria: the issue's items are met as written, with those results at `519d9c2b` and the route meeting the WNS floor on all three directives. F2, F3 and F4 are fixed for re-review.
Open risks/questions:
- **F1 stays open and blocks merge: the owner decision is pending.** The gate refuses this growth on both endpoints.
- New since the reviews: the gate selects ExtraTimingOpt, so LUT is refused too, and `docs/integration/BUILDING.md` section 5 builds the shipping image from that directive, which leaves 15 of 15,850 slices free, not 70.
- The deltas are from the `f65c8ff7` records and include dev's own movement. No `ooc-1x1` figure exists at dev's pin `a9e84b66`, so this adoption's share of that endpoint is not measured.
- Whether `ooc-8x8` is needed is for the decision to say.
- The processor's `docs/guides/integrator.md` carries the sentence F2 corrected here and needs a processor follow-up.
