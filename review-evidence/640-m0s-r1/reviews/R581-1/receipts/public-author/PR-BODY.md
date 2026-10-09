[A581]

## Contents

- **[Status](#status)** -- Tooling validation and route prerequisite.
- **[Linked Issue / roles](#linked-issue--roles)** -- Scope and independent reviewers.
- **[Description](#description)** -- Selected-placement measurement support.
- **[Authoritative references](#authoritative-references)** -- Requirements and assignment.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Reproduction setup.
- **[How to validate](#how-to-validate)** -- Exact checks and expected results.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- Missing integration and unmeasured resources.
- **[Definition of Done](#definition-of-done)** -- Remaining review and merge obligations.

## Status

Tooling validation passes (28 commands, all rc 0); selected route STOP.
`640-m0s` targets `dev`. No remote branch or review object was changed.
Head: `bc89f84e6757f8fcddf21958e99f40f17bc0ee1e`.
Base: `7c1b52bee26b497080ee22b1c1986109f80a5ee7`.

## Linked Issue / roles

Relates to #640.
Assignment: #640, comment 6086604096, M0s step 1.
Executor: `[A581]`.
Internal cleared-context reviewer: `[R580]`.
External reviewer: `[R581]`.

## Description

The measurement recipe previously required one protocol wrapper.
The complete split removes that wrapper.
Explicit `f0-f4` and `full-split` selections now measure integrated exports
without that assumption. They check actual engine populations before
implementation and again at the measurement endpoint. The resource reader
requires matching placement evidence, measures the whole image, and compares
against the unchanged shipping endpoint.

The all-fabric default and standalone 1x1/8x8 references retain their recipes.
The acceptance record shape, policy, thresholds and baseline remain unchanged.
Selected intermediate measurements cannot re-record acceptance; M9 owns it.
The documentation records the integration STOP and missing resource figures.

## Authoritative references

- #640 assignment, comment 6086604096.
- `REQUIREMENTS.md`, section 1; approved #664 placement requirements.
- `docs/design/MARK_II_AREA_PLAN.md`: lane sequence, intermediate ledger,
  firmware and block RAM ledger, D7.
- `docs/design/AREA_BUDGET.md`: unchanged resource comparison policy.
- `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`: selected measurement recipe.
- #665 F0-F4 foundations and parent integration prerequisite.

## How to get into the same state

Obtain the committed `640-m0s` lane and use a fresh checkout.
Initialize the pinned dependencies. Select an external disk-backed scratch
folder as `WORK`. Put the repository's pinned environments on `PATH`.

```sh
git checkout 640-m0s
git rev-parse HEAD
git submodule update --init protocol-processor gptp-processor third_party/verilog-axis
export TMPDIR="$WORK"
export PYTHONDONTWRITEBYTECODE=1
python3 -m pip install --require-hashes -r tools/markdown/requirements.txt
python3 -m pip install pyyaml
```

Before any dependency-local Git operation, verify its repository top-level.

## How to validate

```sh
python3 syn/ooc/pp_baseline.py --selftest
python3 syn/ooc/pp_baseline_mutants.py
python3 syn/ooc/pp_resource_gate.py --selftest
python3 -X cpu_count=4 syn/ooc/pp_resource_gate_mutants.py
python3 syn/ooc/pp_resource_gate.py check-baseline
python3 syn/ooc/pp_baseline_reports_selftest.py
python3 syn/ooc/ooc_tcl_selftest.py
python3 scripts/pp_srcs.py --check --selftest
python3 scripts/docs_check.py
python3 scripts/check_py_idiom.py
python3 scripts/gen_toc.py --check
python3 scripts/check_em_dash.py --base "$(git merge-base origin/dev HEAD)"
git diff --check
```

Expected result: every command exits zero; every planted defect is caught.
Observed: 41 recipe mutations and 180 resource mutations detected; 58 OOC
refusal arms pass. The unchanged resource self-test retains 260 arms and 500
seeded cases. The added-line documentation gate passes all 339 controls.
Self-tests judge synthetic measurements, not a physical implementation.
The handoff contains the full command and evidence table.

## Known limitations / out of scope

- At base `7c1b52be`, the mailbox has idle datapath inputs and discarded TX.
  The fabric wrapper is unconditional. The existing switch does not produce
  F0-F4 ownership. Parent integration must connect the datapath first.
- No selected route was launched. LUT, FF, slices, RAM primitives and timing
  remain unmeasured for the selected image. No memory reclamation is credited.
- The population census proves engine presence or absence. It cannot prove
  firmware execution, mailbox wiring, service deadlines or bench qualification.
- The later route owes actual firmware allocation against the 121.5-tile
  ceiling and separate 10 percent reserve. Partial placement cannot claim
  complete-split storage removal.
- No RTL, firmware behavior, shipping default, policy, threshold or accepted
  resource record changes belong to this lane. Independent review remains open.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per CONTRIBUTING.md
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
