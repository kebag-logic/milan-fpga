# [A752d] kebag-logic/tsn-c-stack#31: the ACMP owed-release mask sized from ACMP_MAX_SINKS (DONOR HANDOFF)

**Status: committed, not pushed. Head `c6013804d0fec6bc763a64b496f1a52d4a5d9f6a`** on branch `31-acmp-mask-width`, one commit on `origin/main` `ea4af6f` (`Merge pull request #28`), in a fresh clone of `https://github.com/kebag-logic/tsn-c-stack.git`. Every `run:` step of the stack's CI that tests passed on a clean clone of the head (section 3). The PR body is `DONOR-PR-BODY.md` ("Closes #31"). The manager pushes the branch and opens the PR.

- Authority: the round 4 ruling on milan-fpga #859 (issuecomment-6746289265), item 1; the owners comment (issuecomment-6746307340): the donor issue is kebag-logic/tsn-c-stack#31.
- STOP condition (a change to tsn-c-stack's public API or to the mailbox contract's major version): not met. No function, callback, configuration, view or counter changes. The changed field, `acmp_owed.release`, is core-owned machine storage (`docs/PORTING.md`, "ACMP machine storage"), and at up to 32 sinks its layout is unchanged. The milan-fpga mailbox contract is untouched by this change.
- Receipts: `receipts/r4/donor/` (`gates/` the clean-clone CI run, `probes/` the probes, `scripts/` the runners). `$SCRATCH`, `$TOOLS`, `$LANES` and `$HOME` stand for the host paths they replaced.

## 1. Changes (file:line at `c6013804`, reason)

| File:line | Change | Reason |
|---|---|---|
| `include/acmp.h:165` | `#define ACMP_RELEASE_WORDS ((ACMP_MAX_SINKS + 31u) / 32u)` | the mask's size from `ACMP_MAX_SINKS` (#31). A plain constant: the coding standard forbids `#if`, so no conditional typedef |
| `include/acmp.h:402` | `uint32_t release[ACMP_RELEASE_WORDS];` in `struct acmp_owed` | one bit per sink at every count; one word at up to 32 sinks, so the owed entry stays 80 bytes there and `AcmpOwed.OwedSetIsEightFramesOfEightyBytes` holds |
| `src/acmp.c:35-36` | `_Static_assert(sizeof ((struct acmp_owed *)0)->release * 8u >= ACMP_MAX_SINKS, ...)` | the ruling's build-time refusal: a mask narrower than the count is refused |
| `src/acmp.c:296`, `:323` | `transmit` and `respond` take `unsigned release`: one plus the sink whose change the frame releases, zero for none | every caller releases at most one sink (two pass `1u << k`, the rest `0u`); the form `probe_of` already uses |
| `src/acmp.c:309-312` | `transmit` clears the stored mask and sets word `(release - 1) / 32`, bit `(release - 1) % 32` | no shift reaches the word width |
| `src/acmp.c:317`, `:1269` | the change-owed loop (`transmit`) and the release loop (`acmp_poll`) read `(o->release[k / 32u] >> (k % 32u)) & 1u` | as above |
| `src/acmp.c:850`, `:905` | `bind_response` and `unbind` call `respond(a, interface, &r, k + 1u)` | in place of `1u << k`, the shift by 32 at sink 32 |
| `CMakeLists.txt:63-68` | `tsn_wide` (the core at `ACMP_MAX_SINKS=33u`, `-fsanitize=shift,undefined -fno-sanitize-recover=shift,undefined`, public so the test sees the same layout) and `core_test(acmp_wide ...)` | the ruling's unit test at 33 sinks |
| `tests/test_acmp_wide.cpp` (new) | `AcmpWide.OwedResponsesHoldOnlyTheirOwnSinksChanges` (`:67`), `AcmpWide.SinkZerosOwedResponseLeavesSinkThirtyTwoFree` (`:92`); the fixture asserts 33 sinks at run time (`:25`) | sinks 32 and 0 bound with no transmit room; each change waits only behind its own owed response (Milan v1.2 5.5; ACMP-09). The conditional gate compiles every test file at the default 16 sinks, so a `static_assert` there failed it (first run, section 4) |
| `scripts/mutation.py:23-26`, `:45`, `:50`, `:53-54`, `:142` | the `acmp_wide` arm: its test source and the `WIDE` flags on its C and C++ compiles and its link | the campaign builds the arm as CMake does |
| `tests/mutations.json` | three new plants (section 2); seven anchors follow the changed lines (section 2) | every test declaration has a named plant (`test_inventory.py`); a plant's `old` must match once |
| `docs/PORTING.md:76-78`, `:328` | the owed set's size by sink count, the build-time refusal, the `release` row's bit numbering | the documented storage; `640 bytes on both targets` kept (a pinned phrase) |
| `docs/VERIFICATION.md:24`, `:26` | 443 core plants; the 33-sink row | the campaign's count; the new binary |
| `docs/TESTS.md`, `docs/TRACEABILITY.md` | regenerated (`test_inventory.py --write`, `traceability.py --write`) | the two tests under ACMP-09 |
| `CHANGELOG.md:5` | the entry | the change log's Unreleased list |

The commit subject is one line with no body and no trailers, under the identity `check_privacy.py` accepts.

## 2. Checks, planted mutants and failing words

| Check | Plant | Fails with |
|---|---|---|
| `AcmpWide.OwedResponsesHoldOnlyTheirOwnSinksChanges` | `acmp-wide-release-word-ignored`: `transmit` writes the bit into word 0 | "sink 32's change waits behind its owed response" |
| the same | `acmp-wide-owed-count-word-ignored`: the change-owed loop reads word 0 | "sink 32's change waits behind its owed response" |
| the same | `acmp-wide-release-loop-word-ignored`: the release loop reads word 0 | "sink 32's response left: one change is reported" |
| `AcmpWide.SinkZerosOwedResponseLeavesSinkThirtyTwoFree` | `acmp-wide-owed-count-word-ignored` | "sink 0's owed response holds sink 0 and not sink 32" |
| the same | `acmp-wide-release-loop-word-ignored` | "leaves sink 32's count at zero" |
| the build-time refusal (`src/acmp.c:35`) | the mask planted back to one word (`uint32_t release[1]`), compiled at 33 sinks | "static assertion failed: \"the owed release mask holds a bit for every sink\"" (`probes/refusal-33.log`); the same tree compiles at 32 (`refusal-32.log`); the head compiles at 16, 33, 64 and 65 (`fix-sizes.log`) |
| the new test against `main`'s core | `main` `ea4af6f`'s `src/acmp.c` at 33 sinks | "src/acmp.c:844:31: runtime error: shift exponent 32 is too large for 32-bit type 'unsigned int'" (`probes/wide-on-main-norecover.log`); recovering, both tests fail: "W1 sink 0, which owes nothing, is not held by sink 32's response", "W2 sink 0's owed response holds sink 0 and not sink 32" (`wide-on-main-recover.log`) |

Each of the three plants passes all 126 tests of the 16-sink `acmp_tests` (`probes/wide-plants-at16.log`, `scripts/wide_plants_at16.py`): only the 33-sink binary detects them.
The seven existing plants whose `old` named a changed line plant the same defect at the new text: `acmp-unbind-echoes-the-talker`, `acmp-unbind-srp-after-response`, `acmp-unbind-change-before-response` and `owed-bind-answer-lost-after-decline` (the call, `k + 1u` for `1u << k`), `acmp-change-not-held-for-its-response` and `acmp-first-owed-releases-every-change` (the two loops), and `owed-entry-widened` (`uint64_t release[ACMP_RELEASE_WORDS]`). All seven are caught in the final campaign. No plant or test was removed.

## 3. Gates (clean clone of `c6013804`)

`git clone --no-local` of the donor clone, checked out detached at the head; status and diff empty before and after (`gates/gates-final.*`). `scripts/run_step.sh` runs the CI's two testing steps concurrently, `--jobs 8` (the CI's 16 on this lane's 8 CPUs):

| `run:` step | rc | Result | Wall, peak |
|---|---:|---|---|
| Install host dependencies (`apt-get`, `npm`) | not run | the host is not the CI image: the pinned GoogleTest/GMock 1.14.0, Clang 18.1.3 (`clang-18`, the lexer), clang-tidy 18.1.3 and Mermaid CLI 11.16.0 stand in; GCC 16.2.1, Clang 23.1.4 (the sanitizer build's `clang`), cppcheck 2.22.0, CMake 4.4.5 and PyYAML are the host's | |
| `python3 scripts/validate.py --work build-validation --jobs 16 --graphs` (run with `--jobs 8`) | 0 | 28 of 28 gates rc 0 (`gates/gates.json`, `gates/*.log`, `*.rc`): mutation `{"CAUGHT": 447, "ESCAPED": 0, "ERROR": 0}` (`campaign-summary.json`; the full `results.json`, 999,398 B, by SHA-256 in `gates/not-copied.txt`); coverage 100 % lines and branches after exclusions, `src/acmp.c` 815/815 and 426/426; GCC and Clang-sanitizer CTest 9 of 9 each; static analysis, boundary, conditionals, comments, needles, traceability, test inventory, privacy, graphs rc 0 | 3 min 54 s, 455,912 kB |
| Install RV32 dependencies | not run | as above: RISC-V GCC 16.2.0 (`riscv64-elf-gcc`), QEMU 11.1.3 | |
| `python3 scripts/baremetal.py --work build-rv32 --jobs 16` (run with `--jobs 8`) | 0 | Debug and Release rc 0 (`gates/results.json`); core imports equal to `main`'s (Release `__umodsi3`, `ctrl_reentry_assert`, `memcpy`, `memset`) | 1.4 s, 145,900 kB |

R807-1's probe, a byte-identical copy of its `acmp_mask_probe.sh` and `acmp_mask_probe.cpp` (SHA-256 `9b19069b...`, `5001e087...`): rc 0 at the head, "2 tests ... PASSED", `change_owed[0]=0` after sink 32's BIND_RX and `change_owed[32]=0` after sink 0's (`probes/probe-head.log`). rc 1 at `main` (`acmp.c:844:31`, `probe-main.log`) and at milan-fpga's pin `70936b77` (`acmp.c:816:31`, `probe-pin.log`).

RV32 size (`probes/rv32-sizes.txt`, `rv32-acmp-text-by-opt.txt`): `src/acmp.c` text at 16 sinks `-Os` 10,825 to 10,921 B, `-O2` 16,029 to 16,141 B, `-O3` 19,365 to 20,365 B. The `-O3` growth is the loops reading the stored mask, which no longer fold at inlined `respond(..., 0u)` calls and are unrolled; milan-fpga compiles the stack at `-Os`. A variant that keeps a local copy of the mask was measured at 10,889 B (`-Os`) and not taken.

## 4. Run history

- 18:33 CET: clone, branch `31-acmp-mask-width` from `origin/main` `ea4af6f`. Toolchain checked (section 3).
- 18:35 to 18:44: the change, the test, the arm and the plants; GCC build and CTest 9 of 9; R807-1's probe rc 0 on the working tree (18:43); the new test against `main` fails as section 2 says; the refusal probe (18:44).
- 18:46: first validation on a copy of the working tree: `conditionals` rc 1, the test's `static_assert(ACMP_MAX_SINKS == 33u)` compiled at the default 16. Changed to a runtime `ASSERT_EQ` in the fixture, sink 32 named `kLast`.
- 18:47: second validation: `entity-controls` rc 1, `entity_selftest.py` reads the last three plants as the entity ones. The three new plants moved before the wire and entity plants.
- 18:57: third validation: mutation rc 1, one plant escaped (`acmp-wide-release-loop-word-ignored`): W1's message-less `ASSERT_EQ` on the change count stopped the test before the needle's assertion. Each fatal assertion now carries its message, and the kill names it; 18:58 `mutation.py --select acmp-wide`: 3 of 3 caught.
- 18:58: committed `c6013804`; 19:02 the clean-clone CI run ended (section 3), rc 0 and rc 0.
- 19:04 to 19:15: probes at the head, `main` and the pin; the 16-sink plant check; the size comparison.
