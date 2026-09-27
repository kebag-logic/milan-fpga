[A360] TAKEN
Branch: `587-8x8-baseline-50mhz`, base `63fe4fb0164d798d44a6476001dc8b887cdd4609`.
Authoritative references: assignment 5855348441, #231 decisions 5844867171 and 5846064333, baseline recipe, REQUIREMENTS.md and CONTRIBUTING.md.
Interpreted scope: remeasure integrated 8x8 default synthesis and preserved-boundary attribution at the configuration's declared 50 MHz, retaining labelled 100 MHz history and reporting area delta and timing. No RTL, configuration or processor edits.
Independent reviewers: [R350] internal and [R351] external.
Validation plan: baseline self-test and maintained mutants, both documentation inventory modes, em-dash check at 63fe4fb0, document style, contents and anchors, paths, whitespace; full image/source hash and missing-ROM checks on both synthesis runs.
Blockers: none identified during recipe inspection. The explicit assignment authorizes this lane; the stale Backlog card is now In progress. Stop if synthesis cannot complete or using the declared clock needs more than deriving a recipe parameter. Local delivery only; no push or PR actions.
