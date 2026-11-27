# REVIEW READY: kebag-logic/lwSRP PR #22, round 2

- Head: `opt-exec-3` `50a2106483141fcd7d1b20654bcf0803e7c3020a` (local; not pushed). Base: `main` `d1bb4f4e5954af6dabe7f210a6bf7adbb76bdd6b`.
- Reviewed head: `73007b4807977517045e8aa485c61ebb8f5ee843` (R959-1 internal, R960-1 external, both NEGATIVE).
- This round: 10 commits `7b5e821`..`50a2106`, one-line subjects, no trailers; 21 files, +567 / -77 against `73007b48`.
  Whole PR against `main`: 24 files, +2940 / -74.
- No history rewritten, nothing rebased or forced, nothing pushed or posted, no hardware.

## Every finding closed

| Finding | Outcome asked | Done | Evidence (receipts/) |
| --- | --- | --- | --- |
| R959-1-F1 (MAJOR), R960-1-F5: committed bytecode | remove it, ignore caches; merge method is the manager's | `7b5e821`: `git rm tests/__pycache__/check_reversals.cpython-314.pyc`; `.gitignore` with `__pycache__/` and `*.pyc` | `gates/inventory-r2.log`: `git ls-files '*.pyc'` empty; 74 tracked files, 52 ASCII + 22 UTF-8 text, 0 generated-output paths |
| R959-1-F2, R960-1 (one-port): the documented difference untested | directed tests built with the option: refusal applies, no policy call, two ports unchanged; end-station unit build in the gates and the guide; recovery test option-aware; a planted `one-port-refusal-kept` KILLED | `91f7c39`: `tests/unit/end_station_test.c` (registered in every build, expectations follow the switches); `registrar_recovery_...` at 1 and 2 ports, policy count option-aware. `7dfe11d`: reversals `one-port-refusal-kept`, `one-port-inert`, `one-port-policy-called` under `--end-station ON`. `a8693e0`: tester guide's "Test the end-station switches" | `gates/units.log` (18 builds exit 0, incl. end-station 27,376 / 27,364); `gates/rev-es-*.log`, `named-failures.txt` |
| R959-1-F3, R960-1-F2: reversal summary counts | report selected / run / killed / skipped; PR states 110 + 4 per profile | `7dfe11d`: SKIP line per unselected case; summary of listed, selected, run, killed, survived, build failures, targets missing, skipped; unreported selected case fails the run | `gates/rev-*.log`; `probes/reversal-count-plant.log` (planted silent skip: `FAIL one-port-inert: selected but reported no result`, rc 1) |
| R959-1-F4, R960-1-F2: "twelve" against 36 | correct the count; sanitizer plant apart | `a8693e0`: "All 38 ...: ten ..., five ..., eleven ..., and twelve in the end-station switches" (2 + 1 + 4 + 5, two added this round); the sanitizer's plant "counted apart from the 38" | `gates/diff-*-r2.log`: 38 of 38 + the sanitizer plant |
| R960-1-F1: empty-type-word shortcut untested | sparse multiword test; a planted scan-ending defect; LWSRP_LEAN_TX alone and combined, both profiles | `7767076`: the differential's test application uses types 1, 2, 31, 32, 129, 255; `lean-tx-word-ends-scan` (end-station set) and `-alone` (LWSRP_LEAN_TX). `91f7c39`: unit test of types 1, 31, 32, 64, 129, 224, 255 in five sets; `7dfe11d`: its unit reversal | `probes/sparse-word-probe.log`: old driver SURVIVED 200 seeds x 4 builds; new driver KILLED at seed 3 x 4; `gates/diff-*-r2.log` |
| R959-1-F5: callback contracts | `mrp.h` and integrator table: decode_attr, encode_attr; narrow "callback" | `e76292a`: `mrp.h` at `encode_attr` and `decode_attr`; integrator "Application callback contract"; the sentence narrowed to output, indication, observation, receive-filter call | `gates/docs-r2.log` |
| R959-1-F6, R960-1-F3: "default objects are main's" | make it true or qualify it, citing `src/core/mrp_mad.c:1205` | made true: `7ca4a6f` drops the default arm's `kept` local (`mrp_mad.c:1205` at 73007b48) for `RX_KEPT` = `sizeof(previous_value)`, so the default arm preprocesses to `main`'s code. A source change with options OFF, the minimal one; behaviour unchanged (differential) | `gates/objects.log`: 64 of 64 byte-identical (8 sources x -O0, -O2, -Os, each with -DLWSRP_MILAN=1, -O0/-O2 -fPIC); before: 61 of 64 (`superseded/`); with `-g`: 24 of 24 identical after `objcopy --strip-debug` (`probes/objects-with-debug-info.txt`) |
| R960-1-F4: no CHANGELOG | entry with nine options, defaults, SCALE selection, direct definitions, one-port exception, issue | `d438de9`: CHANGELOG.md, plus the callback contract and the governing issues (#977, #872, part of #665) and PR 22 | `gates/docs-r2.log` (root pages are scanned) |
| R959-1-R1, R960-1-F6: option comments without issue IDs | add issue IDs; behaviour, reason, requirement IDs; no labels | `adafca8` (and `mrp.h`'s key block): each option block gives a Reason, Requirement clauses and "Issue(s): kebag-logic/milan-fpga#977, part of #665" (#872 too for key, buckets, wheel, merge) | `added-lines-scan.txt`: 0 lane, round, review, reviewer or comment IDs, 0 private paths |

Also: the comment lines moved code, so `50a2106` re-points all 45 guide anchors into `mrp_mad.c` and `msrp.c` to the
lines they named at `73007b48` (by line alignment; each target line checked).

## Gates at `50a2106483141fcd7d1b20654bcf0803e7c3020a` (each on its own clean clone)

| Gate | Result | rc | Receipt (receipts/gates/) |
| --- | --- | --- | --- |
| Host build, ctest, unit_tests, behave, behave --dry-run: default / Milan | 112 tests; 27,348 / 27,336 passes; 3 scenarios, 10 steps | 0 / 0 | `suites-OFF.log`, `suites-ON.log` |
| Unit suite, 18 builds (default, scale, end-station with and without scale, each end-station switch alone; both profiles) | all pass; scale and end-station 27,376 / 27,364 (114 tests); others 27,348 / 27,336 | 0 | `units.log`, `units/` |
| Codec, isolated | 1,690 passes | 0 | `codec.log` |
| Differential, generic, with MemorySanitizer | 22 builds identical (one-port: 177 + 23 refusal seeds); 38 of 38 + sanitizer plant killed; MSan clean 200 seeds; 0 problems | 0 | `diff-OFF-r2.log`, `.differential.json` |
| Differential, Milan, with MemorySanitizer | the same | 0 | `diff-ON-r2.log`, `.differential.json` |
| Reversals, default run / Milan | 118 listed; 110 selected, run, killed; 8 skipped | 0 / 0 | `rev-OFF-r2.log`, `rev-ON-r2.log`, `.summary.json` |
| Reversals, --scale ON / Milan | 4 selected, run, killed; 114 skipped | 0 / 0 | `rev-key-*.log` |
| Reversals, --scale ON --end-station ON / Milan | 8 selected, run, killed; 110 skipped | 0 / 0 | `rev-es-*.log` |
| Reversals, --end-station ON / Milan | 4 selected, run, killed; 114 skipped | 0 / 0 | `rev-es-noscale-*.log` |
| Equivalence / Milan | 22 scenarios, 148 opportunities, 138 PDUs (125 identical, 13 layout-only, 0 different); 1 revised (#20) | 0 / 0 | `eq-OFF.log`, `eq-ON.log` |
| Equivalence controls / Milan | 5 controls, 0 failed | 0 / 0 | `eqc-OFF-r2.log`, `eqc-ON-r2.log` |
| Bare metal: check_embedded; check_freestanding x 5 (none, Milan, scale, end-station, all) | both profile links and dispatch probes; 7 sources, 0 failures each | 0 | `baremetal.log` |
| Default objects against main | 64 of 64 byte-identical | 0 | `objects.log` |
| Tracked-file inventory | 0 Python caches; 74 text files; 0 generated | 0 | `inventory-r2.log` |
| Guides: sentences, references, self-test, links (--github-auth), graphs | 0 over; 0 unlinked; 79 cases; 438 local + 26 external, 0 failures; 29 graphs | 0 | `docs-r2.log` |

Harness faults (mine), superseded and rerun clean: the first inventory regex and link-check origin
(`superseded/gate-inventory.log`, `gate-docs.log`), and an edit of the gate script while six gates ran, which broke
their final lines (`superseded/gate-{diff,eqc,rev}-{OFF,ON}.log`; all six tools had already printed rc 0 and the
same pass summaries as the reruns). Each was rerun from a frozen copy of the script (`scripts/gate-r2.sh`) on a new clean clone.

## Not done, limits

- Not pushed, not posted; PR #22's body is not edited (PR-BODY.md is the text for it).
- The bytecode blob stays in this branch's history (`cce36b5` adds it, `7b5e821` removes it). Keeping it out of `main`
  needs a squash merge or a rebuilt branch: the manager's merge choice, as both reviews say.
- No target (RV32) build or link: no target C library here (`arm-none-eabi-gcc` has no headers; no RISC-V gcc). The
  repository's bare-metal gates, check_freestanding (5 switch sets) and check_embedded, pass.
- No cycle measurement, no hardware, no hosted CI (lwSRP has no workflow).
- The cgreen prefix used is another lane's build (`$VALIDATION_STORAGE/977-a825/cgreen/prefix`, source `abb74b39`), read
  only; the internal reviewer used upstream `25137a17`.

## Manager duties

- Push `opt-exec-3` to `50a2106` and replace PR #22's body with PR-BODY.md, if accepted.
- Choose the merge method for the bytecode blob (squash, or a rebuilt branch).
- Re-review R959-1-F1..F6, R1 and R960-1-F1..F6 at the new head; milan-fpga PR #993's lwSRP pin moves with it.
