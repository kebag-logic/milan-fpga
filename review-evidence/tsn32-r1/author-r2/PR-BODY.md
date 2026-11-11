[A766] Round 2: the 33-sink walk reaches sink 32, completion is asserted to clear every mark, and the residue

Closes #32

This round follows the ruling on this PR, [issuecomment-6789256216](https://github.com/kebag-logic/tsn-c-stack/pull/34#issuecomment-6789256216), items 1 to 6. Its scope is tests, documentation and this body. `src/` and `include/` are byte-identical to round 1's head `9043b92` (`git diff --stat 9043b92 -- src include` is empty). The round adds three commits on `9043b92`, with no merge, rebase or amend. Round 1's sections follow below; their 33-sink paragraph, plant sentence and validation note are corrected in place.

## What (round 2)

### Item 1: the second mark word at 33 sinks

`tests/test_acmp_walk.cpp` changes only at 33 sinks. Each new random draw is made only there, so the entry sequences at 1, 8 and 32 sinks are round 1's.

- **Commands reach every sink.** BIND_RX, UNBIND_RX and GET_RX_STATE go to sink 32 a quarter of the time and to any sink otherwise, sink 32 included. Round 1 folded sink 32's commands onto sink 0.
- **Transmit room comes and goes.** It is withdrawn and restored as at 1, 8 and 32 sinks, so sink 32's responses and probes are owed and released. Round 1 never withdrew room at 33 sinks.
- **Sink 32 has an interface of its own.** It sits alone on a third interface, so a mark it misses shows in that interface's timer calls whatever the other sinks' deadlines are. Sinks 0 to 31 keep the two-interface map of 32 sinks. Talker commands, ADPDUs and timer expiries are drawn over the three interfaces.
- **Owed frames leave.** While frames are owed and the port has room, half the steps poll first. In the run measured without it, a later command, restore or rollback overtook every owed probe of sink 32 before the probe left.
- **The test checks that it reached these paths.** At 33 sinks it now also requires that a response of sink 32 is owed ("the random entries owe a sink's response, on the second mark word at 33 sinks"). It also requires that an owed probe of sink 32 leaves while its timer waits for it ("at 33 sinks the second mark word's sink sends an owed probe its timer waits for"). Round 1's reservation requirement stays.
- **Four new plants**, each a mark missing only for a sink of the second word. Each puts `if (k < 32u) { mark(a, k); }` at its site, and `AcmpWalk.ThirtyThreeSinksMatchTheFullWalk` catches each with "the changed-sink walk makes the full walk's calls":
  - `walk-bind-second-word-unmarked` (`bind()`)
  - `walk-unbind-second-word-unmarked` (`unbind()`)
  - `walk-release-second-word-unmarked` (the release loop of `acmp_poll`)
  - `walk-probe-left-second-word-unmarked` (`probe_left()`)
- `walk-release-unmarked` and `walk-probe-left-unmarked` are now also caught at 33 sinks, and their kill lists name that test.

### Item 2: completion clears every mark

- After every step, the test requires each `dirty` word and `dirty_if` of the changed-sink core to be zero ("a completed entry leaves no sink marked", "a completed entry leaves no interface marked"). Every step ends with an entry that either completes or is refused before it marks. `acmp_restore_binding` and `acmp_restore_rollback` are each followed by `acmp_open` in the same step.
- Three new plants. All three pass the call-trace assertion, because a core that keeps its marks still makes the full walk's calls.
  - `walk-marks-never-cleared` (no `memset` of `dirty`): caught at 1, 8, 32 and 33 sinks.
  - `walk-interface-marks-never-cleared` (no `dirty_if = 0u`): caught at 1, 8, 32 and 33 sinks.
  - `walk-clear-first-word-only` (`sizeof a->dirty[0]`): caught at 33 sinks.
- ACMP-13's row in `docs/TRACEABILITY.md` names the four `AcmpWalk` tests, which carry these assertions. `docs/TESTS.md` lists the plants each test catches.

### Item 3: the parent consumer bar

The ruling defers this bar to the milan-fpga pin move. That move carries #28, #31 and #32 together. Before adoption it runs every parent firmware gate at the moved pin: `firmware-unit`, `firmware-control-mutants`, `firmware-boundary`, `firmware-verilator` and the image ROM ledger. Nothing in milan-fpga consumes this change before that move.

- **Code size of this change.** Measured on RV32 with `scripts/baremetal.py`'s builds, `main` `9deb0dd` against this head:

  | | Debug | Release |
  |---|---:|---:|
  | `acmp.c` text, bytes | 21,429 to 22,189 (+760) | 20,365 to 21,077 (+712) |
  | smoke image text, bytes | 51,964 to 52,652 (+688) | 41,645 to 42,337 (+692) |

  `struct acmp` grows by 8 bytes at 16, 32 and 33 sinks. Round 2 changes none of these: round 1's head and this one build images that are equal once their debug sections are stripped.
- **Known consumer effect.** With this change at milan-fpga's pin, the 8x8/2if `answering-every-port` image is 123,012 bytes. That is 132 bytes over its 122,880-byte granule (kebag-logic/milan-fpga#665, issuecomment-6778599191, item 5), and the pin move owes those 132 bytes.

### Item 4: residue

- `docs/REQUIREMENTS.md` (R824-1 RES-1) now says that each entry marks a sink before the next walk reads it, and that the two restores mark right after the reset.
- `docs/VERIFICATION.md` (R824-1 RES-2, which also covers R823-1 R1's line): the mutation row says what each walk plant plants, and counts 473 core plants.
- This body: R823-1 R2 corrects round 1's plant sentence. R824-1 RES-3 corrects round 1's validation note; R823-1 R3's line takes RES-3's text. R823-1-F1 replaces round 1's 33-sink paragraph with what the test does now.

### Item 5: suggestions taken

- **R824-1 S-3.** `tests/test_acmp_walk.cpp` asserts at compile time that `dirty_if` holds a bit for every interface: `static_assert(ACMP_MAX_INTERFACES <= sizeof(acmp::dirty_if) * 8u, ...)`. The conditional gate (`scripts/check_conditionals.py --selftest`) compiles the walk test with GCC and Clang. With `ACMP_MAX_INTERFACES` at 4 and 32 it compiles; at 33 it is refused, by that assertion's message.
- **R824-1 S-2: the parent's target figures** (kebag-logic/milan-fpga#665). The parent grades its control-service load against a 0.70 ceiling.
  - Before this change, the walk over every sink was 18,782 of an ADP record's 22,170 cycles at 8x8/2if (issuecomment-6751120577).
  - With this change ported to the parent's pin, the parent measured these costs at 8x8/2if (issuecomment-6778599191). The load went from 0.844 to 0.747.

    | Cost | At the pin, us | With this change, us |
    |---|---:|---:|
    | ACMP record | 440 | 305 |
    | ADP record | 240 | 125 |
    | ACMP's timer slot | 350 | 205 |
    | ACMP's owed frame | 185 | 40 |

  - After the parent's next cuts, the 8x8/2if load is 0.815 at the pin and 0.719 with this change (issuecomment-6788757307).

## How to validate (round 2)

These are the `run:` steps of `.github/workflows/quality.yml` that test, run on a clean clone of this head:

```
python3 scripts/validate.py --work build-validation --jobs 16 --graphs
python3 scripts/baremetal.py --work build-rv32 --jobs 16
```

| Step | rc | Result |
|---|---:|---|
| `validate.py --jobs 16 --graphs` | 0 | 28 of 28 gates rc 0. Mutation: 477 caught, 0 escaped, 0 error, the 25 walk plants among them. Coverage is 100 % of lines and branches after the exclusions, with `src/acmp.c` at 847/847 lines and 436/436 branches. All 10 CTest binaries pass in the GCC build and in the sanitizer build, `acmp_walk` among them. The conditional gate's interface control is refused at 33 interfaces and compiles at 4 and 32 |
| `baremetal.py --jobs 16` | 0 | Debug and Release rc 0, with the core imports of `main` at `9deb0dd`. Debug imports `__mulsi3`, `__umodsi3`, `ctrl_reentry_assert`, `memcpy`, `memset` and `port_assert_failed`; Release imports `__umodsi3`, `ctrl_reentry_assert`, `memcpy` and `memset`. The Release image is byte-identical to round 1's |

The dependency install steps were not run. The host stands in with the pinned GoogleTest/GMock 1.14.0 and clang-tidy 18.1.3, with Mermaid CLI 11.16.0, and with the RISC-V GCC and QEMU that the bare-metal step uses. The GCC and Clang-sanitizer CTest gates ran with the host's GCC 16.2.1 and Clang 23.1.4, because the pinned Clang 18 cannot build against the host's C++ library. The gates that call `clang-18` used the pinned Clang 18.1.3. The hosted run follows the push.

To see the round's tests on their own:

```
cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug
cmake --build build -j16 --target acmp_walk
./build/acmp_walk
python3 scripts/mutation.py --work build-mutations --jobs 16 --select walk-
python3 scripts/check_conditionals.py --selftest --work build-conditionals --jobs 16
```

The second-to-last command runs the 25 walk plants: 25 caught.

Both round 1 reviews' scripts were run unchanged at this head:

- **R823-1's old-against-new differential** (`main`'s real core against this head's, 480 cases with commands lifted onto sink 32 and without): 0 divergent.
- **R823-1's fault probes.** `bind-`, `unbind-`, `release-` and `probe-left-marks-only-word-zero` now each fail `AcmpWalk.ThirtyThreeSinksMatchTheFullWalk`. `marks-never-cleared` fails all four `AcmpWalk` tests.
- **R824-1's differential matrix**: 560 of 560 pass, at mask widths 16, 32, 33, 64 and 255, in its LIFT, REENTER and NOOPEN modes.
- **R824-1's probe controls.** The suite now catches c2 and c3 (the release loop's mark in the wrong word or for sinks below 32 only) in `acmp_walk` as well as in `acmp_wide`. It also catches c4 (`probe_left()` marking word 0), which no test caught in round 1, because sink 32 now has its own interface.
- **Both reviewers' plant-table audits**: no plant is dropped. The seven new plants are the only ones in neither parent, and the entity plants stay last.
- **Both sanitizer stand-ins**: 10 of 10.
- **R824-1's CI wrapper (`ci_run.sh`)**, with its own environment, in which `clang` and `clang++` are the pinned Clang 18.1.3: `baremetal.py` rc 0. `validate.py` rc 1: 16 of its 17 source gates are rc 0, and `conditionals` is rc 1, so the fail-fast never starts the compiled gates. That Clang cannot parse the review host's libstdc++ 16 headers, which is why `clang-sanitizers-build` failed in R824-1's own round 1 run. Round 2's interface control compiles the gtest walk test with `clang++`, so it meets the same limit at its first case. The C capacity controls before it pass. With the host's Clang 23.1.4 the gate is rc 0 (the table above). In CI the control's compile is the one the Clang sanitizer build already makes (the same file, with `-std=c++20 -Wall -Wextra -Werror` at 33 sinks), which passes there. On that host, a review run needs the host's Clang as `clang++`, as both round 1 reviews already used for the sanitizer gate.

Across 24 further seeds per size, every walk plant is caught at 33 sinks in all 24, and the head passes them all.

---

[A683zf] Round 1: walk only the sinks an ACMP entry changed

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
- Four tests at 1, 8, 32 and 33 sinks on two interfaces (three at 33 sinks, since round 2): `AcmpWalk.OneSinkMatchesTheFullWalk` (4,000 entries), `EightSinksMatchTheFullWalk` (6,000), `ThirtyTwoSinksMatchTheFullWalk` (8,000), `ThirtyThreeSinksMatchTheFullWalk` (8,000, sink 32 in the second mark word). Each also requires that its entries reach a registered reservation and owe a response, on the second word at 33 sinks, where an owed probe of sink 32 must also leave while its timer waits for it. After every step each mark word and the interface mark must be zero (round 2).
- At 33 sinks (since round 2) BIND_RX, UNBIND_RX and GET_RX_STATE reach every sink, a quarter of them sink 32, and transmit room is withdrawn and restored as at 1, 8 and 32 sinks, so sink 32's responses and probes are owed and released. Sink 32 sits alone on a third interface. While frames are owed and the port has room, half the steps poll first. Round 1's test sent no command to sink 32 and withdrew no room at 33 sinks, a restriction from before #31 widened the owed-release mask; the merge of #33 made it unnecessary, and round 2 lifts it.
- 18 new plants, one for each mark site, the mark word's write and its read, each caught by the trace assertion ("the changed-sink walk makes the full walk's calls"): `walk-bind-unmarked`, `walk-unbind-unmarked`, `walk-probe-response-unmarked`, `walk-adp-unmarked`, `walk-expired-interface-unmarked`, `walk-aging-unmarked`, `walk-expiry-unmarked`, `walk-registered-unmarked`, `walk-kind-unmarked`, `walk-unregistered-unmarked`, `walk-started-unmarked`, `walk-release-unmarked`, `walk-probe-left-unmarked`, `walk-restore-unmarked`, `walk-rollback-unmarked`, `walk-mark-interface-dropped` (`mark()` without the interface bit), `walk-mark-word-zero` and `walk-marked-word-zero` (word 0 for every sink, caught at 33 sinks only). They sit after #31's plants and before the wire and entity plants (the entity self-test reads the table's last three).
- Thirteen existing plants follow the lines they plant into, with the same defect: `acmp-unbind-keeps-srp`, `acmp-unbind-srp-after-response`, `acmp-registered-keeps-no-tk`, `acmp-unregistered-keeps-srp`, `acmp-expiry-not-consumed`, `owed-answer-keeps-the-hold`, `acmp-first-owed-releases-every-change`, `acmp-no-aging`, `acmp-roll-back-keeps-the-bindings`, `acmp-expiry-reads-the-clock-twice`, `acmp-owed-probe-never-starts`, `acmp-owed-probe-no-resp-2s`, `acmp-expiry-due-at-its-first-read`.
- Two existing plants escaped the walk at first: `acmp-timer-port-called-every-time` (`rearm()` calling the port for every armed interface) and `acmp-publish-stream-cache-stale` (the published stream cached as 0). Each showed only on an entry that visited an untouched sink or interface, which the changed-sink walk no longer makes. Their tests now make such an entry: A17 adds `acmp_set_started` on interface 1's sink and requires no timer call ("A17 a change that leaves an interface's earliest deadline keeps its timer"), and A31 adds `acmp_set_started` on the settled sink and requires no publication ("A31 an entry that leaves the settled stream publishes nothing"). Both plants are caught by those assertions.
- `docs/TESTS.md` and `docs/TRACEABILITY.md` are regenerated (`test_inventory.py --write`, `traceability.py --write`); ACMP-13 has its record in `docs/requirements.json` and its origin in `scripts/requirement_records.py`. `docs/VERIFICATION.md` counted 466 core plants (473 since round 2).

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

The dependency install steps were not run: the host stands in with the pinned GoogleTest/GMock 1.14.0, Clang 18.1.3 and clang-tidy 18.1.3 the gates require, Mermaid CLI, and the RISC-V GCC and QEMU the bare-metal step uses. The GCC and Clang-sanitizer CTest gates ran with the host's GCC 16.2.1 and Clang 23.1.4 (the pinned Clang 18 cannot build against the host's C++ library); the hosted run at the head used the CI image's GCC 13.3.0 and Clang 18.1.3.

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
