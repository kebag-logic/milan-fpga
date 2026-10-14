[A587]

## Contents

- **[Status](#status)** -- Local donor and parent heads.
- **[Linked Issue / roles](#linked-issue--roles)** -- Assignment and review roles.
- **[Description](#description)** -- Timer storage, merge and style corrections.
- **[Authoritative references](#authoritative-references)** -- Governing contracts.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Local state checks.
- **[How to validate](#how-to-validate)** -- Required commands and evidence.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- Historical measurement limits.
- **[Definition of Done](#definition-of-done)** -- Remaining review requirements.

## Status

**REVIEW READY** on local `640-m7`; all donor constituent checks pass.
Donor head: `e4869fd0c42889b2ac806587cc5c78afb1c33461`.
Parent head: `412e3f6c8c402bce63e94c291d2782b5579aaa1d`.
Both tracked trees are clean; neither head was pushed.

## Linked Issue / roles

Relates to #640 in the parent repository.

Executor: `[A587]`
Internal cleared-context reviewer: `[R592]`
External reviewer: `[R593]`

Parent issue #640 comments 6097272538, 6161607579 and 6162175442 govern this work.
Prior reviews cover `18dd997b`, not the new donor head.

## Description

The M7 timer deadlines use distributed RAM, retaining their indexed write and
combinational sweep read. Reset still clears the armed bits that gate readers.
The local merge `6b5a4282` retains M7 `18dd997b` and incoming main `61d486e9`.
Its only conflict, `docs/MANAGER.md`, preserves both measurement histories.

The continuation fixes the parent integration style failures. The clock
self-test separates fixture construction from execution and documents its
nested evaluator. All 29 defect fixtures, expected findings and production
functions remain unchanged. Four parser test declarations now declare one
variable each. The ROM paragraph now matches the generator: 1,016 of 1,024
words (99.2%), eight free, `FUTO@249` outside the prefix.

Historical standalone measurements at `18dd997b`, compared with `5dce647a`,
used the then-unconstrained flow:

| Metric | Before | After |
|---|---:|---:|
| Engine LUT | 4,853 | 4,748 |
| Engine FF | 3,652 | 3,396 |
| Memory LUT | 466 | 490 |
| BRAM tiles / DSP | 1.5 / 4 | 1.5 / 4 |
| WNS, ns | +1.773 | +2.249 |

The deadline mapping changed from 256 FF plus a read mux to 5 RAM32M and
2 RAM32X1D. These measurements do not qualify the current donor or merged
parent. The continuation ruling requires no new physical measurement here;
the daily parent #640 measurement records the merged effect after merging.

## Authoritative references

- Parent `REQUIREMENTS.md`, Mark II plan L10a and the firmware memory ledger.
- Parent area budget and M0s recipe; D7 reserves acceptance re-recording to M9.
- `docs/INTEGRATION.md`, `docs/MANAGER.md`, `docs/TEST_DEVELOPER.md`.
- IEEE 802.1AS-2011 and Milan v1.2 section 4.2.6.

## How to get into the same state

Use the current local parent lane; these heads have not been published.
From the parent root, verify the donor root first:

```sh
git -C gptp-processor rev-parse --show-toplevel
```

After confirming it names that submodule directory:

```sh
git -C gptp-processor status --short --branch
git -C gptp-processor rev-parse HEAD
```

## How to validate

From the parent root:

```sh
python3 gptp-processor/syn/ooc/check_ooc_clock.py
python3 gptp-processor/syn/ooc/check_ooc_clock.py --selftest
MAKEFLAGS=w VERILATOR_JOBS=2 make -j8 -C gptp-processor/tb/verilator/parser run
make -C gptp-processor contract lint docs
python3 scripts/check_py_idiom.py
python3 scripts/check_cpp_idiom.py
MAKEFLAGS=w VERILATOR_JOBS=2 make -j8 -C gptp-processor tb
```

Use the pinned compiler, CPython 3.12.3 and GNU make 4.3 with disk scratch.
The clock checks pass 30/30 before and after; all parser output matches,
337/337 checks. Parent Python/C++ gates pass without exceptions or budget changes.
The complete donor constituent results and runtime-bounded mutation batches
are recorded in the parent HANDOFF.md. Current results: table clean run 36/36 and all 26 table controls; plane 29/29;
PHC-step 62 clean checks and all eight arms; shadow 309/309; all 33 donor
engine mutants plus their clean controls; parser 337/337 and eight mutants;
gaskets 81/81 and four mutants; traffic generator 288/288 and three mutants.
All 35 parent static gates, CI contract checks, pin records and generated-asset
checks pass. The batch audit proves no missing or duplicated original entry.
The donor aggregate was interrupted to respect the command window; completed
constituents and disjoint mutation batches supply the passing evidence.
No aggregate rc-0 verdict is claimed.

## Known limitations / out of scope

- Independent review is required on the new heads.
- Historical area and timing numbers apply only to the named revisions.
- No protocol, register-map, timestamp or default-placement change is introduced
  by the continuation corrections.
- Physical access, new routes, acceptance re-recording and publication remain
  outside this assignment.

## Definition of Done

- [x] Assigned style and documentation corrections are implemented
- [x] Before/after clock and parser results match
- [x] Parent Python/C++ integration gates pass
- [x] Remaining donor campaigns pass
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Parent merge bar and post-merge containment are complete
