[A587]

## Contents

- **[Status](#status)** -- Current validation state and heads.
- **[Linked Issue / roles](#linked-issue--roles)** -- Assignment and review roles.
- **[Description](#description)** -- Storage changes and integration corrections.
- **[Authoritative references](#authoritative-references)** -- Requirements and decisions.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Verify the local lane.
- **[How to validate](#how-to-validate)** -- Commands and results.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- Measurement and review limits.
- **[Definition of Done](#definition-of-done)** -- Outstanding merge requirements.

## Status

**REVIEW READY** on local `640-m7` -> `dev`; all assigned Round 4 continuation checks pass.

- Parent: `412e3f6c8c402bce63e94c291d2782b5579aaa1d`.
- Donor: `e4869fd0c42889b2ac806587cc5c78afb1c33461`.
- The parent merge preserves both `354f7818` and dev `fa820988`.
- The donor preserves the earlier `18dd997b` lane and incoming `61d486e9`.
- Both heads remain local. This body prepares the next independent review.

## Linked Issue / roles

Relates to #640

Executor: `[A587]`
Internal cleared-context reviewer: `[R592]`
External reviewer: `[R593]`

Assignment: issue #640, comment 6097272538.
Round 4 integration: comment 6161607579.
Continuation ruling: comment 6162175442.
Earlier positive reviews cover `354f7818` / `18dd997b`, not these heads.

## Description

M7 (plan L10a) reduces fabric gPTP storage area while preserving function,
registers, timestamps and read latency. The tap and transmit FIFOs encode
lane metadata compactly. Ledger fields, results and timer deadlines use
distributed RAM with the existing read behavior. The message bank remains
in distributed RAM after the block-RAM experiment increased logic use.

The following primitive mappings were measured in the `e8454e27` lineage,
with final routed M7 RTL at `49e1ce48`. They are historical measurements.

| Table | Before | After |
|---|---|---|
| Tap FIFO, 256 beats | RAMB36 + RAMB18 | One RAMB36 |
| Transmit FIFO, 256 beats | RAMB36 + RAMB18 | One RAMB36 |
| Ledger, 8 x 21 | 168 FF and read muxes | 4 RAM32M + 1 RAM32X1D |
| Results, 8 x 89 | 712 FF and read muxes | 16 RAM32M + 1 RAM32X1D |
| Deadlines, 8 x 32 | 256 FF and read mux | 5 RAM32M + 2 RAM32X1D |

Round 4 retains both measurement histories and incoming dev changes.
The donor clock self-test now separates fixture definitions from execution;
its production checks and all defect fixtures are unchanged. Four parser
test declarations now declare one variable each. The donor ROM paragraph
matches the generator: 1,016 words, eight free, `FUTO@249`.
The parent pin references, diagrams and ROM record follow the corrected donor.

Historical integrated M0s recipe measurements:

| Metric | Base `e8454e27` | M7 `49e1ce48` |
|---|---:|---:|
| LUT | 50,267 | 49,898 |
| FF | 54,413 | 53,220 |
| RAMB36 / RAMB18 | 74 / 27 | 74 / 25 |
| WNS / WHS, ns | +0.299 / +0.031 | +0.122 / +0.019 |

The route passed the record at `e8454e27` with every endpoint met.
The plane measurements in that lineage saved 107-253 LUTs, below the plan's
500 estimate (300-700), plus 1,149 FFs and one block-RAM tile.
None of these numbers qualifies the current merged tree. The continuation
ruling requires no physical remeasurement for this merge; the daily #640
measurement records the integrated effect the day after merging. D7 leaves
acceptance re-recording to M9.

## Authoritative references

- `REQUIREMENTS.md`, REQ-PTP-01 through REQ-PTP-09.
- `docs/design/MARK_II_AREA_PLAN.md`, L10a and the memory ledger.
- `docs/design/AREA_BUDGET.md` and `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`.
- `docs/design/GPTP_PLANE.md`, `docs/design/TIME_SYNC.md` and donor interfaces.
- Owner decisions D1, D3, D7 and D8, issue #640 comment 5990755268.
- IEEE 802.1AS-2011 and Milan v1.2 section 4.2.6; no new interpretation.

## How to get into the same state

Use the existing local lane. Its latest commits are not yet available remotely.
From the parent root:

```sh
git status --short --branch
git rev-parse HEAD HEAD^1 HEAD^2
git ls-files --stage gptp-processor
git -C gptp-processor rev-parse --show-toplevel
```

Verify that the last command names the submodule directory before further
Git commands inside it:

```sh
git -C gptp-processor status --short --branch
git -C gptp-processor rev-parse HEAD
```

Expected heads are listed under Status; both tracked trees are clean.
Use CPython 3.12.3, GNU make 4.3, pinned Verilator 5.050 and disk scratch.
The table mutation driver also requires Python's pidfd support; the supplied
3.12.3 build lacks it, so that driver uses the native interpreter.

## How to validate

```sh
python3 gptp-processor/syn/ooc/check_ooc_clock.py
python3 gptp-processor/syn/ooc/check_ooc_clock.py --selftest
MAKEFLAGS=w VERILATOR_JOBS=2 make -j8 -C gptp-processor/tb/verilator/parser run
make -C gptp-processor contract lint docs
python3 scripts/check_py_idiom.py
python3 scripts/check_cpp_idiom.py
MAKEFLAGS=w VERILATOR_JOBS=2 make -j8 -C tb/verilator/gptp_tables run limits
python3 tb/verilator/gptp_tables/mutants.py
MAKEFLAGS=w VERILATOR_JOBS=2 make -j8 -C tb/verilator/gptp_plane run
MAKEFLAGS=w VERILATOR_JOBS=2 make -j8 -C tb/verilator/gptp_plane phc-step
MAKEFLAGS=w VERILATOR_JOBS=2 make -j8 -C tb/verilator/gptp_shadow run
python3 scripts/gen_one_valued_table.py --check
python3 scripts/ci_scope.py --selftest
python3 scripts/ci_events.py --check
python3 scripts/check_gptp_docs.py --with-submodule
python3 scripts/check_submodule_docs.py
python3 docs/diagrams/submodule_boundaries.gen.py --check
python3 docs/diagrams/timesync_chain.gen.py --check
python3 scripts/check_diagram_pngs.py
python3 scripts/lint_rtl.py --check
python3 syn/ooc/pp_resource_gate.py check-baseline
python3 scripts/check_em_dash.py --base fa820988
```

Inside a disposable container with read-only source, no network, credentials
or Docker socket, run the offline workflow self-test:

```sh
python3 -I scripts/act_ci.py --selftest
```

The candidate script is not used as the host-side workflow orchestrator.
All listed gate results and complete receipts are recorded in HANDOFF.md.
Current results: table clean run 36/36 and all 26 table controls; plane 29/29;
PHC-step 62 clean checks and all eight arms; shadow 309/309; all 33 donor
engine mutants plus their clean controls; parser 337/337 and eight mutants;
gaskets 81/81 and four mutants; traffic generator 288/288 and three mutants.
All 35 parent static gates, CI contract checks, pin records and generated-asset
checks pass. The batch audit proves no missing or duplicated original entry.
The donor aggregate was interrupted to respect the command window; completed
constituents and disjoint mutation batches supply the passing evidence.
No aggregate rc-0 verdict is claimed.

## Known limitations / out of scope

- The new heads require independent review. Prior reviews do not approve them.
- Historical area and timing evidence applies only to the revisions named above.
- The table stimulus declares `ledger.tag`, `results.ok` and `results.gen`
  one-valued at 1. The declaration file and generated README identify the
  limits and complementary coverage. No declaration was weakened.
- Existing #714 limits per-segment coverage; this lane does not alter it.
- M10 shared execution and #117 physical evidence remain outside this assignment.
- No hardware access, new route, acceptance re-record, push or PR edit occurred.
- Full candidate-merge and hosted gates remain part of the later merge bar.

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

