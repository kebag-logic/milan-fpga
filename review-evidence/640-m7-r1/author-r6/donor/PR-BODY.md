[A587]

## Contents

- **[Status](#status)** -- Current heads and review state.
- **[Linked Issue / roles](#linked-issue--roles)** -- Assignment and review roles.
- **[Description](#description)** -- Timer storage and integration corrections.
- **[Authoritative references](#authoritative-references)** -- Governing contracts.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Revision checks.
- **[How to validate](#how-to-validate)** -- Commands and evidence.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- Measurement limits.
- **[Definition of Done](#definition-of-done)** -- Remaining review requirements.
- **[Round 5](#round-5)** -- Unchanged donor and parent integration fix.

## Status

REVIEW READY with the unchanged published donor revision.
Donor: `e4869fd0c42889b2ac806587cc5c78afb1c33461`.
Parent: `4c5d70b50230fbd5da347852d39daf7f23b3df0b` (local continuation).
Both tracked trees are clean. Round 5 adds no donor commit or push.

## Linked Issue / roles

Relates to #640 in the parent repository.

Executor: `[A587]`
Internal cleared-context reviewer: `[R592]`
External reviewer: `[R593]`

Parent issue comments 6097272538, 6161607579 and 6162175442 govern prior work.
Comment 6163132636 defines Round 5's parent-only corrections.

## Description

M7 timer deadlines use distributed RAM, retaining indexed writes and
combinational sweep reads. Reset clears the armed bits that gate readers.
Merge `6b5a4282` preserves M7 `18dd997b` and incoming main `61d486e9`.
Its documentation conflict retains both measurement histories.

The following style commit separates clock fixture construction from execution.
All 29 defect fixtures and production checks remain unchanged.
Four parser declarations each declare one variable.
ROM documentation matches generation: 1,016 words, eight free, `FUTO@249`.

Historical standalone measurements at `18dd997b` against `5dce647a`
used the then-unconstrained flow:

| Metric | Before | After |
|---|---:|---:|
| Engine LUT | 4,853 | 4,748 |
| Engine FF | 3,652 | 3,396 |
| Memory LUT | 466 | 490 |
| BRAM tiles / DSP | 1.5 / 4 | 1.5 / 4 |
| WNS, ns | +1.773 | +2.249 |

Deadline storage changed from 256 FF plus a mux to
5 RAM32M and 2 RAM32X1D. These measurements qualify neither the merged
donor nor the merged parent. The owner assigns the integrated measurement
to the parent's post-merge daily run.

## Authoritative references

- Parent requirements, Mark II plan L10a and firmware memory ledger.
- Parent area budget and M0s recipe; D7 reserves re-recording for M9.
- `docs/INTEGRATION.md`, `docs/MANAGER.md`, `docs/TEST_DEVELOPER.md`.
- IEEE 802.1AS-2011 and Milan v1.2 section 4.2.6.

## How to get into the same state

Use the published donor revision above or the parent's exact pinned checkout.
From the parent root, verify the donor directory before further Git commands:

```sh
git -C gptp-processor rev-parse --show-toplevel
```

After confirming that directory:

```sh
git -C gptp-processor status --short --branch
git -C gptp-processor rev-parse HEAD
```

## How to validate

From a parent checkout with disk scratch and the pinned compiler:

```sh
python3 gptp-processor/syn/ooc/check_ooc_clock.py
python3 gptp-processor/syn/ooc/check_ooc_clock.py --selftest
MAKEFLAGS=w VERILATOR_JOBS=2 make -j8 -C gptp-processor/tb/verilator/parser run
make -C gptp-processor contract lint docs
python3 scripts/check_py_idiom.py
python3 scripts/check_cpp_idiom.py
MAKEFLAGS=w VERILATOR_JOBS=2 make -j8 -C tb/verilator/gptp_tables run limits
MAKEFLAGS='w -j8' VERILATOR_JOBS=2 python3 tb/verilator/gptp_tables/mutants.py
```

Round 4 receipts at this unchanged donor record clock 30/30,
parser 337/337 with identical before/after output, 33 engine mutants,
eight parser mutants, gaskets 81/81 plus four mutants, and traffic-generator
288/288 plus three mutants. Constituents pass; the interrupted aggregate
has no aggregate rc-zero claim.

Round 5 freshly passes the parent table baseline 36/36 and all 26 controls.
The donor timer participates unchanged. Parent Python/C++ gates pass.
The handoff identifies all commands, planted defects and receipt hashes.

## Known limitations / out of scope

- Round 5 reruns no donor-only bank, route or physical measurement.
- Historical area and timing figures apply only to their named revisions.
- No protocol, register-map, timestamp or default-placement change is added.
- Corrected-parent review and required hosted evidence remain pending.
- Land this donor before parent pin adoption; validate containment afterward.

## Definition of Done

- [x] Donor corrections retain behavior and fixture coverage
- [x] Round 4 donor constituent evidence is retained at this revision
- [x] Round 5 parent integration checks pass
- [ ] Corrected-parent independent reviews are positive
- [ ] Required contexts and current-dev candidate validation pass
- [ ] No review round remains in flight
- [ ] Donor/parent merge ordering and containment are complete

## Round 5

No donor file changed. The parent now records `gptp_tables` provisionally
at 1,800 seconds and schedules six workers under the unchanged headroom rule.
All 63 default suites have complete, disjoint ownership; the contract passes
2,175 items and 3,096 defect controls, and the serial preflight passes.
Current reach descriptions now match TX depth 25 and result depth two.
The suite duration and new-worker overhead await a successful hosted measurement.
