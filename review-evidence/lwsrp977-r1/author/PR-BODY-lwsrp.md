[A825] Build options for an end station's MRP work: lookup buckets, timer wheel, merged and reversed Message builds, one-port MAP work, lean validation, rapid replacement, lean copies and lean tx!, every one off by default

Base: `main` (`d1bb4f4e`, PR #21's merge). Head: `opt-exec-3` (`73007b48`). The whole optimisation line, which has
never been reviewed into `main`: `opt-exec-1` (343c610) and `opt-exec-2` (4d6e89a), rebased onto `main` as new commits,
and the round-3 options on top. The pushed `opt-exec-1` and `opt-exec-2` are not rewritten.

Relates to kebag-logic/milan-fpga#977 (registering a peer's Talkers costs the split control CPU most of its slice) and
kebag-logic/milan-fpga#665.

## Why

milan-fpga runs lwSRP on a cacheless RV32I core at 100 MHz, about five CPU cycles an instruction, a taken branch about
twenty. A peer may replace every input's Talker at each transmit opportunity (IEEE 802.1Q-2018 35.2.6, 10.7.11; Milan
v1.2 4.2.7.2.2), and each replacement walked every attribute, delivered three events, copied 64-octet values, and the
MRPDU build after it re-encoded every vector it sorted. Each option below removes such work without changing any output,
indication, observation or their order; the default build compiles every object `main` does.

## What

| Option | Set | Difference |
| --- | --- | --- |
| `LWSRP_ATTR_KEY` (with the buckets or `LWSRP_SCALE`) | each attribute keeps `attr_key`'s octet, compared before `attr_cmp` and `attr_replaces` | none |
| `LWSRP_ATTR_BUCKETS` | a lookup scans one bucket by key, each bucket in the list's order | none |
| `LWSRP_TIMER_SLOTS` | a tick visits only its wheel slot's timers, keeping the list's firing order | none |
| `LWSRP_TX_MERGE` | runs of encoded vectors are merged, an ordered Message skips it, a strictly descending one is reversed in place | none |
| `LWSRP_ONE_PORT_MAP` | a one-port participant reserves no MAP work and calls no policy | a refused reservation can no longer refuse a receive at one port (doc/integrator.md, one-port propagation) |
| `LWSRP_LEAN_VALIDATE` | the validation pass leaves the decoded value unzeroed | none |
| `LWSRP_RAPID_REPLACE` | a replaced registration that rLv! left MT takes no leave timer event | none: in MT that row changes neither machine |
| `LWSRP_LEAN_COPY` | a Registrar row copied only where its indication is rewritten, a restore kept at the stored length, MSRP's fixed-size fields stored an octet at a time | none |
| `LWSRP_LEAN_TX` | after a send, tx! only to an Applicant its row moves; the assembler passes over empty type words | none: the Registrar ignores tx! |

`LWSRP_SCALE` selects the first four; the end-station options are defined directly. doc/integrator.md documents each;
doc/tester.md the checks below.

## Rebase onto main

`main` gained PR #19 (switch scenario steps) and PR #21 (one Applicant event at the own LeaveAll). The rebase kept
both: the key suite and the own-LeaveAll suite are both registered, `failed_scenarios` and the key reversals' guard
both kept, and the guides' line anchors re-pointed from the revision each line came from (12 of them, stale since
opt-exec-1, now point at the code they name). The differential's base is now `main` (`d1bb4f4e`), so every build is
held to the own-LeaveAll behaviour. A stray shell output file committed on opt-exec-2 is removed. The `callback-order`
reversal had lost its target text to opt-exec-2's one-port gate (that round could not run the reversals) and is
re-anchored; so are two reversals the round-3 options moved.

## Evidence (head `73007b48`)

Each gate ran on a clean clone at this head.

| Gate | Command | Result |
| --- | --- | --- |
| Unit tests | `unit_tests` built with the default, `LWSRP_MILAN`, `LWSRP_SCALE` and both | 27,199, 27,187, 27,227 and 27,215 passes, 0 failures |
| Differential, generic | `python3 tests/check_differential.py --work-dir <dir>` | 2 drivers, 22 builds, 36 of 36 planted defects killed, 0 problems |
| Differential, Milan | `... --milan ON` | 2 drivers, 22 builds, 36 of 36 killed, 0 problems |
| MemorySanitizer | `... --no-mutants --sanitize-memory clang`, and with `--milan ON` | the end-station build unreported; its planted defect (a Talker decoder reading a field before writing it) reported; 0 problems |
| Reversals | `python3 tests/check_reversals.py --prefix <cgreen>`, with `--milan ON`, `--scale ON` and both | 114 reversals each, 0 failures |
| Equivalence | `python3 tests/check_equivalence.py`, and with `--milan ON` | every scenario equal, or revised by its issue as recorded |
| Equivalence controls | `python3 tests/check_equivalence_controls.py`, and with `--milan ON` | 5 controls, 0 failed |
| Embedded, freestanding, behaviour | `check_embedded.py`, `check_freestanding.py` (also with `-DLWSRP_MILAN=1`), `behave tests/features` | pass; 1 feature, 3 scenarios, 10 steps |
| Guides | `doc/tools/check_sentences.py`, `check_references.py` (and `--self-test`), `check_links.py` | 0 over the limit, 0 unlinked, 79 self-test cases, 0 failed links |

The differential builds each driver (the timer, and the MAD with MSRP, MVRP and MMRP) against `main` (`d1bb4f4e`)
and against this head in eleven configurations: the defaults, the scale set and three of its edges (a four-slot wheel
started short of the tick counter's wrap, one bucket, 256 buckets), each end-station option alone, and the end
station's whole set. It runs both on the same seeds and requires byte-identical traces (every call, result, callback
and transmitted byte) but for the one-port difference above. Its 36 planted defects are each an incorrect version of
one option, and some seed's trace shows every one.

## Review notes

- Every option is a preprocessor switch defaulting to 0; the default objects are `main`'s.
- `LWSRP_RAPID_REPLACE` skips the leave timer's delivery only where the Registrar is MT after rLv!: the leave timer's row
  in MT is `{none, none, MT}` and the Applicant's row is all `_X`, so the delivery would change nothing; where rLv! left
  LV (the generic table) it is delivered.
- `LWSRP_LEAN_TX` skips tx! for VO, QA, AO, QO and QP only (the tx! row's `_X` entries); AN's special case moves, so it
  is delivered.
- The reversal is taken only for a strictly descending Message (no tie), the order `tx_order` gives such a list.
