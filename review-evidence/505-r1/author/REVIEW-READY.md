[A155] REVIEW READY (author handoff; manager validation pending)

Commit: `6af65a151663e1301f1983a6c9d22650a0b35da9`

Changed: `scripts/ci_events.py` pins all 56 carrier run bodies, retains the
specialized/sequence protections, and adds reason-pinned controls.
`docs/testing/CI_WORKFLOWS.md` records the closed residue and maintenance remedy.
Workflow YAML and gate semantics are unchanged.

Validation: `python3 scripts/ci_events.py --check` passes 1505 items;
`python3 scripts/ci_events.py --selftest` passes 931 arms. The new population
contains 243 workflow mutations and 57 record controls. A zero-finding checker
fails all 833 workflow mutations; disabling only the new comparison fails all
187 body assertions with specialized checks still active. Mutation labels
are unique.

`python3 -B scripts/docs_check.py`, `python3 scripts/gen_toc.py --check`,
`python3 scripts/check_doc_paths.py`, Python idiom gate/selftest (54/54),
ci_scope selftest, baremetal-only check, control-flow selftest (45/45),
documentation style, and post-commit em-dash check all pass. Lint passes at
90/90; real xvlog analysis passes at its existing four processor findings and
zero parent findings. Build parallelism was capped at 8. Exact commands and
logs are in the author HANDOFF.md.

Acceptance: AC1-4 are supported by the focused evidence. AC5's isolated
real-act fixture/recipe is prepared but NOT RUN. It requires a green tampered
idiom step, both named contract refusals, a failed complete docs-check job,
and both failed exhaustive aggregates. No measured AC5 result is claimed.

Open work: manager-owned complete parent RTL/local bar, publication, trusted
exact-head replicas, required hosted evidence, AC5 receipts, and cold
R219/R220 review. No implementation design decision remains. This comment is
author evidence, not a review verdict or a claim that the merge bar is met.
