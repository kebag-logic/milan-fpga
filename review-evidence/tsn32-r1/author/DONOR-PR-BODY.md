[A683zf] Walk only the sinks an ACMP entry changed

Closes #32

## What

At `main` `9deb0dd` (and at `ea4af6f`, where this change was drafted), `finish()` in `src/acmp.c` walks every sink at the end of every ACMP entry: `publish()` compares each sink's published triple, `rearm()` every sink of every interface, `admit()` each sink's admission, and the last loop builds each sink's binding record and reported view and compares both. `transmit()` runs `publish()` over every sink again before each new frame. So the work every entry does at its completion grows with `n_sinks`, whatever the entry changed.

This change keeps the calls and walks only what changed:

- `struct acmp` gains `uint32_t dirty[ACMP_DIRTY_WORDS]`, one bit a sink, with `ACMP_DIRTY_WORDS` defined as `(ACMP_MAX_SINKS + 31u) / 32u` like #31's `ACMP_RELEASE_WORDS`, and `uint32_t dirty_if`, one bit an interface (`include/acmp.h`).
- `mark(a, k)` sets sink k's bit and its interface's (`src/acmp.c`). An entry marks a sink before it changes the sink's binding, state, timers or owed changes:
  - `bind()` and `unbind()`, a matching `PROBE_TX_RESPONSE` in `probe_response()`, each bound sink of the talker an ADPDU names on its interface in `acmp_adp_rx`;
  - in `acmp_timer_expired`, each sink of its interface whose discovery ages or whose connection timer is due, and the interface itself, whose timer the expiry consumed;
  - `acmp_tk_registered`, `acmp_tk_kind_changed`, `acmp_tk_unregistered` and `acmp_set_started`, their sink;
  - an accepted `acmp_poll`, each sink its frame releases and, in `probe_left()`, the sink of a probe it sends;
  - `acmp_restore_binding` its sink and `acmp_restore_rollback` every sink, for the next `acmp_open`.
- `publish()`, `admit()` and `finish()`'s record and view loop skip unmarked sinks; `rearm()` skips interfaces with no mark. `finish()` clears every mark at its end. A GET_RX_STATE, a refused command and a talker command mark nothing.
- The order and arguments of `p_publish`, `p_timer`, `p_admit`, `p_persist` and `p_changed` are those of the walk over every sink: each walk still visits sinks in ascending order, and a sink no entry marked has nothing to report, since every field these walks compare changes only under a mark.
- `acmp_poll`'s release loop now decrements only the sinks its frame releases, each read from its word of #31's release mask, so it can mark them: the same counts as before.

ACMP-13 ([REQUIREMENTS.md](docs/REQUIREMENTS.md#acmp-changed-sink-walk)) states the requirement; the port contract's new [ACMP changed-sink walk](docs/PORTING.md#acmp-changed-sink-walk) says what each entry marks, and [ACMP machine storage](docs/PORTING.md#acmp-machine-storage) lists the two fields. No public function, callback, configuration, view or counter changes.

## Tests and plants (acceptance items 1 and 2)

- `tests/test_acmp_walk.cpp`, a new binary `acmp_walk`, links the 33-sink core #31 added (CMake target `tsn_wide`, `ACMP_MAX_SINKS=33u` under `-fsanitize=shift,undefined -fno-sanitize-recover=shift,undefined`), as the mutation driver's new `acmp_walk` arm does with `acmp_wide`'s flags (`scripts/mutation.py`).
- It runs two cores side by side on the same random entry sequence, each with its own recording ports: the changed-sink walk, and the same core with every sink and interface marked before each entry, so that its every completion and every publication before a frame visits every sink, which is the walk at `main`. After every entry it requires the two cores' complete call traces to be equal: every send with its frame bytes, every clock read, timer, grandmaster read, seed, admission, publication, lock query, source read, SRP call, persist and change report, in order.
- The entries: BIND_RX, UNBIND_RX and GET_RX_STATE from two controllers, with and without STREAMING_WAIT and under a lock; PROBE_TX_RESPONSEs matching a sent probe (success and failure) and mismatched ones; talker commands; ENTITY_AVAILABLE and ENTITY_DEPARTING ADPDUs with varied indices, valid times and grandmasters; timer expiries of either interface after short and long clock advances, with nothing due as well; `acmp_tk_registered`, `acmp_tk_kind_changed`, `acmp_tk_unregistered`, `acmp_set_started`, `acmp_poll`; transmit room withdrawn and restored, so frames are owed and released; `acmp_restore_binding` and `acmp_restore_rollback`, each followed by `acmp_open`.
- Four tests at 1, 8, 32 and 33 sinks on two interfaces: `AcmpWalk.OneSinkMatchesTheFullWalk` (4,000 entries), `EightSinksMatchTheFullWalk` (6,000), `ThirtyTwoSinksMatchTheFullWalk` (8,000), `ThirtyThreeSinksMatchTheFullWalk` (8,000, sink 32 in the second mark word). Each also requires that its entries reach a registered reservation, on the second word at 33 sinks.
- At 33 sinks the test sends no BIND_RX or UNBIND_RX to sink 32 and withdraws no transmit room: it was written before #31 widened the owed-release mask, when `1u << 32` would have been undefined. Sink 32 is bound through `acmp_restore_binding`, discovered, probed and registered. The walk's owed paths are tested at 1, 8 and 32 sinks; sink 32's owed paths are #31's `acmp_wide` test's.
- 18 new plants, one for each mark site and the two mark-word reads, each caught by the trace assertion ("the changed-sink walk makes the full walk's calls"): `walk-bind-unmarked`, `walk-unbind-unmarked`, `walk-probe-response-unmarked`, `walk-adp-unmarked`, `walk-expired-interface-unmarked`, `walk-aging-unmarked`, `walk-expiry-unmarked`, `walk-registered-unmarked`, `walk-kind-unmarked`, `walk-unregistered-unmarked`, `walk-started-unmarked`, `walk-release-unmarked`, `walk-probe-left-unmarked`, `walk-restore-unmarked`, `walk-rollback-unmarked`, `walk-mark-interface-dropped` (`mark()` without the interface bit), `walk-mark-word-zero` and `walk-marked-word-zero` (word 0 for every sink, caught at 33 sinks only). They sit after #31's plants and before the wire and entity plants (the entity self-test reads the table's last three).
- Thirteen existing plants follow the lines they plant into, with the same defect: `acmp-unbind-keeps-srp`, `acmp-unbind-srp-after-response`, `acmp-registered-keeps-no-tk`, `acmp-unregistered-keeps-srp`, `acmp-expiry-not-consumed`, `owed-answer-keeps-the-hold`, `acmp-first-owed-releases-every-change`, `acmp-no-aging`, `acmp-roll-back-keeps-the-bindings`, `acmp-expiry-reads-the-clock-twice`, `acmp-owed-probe-never-starts`, `acmp-owed-probe-no-resp-2s`, `acmp-expiry-due-at-its-first-read`.
- Two existing plants escaped the walk at first: `acmp-timer-port-called-every-time` (`rearm()` calling the port for every armed interface) and `acmp-publish-stream-cache-stale` (the published stream cached as 0). Each showed only on an entry that visited an untouched sink or interface, which the changed-sink walk no longer makes. Their tests now make such an entry: A17 adds `acmp_set_started` on interface 1's sink and requires no timer call ("A17 a change that leaves an interface's earliest deadline keeps its timer"), and A31 adds `acmp_set_started` on the settled sink and requires no publication ("A31 an entry that leaves the settled stream publishes nothing"). Both plants are caught by those assertions.
- `docs/TESTS.md` and `docs/TRACEABILITY.md` are regenerated (`test_inventory.py --write`, `traceability.py --write`); ACMP-13 has its record in `docs/requirements.json` and its origin in `scripts/requirement_records.py`. `docs/VERIFICATION.md` counts 466 core plants.

## The merge of `main` (#33)

`main` moved after this change was drafted: #33 (#31, the owed-release mask sized from `ACMP_MAX_SINKS`) merged at `9deb0dd`. The branch takes it by a merge commit, `dd8b026`, no rebase, and `9043b92` on it:
- `src/acmp.c`: the one conflict, the release loop. #31 reads each sink's bit from its word, `o->release[k / 32u] >> (k % 32u)`; this change decrements and marks only the released sinks. The merged loop does both. The walk's diff against `main` is the drafted one but for that line.
- `include/acmp.h`: `ACMP_RELEASE_WORDS` and `ACMP_DIRTY_WORDS` side by side.
- `CMakeLists.txt` and `scripts/mutation.py`: both changes added a 33-sink target with the same definition and sanitizers; one target, `tsn_wide`, now builds both `acmp_wide` and `acmp_walk`, and the mutation driver gives both arms the same flags.
- `tests/mutations.json`: merged by plant name, each parent's plant order kept. Two plants were changed on both sides and are merged by hand (`acmp-unbind-srp-after-response`, `acmp-first-owed-releases-every-change`), and #31's two plants on the release loop (`acmp-wide-release-loop-word-ignored`, `acmp-wide-release-loop-word-off-by-one`) re-anchor on the merged line, the same defects. The first CI run at `dd8b026` failed `entity-controls`: the merged table had put the walk's plants after the entity plants the entity self-test reads last. `9043b92` restores both parents' orders.
- `CHANGELOG.md`, `docs/VERIFICATION.md`: both entries kept; `docs/TESTS.md` and `docs/TRACEABILITY.md` regenerated by their generators.

## Validation (acceptance item 3)

On a clean clone of the head `9043b92`, the two `run:` steps of `.github/workflows/quality.yml` that test:

| Step | rc | Result |
|---|---:|---|
| `python3 scripts/validate.py --work build-validation --jobs 16 --graphs` (run with `--jobs 12`) | 0 | 28 of 28 gates rc 0. Mutation: 470 caught, 0 escaped, 0 error. Coverage 100 % of lines and branches after the exclusions: `src/acmp.c` 847/847 lines, 436/436 branches. All 10 CTest binaries pass in the GCC and the sanitizer builds, `acmp_walk` 4 of 4 |
| `python3 scripts/baremetal.py --work build-rv32 --jobs 16` (run with `--jobs 12`) | 0 | Debug and Release rc 0; the core imports are those of `main` at `9deb0dd` (Debug `__mulsi3`, `__umodsi3`, `ctrl_reentry_assert`, `memcpy`, `memset`, `port_assert_failed`; Release `__umodsi3`, `ctrl_reentry_assert`, `memcpy`, `memset`) |

The dependency install steps were not run: the host stands in with the pinned GoogleTest/GMock 1.14.0, Clang 18.1.3 and clang-tidy 18.1.3 the gates require, Mermaid CLI, and the RISC-V GCC and QEMU the bare-metal step uses.

## Cycles (acceptance item 4)

A host benchmark (x86 TSC cycles, median of 200,000 entries, one pinned CPU) of `acmp_set_started` on one bound sink of a core built at `ACMP_MAX_SINKS=32u` with every sink bound, whose only work besides the flag is its completion: the `finish()` walk, with its publication, persist and change report for the one sink.

| Sinks | `main` `9deb0dd`, -O2 | this change, -O2 | `main`, -Os | this change, -Os |
|---:|---:|---:|---:|---:|
| 8 | 558 | 124 | 961 | 217 |
| 32 | 2,294 | 279 | 3,844 | 465 |

Measured at the merged head; the drafted head's run, on a busier host, gave 899 to 248 and 3,596 to 558 at -O2.

## Notes for the integrator

- The branch carries `main` at `9deb0dd`; a later `main` merges as `9deb0dd` did.
- milan-fpga's pin (`70936b77`) does not move with this PR. kebag-logic/milan-fpga#665 measures this change ported to its pin in a scratch build (the merged head's `src/acmp.c` and `include/acmp.h` diff against `main`, with #31's word read taken back to the pin's one-word mask: byte-identical to the drafted head's port).
