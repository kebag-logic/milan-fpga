Base: `main` (`d1bb4f4e`, PR #21's merge). Head: `opt-exec-3` (`50a2106`). The whole optimisation line, which has
never been reviewed into `main`: `opt-exec-1` (343c610) and `opt-exec-2` (4d6e89a), rebased onto `main` as new commits,
then the end-station options, then the fixes for the two reviews at `73007b48`. The pushed `opt-exec-1` and
`opt-exec-2` are not rewritten.

Relates to kebag-logic/milan-fpga#977 (registering a peer's Talkers costs the split control CPU most of its slice),
kebag-logic/milan-fpga#872 (the lookup, timer and Message-build options began there) and kebag-logic/milan-fpga#665.

## Why

milan-fpga runs lwSRP on a cacheless RV32I core at 100 MHz, about five CPU cycles an instruction, a taken branch about
twenty. A peer may replace every input's Talker at each transmit opportunity (IEEE 802.1Q-2018 35.2.6, 10.7.11; Milan
v1.2 4.2.7.2.2), and each replacement walked every attribute, delivered three events, copied 64-octet values, and the
MRPDU build after it re-encoded every vector it sorted. Each option below removes such work without changing any
transmitted octet, indication, observation, receive-filter call or their order, but for the one-port difference below.
With every option at 0, every library object is byte-identical to `main`'s without debug information, at -O0, -O2 and
-Os; with it, only the debug sections differ, as source lines moved.

## What

| Option | Set | Difference |
| --- | --- | --- |
| `LWSRP_ATTR_KEY` (with the buckets or `LWSRP_SCALE`) | each attribute keeps `attr_key`'s octet, compared before `attr_cmp` and `attr_replaces` | those two callbacks run less often |
| `LWSRP_ATTR_BUCKETS` | a lookup scans one bucket by key, each bucket in the list's order | as the key |
| `LWSRP_TIMER_SLOTS` | a tick visits only its wheel slot's timers, keeping the list's firing order | none |
| `LWSRP_TX_MERGE` | runs of encoded vectors are merged, an ordered Message skips it, a strictly descending one is reversed in place | `encode_attr` may run again for a vector the sort moves |
| `LWSRP_ONE_PORT_MAP` | a one-port participant reserves no MAP work and calls no policy | the policy is not called at one port, and a refused reservation no longer refuses the receive there (doc/integrator.md, one-port propagation) |
| `LWSRP_LEAN_VALIDATE` | the validation pass leaves the decoded value unzeroed | `decode_attr`'s result must not depend on its buffer's prior content |
| `LWSRP_RAPID_REPLACE` | a replaced registration that rLv! left MT takes no leave timer event | none: in MT that row changes neither machine |
| `LWSRP_LEAN_COPY` | a Registrar row copied only where its indication is rewritten, a restore kept at the stored length, MSRP's fixed-size fields stored an octet at a time | none |
| `LWSRP_LEAN_TX` | after a send, tx! only to an Applicant its row moves; the assembler passes over empty type words | none: the Registrar ignores tx! |

`LWSRP_SCALE` selects the first four; the end-station options are defined directly for every source. CHANGELOG.md
lists the set. doc/integrator.md documents each option and, in "Application callback contract", what `decode_attr`,
`encode_attr`, `attr_cmp` and `attr_replaces` must meet under them; `mrp.h` states the same at `encode_attr` and
`decode_attr`. doc/tester.md documents the checks below.

## Changes since `73007b48`

Both reviews at `73007b48` are addressed in ten commits (`7b5e821`..`50a2106`); with every option at 0 the library
changes only in comments and in one restore's spelling, and the objects are `main`'s (below).

| Finding | Change | Check |
| --- | --- | --- |
| R959-1-F1, R960-1-F5: committed bytecode | `7b5e821` removes `tests/__pycache__/check_reversals.cpython-314.pyc` and adds `.gitignore` (`__pycache__/`, `*.pyc`) | `git ls-files '*.pyc'` is empty; every tracked file is text, none generated. The blob stays in this branch's history (`cce36b5`): merge by squash or a rebuilt branch so `main` does not carry it, the manager's choice |
| R959-1-F2: one-port difference untested | `tests/unit/end_station_test.c`, registered in every build, its expectations following the switches: a refused one-port reservation refuses the receive in the default build and applies under `LWSRP_ONE_PORT_MAP`; no policy call at one port; two ports refuse and call the policy in every build. `registrar_recovery_stops_aging_without_duplicate_join_or_map` runs at one and two ports, its policy count option-aware | end-station unit build exit 0; reversals `one-port-refusal-kept`, `one-port-inert`, `one-port-policy-called` KILLED by those named tests |
| R959-1-F3, R960-1-F2: reversal counts | the runner prints a SKIP line for every case it does not select and a summary of listed, selected, run, killed, survived and skipped cases; a selected case with no result fails the run | a planted silent skip fails with `FAIL one-port-inert: selected but reported no result` (rc 1) |
| R959-1-F4, R960-1-F2: the guide's 36 | the guide counts each group: ten timer, five bucket, eleven order and twelve end-station defects, 38 with the two added below; the sanitizer's plant counted apart | 38 `MUTANTS` entries: 10 + 5 + 11 + 12 |
| R960-1-F1: the empty-word shortcut untested | the differential's test application uses AttributeTypes 1, 2, 31, 32, 129 and 255; planted `lean-tx-word-ends-scan` (`type = 255u`) with `LWSRP_LEAN_TX` alone and with the whole set; the end-station suite sends types 1, 31, 32, 64, 129, 224 and 255 in five combinations | with `73007b48`'s driver the defect survives 200 seeds in all four builds; with this one it is caught at seed 3 in each; the unit reversal fails `sparse_attribute_types_each_send_one_message_in_type_order` |
| R959-1-F5: callback contracts | `mrp.h` at `encode_attr` and `decode_attr`; doc/integrator.md's "Application callback contract"; "changes no output, callback or order" narrowed to transmitted octets, indications, observations and receive-filter calls | doc checks |
| R959-1-F6, R960-1-F3: default objects | `src/core/mrp_mad.c:1205` kept a whole-value `kept` local in the default arm, which changed `rx_on_attr`'s code at -O0. The default arm now spells the length `sizeof(previous_value)` with no local (`RX_KEPT`), as `main` does | 64 of 64 objects byte-identical to `main`'s (8 sources; -O0, -O2, -Os, each also with -DLWSRP_MILAN=1, and -O0/-O2 -fPIC), without debug information; with `-g`, 24 of 24 identical once debug sections are stripped |
| R960-1-F4: no changelog | CHANGELOG.md: the nine options, defaults, `LWSRP_SCALE`'s selection, the direct end-station definitions, the one-port exception and the callback contract, with the governing issues | doc checks |
| R959-1-R1, R960-1-F6: option comments | each option's comment gives its reason, requirement clauses and the milan-fpga issue IDs (#977, part of #665; #872 too for the key, buckets, wheel and merge) | no lane, round or review label in any added line |

The new comment lines moved code in `mrp_mad.c` and `msrp.c`; every guide anchor into them is re-pointed to the line it
named at `73007b48`.

## Evidence (head `50a2106`)

Each gate ran on its own clean clone at this head.

| Gate | Command | Result |
| --- | --- | --- |
| Unit tests | `cmake -DCMAKE_BUILD_TYPE=Debug`, `ctest`, `unit_tests`, with `-DLWSRP_MILAN=OFF` and `ON` | exit 0; 112 tests, 27,348 and 27,336 passes |
| Unit tests, scale and end station | 18 builds: default, `LWSRP_SCALE`, the end-station set with and without it (`-DCMAKE_C_FLAGS="-DLWSRP_ONE_PORT_MAP=1 ... -DLWSRP_LEAN_TX=1"`), each end-station option alone; both profiles | all exit 0; scale and end-station 27,376 / 27,364 passes (114 tests); without scale and each option alone 27,348 / 27,336 |
| Scenarios | `behave`, and `behave --dry-run` | 1 feature, 3 scenarios, 10 steps pass, both profiles |
| Codec, isolated | the tester guide's `mrp_pdu_tests` command | exit 0, 1,690 passes |
| Differential, generic | `python3 tests/check_differential.py --work-dir <dir> --sanitize-memory clang` | 2 drivers, 22 builds; 38 of 38 planted defects and the sanitizer's plant killed; end-station build clean under MemorySanitizer over 200 seeds; 0 problems |
| Differential, Milan | `... --milan ON --sanitize-memory clang` | the same |
| Reversals | `python3 tests/check_reversals.py --prefix <cgreen>`, and with `--milan ON` | 118 listed; 110 selected, run and killed, 8 skipped (the key's 4, the end-station's 4); 0 failures, each profile |
| Reversals, key | `... --scale ON`, both profiles | 4 selected, run and killed; 114 skipped; 0 failures |
| Reversals, end station | `... --scale ON --end-station ON`, and `--end-station ON` alone, both profiles | 8 (key and end-station) and 4 selected, run and killed; 0 failures |
| Equivalence | `python3 tests/check_equivalence.py`, and with `--milan ON` | 22 scenarios, 148 opportunities, 138 PDUs: 125 byte-identical, 13 layout-only, 0 different; the one revised test (#20) |
| Equivalence controls | `python3 tests/check_equivalence_controls.py`, and with `--milan ON` | 5 controls, 0 failed |
| Bare metal | `check_embedded.py`; `check_freestanding.py` with no switch, `-DLWSRP_MILAN=1`, the scale set, the end-station set, and all of them | pass; 7 freestanding sources, 0 failures each |
| Default objects | 8 sources of `main` and this head, each flag set, compared byte for byte | 64 of 64 identical (-O0, -O2, -Os, each with `-DLWSRP_MILAN=1`, -O0/-O2 `-fPIC`); with `-g`, 24 of 24 identical after stripping debug sections |
| Tracked files | `git ls-files '*.pyc'`; every tracked file's encoding | none; 74 files, all text, no generated output |
| Guides | `doc/tools/check_sentences.py`, `check_references.py` (and `--self-test`), `check_links.py --github-auth`, `render_mermaid.py` | 0 over the limit, 0 unlinked, 79 self-test cases, 438 local links and 26 external URLs with 0 failures, 29 graphs rendered |

The differential builds each driver (the timer, and the MAD with MSRP, MVRP and MMRP) against `main` (`d1bb4f4e`)
and against this head in eleven configurations: the defaults, the scale set and three of its edges (a four-slot wheel
started short of the tick counter's wrap, one bucket, 256 buckets), each end-station option alone, and the end
station's whole set. It runs both on the same seeds and requires byte-identical traces (every call, result, callback
and transmitted byte) but for the one-port difference, whose refusal seeds it counts and does not compare; the
end-station unit suite tests that difference instead. Its 38 planted defects are each an incorrect version of one
option, and some seed's trace shows every one.

## Review notes

- Every option is a preprocessor switch defaulting to 0. With all at 0 the objects are `main`'s at -O0, -O2 and -Os
  without debug information; with it, only the debug sections differ, as source lines moved.
- `LWSRP_RAPID_REPLACE` skips the leave timer's delivery only where the Registrar is MT after rLv!: the leave timer's row
  in MT is `{none, none, MT}` and the Applicant's row is all `_X`, so the delivery would change nothing; where rLv! left
  LV (the generic table) it is delivered.
- `LWSRP_LEAN_TX` skips tx! for VO, QA, AO, QO and QP only (the tx! row's `_X` entries); AN's special case moves, so it
  is delivered.
- The reversal is taken only for a strictly descending Message (no tie), the order `tx_order` gives such a list.
- Not run: a target (RV32) build or link, cycle measurements, hardware. lwSRP has no hosted workflow; every gate above
  ran locally.
