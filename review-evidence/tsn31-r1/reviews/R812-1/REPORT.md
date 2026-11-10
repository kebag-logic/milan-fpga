[R812] NEGATIVE - exact head c6013804d0fec6bc763a64b496f1a52d4a5d9f6a

# R812-1: external independent review of kebag-logic/tsn-c-stack PR #33 (issue #31)

- **Head:** `c6013804d0fec6bc763a64b496f1a52d4a5d9f6a`, tree `05c1f379ee6e0387ff078faf417a3941438c011b`. One commit on `main` `ea4af6f1`.
- **Scope:** issue #31 and the ruling at kebag-logic/milan-fpga#859 issuecomment-6746289265, item 1.
- **Reviewer:** the external reviewer. This was a cleared-context session on its own detached clone. I made no GitHub writes and no source edits.

## Verdict

The fix is correct. Every use of the owed-release mask is sized from `ACMP_MAX_SINKS`, and no shift reaches the word width. The build-time refusal has the right bound. The required 33-sink sanitizer test exists and passes, and the mask probe exits 0 at the head and 1 at `main`. Both of the CI's testing steps pass on a clean clone of the head with Clang 18.1.3 and GoogleTest 1.14.0. The hosted checks at the head are green. The size figures in the PR reproduce to the byte.

The verdict is NEGATIVE because of one MINOR test finding, F1. Two behaviours of the new multi-word mask are not checked by any test or plant, although the PR's verification table claims them:
- the clear of every mask word when a slot is reused;
- sink 31, the last bit of word 0.

A defect planted on either one passes the 16-sink binary, both `acmp_wide` tests and the whole 447-plant campaign. A disposable 33-sink reviewer test passes at the head and catches each planted defect.

## Scope reconstructed

- **Rules:** CONTRIBUTING.md asks for a failing assertion and a runnable planted defect for each regression, a ratchet that is never lowered, one-line commits and neutral public text. Also read: README, `docs/VERIFICATION.md`, `docs/PORTING.md` (ACMP owed bound and machine storage), `docs/CODING_STANDARD.md` (conditional macros) and `docs/REQUIREMENTS.md` ACMP-09 ("Queue bounded responses and delay notifications until their responses are accepted"; Milan v1.2 5.5.3.5).
- **Issue #31:** the mask must be sized from `ACMP_MAX_SINKS` at every use, there must be a build-time refusal, and there must be a 33-sink UBSan unit test. The issue has no comments.
- **Ruling item 1:**
  - `respond`, `transmit`, the change-owed loop and the release loop are sized from `ACMP_MAX_SINKS`, and no shift reaches the word width.
  - A build is refused for any sink count the type cannot hold.
  - A test at `ACMP_MAX_SINKS=33u` under `-fsanitize=shift,undefined` binds sink 32 and sink 0 with no transmit room. Each change notice must wait only behind its own owed response.
  - The mask probe exits 0.
  - The branch-coverage target and the CI steps are kept.
  - STOP if a public API or the mailbox contract must change.
- **PR #33:** body read, and snapshotted in `receipts/pr33-body-at-review.md`. There were 0 PR reviews and 0 review comments. The only comments are the author's REVIEW READY note and the two review-start notices.
- **Diff `ea4af6f1..c6013804`:** 11 files, +218/−28. I read the whole diff before any evidence.

## STOP condition

STOP is not triggered.
- No function, callback, configuration field, view or counter changes.
- The public header gains `ACMP_RELEASE_WORDS` (`include/acmp.h:165`). It is the dimension of `acmp_owed.release` (`:402`) and is used nowhere else, so I count it as part of the `acmp_owed.release` change.
- `docs/PORTING.md` changes only the `release` row of ACMP machine storage (`:328`) and the size paragraph of the owed bound (`:76-78`). Both are about `acmp_owed.release`.
- `docs/CODING_STANDARD.md:73` allows only the two capacity defaults as configuration definitions. `ACMP_RELEASE_WORDS` is a derived constant with no `#ifndef`, and the conditional gate passes.

## Every use of the mask (src/acmp.c at the head)

| Use | Line | Reading | Evidence |
|---|---|---|---|
| Field | `include/acmp.h:402` | `uint32_t release[(ACMP_MAX_SINKS + 31u) / 32u]` | Entry sizes in `receipts/size-refusal-probe.txt`, section 3. It is 80 B at 16 and 32 sinks, 84 B at 33 and 64, and 88 B at 65, on x86-64 and RV32I. This matches PORTING `:76-77`. |
| Refusal | `:35` | `sizeof release * 8u >= ACMP_MAX_SINKS` | Section 1: compiles at 1, 16, 31, 32, 33, 63, 64, 65 and 254 sinks, and is refused only at the unsigned wrap (4294967295). Section 2: with the one-word mask planted back, it compiles at 16 and 32 and is refused at 33 and 64, with the stated message. The bound is exact. |
| Callers | `:850`, `:905` | `bind_response` and `unbind` pass `k + 1u`. All other `respond` calls pass `0u` (`:928-1034`). The probe passes `0u` (`:742`). | Read. `k < n_sinks <= ACMP_MAX_SINKS` (`:1042`). |
| Clear | `:309` | `memset(o->release, 0, sizeof o->release)`, all words | Correct. No test or plant checks it (F1). |
| Set | `:310-312` | word `(r-1)/32`, bit `(r-1)%32`, only when `r != 0` | Correct. The shift is at most 31 and the index is below `ACMP_RELEASE_WORDS`. |
| Change-owed loop | `:317` | word `k/32`, bit `k%32` | Correct. |
| Release loop | `:1269` | word `k/32`, bit `k%32` | Correct. |

No other ACMP shift depends on a sink index. I checked every `<<` and `>>` in `src/acmp.c` and `include/acmp.h`.

## Executed evidence

All of this was run on clean clones made under the scratch directory. The receipts are listed in `MANIFEST.sha256`.

**CI testing steps (quality.yml `run:`).** These were run on a fresh clone of the exact head, with Clang 18.1.3, GoogleTest/GMock 1.14.0 and clang-tidy 18.1.3. See `scripts/TOOLCHAIN.md` and `receipts/run2/`.
- `python3 scripts/validate.py --work build-validation --jobs 3 --graphs`: rc 0, 28 of 28 gates rc 0.
  - `gcc-test` and `clang-sanitizers-test` each ran 9 of 9 CTest binaries, including `acmp_wide`.
  - `clang-sanitizers-configure` identifies Clang 18.1.3 for C and C++.
  - Mutation: 447 caught, 0 escaped, 0 errors.
  - Coverage: `src/acmp.c` 815/815 lines and 426/426 branches. The coverage table is byte-identical to the author's.
- `python3 scripts/baremetal.py --work build-rv32 --jobs 4`: rc 0 for Debug and Release, with the QEMU smoke run. The core imports equal those of `main` in both configurations (`receipts/rv32-imports-main-vs-head.txt`).
- The clone's status and diff were empty before and after.
- **Note on run 1.** An earlier run (`receipts/run1-envfail/`) is kept for completeness. Its Clang 18 build failed inside the host's GCC 16 libstdc++ headers, in every test binary. That was an environment fault, not evidence about the PR, and it was fixed for run 2 by using the CI image's GCC 13 libstdc++.

**Mask probe.** This is the public `acmp_mask_probe.sh` and `.cpp`, unchanged; provenance is in `probe-src/PROVENANCE.txt`. Run at 33 sinks:
- head: **rc 0**, 2 of 2 passed, no shift report. After BIND_RX for sink 32, `change_owed[32]=1` and `change_owed[0]=0`.
- `main`: **rc 1**, `src/acmp.c:844:31: runtime error: shift exponent 32 is too large for 32-bit type 'unsigned int'`.

**PR test against main's core** (`receipts/wide-on-main.txt`):
- Without recovery, it stops at `src/acmp.c:844:31`.
- With recovery, both tests fail on the alias, and the sanitizer also reports `:311:75` and `:1263:80`.

This reproduces the PR's claim and shows that the test detects the issue's defect.

**Plants** (`receipts/plant-probe.txt` and `.json`, `scripts/plant_probe.py`). Each plant was built into the full 16-sink `acmp_tests` and the 33-sink `acmp_wide`:

| Plant | 16-sink acmp_tests (126) | acmp_wide (33 sinks) |
|---|---|---|
| `acmp-wide-release-word-ignored` | passes (escapes) | fails `OwedResponsesHoldOnlyTheirOwnSinksChanges` |
| `acmp-wide-owed-count-word-ignored` | passes (escapes) | fails both tests |
| `acmp-wide-release-loop-word-ignored` | passes (escapes) | fails both tests |
| unmasked shift in set, add loop or release loop | passes | sanitizer abort, rc 1 |
| `if (release != 0u)` made always true | SIGSEGV | sanitizer abort |
| bind releases sink k+1 | 2 fail | both fail |
| unbind releases nothing | 1 fails | passes |
| **clear narrowed to one word** (`sizeof o->release[0]`) | passes | **passes** (F1) |
| **clear removed** | passes | **passes** (F1) |
| **set index off by one** (`o->release[release / 32u]`) | passes | **passes** (F1) |
| change-owed or release loop reads word `(k+1)/32` | passes | passes (only sink 31 differs; F1) |
| refusal removed, or `>=` changed to `>` | passes | passes (S2) |

- Each of the three new plants is caught by its named assertion in the `acmp_wide` arm (`receipts/run2/plants-new-and-moved.txt`).
- At up to 32 sinks the three plants are equivalent mutants, because `ACMP_RELEASE_WORDS` is 1 and every word index is 0. So no 16-sink binary can catch them, which is what the PR claims. The author's `wide-plants-at16.log` shows the same 126 passes.

**Seven moved plants.** Each changes only the text it plants into: `1u << k` becomes `k + 1u`, the loop reads `o->release[k / 32u] >> (k % 32u)`, and the field becomes `[ACMP_RELEASE_WORDS]`. Each keeps the same defect and the same kills, and each is CAUGHT in my campaign by its unchanged named test. No plant was removed.

**Code size.** RV32I `src/acmp.c` text at 16 sinks (`receipts/size-refusal-probe.txt`, section 4):

| Flags | main | head | delta |
|---|---:|---:|---:|
| `-Os` | 10,825 B | 10,921 B | +96 B |
| `-O2` | 16,029 B | 16,141 B | +112 B |
| `-O3` | 19,365 B | 20,365 B | +1,000 B |

- These are exactly the PR's figures.
- At 33 sinks the text is 10,985 B at `-Os` and 18,813 B at `-O3`.
- The undefined symbols are only `ctrl_reentry_assert`, `memcpy` and `memset`, as at `main`. The `/ 32u` and `% 32u` add no libcall.

**Hosted checks** (`receipts/hosted-jobs.txt`, `pr_checks.txt`, `check_runs.txt`):
- `gh pr checks 33`: 4 passed, 0 failed.
- These are the `quality` and `bare-metal` jobs of both the push run (42724744778) and the pull_request run (42724774168), all on `c6013804`.
- Every step executed with conclusion success: install, "Validate the portable cores" or "Validate the freestanding cores", and the evidence upload. None was skipped.

## Findings

### Prior public findings

No public review finding exists on PR #33 at this head. There are 0 reviews and 0 review comments, and the PR's comments are the REVIEW READY note and the two review-start notices. Nothing needed resolving or carrying over.

### R812-1-F1: MINOR (Tests, Docs). Two behaviours of the multi-word mask are unchecked

- **Where:**
  - `src/acmp.c:309`, the clear.
  - `src/acmp.c:311`, the set index.
  - `tests/test_acmp_wide.cpp:67` and `:92`, which bind only sinks 0 and 32.
  - `docs/VERIFICATION.md:26`, which claims "Each sink's change waits only behind its own owed response" for `acmp_wide`.
- **Authority:**
  - Ruling item 1: "the mask is sized from `ACMP_MAX_SINKS` at every use", and the test "requires each change notice to wait only behind its own owed response" (IEEE 1722.1-2021 8.2, Milan v1.2 5.5).
  - ACMP-09.
  - CONTRIBUTING: each regression needs a failing assertion and a runnable planted defect.
- **Evidence:**
  - (a) The clear is the one use of the mask that is new in this PR and that no test checks. Narrowing it to one word (`sizeof o->release[0]`) or removing it passes all 126 tests of `acmp_tests`, both `acmp_wide` tests and the 447-plant campaign, which has no plant on `:309`.
    - With the narrowed clear, a 33-sink owed slot that once held sink 32's response keeps sink 32's bit in word 1. A later frame in that slot that releases nothing, such as a GET_RX_STATE response or a probe, then holds sink 32's change.
    - The disposable `scripts/test_wide_gaps.cpp` (`ReusedSlotCarriesNoStaleReleaseBit`) passes at the head and fails under both plants (`receipts/wide-gaps.txt`).
    - The gap behind full removal is older than this PR: on `main`, changing `o->release = release;` to `|=` also passes all 126 tests (`receipts/main-release-store-or.txt`). The clear's width, though, exists only since this PR.
  - (b) The tests check the word split only at sinks 0 and 32. An off-by-one in the set index (`o->release[release / 32u]`) moves sink 31's bit into word 1, so sink 31's change is not held behind its response. That plant passes every test and plant. `SinkThirtyOneIsHeldByItsOwnResponse` in the same probe file catches it.
- **Impact:**
  - The code at the head is correct.
  - What is unchecked is part of the property the ruling asked the test to pin.
  - The verification table claims more than the binary checks.
  - A later edit to the clear or the index would bring back over-holding or early release at more than 32 sinks, and no gate would notice.
- **Required outcome:**
  - In `acmp_wide`, add assertions that:
    - owe a frame releasing sink 32, drain it, owe a frame in the same slot that releases nothing, and require sink 32 to stay unheld;
    - bind sink 31 with no room and require it to be held only by its own response, and released when that response leaves.
  - Register plants for the one-word clear and the off-by-one set index in the `acmp_wide` arm, each caught by its named assertion.
  - Regenerate `docs/TESTS.md` and `docs/TRACEABILITY.md`, and update the plant count in `docs/VERIFICATION.md`.
- **Verification:** both plants are CAUGHT in `scripts/mutation.py`, `validate.py` passes 28 of 28, and the coverage ratchet is unchanged.

### R812-1-F2: RESIDUE (Docs). The 33-sink command names one build directory

- **Where:** `docs/VERIFICATION.md:26`.
- **Defect:** The row says "`ctest --test-dir build-gcc -R acmp_wide` in either build above", but the sanitizer build above is `build-sanitize`. The fix is wording only.
- **Exact fix:** replace the command cell with:

  > `ctest --test-dir build-gcc -R acmp_wide` or `ctest --test-dir build-sanitize -R acmp_wide`

### R812-1-F3: RESIDUE (PR body). The size table does not name its compiler

- **Where:** PR #33 body, "Size".
- **Defect:** The figures reproduce exactly with riscv64-elf-gcc 16.2.0, but the PR does not name that compiler. The CI's bare-metal job uses a different RISC-V GCC.
- **Exact fix:** change the first line of the Size section to:

  > Text of `src/acmp.c` for RV32I (`riscv64-elf-gcc` 16.2.0, `-march=rv32i -mabi=ilp32 -ffreestanding -fno-builtin -nostdinc -DNDEBUG -DCTRL_REENTRY_ASSERT`) at the default 16 sinks:

### R812-1-S1: SUGGESTION (RTL, Robustness). Increment the released sink directly in `transmit`

- **Proposal:** At `src/acmp.c:310-318`, increment `a->sinks[release - 1u].change_owed` inside the `release != 0u` branch, and drop the loop over every sink.
- **Why:** Every `respond(..., 0u)` currently runs that loop over the stored mask, which is the source of the `-O3` +1,000 B.
- **Measured** (`receipts/direct-increment-variant.txt`): this variant passes 126 of 126 and 2 of 2. RV32I text is 10,861 B at `-Os` (+36 against `main`), 16,081 B at `-O2` (+52) and 19,133 B at `-O3` (−232).
- **Status:** optional. It does not affect the verdict.

### R812-1-S2: SUGGESTION (Tests, Robustness). Add a compile control for the refusal

- **Why:** Removing `src/acmp.c:35`, or changing `>=` to `>`, passes every gate. The refusal is still correct defence in depth, because the committed array holds every count below the unsigned wrap.
- **Proposal:** Add a compile control next to the existing selftests. With the mask planted back to one word, it should require refusal at 33 sinks and acceptance at 32.

### R812-1-S3: SUGGESTION (Robustness). Bound `probe_of` at build time

- **Context:** `probe_of` is a `uint8_t` that stores one plus a sink index, so it cannot name a sink past 254. The PR body already says so under "Not in this PR".
- **Proposal:** A `_Static_assert(ACMP_MAX_SINKS <= 254u, ...)` would refuse such builds the same way the mask refusal does. This predates the PR and is outside its scope.

### Comment rule

The new source comments are `scripts/mutation.py:25` and the SPDX, `Milan v1.2 5.5.3.5` and `REQ: ACMP-09` lines in `tests/test_acmp_wide.cpp`. They state behaviour and cite `#31` and ACMP-09. The assertion messages use test-step labels (W0–W2) and `(#653)`, as the existing ACMP tests do. No bench lane label, lane name, review round, reviewer ID or issue-comment ID appears in the reviewed delta, so there is no new residue. The commit is a one-line subject with no body, and the privacy gate is rc 0.

## Ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | ACMP-09 and the Milan v1.2 5.5.3.5 hold-until-accepted rule against `src/acmp.c:296-327`, `:850`, `:905` and `:1260-1278`. Mask probe: head rc 0, `main` rc 1. PR test against `main`: alias and shift UB reproduced. At the head, each of sinks 0 and 32 waits only behind its own response. | R812-1 | c6013804d0fec6bc763a64b496f1a52d4a5d9f6a |
| RTL | CLEAN (no HDL in this repository; the lens covers the RV32 firmware target) | `baremetal.py` Debug and Release rc 0 with QEMU smoke, imports equal to `main`. RV32I 33-sink compile with no new libcall. Text at `-Os`/`-O2`/`-O3` reproduces +96, +112 and +1,000 B. RV32 entry size 84 B at 33 sinks. Hosted bare-metal jobs executed. | R812-1 | c6013804d0fec6bc763a64b496f1a52d4a5d9f6a |
| Robustness | CLEAN | Index and shift bounds by construction. Refusal bound exact (one-word mask: 32 accepted, 33 and 64 refused; committed array holds every count up to the wrap). `n_sinks` is checked at init. Sanitizer plants abort at 33 sinks. Clang 18 ASan and UBSan suite plus the GCC shift and UBSan binary pass. | R812-1 | c6013804d0fec6bc763a64b496f1a52d4a5d9f6a |
| Tests | UNCLEAN (F1) | `tests/test_acmp_wide.cpp`, the CMake `tsn_wide` and `acmp_wide` targets, the mutation `acmp_wide` arm, 3 new and 7 moved plants (all CAUGHT), the 447-plant campaign, coverage 815/815 and 426/426, and 15 reviewer plants plus 2 reviewer probe tests. | R812-1 | c6013804d0fec6bc763a64b496f1a52d4a5d9f6a |
| Docs | UNCLEAN (F1; F2 and F3 are residue) | CHANGELOG; PORTING `:76-78` and `:328`, with sizes verified; VERIFICATION `:25` and `:26`; TESTS and TRACEABILITY rows (anchors `:67` and `:92` checked, generators' gates rc 0); CODING_STANDARD macro rules; PR body. | R812-1 | c6013804d0fec6bc763a64b496f1a52d4a5d9f6a |

## Real limits

- **Toolchain differences from CI:**
  - Clang 18.1.3 needed compiler-rt 18.1.3 and the GCC 13 libstdc++ headers from the Ubuntu 24.04 archive, extracted in scratch. The hashes are in `scripts/TOOLCHAIN.md`.
  - The rest came from the host: GCC 16.2.1 (CI uses GCC 13), riscv64-elf-gcc 16.2.0 (CI uses Ubuntu's gcc-riscv64-unknown-elf), Cppcheck 2.22.0, CMake 4.4.5 and QEMU 11.1.3.
  - The `apt-get` and `npm` install steps were not run.
  - Jobs were capped at `--jobs 3` for validate and `--jobs 4` for RV32 to stay within 16 parallel jobs; CI uses 16.
- **Not run:** Docker or act, a manager source bank, any milan-fpga image, simulation or pin move, and the ruling's round-5 duties (the R808-1-F8 probe on index 32, the 32x32 image rebuild, and the `bind_response`/`transmit` disassembly). Those belong to the milan-fpga lane after the pin move.
- **Hardware:** physical calibration NOT RUN. No hardware was used, and field skips are not hardware proof.
- **Reviewer probes:** these are disposable. `test_wide_gaps.cpp` and the variant are evidence, not proposed source.
- **Author evidence:** I fetched only a subset of the author receipts. I compared their gates list, coverage table, refusal log, plants-at-16 log and size figures with mine; they agree.

## Pending manager duties

- Validate the current-dev merge candidate (source base `ea4af6f1`, live dev `123f57a922bf07476cd69f91867f3b6f07080804`) at the merge turn, run the builder and native banks, and own hosted/act acceptance.
- Obtain the second independent review. The internal review R811-1 is in progress, and I did not read it.
- Carry F2 and F3 to the residue checklist.
- Route F1 to the author and re-review its fix.
- Merge needs two independent positive reviews and the full completion bar.

R812-1 FINISHED
