# [A766] kebag-logic/tsn-c-stack#32, PR #34 round 2 (HANDOFF)

**Status: committed, not pushed. Head `a530ecafe7e503a57c81a5aba4ffe38fa8f37e7e`** (tree `3a247e5d`) on branch `32-acmp-dirty-walk` in `<lanes>/tsn-c-stack-32-walk`. That is three commits on round 1's `9043b926`, with no merge, rebase, force or amend. `git diff --stat 9043b926 -- src include` is empty.

- **Authority:** the ruling on PR #34, issuecomment-6789256216, items 1 to 6.
- **TAKEN:** issue #32, issuecomment-6789295592 (07:58 CET). **REVIEW READY:** issuecomment-6791062315 (09:31 CET), with the head.
- **PR body:** `PR-BODY.md` (first line "[A766]", "Closes #32"; round 1's body follows, corrected in place).
- **Receipts:** `receipts/`. `<scratch>`, `<lanes>`, `<tools>`, `<management>`, `<home>` and `<node>` (the Node.js install that runs the Mermaid CLI) stand for the host paths they replace. Files over 200 KB are listed by SHA-256 and size in each directory's `not-copied.txt`.

**Host incidents.**
- Some time between 08:04 and about 08:33 CET, the host's root filesystem, which holds `<home>`, went into emergency read-only mode (`/ ext4 rw,relatime,emergency_ro`), so every write to this directory failed with EROFS. This handoff, `PR-BODY.md`, `receipts/` and `scripts/` were therefore written to `<scratch>/out/`, in this directory's layout. The lane and the scratch area stayed writable.
- From about 08:42 I/O on the scratch area stalled: `index-pack` sat in `xlog_force_lsn`, I/O pressure reached about 50 % and load about 160.
- About 09:50 the host was restarted. Nothing of this round was mid-run: the commits, the clean-clone gates and the reviewers' scripts had all finished.
- After the restart the root filesystem was writable (`rw,relatime`). At 09:56 `<scratch>/out/` was copied here unchanged, except for a draft fragment of the PR body, which was not kept. R824-1's `ci_run.sh` was then run to its end (section 5), and this file and `PR-BODY.md` were updated with its result.

## 1. Changes (file:line at `a530ecaf`)

| Commit | File:line | Change | Ruling item |
|---|---|---|---|
| `4cdf2a2` | `tests/test_acmp_walk.cpp:136-142` | At 33 sinks, three interfaces: sinks 0 to 31 keep the 32-sink map, and sink 32 sits alone on interface 2 (MAC `kMac1 + 1`) | 1 |
| `4cdf2a2` | `tests/test_acmp_walk.cpp:188-189` | `commanded_sink()`: at 33 sinks a quarter of BIND_RX, UNBIND_RX and GET_RX_STATE go to sink 32 and the rest to any sink. Round 1 folded sink 32 onto sink 0 | 1 |
| `4cdf2a2` | `tests/test_acmp_walk.cpp:239`, `:251`, `:288` | Talker commands, ADPDUs and expiries are drawn over `cfg.n_interfaces` (still `below(2)` at 1, 8 and 32 sinks) | 1 |
| `4cdf2a2` | `tests/test_acmp_walk.cpp:269-272` | At 33 sinks, while frames are owed and the port has room, half the steps poll first | 1 |
| `4cdf2a2` | `tests/test_acmp_walk.cpp:310` | Transmit room is withdrawn at every size (round 1 had `wide ||`) | 1 |
| `4cdf2a2` | `tests/test_acmp_walk.cpp:329-336`, `:349-359` | Reach checks: a response of sink 32 owed, and at 33 sinks an owed probe of sink 32 leaving while its timer waits for it | 1 |
| `4cdf2a2` | `tests/test_acmp_walk.cpp:341-346` | After every step each `dirty` word and `dirty_if` is zero ("a completed entry leaves no sink marked" / "... no interface marked") | 2 |
| `4cdf2a2` | `tests/mutations.json:7610-7757` | Seven plants after round 1's 18 walk plants (`walk-marked-word-zero`) and before the wire and entity plants; the last three stay the entity plants | 1, 2 |
| `4cdf2a2` | `tests/mutations.json:7420`, `:7454` | `walk-release-unmarked` and `walk-probe-left-unmarked` also list `AcmpWalk.ThirtyThreeSinksMatchTheFullWalk` | 1 |
| `4cdf2a2` | `docs/VERIFICATION.md:24` | RES-2's text (covering R823-1 R1's line), with the seven new plants and 473 core plants | 4 |
| `4cdf2a2` | `CHANGELOG.md:5` | The walk entry gains the 33-sink shape and the cleared-mark requirement | 1, 2 |
| `4cdf2a2` | `docs/TESTS.md`, `docs/TRACEABILITY.md:27` | Regenerated (`test_inventory.py --write`, `traceability.py --write`). ACMP-13's row names the four `AcmpWalk` tests that carry the item 2 assertions | 2 |
| `8661947` | `tests/test_acmp_walk.cpp:20` | `static_assert(ACMP_MAX_INTERFACES <= sizeof(acmp::dirty_if) * 8u, "the interface mark holds a bit for every interface")` | 5 (S-3) |
| `8661947` | `scripts/check_conditionals.py:13`, `:140`, `:175-198` | `interface_controls()`: the walk test, with GCC and Clang and `-fsyntax-only`, compiles with `ACMP_MAX_INTERFACES` at 4 and 32 and is refused at 33 by that message | 5 (S-3) |
| `8661947` | `docs/VERIFICATION.md:33` | The conditional row states the interface control | 5 |
| `a530eca` | `docs/REQUIREMENTS.md:41-43` | RES-1's text: each entry marks a sink before the next walk reads it, the two restores right after the reset | 4 |
| (PR body) | `PR-BODY.md` | Round 2 section. Round 1's 33-sink paragraph is replaced (F1), with R2's plant sentence and RES-3's compilers (R3's line). It states the code size, the +132 B consumer effect and the ruling link (item 3), and the parent's target figures (S-2) | 1, 3, 4, 5 |

## 2. Tests and the plants they kill

**The new plants.** Each plant's "escape without the test" is its result under round 1's ACMP suites at `9043b926`: `acmp_tests` (16 sinks), `acmp_wide` and `acmp_walk` (33 sinks). They were built as the mutation driver builds those arms, with the plant in the head's `src/acmp.c`, which equals round 1's (`scripts/escape_light.sh`, `receipts/escape/escape.txt`). The unplanted core passes all three. R824-1's `suite_on_plant.sh` was started for this first and stopped during the host's I/O stall, because its full CMake build per plant was too slow. R823-1's probes of the same four second-word texts at round 1 agree.

| Plant | Site | Killed by (message) | Without round 2's test |
|---|---|---|---|
| `walk-bind-second-word-unmarked` | `bind()`: `if (k < 32u) { mark(a, k); }` | `AcmpWalk.ThirtyThreeSinksMatchTheFullWalk` ("the changed-sink walk makes the full walk's calls") | escapes: `acmp_tests`, `acmp_wide` and `acmp_walk` all pass |
| `walk-unbind-second-word-unmarked` | `unbind()` | the same | escapes: all three pass |
| `walk-release-second-word-unmarked` | `acmp_poll`'s release loop | the same | caught only by #31's `acmp_wide` (`AcmpWide.OwedResponsesHoldOnlyTheirOwnSinksChanges`, `SinksThirtyOneAndThirtyTwoWaitOnlyForTheirOwnResponses`); round 1's walk test passes |
| `walk-probe-left-second-word-unmarked` | `probe_left()` | the same | escapes: all three pass |
| `walk-marks-never-cleared` | `finish()`: no `memset(a->dirty, ...)` | all four `AcmpWalk` tests ("a completed entry leaves no sink marked") | escapes: all three pass |
| `walk-interface-marks-never-cleared` | `finish()`: no `a->dirty_if = 0u` | all four ("a completed entry leaves no interface marked") | escapes: all three pass |
| `walk-clear-first-word-only` | `finish()`: `sizeof a->dirty[0]` | `ThirtyThreeSinks` ("a completed entry leaves no sink marked") | escapes: all three pass |

- In the clean-clone campaign, each is CAUGHT by exactly its listed needles: `receipts/gates/build-validation/mutations/results-summary.json` and R824-1's `plant_kills.py` output (`receipts/reviewers/r824/new-and-merged-plants.txt`).
- At 33 sinks, the four second-word plants fail at steps 12, 52, 274 and 276 of 8,000 (the discovery run, `receipts/discovery/`).
- **The existing walk plants after the change.** All 18 are still CAUGHT by their listed tests. `walk-release-unmarked` and `walk-probe-left-unmarked` are now also caught at 33 sinks, which their kill lists name. `walk-expiry-unmarked` and `walk-kind-unmarked`, round 1's 33-only kills, are caught at the new 33-sink sequence: at steps 438 and 512.

## 3. Boundary evidence

- **Sink 32 is the boundary.** It is the only sink in the second mark word at 33 sinks, one past the first word. Over 24 further seeds a size, with the campaign's own plant text (`receipts/seeds/results.json`, `scripts/seed_sweep.py`):

  | Variant | 1 sink | 8 sinks | 32 sinks | 33 sinks |
  |---|---:|---:|---:|---:|
  | head (no plant) | 0 | 0 | 0 | 0 |
  | the four `*-second-word-unmarked` plants, each | 0 | 0 | 0 | 24 |
  | `walk-clear-first-word-only` | 0 | 0 | 0 | 24 |
  | `walk-marks-never-cleared`, `walk-interface-marks-never-cleared`, each | 24 | 24 | 24 | 24 |
  | `walk-kind-unmarked` | 4 | 16 | 19 | 24 |
  | `walk-expiry-unmarked` | 14 | 23 | 22 | 24 |
  | `walk-probe-left-unmarked` | 0 | 20 | 24 | 24 |

  Cells count the failing seeds of 24. The second-word plants are seen only where a second word exists, every time. The head passes every seed at every size, its reach checks included.
- **Why sink 32 has its own interface and why owed frames are polled first.** Both were measured with an instrumented copy of the test (`receipts/discovery/`):
  - Measured on the draft that already had sink 32's own interface. Without the poll bias, at 33 sinks, no owed probe of sink 32 left while its timer waited for it. Over 0, 1 in 4, 1 in 8 and 1 in 16 commands to sink 32, 0 of 7 to 36 polls that found sink 32's probe at the queue head found it still awaited: a later command, restore or rollback had always overtaken it.
  - With half the steps polling first while frames are owed, 20 such probes leave. `walk-probe-left-second-word-unmarked` then fails at step 276.
  - On a shared interface, a missed probe-left mark shows only when sink 32's new deadline is that interface's earliest. On its own interface it always does.
  - As a side effect, R824-1's c4 (`probe_left()` marking word 0 instead of sink 32) is now caught by `AcmpWalk.ThirtyThreeSinksMatchTheFullWalk`. Round 1's suite and R824-1's own driver do not catch it.
- **The interface mark's width.** The walk test compiles at `ACMP_MAX_INTERFACES` 4 and 32 and is refused at 33 with GCC and Clang (`receipts/gates/build-validation/conditionals.log`).
- **`struct acmp` on RV32** (`riscv64-elf-gcc -march=rv32imac -mabi=ilp32`):

  | Sinks | `main` `9deb0dd`, bytes | head, bytes |
  |---:|---:|---:|
  | 16 | 5,072 | 5,080 |
  | 32 | 9,184 | 9,192 |
  | 33 | 9,480 | 9,488 |

  `struct acmp_owed` is unchanged: 80 bytes, and 84 at 33 sinks. Round 2 does not change these.
- **R824-1's matrix at the head:** 560 of 560 PASS, at mask widths 16, 32, 33, 64 and 255, sink counts 1 to 255, and LIFT, REENTER and NOOPEN.

## 4. Gates (clean clone of `a530ecaf`, `git clone --no-local`, detached; status empty before and after)

Both `run:` testing steps of `quality.yml` ran concurrently, `--jobs 16` (`scripts/tsn_ci.sh`, `receipts/gates/`):

| Target | Step | rc | Result |
|---|---|---:|---|
| Linux hosted | `python3 scripts/validate.py --work <w> --jobs 16 --graphs` | 0 | See below. 570 s |
| RV32 bare-metal | `python3 scripts/baremetal.py --work <w> --jobs 16` | 0 | See below |
| (not run) | the two dependency install steps | n/a | The host is not the CI image; the pinned tools stand in (`receipts/gates/tools.txt`) |

- **Linux, validate.py:** 28 of 28 gates rc 0 (`gates.json`).
  - entity-golden, entity-controls, boundary, needles, assertion-templates, dependencies, comments, conditionals (with the new interface control), port-contracts, acmp-cache, registration-controls, license, traceability, test-inventory, coverage-controls, privacy-selftest, privacy.
  - The GCC build: configure, build, test (10 of 10, `acmp_walk` among them) and coverage. Coverage is 100 % after exclusions; `src/acmp.c` is 847/847 lines and 436/436 branches.
  - The Clang-sanitizer build: configure, build and test, 10 of 10.
  - mutation: `{"CAUGHT": 477, "ESCAPED": 0, "ERROR": 0}`. mutation-controls, static-analysis and graphs (4 rendered).
- **RV32, baremetal.py:** Debug and Release rc 0. The core imports are those of `main`: Debug `__mulsi3`, `__umodsi3`, `ctrl_reentry_assert`, `memcpy`, `memset`, `port_assert_failed`; Release without `__mulsi3` and `port_assert_failed`. The Release ELF is byte-identical to round 1's (`a9cc5f9e...`).
- **Toolchain.** GCC 16.2.1 and the host Clang 23.1.4 (`clang`, which the CMake gates call), the pinned Clang 18.1.3 (`clang-18`), clang-tidy 18.1.3, cppcheck 2.22.0, GoogleTest/GMock 1.14.0, Mermaid CLI 11.16.0 (installed in scratch), riscv64-elf-gcc 16.2.0 and QEMU 11.1.3.

### Bare-metal image size, before and after (`riscv64-elf-size`; `receipts/rv32/`)

| Build | `main` `9deb0dd` | round 1 `9043b926` | round 2 `a530ecaf` |
|---|---:|---:|---:|
| Debug smoke image, text | 51,964 | 52,652 | 52,652 |
| Release smoke image, text | 41,645 | 42,337 | 42,337 |
| Debug `acmp.c`, text | 21,429 | 22,189 | 22,189 |
| Release `acmp.c`, text | 20,365 | 21,077 | 21,077 |
| bss (both) | 65,552 | 65,552 | 65,552 |
| image hash with debug stripped, Debug | `01185b9c` | `35a76f5f` | `35a76f5f` |
| image hash with debug stripped, Release | `c3e91855` | `dcbc5bb0` | `dcbc5bb0` |

Round 2 moves no byte of either image. The change against `main` is +688 B (Debug) and +692 B (Release) of image text, +760 and +712 B of `acmp.c` text.

## 5. Both reviewers' scripts at `a530ecaf`, unchanged (`receipts/reviewers/`)

All scripts were copied from the review packets and checked against their SHA-256 (`receipts/reviewers/*/scripts.sha256`, 0 mismatches). I wrote only the drivers that call them (`scripts/r823_runs.sh`, `r824_runs.sh`, `r824_runs2.sh`, `r824_ci.sh`).

**R823-1:**

| Script | rc | Output at the new head |
|---|---:|---|
| `launch.sh` + `differential.sh HEAD MAIN OUT 60` | 0 | 480 cases, 0 divergent. At 33 sinks with lift 1: owed-max 8, and sink-32 changes reported |
| `launch.sh` + `probe_mutants.py` | 0 | `bind-`, `unbind-`, `probe-left-` and `release-marks-only-word-zero` each fail `AcmpWalk.ThirtyThreeSinksMatchTheFullWalk`; at round 1 the first three passed every test. `marks-never-cleared` fails all four `AcmpWalk` tests. The tree was restored by hash |
| `plant_merge.py`, `plant_delta.py`, `plant_defects.py` | 0 | Both parents' orders kept and nothing lost. The seven new plants are new; the last three are the entity plants |
| `sanitizers_standin.sh` (host Clang 23.1.4) | 0 | 10 of 10 |

R823-1's packet has no CI script of its own: its validate and baremetal receipts are the repository's two gates, which section 4 ran.

**R824-1:**

| Script | rc | Output at the new head |
|---|---:|---|
| `build_dwalk.sh` (16, 32, 33, 64, 255) and `matrix.sh ... 20000` | 0 | 560 of 560 PASS |
| `build_dwalk.sh` with c1 to c4, and `dwalk` | n/a | The same as at round 1: c1 caught; c2 and c3 caught only under LIFT; c4 passes. This is the reviewer's own driver, whose map puts k and k mod 32 on one interface |
| `suite_on_plant.sh` with c1 to c4 | n/a | c1 is caught by `acmp_tests`, `acmp_wide` and `acmp_walk`. c2 and c3 are now caught by `acmp_walk` as well as `acmp_wide`. c4 is now caught by `acmp_walk` (`ThirtyThreeSinks`); at round 1 no binary caught it |
| `merge_survival.sh` | 0 | As at round 1 for every path, except `tests/test_acmp_walk.cpp`, which round 2 changes |
| `plant_merge_audit.py` | 0 | 477 plants. 470 are round 1's (464 equal to an unconflicted parent version, and the four hand-merged or re-anchored of round 1). The two kill lists extended here now differ from their parent. The seven new plants are in neither parent. Both orders kept, the walk plants contiguous, the entity plants last |
| `plant_kills.py` on the clean-clone campaign | 0 | 477 CAUGHT. Each walk plant's kill words are as listed above |
| `sanitizer_gate.sh ... /usr/bin/clang /usr/bin/clang++` | 0 | configure, build and test rc 0, 10 of 10 |
| `ci_run.sh` (first attempt) | 1 | My driver did not put `clang-18` on PATH. The script's `env.sh` adds only its `bin/` links and clang-tidy, so the gates that call `clang-18` could not start (`FileNotFoundError: 'clang-18'`). Kept as `ci-head-1/`; baremetal rc 0 |
| `ci_run.sh` (second attempt, `clang-18` and the Mermaid CLI on PATH) | stopped | Started 08:41. Under the host's I/O stall it had reached only the third of its 28 gates after 25 minutes (entity-golden and entity-controls rc 0). I stopped it at 09:07 to cut my share of the I/O load |
| `ci_run.sh` (third attempt, after the host restart, the same driver `scripts/r824_ci.sh`) | validate 1, baremetal 0 | 09:56 to 09:59, `receipts/reviewers/r824/ci-head-2/`; the clone's status is clean before and after. Of the 17 source gates, 16 are rc 0. `conditionals` is rc 1, so validate's fail-fast does not start the build, test, campaign, static-analysis or graphs tasks. Baremetal is rc 0: Debug and Release, the same as section 4. **Why `conditionals` fails, and why only here:** the script's `bin/clang++` is a link to the pinned Clang 18.1.3. Its front end cannot parse this host's libstdc++ 16 headers, the same limit that makes `clang-sanitizers-build` fail in R824-1's own run. Round 2's interface control (`interface_controls()`) compiles the gtest walk test with `clang++`, and it stops at its first case, 4 interfaces, inside `<semaphore>`. The C capacity controls before it pass with that Clang. With the host's Clang 23.1.4 as `clang++` the gate is rc 0 (section 4). In the CI image the control's compile is the one CMake's Clang build already makes and passes: the same file, `-std=c++20 -Wall -Wextra -Werror` and `ACMP_MAX_SINKS=33u` (`compile_commands.json` of section 4's sanitizer build) |

## 6. Ruling items: acceptance

| Item | Required | Met by |
|---|---|---|
| 1 | Commands reach every sink at 33, sink 32 included; room withdrawn as at 1, 8, 32; four second-word plants CAUGHT through `ThirtyThreeSinks` by its own message | Sections 1 and 2; the campaign 477/0/0. The PR body's 33-sink paragraph is replaced |
| 2 | The cleared-mark assertion; a plant dropping the clear CAUGHT; ACMP-13's row names the test | Three plants CAUGHT; `docs/TRACEABILITY.md:27` |
| 3 | Deferred to the pin move; the PR body states the code size and the +132 B, linking the ruling | PR body, item 3 |
| 4 | R823-1 R1 to R3, R824-1 RES-1 to RES-3, R824-1's text where both cover one line | `docs/REQUIREMENTS.md:41-43` (RES-1), `docs/VERIFICATION.md:24` (RES-2 for R1), the PR body (R2; RES-3 for R3) |
| 5 | S-3 compile-time; S-2 the parent's figures | `tests/test_acmp_walk.cpp:20` and its conditional control; PR body, item 5 |
| 6 | Gates on a clean clone; both reviewers' scripts | Sections 4 and 5 |

## 7. Not done, and limits

- Nothing is pushed and no PR is opened; the manager does both. No hosted run exists for this head yet.
- **The "only the changed sinks" claim.** The new assertion catches a mark that outlives its completion, so a core that never clears walks every sink it ever touched. It cannot see an entry that marks more sinks than it changed and then clears them, since such a core makes the full walk's calls. The ruling asks for the outlives-completion assertion, and that is what is built.
- The reviewers' benchmark source (`bench_finish_author_copy.c`) was not re-run: `src/` and `include/` are byte-identical to round 1's, so its cycles are round 1's.
- R823-1 S-1 and S-3 were not taken; the ruling takes S-2 and S-3 of R824-1 only.
- **The interface control on a host where `clang++` is the pinned Clang 18 (found after REVIEW READY, by R824-1's `ci_run.sh`).**
  - Before round 2, the conditional gate compiled C++ only with `g++`. Its new interface control (`scripts/check_conditionals.py:175-198`) also compiles the walk test with `clang++`.
  - So on this host, under an environment that puts the pinned Clang 18 first as `clang++` (R824-1's `env.sh`, R823-1's shims), `conditionals` is now rc 1, and validate's fail-fast skips the compile and campaign tasks that this environment used to run.
  - Hosted CI and section 4's run are unaffected. A reviewer on this host can let `clang`/`clang++` be the host's Clang 23.1.4, as both reviews already did for the sanitizer gate.
  - If the gate should also pass in that environment, the control could compile with `g++` alone. That change is to a script, but it would move the head, and REVIEW READY is already posted for `a530ecaf`. I left the head as it is: the choice is the manager's.

## 8. Run history (2026-11-11, CET)

- 07:57 Read the handoff, the ruling and both reviews. 07:58 posted TAKEN.
- 08:04 Mermaid CLI 11.16.0 installed in scratch. Skeleton HANDOFF written to the output directory.
- 08:05 to 08:14 Test edits. A discovery campaign over the 25 walk plants:
  - The first lift (commands to sink 32 and room withdrawn) left `walk-probe-left-second-word-unmarked` uncaught and lost `walk-kind-unmarked` at 33 sinks.
  - An instrumented copy showed why: owed probes of sink 32 were always overtaken before they left.
  - Sink 32 was given its own interface and owed frames a poll bias. All 25 were then caught.
- 08:14 The seed sweep (24 seeds a size), then the cheap source gates on the working tree: needles, comments, privacy, license, port contracts, static analysis and conditionals, each rc 0.
- 08:16 Commits `4cdf2a2`, `8661947`, `a530eca`, each stage with its docs regenerated.
- 08:18 to 08:28 The clean-clone gates at `a530ecaf`: validate rc 0 in 570 s, baremetal rc 0. Bare-metal also ran at `main` and at `9043b926` for the size table.
- 08:19 onwards Both reviewers' scripts.
- About 08:33 The root filesystem was found read-only, and the output directory with it. Staged in `<scratch>/out/`.
- 08:41 R824-1's `ci_run.sh` re-run with `clang-18` on PATH.
- About 08:42 to 08:47 the scratch area's I/O stalled, then resumed. It stalled again from about 08:55 (I/O pressure about 50 %, load about 125). The escape check by `suite_on_plant.sh` was replaced by a direct build (`scripts/escape_light.sh`), and the second `ci_run.sh` was stopped at 09:07.
- 09:31 Posted REVIEW READY with the head. Stopped.
- About 09:50 the host restarted. 09:54 Resumed: the lane is clean at `a530ecaf` (with `src/` and `include/` equal to `9043b926`), and every gate and reviewer run of the round had completed before the restart. The root filesystem was writable again.
- 09:56 Copied `<scratch>/out/` here. Ran R824-1's `ci_run.sh` to its end; it finished 09:59 (section 5). Updated this file and `PR-BODY.md`. No comment was posted again.
