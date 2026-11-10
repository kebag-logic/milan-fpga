[A683ze] Walk only the sinks an ACMP entry changed

Closes #32

## What

At `main` `ea4af6f`, `finish()` in `src/acmp.c` walks every sink at the end of every ACMP entry: `publish()` compares each sink's published triple, `rearm()` every sink of every interface, `admit()` each sink's admission, and the last loop builds each sink's binding record and reported view and compares both. `transmit()` runs `publish()` over every sink again before each new frame. So the work every entry does at its completion grows with `n_sinks`, whatever the entry changed.

This change keeps the calls and walks only what changed:

- `struct acmp` gains `uint32_t dirty[ACMP_DIRTY_WORDS]`, one bit a sink, with `ACMP_DIRTY_WORDS` defined as `(ACMP_MAX_SINKS + 31u) / 32u` like the owed-release mask of #31, and `uint32_t dirty_if`, one bit an interface (`include/acmp.h`).
- `mark(a, k)` sets sink k's bit and its interface's (`src/acmp.c`). An entry marks a sink before it changes the sink's binding, state, timers or owed changes:
  - `bind()` and `unbind()`, a matching `PROBE_TX_RESPONSE` in `probe_response()`, each bound sink of the talker an ADPDU names on its interface in `acmp_adp_rx`;
  - in `acmp_timer_expired`, each sink of its interface whose discovery ages or whose connection timer is due, and the interface itself, whose timer the expiry consumed;
  - `acmp_tk_registered`, `acmp_tk_kind_changed`, `acmp_tk_unregistered` and `acmp_set_started`, their sink;
  - an accepted `acmp_poll`, each sink its frame releases and, in `probe_left()`, the sink of a probe it sends;
  - `acmp_restore_binding` its sink and `acmp_restore_rollback` every sink, for the next `acmp_open`.
- `publish()`, `admit()` and `finish()`'s record and view loop skip unmarked sinks; `rearm()` skips interfaces with no mark. `finish()` clears every mark at its end. A GET_RX_STATE, a refused command and a talker command mark nothing.
- The order and arguments of `p_publish`, `p_timer`, `p_admit`, `p_persist` and `p_changed` are those of the walk over every sink: each walk still visits sinks in ascending order, and a sink no entry marked has nothing to report, since every field these walks compare changes only under a mark.
- `acmp_poll`'s release loop now decrements only the sinks its frame releases, so it can mark them: the same counts as before.

ACMP-13 ([REQUIREMENTS.md](docs/REQUIREMENTS.md#acmp-changed-sink-walk)) states the requirement; the port contract's new [ACMP changed-sink walk](docs/PORTING.md#acmp-changed-sink-walk) says what each entry marks, and [ACMP machine storage](docs/PORTING.md#acmp-machine-storage) lists the two fields. No public function, callback, configuration, view or counter changes.

## Tests and plants (acceptance items 1 and 2)

- `tests/test_acmp_walk.cpp`, a new binary `acmp_walk` (CMake target `tsn_walk`), builds the ACMP core and its test at `ACMP_MAX_SINKS=33u` under `-fsanitize=shift,undefined -fno-sanitize-recover=shift,undefined`, as the mutation driver's new `acmp_walk` arm does (`scripts/mutation.py`).
- It runs two cores side by side on the same random entry sequence, each with its own recording ports: the changed-sink walk, and the same core with every sink and interface marked before each entry, so that its every completion and every publication before a frame visits every sink, which is the walk at `main`. After every entry it requires the two cores' complete call traces to be equal: every send with its frame bytes, every clock read, timer, grandmaster read, seed, admission, publication, lock query, source read, SRP call, persist and change report, in order.
- The entries: BIND_RX, UNBIND_RX and GET_RX_STATE from two controllers, with and without STREAMING_WAIT and under a lock; PROBE_TX_RESPONSEs matching a sent probe (success and failure) and mismatched ones; talker commands; ENTITY_AVAILABLE and ENTITY_DEPARTING ADPDUs with varied indices, valid times and grandmasters; timer expiries of either interface after short and long clock advances, with nothing due as well; `acmp_tk_registered`, `acmp_tk_kind_changed`, `acmp_tk_unregistered`, `acmp_set_started`, `acmp_poll`; transmit room withdrawn and restored, so frames are owed and released; `acmp_restore_binding` and `acmp_restore_rollback`, each followed by `acmp_open`.
- Four tests at 1, 8, 32 and 33 sinks on two interfaces: `AcmpWalk.OneSinkMatchesTheFullWalk` (4,000 entries), `EightSinksMatchTheFullWalk` (6,000), `ThirtyTwoSinksMatchTheFullWalk` (8,000), `ThirtyThreeSinksMatchTheFullWalk` (8,000, sink 32 in the second mark word). Each also requires that its entries reach a registered reservation, on the second word at 33 sinks.
- At 33 sinks the test sends no BIND_RX or UNBIND_RX to sink 32 and withdraws no transmit room: at `main` the owed-release mask is one word, so `1u << 32` and `release >> 32` would be undefined there (#31). Sink 32 is bound through `acmp_restore_binding`, discovered, probed and registered. The owed paths are tested at 1, 8 and 32 sinks.
- 18 new plants, one for each mark site and the two mark-word reads, each caught by the trace assertion ("the changed-sink walk makes the full walk's calls"): `walk-bind-unmarked`, `walk-unbind-unmarked`, `walk-probe-response-unmarked`, `walk-adp-unmarked`, `walk-expired-interface-unmarked`, `walk-aging-unmarked`, `walk-expiry-unmarked`, `walk-registered-unmarked`, `walk-kind-unmarked`, `walk-unregistered-unmarked`, `walk-started-unmarked`, `walk-release-unmarked`, `walk-probe-left-unmarked`, `walk-restore-unmarked`, `walk-rollback-unmarked`, `walk-mark-interface-dropped` (`mark()` without the interface bit), `walk-mark-word-zero` and `walk-marked-word-zero` (word 0 for every sink, caught at 33 sinks only). They sit before the wire and entity plants.
- Thirteen existing plants follow the lines they plant into, with the same defect: `acmp-unbind-keeps-srp`, `acmp-unbind-srp-after-response`, `acmp-registered-keeps-no-tk`, `acmp-unregistered-keeps-srp`, `acmp-expiry-not-consumed`, `owed-answer-keeps-the-hold`, `acmp-first-owed-releases-every-change`, `acmp-no-aging`, `acmp-roll-back-keeps-the-bindings`, `acmp-expiry-reads-the-clock-twice`, `acmp-owed-probe-never-starts`, `acmp-owed-probe-no-resp-2s`, `acmp-expiry-due-at-its-first-read`.
- Two existing plants escaped the walk at first: `acmp-timer-port-called-every-time` (`rearm()` calling the port for every armed interface) and `acmp-publish-stream-cache-stale` (the published stream cached as 0). Each showed only on an entry that visited an untouched sink or interface, which the changed-sink walk no longer makes. Their tests now make such an entry: A17 adds `acmp_set_started` on interface 1's sink and requires no timer call ("A17 a change that leaves an interface's earliest deadline keeps its timer"), and A31 adds `acmp_set_started` on the settled sink and requires no publication ("A31 an entry that leaves the settled stream publishes nothing"). Both plants are caught by those assertions.
- `docs/TESTS.md` and `docs/TRACEABILITY.md` are regenerated (`test_inventory.py --write`, `traceability.py --write`); ACMP-13 has its record in `docs/requirements.json` and its origin in `scripts/requirement_records.py`. `docs/VERIFICATION.md` counts 458 core plants.

## Validation (acceptance item 3)

On a clean clone of the head, the two `run:` steps of `.github/workflows/quality.yml` that test:

| Step | rc | Result |
|---|---:|---|
| `python3 scripts/validate.py --work build-validation --jobs 16 --graphs` (run with `--jobs 6`) | 0 | 28 of 28 gates rc 0. Mutation: 462 caught, 0 escaped, 0 error. Coverage 100 % of lines and branches after the exclusions: `src/acmp.c` 845/845 lines, 434/434 branches. All 9 CTest binaries pass in the GCC and the sanitizer builds |
| `python3 scripts/baremetal.py --work build-rv32 --jobs 16` (run with `--jobs 6`) | 0 | Debug and Release rc 0; the core imports are those of `main` (Debug `__mulsi3`, `__umodsi3`, `ctrl_reentry_assert`, `memcpy`, `memset`, `port_assert_failed`; Release `__umodsi3`, `ctrl_reentry_assert`, `memcpy`, `memset`) |

The dependency install steps were not run: the host stands in with the pinned GoogleTest/GMock 1.14.0, Clang 18.1.3 and clang-tidy 18.1.3 the gates require, Mermaid CLI, and the RISC-V GCC and QEMU the bare-metal step uses.

## Cycles (acceptance item 4)

A host benchmark (x86 TSC cycles, median of 200,000 entries, one pinned CPU) of `acmp_set_started` on one bound sink of a core built at `ACMP_MAX_SINKS=32u` with every sink bound, whose only work besides the flag is its completion: the `finish()` walk, with its publication, persist and change report for the one sink.

| Sinks | `main`, -O2 | this change, -O2 | `main`, -Os | this change, -Os |
|---:|---:|---:|---:|---:|
| 8 | 899 | 248 | 1,705 | 403 |
| 32 | 3,596 | 558 | 6,665 | 836 |

PARENT_FIGURES

## Notes for the integrator

PARENT_NOTES
