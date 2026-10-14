[A587]

## Contents

- **[Status](#status)** -- Current heads and validation.
- **[Linked Issue / roles](#linked-issue--roles)** -- Assignment and review roles.
- **[Description](#description)** -- Storage changes and measured results.
- **[Authoritative references](#authoritative-references)** -- Requirements and decisions.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Revision checks.
- **[How to validate](#how-to-validate)** -- Reproduction and expected results.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- Evidence limits.
- **[Definition of Done](#definition-of-done)** -- Remaining merge requirements.
- **[Round 5](#round-5)** -- Scheduler integration and corrected reach.
- **[Round 6](#round-6)** -- Worker-count documentation and publication wording.

## Status

- Published parent: `4c5d70b50230fbd5da347852d39daf7f23b3df0b`.
- Published donor: `e4869fd0c42889b2ac806587cc5c78afb1c33461`.

REVIEW READY at the published parent and donor revisions listed above.

Round 6's local continuation is listed below, pending publication and review.
Branch: `640-m7` -> `dev`.

## Linked Issue / roles

Relates to #640

Executor: `[A587]`
Internal cleared-context reviewer: `[R592]`
External reviewer: `[R593]`

Issue comments 6097272538, 6161607579 and 6162175442 define the earlier work.
Comments 6163132636 and 6164557611 define Rounds 5 and 6.
Round 5 resolved R592-4-F1, R593-4-F1 and R593-4-F2.
Round 6 answers R592-5-F1 and the optional R592-5-S1.
R593-4-D1 supplies the publication wording below; corrected-head review remains pending.

## Description

M7 reduces fabric gPTP storage area while preserving function and latency.
The tap and transmit FIFOs encode lane metadata compactly.
Ledger fields, results and timer deadlines use distributed RAM.
The message bank and required multi-read operand files retain their storage.
Registers, timestamps and default placement remain unchanged.

Historical primitive mappings in the `e8454e27` lineage, routed at `49e1ce48`:

| Table | Before | After |
|---|---|---|
| Tap FIFO, 256 beats | RAMB36 + RAMB18 | One RAMB36 |
| Transmit FIFO, 256 beats | RAMB36 + RAMB18 | One RAMB36 |
| Ledger, 8 x 21 | 168 FF plus mux | 4 RAM32M + 1 RAM32X1D |
| Results, 8 x 89 | 712 FF plus mux | 16 RAM32M + 1 RAM32X1D |
| Timer, 8 x 32 | 256 FF plus mux | 5 RAM32M + 2 RAM32X1D |

Historical integrated M0s measurements:

| Metric | Base `e8454e27` | M7 `49e1ce48` |
|---|---:|---:|
| LUT | 50,267 | 49,898 |
| FF | 54,413 | 53,220 |
| RAMB36 / RAMB18 | 74 / 27 | 74 / 25 |
| WNS / WHS, ns | +0.299 / +0.031 | +0.122 / +0.019 |

The historical route passed its recorded gate with every endpoint met.
Plane savings were 107-253 LUTs, below the 500 estimate (300-700),
plus 1,149 FFs and one block-RAM tile.
These measurements do not qualify the merged tree.
The owner assigns the integrated remeasurement to the post-merge daily run.
D7 reserves acceptance re-recording for M9.

Round 4 preserves both merge inputs and measurement histories.
Its donor style corrections retain all clock fixtures and parser behavior.
ROM documentation matches generation: 1,016 words, eight free, `FUTO@249`.

## Authoritative references

- `REQUIREMENTS.md`, REQ-PTP-01 through REQ-PTP-09 and REQ-VER-01.
- `docs/design/MARK_II_AREA_PLAN.md`, L10a and the memory ledger.
- `docs/design/AREA_BUDGET.md` and `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`.
- `docs/design/GPTP_PLANE.md` and donor integration contracts.
- `scripts/suite_shards.py`, documented new-suite procedure.
- `docs/testing/TESTING.md` and `docs/testing/CI_WORKFLOWS.md`.
- IEEE 802.1AS-2011 and Milan v1.2 section 4.2.6.

## How to get into the same state

Check out the published parent revision and initialize its pinned submodules.
The Round 6 continuation remains local until publication.
From the selected parent checkout:

```sh
git status --short --branch
git rev-parse HEAD
git ls-files --stage gptp-processor
git -C gptp-processor rev-parse --show-toplevel
```

Confirm the donor root before further Git commands inside it:

```sh
git -C gptp-processor status --short --branch
git -C gptp-processor rev-parse HEAD
```

Use the pinned simulator 5.050, GNU make 4.3 and CPython 3.12.3.
Install declared Python dependencies in a separate scratch environment.
Process-ownership tests require an interpreter with pidfd support;
the supplied 3.12.3 build lacks it, so those checks used native Python.
Build in a disposable checkout on disk scratch.

## How to validate

```sh
python3 scripts/suite_shards.py --selftest
python3 scripts/ci_events.py --check
python3 scripts/ci_events.py --selftest
python3 scripts/ci_scope.py --selftest
for index in 0 1 2 3 4 5; do
  scripts/run_all_suites.sh --shard "$index/6" --list
done
scripts/run_all_suites.sh --list
MAKEFLAGS=w VERILATOR_JOBS=2 make -j8 -C tb/verilator/gptp_tables run limits
MAKEFLAGS='w -j8' VERILATOR_JOBS=2 python3 tb/verilator/gptp_tables/mutants.py
python3 scripts/gen_one_valued_table.py --check
python3 scripts/check_py_idiom.py
python3 scripts/check_cpp_idiom.py
python3 scripts/docs_check.py
python3 scripts/check_em_dash.py --base 412e3f6c
```

Expected: 63 default suites, each owned exactly once; `gptp_tables` on 0/6,
`milan_dp` alone on 5/6. Predicted maximum 3,747 seconds is below 4,320.
CI contract: 2,175 items and 3,096 self-test arms pass.
Table baseline: 36/36; controls: 26/26 caught by their named checks.
Observed TX depth is 25, result depth two, with 111 writes behind a waiting result.
All eight serial preflight gates also pass; their plain commands and receipts
are recorded in the Round 5 handoff. No full sweep is claimed this round.

## Known limitations / out of scope

- The 1,800-second suite duration and new-worker overhead remain provisional.
  Replace them from the first successful hosted run under selector step 3.
- The local component times total 424.738 seconds across separate executions;
  this is neither a hosted measurement nor one default-target wall time.
- The executor performed no push or PR edit during implementation.
  The listed published revisions reflect subsequent publication.
- Round 6 ran no route, hardware operation or merge.
- Historical resource figures retain their original revision limits.
- Full banks, required hosted contexts and current-dev candidate validation
  remain integration duties. The donor must land before parent pin adoption.
- Earlier residues and optional suggestions remain assigned as reviewed.
  The optional inert ROM-ledger row remains unchanged.

## Definition of Done

- [x] Round 5 and Round 6 assigned corrections are implemented
- [x] Round 5 scheduler, contract, preflight and focused checks pass
- [x] Round 6 documentation, CI contract and prose-style gates pass
- [x] Generated table and measured-reach descriptions are current
- [x] No requirement, RTL or interface change remains undocumented
- [ ] Corrected-head internal and external reviews are positive
- [ ] Hosted measurements replace provisional duration and overhead
- [ ] Required local and hosted merge bar passes
- [ ] No review round remains in flight
- [ ] Current-dev candidate and post-merge containment are validated

## Round 5

`fb4d30b1a` adds the required provisional inventory entry and sixth worker.
It updates ownership, aggregate expectations and every affected defect fixture.
Timeouts and headroom limits remain unchanged; no suite is dropped or renamed.
`90f75192f` corrects only two README figures and two C++ comment lines.
The baseline output is byte-identical before and after those comment edits.
`4c5d70b50` advances the final stale-denominator fixture; all 3,096 arms pass again.
The donor remains `e4869fd0c42889b2ac806587cc5c78afb1c33461`.

## Round 6

Parent continuation: `7fb3664b9b53d0c4caa4b64415dd9cc3e850e4b0` (local, unpushed).
Donor unchanged at the published revision above.

`docs/testing/CI_WORKFLOWS.md:1322` defines the expected artifact count
as the worker matrix size, with the current six/four values.
Lines 1337-1338 match the existing seven-worker, stale-six fixture.
Only this documentation file changes in the repository.
R593-4-D1's exact publication wording replaces the stale local-only prose.
The status separates the published revisions from this local continuation.

```sh
python3 scripts/docs_check.py
python3 scripts/ci_events.py --check
python3 scripts/check_doc_style.py
```

All three commands return 0 under CPython 3.12.3.
The CI contract checks 2,175 items; prose style checks 22 documents.
A direct comparison also confirms the documented counts match both matrices
and aggregate verifiers. These checks supply documentation evidence only.
Historical table controls and M0s resource figures retain their stated limits.
