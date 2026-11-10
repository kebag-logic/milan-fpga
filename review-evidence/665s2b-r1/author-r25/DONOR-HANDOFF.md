# [A683ze] kebag-logic/tsn-c-stack#32: the ACMP core walks only the sinks an entry changed (DONOR HANDOFF)

**Status: committed, not pushed. Head `fa31d4c8052b60443572ee8338228e82ae6cbf05`** on branch `32-acmp-dirty-walk`, one commit on `origin/main` `ea4af6f` (`Merge pull request #28`), in a fresh clone of `https://github.com/kebag-logic/tsn-c-stack.git` (`$LANES/tsn-c-stack-32-walk`, the assigned path). Both testing `run:` steps of the stack's CI passed on a clean clone of the head (section 3). The PR body is `DONOR-PR-BODY.md` ("Closes #32"). The manager pushes the branch and opens the PR.

- Authority: the round 25 ruling on milan-fpga #665 (issuecomment-6751196896), item 3; the issue's four acceptance items.
- Receipts: `receipts/donor/` (`gates/` the clean-clone CI run, `probes/` the plants and the port to the pin, `bench/` the host benchmark, `scripts/` the runners). `<scratch>`, `<tools>`, `<home>` and `<lanes>` stand for the host paths they replaced.

## 1. Changes (file at `fa31d4c8`, reason)

| File | Change | Reason |
|---|---|---|
| `include/acmp.h` | `ACMP_DIRTY_WORDS` = `(ACMP_MAX_SINKS + 31u) / 32u`; `struct acmp` gains `uint32_t dirty[ACMP_DIRTY_WORDS]` and `uint32_t dirty_if` | the per-sink mark, sized from `ACMP_MAX_SINKS` like #31's release mask, and the interfaces whose timer the next completion re-arms |
| `src/acmp.c` | `mark()` and `marked()`; `publish()`, `admit()` and `finish()`'s record and view loop skip unmarked sinks, `rearm()` unmarked interfaces; `finish()` clears the marks | issue #32's change; `publish()` also runs before each new frame (`transmit()`), on the same marks |
| `src/acmp.c` | a mark at `bind()`, `unbind()`, `probe_response()` (a matching response), `acmp_adp_rx` (each sink of the talker on the interface), `acmp_timer_expired` (each aging or due sink, and the interface), `acmp_tk_registered`, `acmp_tk_kind_changed`, `acmp_tk_unregistered`, `acmp_set_started`, `acmp_poll`'s release loop (each released sink) and `probe_left()` (a sent probe's sink), `acmp_restore_binding`, `acmp_restore_rollback` | every place a sink's binding, state, timers or owed changes change, before the change |
| `src/acmp.c` | `acmp_poll`'s release loop decrements only the sinks its frame releases | so it can mark them; the same counts |
| `tests/test_acmp_walk.cpp` (new), `CMakeLists.txt` (`tsn_walk`, `acmp_walk`), `scripts/mutation.py` (`acmp_walk` arm) | the differential test at 1, 8, 32 and 33 sinks, at `ACMP_MAX_SINKS=33u` under the shift and UB sanitizers | acceptance item 1 |
| `tests/mutations.json` | 18 new plants (one a mark site, the interface bit in `mark()`, and word 0 in `mark()` and `marked()`); 13 plants re-anchored on the lines they plant into, the same defects; two plants' kills renamed (below) | acceptance item 2; every plant must match once |
| `tests/test_acmp.cpp` | A17 and A31 each add an entry that visits an untouched interface or sink, with its assertion | `acmp-timer-port-called-every-time` and `acmp-publish-stream-cache-stale` escaped the changed-sink walk: their defects showed only when a walk visited what no entry changed |
| `docs/REQUIREMENTS.md`, `docs/requirements.json`, `scripts/requirement_records.py` | ACMP-13, its record and its origin (issue #32) | a tested requirement needs its record; the traceability gate refuses an unknown ID |
| `docs/PORTING.md` | "ACMP changed-sink walk" (what each entry marks); the two fields in "ACMP machine storage" | the port contract |
| `docs/TESTS.md`, `docs/TRACEABILITY.md` | regenerated (`test_inventory.py --write`, `traceability.py --write`) | generated files |
| `docs/VERIFICATION.md`, `CHANGELOG.md` | 458 core plants and the walk arm; the change log entry | the campaign's count; the Unreleased list |

The commit subject is one line with no body and no trailers, under the identity `check_privacy.py` accepts.

## 2. Checks, planted mutants and failing words

The four `AcmpWalk` tests drive two cores with one random entry sequence: the changed-sink walk, and the same core with every sink and interface marked before each entry, which is `main`'s walk. Each requires equal call traces after every entry ("the changed-sink walk makes the full walk's calls, in order, at step n of s sinks").

| Plant | Defect | Caught by (all on the trace assertion) |
|---|---|---|
| `walk-bind-unmarked`, `walk-unbind-unmarked`, `walk-probe-response-unmarked`, `walk-adp-unmarked`, `walk-expired-interface-unmarked`, `walk-aging-unmarked`, `walk-registered-unmarked`, `walk-unregistered-unmarked`, `walk-started-unmarked`, `walk-restore-unmarked`, `walk-rollback-unmarked`, `walk-mark-interface-dropped` | the mark not set at that site | all four tests |
| `walk-release-unmarked` | a released sink not marked | 1, 8 and 32 sinks (no owed frames at 33) |
| `walk-expiry-unmarked`, `walk-kind-unmarked` | the mark not set at a due timer, at a kind change | 33 sinks |
| `walk-probe-left-unmarked` | a sent probe's sink not marked | 32 sinks |
| `walk-mark-word-zero`, `walk-marked-word-zero` | every sink's bit in word 0 | 33 sinks |
| `acmp-timer-port-called-every-time` (kill renamed) | `rearm()` calls the port for every armed interface | "A17 a change that leaves an interface's earliest deadline keeps its timer" |
| `acmp-publish-stream-cache-stale` (kill renamed) | the published stream cached as 0 | "A31 an entry that leaves the settled stream publishes nothing" |

Each plant was first run by a local runner (`probes/walk-plants-local.json`, `scripts/walk_plants.py`) and then by the stack's own campaign (`mutation.py --select walk-`: 18 of 18 caught, `probes/mutation-select-walk.log`); the full campaign at the head: 462 caught, 0 escaped (`gates/mutation.log`).

`walk-probe-left-unmarked` first escaped: the driver answered owed probes before they were sent, so `probe_left()`'s marked branch never ran. The driver now answers only probes that left (a sink not `timer_held`).

## 3. Gates (clean clone of `fa31d4c8`)

`git clone --no-local` of the donor clone, detached at the head; status empty before and after (`gates/before.txt`, `after.txt`). `scripts/tsn_ci.sh` runs the CI's two testing steps, `--jobs 6`:

| `run:` step | rc | Result |
|---|---:|---|
| Install host dependencies (`apt-get`, `npm`) | not run | the host is not the CI image: the pinned GoogleTest/GMock 1.14.0, Clang 18.1.3 and clang-tidy 18.1.3, and Mermaid CLI stand in; GCC, the sanitizer build's Clang, cppcheck, CMake and PyYAML are the host's |
| `python3 scripts/validate.py --work build-validation --jobs 16 --graphs` (run with `--jobs 6`) | 0 | 28 of 28 gates rc 0 (`gates/gates.json`, `gates/*.log`, `*.rc`): mutation `{"CAUGHT": 462, "ESCAPED": 0, "ERROR": 0}` (the full `results.json` by SHA-256 in `gates/not-copied.txt`); coverage 100 % lines and branches after exclusions, `src/acmp.c` 845/845 and 434/434; GCC and Clang-sanitizer CTest 9 of 9 each; static analysis, boundary, conditionals, comments, needles, traceability, test inventory, privacy and graphs rc 0. 599 s |
| Install RV32 dependencies | not run | as above: the host's RISC-V GCC and QEMU |
| `python3 scripts/baremetal.py --work build-rv32 --jobs 16` (run with `--jobs 6`) | 0 | Debug and Release rc 0 (`gates/rv32-results.json`); core imports equal to `main`'s (`gates/rv32-results-main.json`): Debug `__mulsi3`, `__umodsi3`, `ctrl_reentry_assert`, `memcpy`, `memset`, `port_assert_failed`; Release `__umodsi3`, `ctrl_reentry_assert`, `memcpy`, `memset`. 4 s |

Host benchmark (acceptance item 4; `bench/bench_finish.c`, `bench-o2.txt`, `bench-os.txt`): x86 TSC cycles, median of 200,000 `acmp_set_started` entries on one of `n` bound sinks, a core at `ACMP_MAX_SINKS=32u`:

| Sinks | `main` -O2 | head -O2 | `main` -Os | head -Os |
|---:|---:|---:|---:|---:|
| 8 | 899 | 248 | 1,705 | 403 |
| 32 | 3,596 | 558 | 6,665 | 836 |

## 4. At milan-fpga's pin (scratch only; the pin does not move)

The change's `src/acmp.c` and `include/acmp.h` diff applies to the pin `70936b77` (`git apply --3way`; `probes/` holds the files' SHA-256). On the port: the pin's own 8 CTest binaries pass, and so does the walk test (4 of 4) built against it. That port is the stack of the round's scratch measurement (HANDOFF section 4).

PIN_FIGURES

## 5. Run history

- 02:5x CET 2026-11-10: clone, branch `32-acmp-dirty-walk` from `origin/main` `ea4af6f`; toolchain from the host's pinned set.
- 03:0x: the change; the stack's 8 binaries pass; the differential test; 17 of 18 plants caught locally, `walk-probe-left-unmarked` escaped (the driver answered unsent probes); the driver fixed, 18 of 18.
- 03:1x: the mutation table, ACMP-13 and the docs; first validation on a working copy: 28 gates, `mutation` rc 1 with two existing plants escaped (`acmp-timer-port-called-every-time`, `acmp-publish-stream-cache-stale`), A17 and A31 strengthened, both caught.
- 03:2x: committed `fa31d4c8`; the clean-clone CI run, rc 0 and rc 0; the host benchmark; the port to the pin.
