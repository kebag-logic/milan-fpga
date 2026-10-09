M0s: split-aware resource measurement support for selected placements (#640) | head 6904af6b79aae0566e6e47979223f54b8ba0eb6f | draft false | base dev
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
- **[Round 2](#round-2)** -- Answers to the first review round.
- **[Round 3](#round-3)** -- Answers to the second review round.

## Status

Tooling validation passes (51 commands, all rc 0, on the hosted runner's CPython 3.12.3 and a newer CPython); selected route STOP.
`640-m0s` targets `dev`. The author completed this work locally before publication.
Head: `6904af6b79aae0566e6e47979223f54b8ba0eb6f` (round 3).
Round-2 head: `d10aee62100c7407a86e13e7d54b20ab9050a448`.
Round-1 head: `bc89f84e6757f8fcddf21958e99f40f17bc0ee1e`.
Base: `7c1b52bee26b497080ee22b1c1986109f80a5ee7`.

## Linked Issue / roles

Relates to #640.
Assignment: #640, comment 6086604096, M0s step 1; round 2: comment 6087671877; round 3: comment 6089650427.
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

The default all-fabric selection keeps its recipe byte for byte.
For an integrated route, the gate now also checks its control-engine population.
It reads the hierarchy report's module column, and `check` and `record --write`
refuse any role outside its all-fabric count by name.
The standalone 1x1/8x8 references retain their recipes and checks.
The acceptance record shape, policy, thresholds and baseline remain unchanged.
Selected intermediate measurements cannot re-record acceptance; M9 owns it.
The documentation records the integration STOP and missing resource figures.

## Authoritative references

- #640 assignment, comment 6086604096; round 2, comment 6087671877.
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
Observed at the round-2 head:
- 45 recipe mutations and 191 resource mutations are detected, each with its control passing;
- the 58 OOC refusal arms pass;
- the resource self-test retains 260 arms and 500 seeded cases;
- the added-line documentation gate passes all 339 controls.

Each campaign driver also fails if its self-test skips the placement controls.
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
- The default census applies to integrated routes. Standalone references lack
  the parent MAAP, gPTP and mailbox, and they keep their legacy checks.
  A printed record without `--write` is not judged.
- Two rows of the first review's parity probe (`fuzz 3000 seed 234` and the
  self-test line prefix) differ by necessity. The manager ruled this difference
  expected (#640 comment 6089329720); see Round 2.
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

## Round 2

Round 2 answers R580-1 (NEGATIVE: two MINOR findings) and R581-1 (POSITIVE).
It adds three commits on `bc89f84e`, with no rebase or amend.

| Commit | Subject |
|---|---|
| `b1f110be788855bdb7461969bb939d597a756e10` | Reject incomplete all-fabric control populations in resource measurements |
| `d4447e1b98539e5ff52c05c75cb3c229a409514e` | Judge the default route's control population after identity and test the split marker and retained ROM geometry |
| `d10aee62100c7407a86e13e7d54b20ab9050a448` | Document the default route's population check and the recipe's split marker and retained ROM controls |

**R580-1-F1 (default population).**
Under the default selection, `check` and `record --write` now exit 2 for an
integrated route whose hierarchy report holds any control role in other than
its all-fabric number. Each such role is named.
- A wrapper-retaining F0-F4 hierarchy without a marker names ADP, both ACMP engines, SRP and MAAP.
- An all-fabric export with SRP removed names SRP.
- A split census left in a default directory is refused.
- The population is judged after the existing identity comparison, so a recorded endpoint's existing check results are unchanged.
- The census passes all 23 published integrated route reports, including the accepted route-1x1 report.
- The cited plan and budget sentences are now accurate and stay unchanged; the recipe page states the check.

**R580-1-F2 (tests).**
- The recipe self-test requires exactly one marker naming the requested selection, accepted by the gate's selection check.
- An F0-F4 or full-split export that still binds a removed protocol's ROM keeps that ROM in its inventory. A short or narrow image is refused naming the image.
- B4 and B5 are in the recipe campaign, and both are detected.

**Optional S1.** B1, B6 and G10 now have controls and campaign entries.
Each campaign driver also fails when its self-test skips the placement controls (G13, B9).
**S2** is not adopted: placement of the remaining blocks belongs to the integration lane.

**Reviewer probes, unmodified.**
- P1: 29 of 34 detected, including B4 and B5.
- P3: every default-selection case that documented F1 now exits 2, with the baseline unchanged.
- P2: 18 of 20 rows IDENTICAL. These cover every recipe output, `check-baseline` on the real record, `record` of both legacy fixtures, and `check` of the legacy fixture against the real record.

**P2 `fuzz` and self-test line prefix (ruled expected in #640 comment 6089329720).**
Both rows run the gate's own synthetic fixture. At the base, its route hierarchy named no control engine, the very population F1 requires refusing. The fixture therefore now names the shipping population, and those two rows cannot stay byte-identical without a fail-open exemption.
- The 210 legacy arm lines are identical; only the seeded fuzz tallies differ, with zero failures on both sides.
- Base and head code on the same new fixture differ only in 17 of 3000 seeded hierarchy mutations that removed or misordered a control-role row.

**Validation.** 28 local commands, all rc 0 at the round-2 head. Re-review is required in all five lenses.

## Round 3

Round 3 answers R580-2 (NEGATIVE: one BLOCKER) and R581-2 (NEGATIVE: one MAJOR), which name the same defect.
It adds one commit on `d10aee62`, with no rebase or amend.

| Commit | Subject |
|---|---|
| `6904af6b79aae0566e6e47979223f54b8ba0eb6f` | Call the gate in its documented order in the default-population self-test and pin the unjudged printed record |

**R580-2-F1 = R581-2-F1 (argument order on the hosted interpreter).**
The round-2 default-population arms called `record --write <directory>`. The gate has two optional positionals, and the hosted runner's CPython 3.12.3 binds both at the command word, so it rejected the directory. Hosted `yosys-elaboration` therefore failed, and `rtl-fast` with it.
- Both arms now call the gate in its documented order, `check <directory> --endpoint ...` and `record <directory> --endpoint ... --write` (`syn/ooc/pp_placement_selftest.py:242-260`).
- No assertion is weakened. Each wrong population is still refused with exit 2 naming each role under `check` and `record --write`, and the baseline bytes are still compared.
- Every other self-test and mutation driver was searched for the same order, and none uses it.
- The product refusal was already correct in the documented order; no product code changed.

**R580-2-S1 (optional, adopted).**
- A printed `record` of each wrong population now exits 0 and prints the record, as documented (`pp_placement_selftest.py:254-255`). The exception is an absent wrapper, which has no record root.
- The gate campaign gains the mutant that judges a printed record. It grows from 191 to 192, all detected.

**R580-2-R1 = R581-2-R1.** The P2 ruling is now stated as decided in Known limitations and in Round 2.

**Planted defects.**
- Reverting either call to the old order fails the gate self-test on CPython 3.12.3 with the hosted job's assertion. It passes on the newer interpreter, where both orders parse alike, so hosted `yosys-elaboration` is the check that catches this class.
- Judging a printed record fails on both interpreters.

**Validation.** All 51 commands exit 0 at `6904af6b`.

Run on both CPython 3.12.3 (hosted-equivalent) and the host's newer CPython:
- the failing hosted step, command for command (`.github/workflows/rtl-fast.yml:207-216`): the gate self-test with 138 placement lines; the gate campaign, control and 192 of 192; the recipe campaign, control and 45 of 45; `check-baseline`; 58 OOC arms; the `dp_srcs` self-test and both tops;
- the reviewers' P1 (29 of 34, unchanged) and P4 (0 unexpected), unmodified.

Run on CPython 3.12.3 only: the job's two later Yosys steps.

Run on the host only:
- P2 (18 of 20 IDENTICAL, the two others as ruled) and P3;
- documentation, TOC and anchors;
- the em-dash gate, 339 of 339 arms;
- the idiom, hygiene and evidence ratchets;
- lint at 90 of 90;
- `git diff --check`.

The 212 legacy self-test lines are byte-identical at base, at round 2 and at this head on both interpreters.

The manager pushes, and confirms that hosted `yosys-elaboration` and `rtl-fast` are green, before the delta reviews.

