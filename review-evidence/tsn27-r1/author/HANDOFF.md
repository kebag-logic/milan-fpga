# [A751] tsn-c-stack #27: wire_put_be in two 32-bit halves

Status: **REVIEW READY**. Branch `27-wire-halves`, head **c687810b74b53b69c1fbdff7bfd0ec9da94eaa78**, one commit on `main` 70936b77dc41981e192438388cd0aced69954f18. Not pushed (the manager pushes the branch and opens the PR; the body is `PR-BODY.md`).

- Repository: kebag-logic/tsn-c-stack, local clone `$LANES/tsn-c-stack-27-wire`. `git rev-parse HEAD` on branch creation: 70936b77dc41981e192438388cd0aced69954f18.
- Commit: `c687810b` "Pack wire_put_be as two 32-bit halves so no byte calls the 64-bit shift helper (#27)", author and committer hackerman-kl <hackerman-kl@kebag-logic.com>, one line, no body, no trailers.
- TAKEN on #27: issuecomment-6719201932. REVIEW READY posted with the head (see Run history).
- Every acceptance item of #27 is met, so the PR body says "Closes #27".

## Acceptance items of #27

| Item | Result | Evidence |
|---|---|---|
| `scripts/validate.py` passes in the pinned CI environment | All 28 gates rc 0 at the head (run v4); `scripts/baremetal.py` rc 0 | `receipts/gates/validate-gates.json`, `validate-summary.txt`, `baremetal-results.json` |
| `tests/coverage.ratchet` regenerated there | `include/wire.h  lines 14/14  branches 2/2` (was 10/10); other files unchanged | `tests/coverage.ratchet:4`; coverage gate rc 0 |
| Both plants killed | `{"CAUGHT": 390, "ESCAPED": 0, "ERROR": 0}`, both wire plants CAUGHT on W1's needle | `receipts/gates/mutation-summary.txt` |
| No `__lshrdi3` left in the parent's split image (`nm`) | 1x1 shipping point: before 1 symbol, 7 call sites; after 0 and 0. 8x8 two-interface point: before 1, after 0 | `receipts/image/*-nm.txt`, `*-lshrdi3-count.txt` |

"Pinned CI environment" here means: GoogleTest/GMock 1.14.0 from `$VALIDATION_TOOLS/gtest-1.14.0`; Clang 18.1.3 (the pinned binary under `$VALIDATION_TOOLS/clang-18/root`; the shared wrapper in `$VALIDATION_TOOLS/clang-18/bin` names a removed directory, so a scratch wrapper runs the same binary); clang-tidy from the CI image's package `clang-tidy-18_18.1.3-1ubuntu1_amd64.deb` (sha256 4880055c77877bce65de8733f0931021a28826bbae3f450b4dc0065fb6b70363, unpacked in scratch); Mermaid CLI 11.16.0, as the workflow installs. Host gcc, cppcheck 2.22.0 and the host clang 23 for the sanitizer build were used as found. The environment is `scripts/env.sh`.

Note on static analysis: with the host's clang-tidy 23 the gate fails on `main` itself, seven times over, at `include/acmp.h:355` (`clang-analyzer-optin.performance.Padding` on `struct acmp_sink`, a file this change does not touch). `receipts/gates/static-analysis-main-host-clang-tidy-23.txt`. With the CI image's clang-tidy 18 it passes on `main` and on the branch.

## Changes (file:line)

| File:line | Change |
|---|---|
| `include/wire.h:38-47` | `wire_put_be` splits the value into `high` and `low` 32-bit halves (`:40-41`) and writes last byte first (`:42-43`), feeding the next byte of `high` into `low` with 32-bit shifts only (`:44-45`). No 64-bit shift by a variable count remains. Results are bit-exact with the old byte form for every width 1 to 8. |
| `tests/test_acmp.cpp:2561-2580` | `// REQ: ACMP-02` and the new `Wire.W1PutBeWritesTheLowBytesMostSignificantFirst` (details below). |
| `tests/mutations.json:5831-5846` | Plant `wire-put-be-skips-an-odd-field-first-byte`. |
| `tests/mutations.json:5847-5862` | Plant `wire-put-be-writes-past-an-odd-field`. Both sit before the three generated-entity plants, which `scripts/entity_selftest.py` requires to stay last. |
| `scripts/mutation.py:36-37` | `arm_module(arm)`: the arm to module mapping, now shared. |
| `scripts/mutation.py:141` | `prepare()` uses it. |
| `scripts/mutation.py:219-225` | In a plant, an arm outside `SOURCES` records ERROR for that plant. Before, a `KeyError` escaped and stopped the campaign. A plant whose header has no `src/<stem>.c` (here `wire.h`) builds the kill's arm module. As before, a header plant also rebuilds the arm's test object with the planted header. |
| `tests/coverage.ratchet:4` | Regenerated: `include/wire.h lines 14/14 branches 2/2`. |
| `docs/TESTS.md:162`, `docs/TRACEABILITY.md:16` | Regenerated (`test_inventory.py --write`, `traceability.py --write`). |
| `docs/VERIFICATION.md:24` | Plant count 384 changed to 386 core plants. |
| `docs/VERIFICATION.md:195` | One sentence on the header-plant build rule. |

The three doc edits sit outside the four named files. Two are generated outputs the gates require after a test change. The third keeps the plant count in the gate table true. No `src/` or other core file changed.

## Review of the draft against #27

The parent lane's draft (`665s2b-a683i/donor/tsn-c-stack-wire-halves.patch`) was applied with `git apply` and then reviewed:

| Draft item | Finding | Action |
|---|---|---|
| Halves loop in `wire.h` | Correct, last byte first, 32-bit shifts only. | Kept. |
| Prose comment above `wire_put_be` | Fails the comment gate, which allows only SPDX, `REQ:` IDs and short standard references. | Removed. |
| Test: prose comment, no `// REQ:` | Fails the comment gate, and `traceability.py` refuses an untraced test. | `// REQ: ACMP-02` (the ACMP PDU build is the issue's path; the test runs in the ACMP binary). |
| Test values `0x0`, `~0x0` | The issue asks for values "whose halves differ in every crossing byte". These two have equal halves. | Five values that all have the property. A fatal `ASSERT_NE` checks it for each value. |
| Guard | Draft checked only the byte past the field. | Field written at offset 1 of a 0x5A-filled 10-byte buffer (0x5A appears in no value), so the bytes before and past the field are both checked. |
| Plants `high << 16` and `high >>= 8` deleted | W1 kills both. With W1 removed, adp_tests, acmp_tests, maap_tests and entity_tests still catch both (`receipts/escape/draft-*`), so they show nothing W1 adds. | Replaced with two plants that only W1 catches (below). |
| Plants appended last in `mutations.json` | `entity-controls` failed: `test_golden_planted_drift` reads the last three entries. | Placed before the generated-entity plants. |
| `mutation.py` inline fallback | Duplicated `prepare()`'s mapping inline. A header plant without an `arm` crashed the campaign pool with a `KeyError`. | `arm_module()` plus an explicit ERROR. |

## Test, its plants, and their escape without it

`Wire.W1PutBeWritesTheLowBytesMostSignificantFirst` (`tests/test_acmp.cpp:2562`, ACMP binary):

- Values 0x0102030405060708, 0x8899AABBCCDDEEFF, 0xF0E1D2C3B4A59687, 0x00000000FFFFFFFF, 0xFFFFFFFF00000000. For each one, byte k of the high half differs from byte k of the low half for k = 0..3 (fatal assertion, `:2565-2568`).
- Every width 1 to 8 (`:2569`). The oracle is the old byte form `value >> (8 * (bytes - 1 - i))` (`:2573-2575`). The whole 10-byte buffer is compared, guard bytes included (`:2577`).
- It also passes against the old byte-form `wire_put_be` (W1 built with `main`'s `wire.h`: 1 test passed), so it checks behaviour, not this implementation.

| Plant | Substitution at `include/wire.h:42` | With W1 (all 8 hosted binaries) | W1 removed (all 8 hosted binaries) |
|---|---|---|---|
| `wire-put-be-skips-an-odd-field-first-byte` | `i > 0u` becomes `i > (bytes & 1u)`: an odd-width field never writes its first byte | Mutation campaign: CAUGHT on the W1 needle. Full ctest: only acmp_tests fails, only on `Wire.W1PutBeWritesTheLowBytesMostSignificantFirst` | ctest rc 0, 100% of 8 binaries pass: **escapes** |
| `wire-put-be-writes-past-an-odd-field` | `i = bytes` becomes `i = bytes + (bytes & 1u)`: an odd-width field is written one byte too wide, past its end | Same: CAUGHT; only W1 fails | ctest rc 0, 100% of 8 binaries pass: **escapes** |

Receipts: `receipts/escape/*-with-w1.txt`, `*-without-w1.txt` (the escape runs used the tree before the plant reorder; `wire.h` and the test are identical to the commit). Why odd widths: the core and its tests call `wire_put_be` only with widths 2, 4, 6 and 8 (58, 6, 19 and 34 calls). Nine candidate substitutions were screened with W1 removed (top byte never written; high half masked to 16 bits, 24 bits or 0xFF00FFFF; width capped at 7; width rounded down to even, up to even, or to odd; first byte skipped on odd widths). Every defect at widths 5 to 8 or in the crossing is caught by other tests. Only the odd-width ones escape (`scripts/candidate.sh`).

## Boundary evidence

- Width boundaries: 1 (`low` only, one iteration) and 8 (all four `high` bytes crossed), plus the 4 to 5 crossing, where the first `high` byte enters `low`. All eight widths run for every value.
- Value boundaries: all-zero and all-one halves, in both orders (0x00000000FFFFFFFF, 0xFFFFFFFF00000000), plus three values with distinct bytes.
- Buffer boundaries: the byte before the field and the byte past it, at every width (0x5A guard).
- Precondition: `docs/PORTING.md:391` (`bytes` from one to eight, that many writable bytes) is unchanged and still holds.
- Repository boundary gate (`scripts/check_boundary.py --selftest`): rc 0. Bare-metal core imports at the head: Debug `__mulsi3, __umodsi3, ctrl_reentry_assert, memcpy, memset, port_assert_failed`; Release `__umodsi3, ctrl_reentry_assert, memcpy, memset`. These are identical to `main` (`receipts/gates/baremetal-results*.json`).

## Gates at the head (c687810b)

| Gate | Linux hosted | Bare-metal RV32 |
|---|---|---|
| entity-golden, entity-controls | rc 0, rc 0 | entity round trips run in the smoke image |
| boundary, needles, assertion-templates, dependencies | rc 0 each | |
| comments, conditionals, port-contracts, acmp-cache, registration-controls, license | rc 0 each | |
| traceability, test-inventory, coverage-controls | rc 0 each | |
| privacy-selftest, privacy | rc 0, rc 0 (also rerun after the commit: 15 commits, 263 blobs, pass) | |
| gcc configure, build, test | rc 0 | |
| clang sanitizers configure, build, test | rc 0 | |
| coverage | rc 0 (100 % lines and branches; wire.h 14/14, 2/2) | |
| static-analysis | rc 0 | |
| mutation, mutation-controls | rc 0 (390 caught, 0 escaped, 0 error), rc 0 | |
| graphs | rc 0 (4 rendered) | |
| `scripts/baremetal.py` Debug, Release | | rc 0, rc 0 (QEMU smoke passes, no unresolved symbols, fatal linker warnings) |

Commands, in the environment of `scripts/env.sh`:

```sh
python3 scripts/validate.py --work build-validation --jobs 16 --graphs
python3 scripts/baremetal.py --work build-rv32 --jobs 16
```

## Bare-metal image sizes, before and after

### The stack's own RV32 smoke images (`scripts/baremetal.py`)

| Build | main 70936b77 (text, ELF bytes) | head c687810b (text, ELF bytes) | `__lshrdi3` (main / head) |
|---|---|---|---|
| Debug | 47508 B, 141580 B | 47428 B (-80), 141884 B | 0 / 0 |
| Release | 36857 B, 46552 B | 37653 B (+796), 47352 B | 0 / 0 |

The stack's own images never called `__lshrdi3`: riscv64-elf-gcc expands the doubleword shift inline at `-O0` and `-O3`. The issue's cost appears at the parent's `-Os`. The halves loop costs +796 B of text in the stack's Release (`-O3`) smoke image, because the unrolled loop no longer folds to one shift per byte. Measured on the three core objects (`receipts/variants/text-sizes.txt`, `scripts/variants.sh`):

| `wire.h` | stack `-O0` | stack `-O3` | parent `-Os` rv32im | parent `-Os` rv32i | `__lshrdi3` refs at `-Os` |
|---|---|---|---|---|---|
| main (byte form) | 32308 | 25908 | 18048 | 18160 | 3 |
| this change (halves) | 32260 | 26584 | 17796 | 17908 | 0 |
| alternative: select a half per byte | 32344 | 25904 | 17888 | 18000 | 0 |

The halves form is kept. It is what the issue prescribes and what the parent measured (up to 1.0 ms off the 1x1 rows), and it is the smallest at the parent's `-Os`. The select form is size-neutral at `-O3` but 92 B larger at `-Os`. This is a reviewer decision if the stack's `-O3` size matters.

### The parent's split image (kebag-logic/milan-fpga#665)

Built with `ctrl_srp_image.py --with-aecp --layout split` (RV32IM, `-Os`) from scratch clones of the parent lane at 3d206bf405bb3c8caa3a5e5509e05a8138e183a1. The runtime archives came from the parent's `runtime_ssp.py`: libc.a sha256 cb03e4fc…c195, libcompiler_rt.a sha256 e007a249…3731. The lane checkout was only read. `scripts/parent_clone.sh`, `scripts/parent_image.sh`.

| Point | | text | data | bss | `.text` section | ELF sha256 | `__lshrdi3` in nm | call sites |
|---|---|---|---|---|---|---|---|---|
| 1x1 tdm8, 1 interface | before (pin 70936b77) | 107278 | 56 | 45256 | 95064 | 3de918df…7add | `00005200 T __lshrdi3` | 7 (`wire_put_be` 3, `declare_sources`, `deliver`, `send_pdu` 1 each; all inlined `wire_put_be`) |
| | after (submodule at c687810b) | 106854 (-424) | 56 | 45256 | 94640 | 35d311f3…5ac4 | none | 0 |
| 8x8, 2 interfaces (ledgered point) | before | 122106 | 448 | 111968 | | 3a9c2742…aac4 | 1 | |
| | after | 121686 (-420) | 448 | 111968 | | 9e56de62…3689 | none | |

- Symbol diff, 1x1 (before vs after `nm`): `__lshrdi3` gone. One more out-of-line `wire_put_be` copy (3 before, 4 after; an inlining decision). Nothing else changed. Before, `__lshrdi3` was the image's only compiler runtime helper. After, the image links none.
- Full lists: `receipts/image/1x1-if1-{before,after}-nm.txt`, `8x8-if2-{before,after}-nm.txt`. Size reports: `*-size.txt`, `*-size-A.txt`, `*-size.json`.
- The after image needs the parent's hot-list entry for `__lshrdi3` removed: `receipts/image/parent-scratch-hot-list.patch`, the parent lane's own variant patch. Without it, the parent refuses the image with `REFUSED: LINKED: hot-list name *libcompiler_rt.a:lshrdi3.o(.text.__lshrdi3) is no section of the linked image` (`receipts/image/1x1-if1-after-without-hot-list-edit-refusal.txt`). So the parent's pin move and that edit go in one commit. The gitlink change used in scratch is `receipts/image/parent-scratch-gitlink.patch`.

## For the manager

- Push `27-wire-halves` (c687810b) and open the PR with `PR-BODY.md`.
- Parent follow-up, outside this lane: move `third_party/tsn-c-stack` to the merged commit and drop the `__lshrdi3` hot-list entry in `sw/firmware/ctrl/plat/ctrl_split.ld` and `plat/ctrl_split_hot.txt` in the same commit.
- Environment fix worth making outside this lane: `$VALIDATION_TOOLS/clang-18/bin/clang-18` points at a deleted directory. The binary is at `$VALIDATION_TOOLS/clang-18/root/usr/bin/clang-18`. The tools also lack clang-tidy-18, and the host clang-tidy 23 fails the static-analysis gate on `main`.

## Scratch and receipts

Scratch: `$VALIDATION_STORAGE/tsn27-a751/` (parent clones, image builds, validate runs v1 to v4, candidate and escape trees). Only receipts under 200 KB are in `receipts/`: `gates/`, `escape/`, `image/`, `variants/`.

## Run history (CET, 2026-11-08)

- 09:20 start; branch created at 70936b77; TAKEN posted.
- 09:25 draft applied (`git apply`); parent scratch clone; before image built.
- 09:28 quick checks: the comment gate needed a working clang-18 (scratch wrapper). Both draft plants were caught, but the escape check showed other suites catch them too.
- 09:29 to 09:32 candidate screening; odd-width plants chosen; ratchet and generated docs regenerated.
- 09:33 validate v1: `entity-controls` failed because the wire plants were last in `mutations.json`. Moved before the entity plants.
- 09:42 validate v2: static-analysis (host clang-tidy 23, fails on main too) and graphs (`mmdc` not on PATH) failed. Fixed in the environment: the CI's clang-tidy-18 package was fetched into scratch, and `mmdc` with its node runtime put on PATH.
- 09:47 validate v3: 28/28 rc 0; bare-metal rc 0.
- 09:50 commit c687810b; privacy rerun pass; validate v4 and bare-metal v4 at the head: all rc 0.
- 09:52 to 09:56 after images (1x1, 8x8); hot-list refusal confirmed; receipts written.
- 10:0x REVIEW READY posted on #27 with head c687810b74b53b69c1fbdff7bfd0ec9da94eaa78: issuecomment-6719542583. Lane stopped.
