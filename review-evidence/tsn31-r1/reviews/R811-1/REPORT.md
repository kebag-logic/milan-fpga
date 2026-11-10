[R811] NEGATIVE - exact head c6013804d0fec6bc763a64b496f1a52d4a5d9f6a

# R811-1: independent internal review of kebag-logic/tsn-c-stack PR #33 (issue #31)

- Head `c6013804d0fec6bc763a64b496f1a52d4a5d9f6a`, tree `05c1f379ee6e0387ff078faf417a3941438c011b`, one commit on `main` `ea4af6f1`.
- Scope authority: issue #31 body; ruling kebag-logic/milan-fpga#859 issuecomment-6746289265, item 1.
- Public review start: PR #33 issuecomment-6755780031.
- Reviewed: CONTRIBUTING.md (there is no AGENTS.md), README, docs (PORTING, TESTS, TRACEABILITY, VERIFICATION, REQUIREMENTS ACMP-09/ACMP-12, CODING_STANDARD, COVERAGE, STATIC_ANALYSIS), `.github/workflows/quality.yml`, the full `git diff ea4af6f1..c6013804`, the head commit object, the PR body and comments, and the author's evidence at milan-fpga `e225885f` `review-evidence/tsn31-r1` (91 files hashed in `receipts/author-evidence-e225885f.sha256`).
- The ruling names one probe, `acmp_mask_probe.sh`/`.cpp`, which comes from an earlier review on another PR. I fetched only those two script blobs (identity in `receipts/mask-probe-identity.txt`). I read no report.

## Verdict

NEGATIVE, for one MINOR finding (F1, Tests).

The fix itself is correct:
- The mask is sized from `ACMP_MAX_SINKS` at every use.
- No shift reaches the word width.
- The build-time refusal has the right bound.
- The three new plants and the seven moved plants behave exactly as the PR claims.
- The size figures reproduce byte for byte.
- Both testing CI steps pass on a clean clone.
- A probe over every sink at 16, 32, 33, 64 and 65 sinks passes at the head.

The gap is in the regression test. Five plausible defects on the lines this PR adds survive all nine CTest binaries and the 447-plant campaign. Two of them are a word-boundary off-by-one and a removed mask clear, both in the defect class #31 fixes. So CI enforces "each change notice waits only behind its own owed response" for sinks 0 and 32 only, and not across reused owed slots.

The STOP condition was not triggered:
- The only public-header change beyond the `acmp_owed.release` field is `ACMP_RELEASE_WORDS`, the field's own dimension.
- The PORTING.md changes are limited to the `release` row and the owed-bound size paragraph.

## Findings

### F1: MINOR. The new mask-storage lines have no catching assertion for word-boundary or stale-bit defects

- **Lenses:** Tests.
- **Where:**
  - `tests/test_acmp_wide.cpp:67-104`: binds only sinks 0 and 32, each into a fresh owed set.
  - The lines it should guard: `src/acmp.c:309-311` (clear and set in `transmit`), `src/acmp.c:317` (change-owed loop), `src/acmp.c:1269` (release loop).
  - `tests/mutations.json`: the three new plants are all of one class, "always word 0".
- **Authority:**
  - Ruling item 1: the test "requires each change notice to wait only behind its own owed response".
  - ACMP-09: "delay notifications until their responses are accepted" (Milan v1.2 5.5.3.5).
  - CONTRIBUTING.md: "A regression needs a failing assertion and a runnable planted defect."
- **Evidence:**
  - `scripts/plants.py` → `receipts/plants/matrix-results.json`
  - `scripts/survivors_full_ctest.sh` → `receipts/survivors-full-ctest.txt`

  Each plant below passes the 16-sink `acmp_tests` and the 33-sink `acmp_wide`. Each also passes the whole 9-binary CTest suite (GCC Debug, `100% tests passed out of 9`; an unplanted control passes the same way). Each is caught only by the review's every-sink probe (`scripts/every_sink_probe.cpp`):

  | Plant | Change | Effect |
  |---|---|---|
  | transmit word off-by-one | `o->release[(release - 1u) / 32u]` → `o->release[release / 32u]` | At 33 sinks, sink 31's bit lands in word 1, so its change is not held behind its own response. At exactly 32 sinks it indexes past the one-word array (undefined behaviour). |
  | change-owed loop off-by-one | `o->release[k / 32u]` → `o->release[(k + 1u) / 32u]` in `transmit` | Sink 31's change is not held. |
  | release loop off-by-one | the same change in `acmp_poll` | Sink 31 is never released. |
  | mask not cleared | `memset(o->release, 0, sizeof o->release);` deleted | A probe frame that reuses a slot inherits the earlier response's bit and holds that sink's change. This happens at the default 16 sinks too. |
  | one word cleared | `sizeof o->release` → `sizeof o->release[0]` | Stale word-1 bits hold sinks 32 and up after slot reuse. |

- **Impact:** a regression of the defect class #31 fixes (a sink's notice held by, or released by, a frame that is not its own response) would pass all 28 gates and both hosted jobs. The ACMP-09 property is enforced only for sinks 0 and 32 in fresh slots.
- **Required outcome:**
  - Extend the wide tests (or add tests) so that:
    - each sink on both sides of the word boundary (at least 31 and 32, or every sink of 33) is held only by its own owed response and released only when that response leaves;
    - an owed probe reuses a slot that held another sink's response and holds no sink.
    The 16-sink suite is also a fit for the stale-bit case, since that defect is live at 16 sinks.
  - Register the five plants (or equivalents) in `tests/mutations.json`, each with a named needle, and update the plant count in `docs/VERIFICATION.md` and the generated `docs/TESTS.md`/`docs/TRACEABILITY.md`.
- **Verification:**
  - At the new head, `scripts/plants.py` and `scripts/survivors_full_ctest.sh` show every `review-*` plant failing `acmp_wide` or `acmp_tests` by a named assertion, with the unplanted row passing.
  - `scripts/mutation.py` reports 0 escaped.
  - The coverage gate stays at 100 % of lines and branches.

### R1: RESIDUE. The PR body's size table does not name its compiler

- **Lenses:** Docs.
- **Where:** PR #33 body, "## Size".
- **Evidence:** the table states flags and the sink count but not the toolchain. All six figures reproduce exactly with `riscv64-elf-gcc` 16.2.0 (`receipts/rv32-acmp-text.txt`). The CI's Ubuntu cross compiler is a different version.
- **Impact:** wording only. No figure changes.
- **Exact fix:** change "Text of `src/acmp.c` for RV32I (`-march=rv32i -mabi=ilp32`) at the default 16 sinks:" to "Text of `src/acmp.c` for RV32I (`-march=rv32i -mabi=ilp32`, riscv64-elf-gcc 16.2.0) at the default 16 sinks:".

### S1: SUGGESTION. Refuse sink counts that `probe_of` cannot name

- **Lenses:** Robustness.
- **Where:** `include/acmp.h:401` (`uint8_t probe_of`) and `src/acmp.c:308`.
- **Issue:** at `ACMP_MAX_SINKS` ≥ 256, sink 255's probe stores 256 as 0 and is taken for a response. The head compiles cleanly at 255 sinks (`receipts/refusal-probe.txt`), and nothing refuses 256.
- **Why only a suggestion:** the PR discloses this under "Not in this PR", the ruling scopes the refusal to the mask, and no shape builds that many sinks.
- **Suggestion:** add `_Static_assert(ACMP_MAX_SINKS <= 255u, ...)` beside the mask refusal, or open a follow-up issue.

### S2: SUGGESTION. Use an explicit-width one in the mask shift

- **Lenses:** Robustness.
- **Where:** `src/acmp.c:311`.
- **Issue:** `1u << ((release - 1u) % 32u)` stores into a `uint32_t` word but shifts an `unsigned int`. This is fine on both required targets (32-bit `int`).
- **Suggestion:** `UINT32_C(1) <<` would follow CODING_STANDARD's explicit-width rule.

## Prior public findings on this PR

None. PR #33 has no reviews and no review comments. Its three issue comments are the author's REVIEW READY and the two review-start notices. None was read before this pass, and none needs resolving.

## Lens evidence

### Conformance

- Issue #31 and the ruling ask that each sink's change notice waits only behind its own owed response (ACMP-09, Milan v1.2 5.5.3.5; the issue also names ACMP-12 ordering). The tests trace ACMP-09, which is the requirement stating this.
- **Every use of the mask, checked:**
  - `transmit` clears all `ACMP_RELEASE_WORDS` words, then sets bit `s % 32` of word `s / 32` (`:309-311`).
  - The change-owed loop (`:317`) and the release loop (`:1269`) read word `k / 32u`, bit `k % 32u`.
  - `respond` and `transmit` now take one plus the sink index (`:296`, `:323`).
  - `bind_response` (`:850`) and `unbind` (`:905`) pass `k + 1u`.
  - The other ten `respond(..., 0u)` calls and the probe call (`:742`, `0u, k + 1u`) release nothing, as before.
  - Every shift count is `% 32u` on a 32-bit operand. Every word index is below `ACMP_RELEASE_WORDS`, because `k < n_sinks ≤ ACMP_MAX_SINKS` (`:1042`).
- **Executed:**
  - The mask probe exits 0 at the head (2 of 2 passed, no shift report) and 1 at main (`src/acmp.c:844:31: runtime error: shift exponent 32`) (`receipts/mask-probe-{head,main}.log`).
  - The review's every-sink probe (each sink bound alone with no room: only that sink is held and only that sink is released; then a slot-reuse case) passes at the head at 16, 32, 33, 64 and 65 sinks under `-fsanitize=shift,undefined -fno-sanitize-recover`.
  - Against main it passes at 16 and fails at 33 (`:311:75` shift report) (`receipts/every-sink-{head,main}.txt`).
- **Result:** CLEAN.

### RTL (target build and firmware artefact)

- No HDL in the delta. Applied to the freestanding RV32 build.
- `scripts/baremetal.py` passes on the clean clone: Debug and Release rc 0, no unresolved final symbols, smoke checks pass on QEMU (`receipts/ci/baremetal.log`, `rv32-results.json`).
- `acmp.c`'s undefined imports are `ctrl_reentry_assert memcpy memset` at main and at the head, at -O0, -O3 and -O3 with 33 sinks. The new `/ 32u` and `% 32u` add no libgcc call (`receipts/rv32-acmp-imports.txt`).
- Text size at 16 sinks (`receipts/rv32-acmp-text.txt`):

  | Flags | main | head | Change |
  |---|---:|---:|---:|
  | -Os | 10,825 B | 10,921 B | +96 B |
  | -O2 | 16,029 B | 16,141 B | +112 B |
  | -O3 | 19,365 B | 20,365 B | +1,000 B |

  These match the PR. At 33 sinks the change is +168 B at -Os and +696 B at -O3.
- Owed storage, on both x86-64 and RV32 (`receipts/owed-storage-sizes.txt`):

  | Sinks | Bytes per frame | Owed set |
  |---|---:|---:|
  | 16 or 32 | 80 B | 640 B |
  | 33 or 64 | 84 B | 672 B |
  | 65 | 88 B | 704 B |

  This matches PORTING.md: 80 B frames up to 32 sinks, and 4 more bytes per frame for each further 32 sinks.
- **Result:** CLEAN.

### Robustness

- **Refusal bound** (`receipts/refusal-probe.txt`, `refusal-clang18-one-word-33.txt`):
  - `_Static_assert(sizeof release * 8u >= ACMP_MAX_SINKS)` at `src/acmp.c:35` compiles at 1, 16, 31, 32, 33, 64, 65, 254 and 255 sinks with GCC and with Clang 18.1.3.
  - Three narrowed masks were planted into the header:
    - one word: refused at 33 and 64, accepted at 16 and 32;
    - floor division: refused at 16 and 33, accepted at 32 and 64;
    - `uint16_t` words: refused at 32, 33 and 64, accepted at 16.
  - So it refuses exactly the counts the planted type cannot hold. Both compilers name the assertion's message.
- **Slot reuse:** at the head, stale bits cannot survive, because the whole mask is cleared for every owed frame. The every-sink probe's reuse case passes.
- The `probe_of` limit is S1.
- **Result:** CLEAN. The missing regression guard is attributed to Tests (F1).

### Tests

- The new binary `acmp_wide` (CMake `tsn_wide`: `ACMP_MAX_SINKS=33u`, `-fsanitize=shift,undefined -fno-sanitize-recover=shift,undefined`, `NDEBUG CTRL_REENTRY_ASSERT`) runs in both the GCC and the Clang-sanitizer builds. The mutation driver's `acmp_wide` arm uses the same definition and flags (`scripts/mutation.py:26` and its `wide()` helper).
- **New plants:** each of the three is caught by `acmp_wide` and by its named needle in the campaign (CAUGHT). Each passes the 16-sink `acmp_tests` (my matrix: pass), exactly as claimed.
- **Moved plants:** all seven apply to the new lines with the same defect and are CAUGHT in the campaign. In my matrix all seven fail the 16-sink `acmp_tests`. `owed-entry-widened` is still caught by the 80-byte entry assertion.
- **Campaign:** 447 caught, 0 escaped, 0 error. Coverage: 100 % lines and branches; `src/acmp.c` 815/815 lines, 426/426 branches.
- **Result:** UNCLEAN, by F1.

### Docs

- **PORTING.md:**
  - The owed-bound paragraph and the `release` row match the code and the measured sizes.
  - The storage contract changes only for `acmp_owed.release`. `check_port_contracts` passes.
- **Other docs:**
  - TESTS.md anchors `test_acmp_wide.cpp#L67` and `#L92` are the two `TEST_F` lines.
  - The plant lists match the `kills` in `tests/mutations.json`.
  - TRACEABILITY ACMP-09 names both tests.
  - VERIFICATION.md says 443 core plants plus 4 configuration plants (= 447) and documents the 33-sink binary.
  - The CHANGELOG entry is accurate.
- **Comment rule:** a scan of every added comment and assertion message in the delta finds no lane label, lane name, review round, reviewer ID or issue-comment ID. The issue references (#31, and #653 as already used in `test_acmp.cpp`) are permitted.
- **Commit:** one-line subject, no body, no trailers (CONTRIBUTING).
- **Result:** CLEAN. R1 is RESIDUE and does not make the lens unclean.

## Executed evidence (this review)

| Run | Result | Receipts |
|---|---|---|
| Clean clone of the head: `python3 scripts/validate.py --work … --jobs 8 --graphs` | rc 0, 28 of 28 gates rc 0; 9/9 CTest in the GCC and Clang-sanitizer builds (incl. `acmp_wide`); mutation 447/0/0; coverage 100 % | `receipts/ci/validate.*`, `receipts/ci/val-*` |
| Clean clone of the head: `python3 scripts/baremetal.py --work … --jobs 8` (run concurrently with the above) | rc 0, Debug and Release | `receipts/ci/baremetal.*`, `rv32-results.json` |
| Clone state before and after | empty status, empty diff (both sha256 of empty input) | `receipts/ci/status-*`, `diffsha-*`, `head` |
| Mask probe, 33 sinks | head rc 0; main rc 1 | `receipts/mask-probe-*.log` |
| Plant matrix: 10 registered plants (3 new, 7 moved), 8 review plants and an unplanted control | as stated under Tests and F1 | `receipts/plants/` |
| Survivors through the full CTest suite | 5 of 5 survive; control passes | `receipts/survivors-full-ctest.txt`, `receipts/plants/survivor-*.ctest.log` |
| Refusal, sizes, imports, every-sink | as stated above | `receipts/refusal-*`, `rv32-*`, `owed-storage-sizes.txt`, `every-sink-*` |

**Toolchain** (`receipts/ci/toolchain.txt`):
- GoogleTest and GMock 1.14.0 (pkg-config).
- Clang 18.1.3 as `clang-18`, used by the comment and assertion lexing gates.
- clang-tidy 18.1.3, cppcheck 2.22.0, Mermaid CLI 11.16.0.
- The host's GCC 16.2.1 and Clang 23.1.4 compiled the two CTest builds. The pinned Clang 18 has no sanitizer runtime here, and its C++ front end rejects the host's GCC 16 libstdc++ headers, so it could not stand in for `clang`/`clang++`.
- RISC-V GCC 16.2.0 and QEMU 11.1.3.

**Hosted, exact head (inspected, not owned):**
- `gh pr checks 33` shows 4 executed jobs, all pass, none skipped: `quality` and `bare-metal` in run 42724744778 and run 42724774168, all at head_sha `c6013804…`.
- The run 42724774168 `quality-evidence` artifact shows:
  - Clang 18.1.3 and GCC 13.3.0 compiler identification;
  - `acmp_wide` passing in both builds;
  - 28 gates rc 0;
  - mutation `{"CAUGHT": 447, "ESCAPED": 0, "ERROR": 0}`;
  - `src/acmp.c` 815/815 lines and 426/426 branches.
- Receipts: `receipts/hosted/`; the artifact zip's sha256 is in `artifact.sha256`.

**Author receipts** at milan-fpga `e225885f`: the probe, refusal, size and plant-at-16 logs agree with my independent runs.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `src/acmp.c` (every mask use, `respond`/`transmit` callers), `include/acmp.h`, ACMP-09/ACMP-12, ruling item 1, mask probe head/main, every-sink probe 16–65 sinks | R811-1 | c6013804d0fec6bc763a64b496f1a52d4a5d9f6a |
| RTL | CLEAN | `baremetal.py` Debug/Release on a clean clone, RV32 text at -Os/-O2/-O3 (16 and 33 sinks), RV32 undefined imports, owed storage sizes x86-64/RV32 | R811-1 | c6013804d0fec6bc763a64b496f1a52d4a5d9f6a |
| Robustness | CLEAN | `_Static_assert` bound (GCC + Clang 18, 9 counts, 3 planted narrowings), slot-reuse probe, `probe_of` limit (S1), shift operand width (S2) | R811-1 | c6013804d0fec6bc763a64b496f1a52d4a5d9f6a |
| Tests | UNCLEAN (F1) | `tests/test_acmp_wide.cpp`, CMake `tsn_wide`, `scripts/mutation.py` arm, `tests/mutations.json` (3 new, 7 moved), 447-plant campaign, coverage, 8 review plants, full-CTest survivors | R811-1 | c6013804d0fec6bc763a64b496f1a52d4a5d9f6a |
| Docs | CLEAN (R1 residue) | CHANGELOG, PORTING (owed bound, storage row), TESTS, TRACEABILITY, VERIFICATION, PR body, commit message, comment-rule scan of the delta | R811-1 | c6013804d0fec6bc763a64b496f1a52d4a5d9f6a |

## Real limits

- The local CTest builds used host GCC 16.2.1 and Clang 23.1.4, not the CI's GCC 13.3.0 and Clang 18.1.3. The Clang 18 and GCC 13 legs are evidenced only by the inspected hosted artifact at this head. Clang 18.1.3 was executed locally for the lexing gates and the C-only refusal compiles.
- The two `apt-get`/`npm` install steps were not run. The pinned toolchain above stood in for them.
- validate.py and baremetal.py ran with `--jobs 8` each, concurrently, against the CI's `--jobs 16`.
- The RV32 size figures are from riscv64-elf-gcc 16.2.0. Those of the CI's Ubuntu cross compiler may differ.
- No manager source bank runs at this head, and none is claimed or inferred. Source-head execution evidence beyond this review's own runs is the author's published receipts.
- Physical calibration NOT RUN. No hardware was used. Field or hosted skips are not hardware proof (no jobs were skipped at this head).
- The 33-sink path is host-tested only. No RV32 build at 33 sinks executes. The parent's 32x32 image, its disassembly check and its pin move are outside this PR.

## Pending manager duties

- Carry R1 to the residue checklist.
- Build and validate the current-dev merge candidate (source base `ea4af6f1`, live dev `123f57a922bf07476cd69f91867f3b6f07080804`) with the builder and native banks at the merge turn, and link those receipts on the PR.
- Own hosted/act acceptance.
- Obtain the second independent review. Merge needs two independent positive reviews.
- After F1 is addressed at a new head, a new review round covers it.

R811-1 FINISHED
