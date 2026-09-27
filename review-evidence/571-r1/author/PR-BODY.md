[A371]

Closes #571

Status: ready for independent review.

The processor previously inherited three unit-count defaults. The builder now
emits `AEM_N_CONTROL_C` from `descriptor_counts`, and the datapath and shadow
wrapper forward AUDIO_UNIT, CLOCK_DOMAIN and CONTROL counts into `u_pp`.
The parent retains `N_CLK_DOM_P`. Model construction always emits these
mandatory descriptor classes, so no zero-count refusal is needed.

All five tracked configurations retain counts of 1/1/1. Each header adds only
the CONTROL line; the other 13 generated artifacts per configuration remain
byte-identical. AX 1x1 and 8x8 post-elaboration statistics match the base.
The shape gate checks both binding hops, headers and descriptor-directory
counts; all 24 new mutants are killed.

Reproduce and validate: run the full builder bank in compiler-present and
compiler-absent modes, `sw/builder/test_declarations.py`,
`scripts/check_entity_shape.py --self-test`, `scripts/check_nvm_capture.py`,
the documentation gates, and `git diff --check` from the repository root.
Detailed commands, artifact hashes, header diffs, statistics and gate results
are recorded in the author handoff.

Validation: both full builder modes and every assigned gate returned rc 0.
The final shape self-test reports 219 checks and zero failures. Both builder
runs lack the historical resource-calibration report; the absent mode also
intentionally skips the compiler-backed census, exercised in the present run.

Reference note: the assigned `docs/spec-refs.md` is absent. The decision
record uses the assignment's Milan v1.2 Section 5.3.3 citation and verifies
positive counts directly in both model and descriptor constructors.

DoD: acceptance evidence complete; independent review pending. The processor
pin and sources are unchanged.
