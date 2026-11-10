[R812] POSITIVE - exact head 97414fe6518cda2bf7c4ea136fdd8bd25c860d83

# R812-2: external independent review of kebag-logic/tsn-c-stack PR #33 (issue #31), round 2

- Head `97414fe6518cda2bf7c4ea136fdd8bd25c860d83`, tree `81556a7e3451a5c0633c93790732520ea81c941e`. Three commits on round 1's `c6013804` (`6a81006`, `a7fb45d`, `97414fe`). Source base `ea4af6f1`.
- Judged against the round 2 ruling (PR #33 issuecomment-6756156104) and the code, not the author's summary.
- Scope came from CONTRIBUTING.md, docs/VERIFICATION.md, docs/PORTING.md, the issue #31 body, the ruling, the diff `ea4af6f1..97414fe6` (delta `c6013804..97414fe6`), and the published author packet `review-evidence/tsn31-r1/author-r2` at milan-fpga `18c77dbe`.
- The repository has no AGENTS.md.
- I read prior public findings (R811-1 and R812-1) only after my own pass. They are resolved below.

## Verdict

**POSITIVE.** Every item of the ruling is met at this head, and I found no open MINOR, MAJOR or BLOCKER.

- **Item 1.** The four new tests check behaviour (counts, change callbacks, their order and sink index), not constants. Each first proves its slot is the reused one.
  - The five round-1 survivors are registered, and each applies at exactly one place.
  - In my own matrix, each one escapes the whole 9-binary suite without its killers and is caught with them, every needle present.
  - My own round-1 plant probe and disposable 33-sink test, run unchanged, now kill every former survivor.
- **Item 3.**
  - S1 bounds the sink count at 255, which is exact. I checked this at run time at 255 sinks.
  - S2 is in place.
  - The compile controls refuse and accept on both sides of each bound, with gcc and clang, and each refusal names its own assertion. I planted four defects into the two `_Static_assert`s, and the controls fail on each one.
  - RV32 object code is byte-identical to round 1 at -Os, -O2 and -O3.
- **Item 2 and the residue.** Both are fixed, and the generated docs are current.
- **My own gate runs.** `validate.py` passes 28 of 28. The mutation campaign catches 452 with 0 escaped and 0 errors, and coverage is 100 % of lines and branches. `baremetal.py` passes Debug and Release.
- **STOP condition.** It does not apply. `include/` is unchanged since round 1, and in round 2 `src/` changes only at S1 and S2.

## Scope reconstructed (frozen acceptance)

- **Issue #31.** The mask is sized from `ACMP_MAX_SINKS` at every use, a build the type cannot hold is refused at build time, and there is a unit test at 33 sinks under UBSan.
- **Ruling item 1 (F1).**
  - Sinks 31 and 32 at 33 sinks are each held only by their own owed response and released only when it leaves.
  - A probe owed in a slot that held another sink's response holds no sink: at 33 sinks for every mask word, and at 16 sinks.
  - The five R811-1 plants are registered with needles, and each is shown escaping without its killer and caught with it.
  - The counts and generated docs are updated.
  - R811-1's `plants.py` and `survivors_full_ctest.sh` and R812-1's 33-sink test are re-run unchanged.
  - The campaign has 0 escaped, and coverage stays at 100 %.
- **Item 2 (residue).** The size table names its compiler and flags. The 33-sink command does not depend on one build directory.
- **Item 3.**
  - S1 is a `probe_of` refusal and S2 an explicit-width one.
  - A compile control shows the refusal at too few `ACMP_RELEASE_WORDS`.
  - R812-1 S1 is allowed only if -Os does not grow, with the bytes stated either way.
- **Done means.** 28 of 28 gates, 0 escaped, baremetal Debug and Release, and the size before and after stated.
- **STOP.** Any `src/` or `include/` change beyond S1 and S2, or any public API change.

## STOP condition check

- `git diff c6013804..97414fe6 -- include` is empty.
- In `src/`, round 2 changes two lines:
  - `src/acmp.c:37` adds `_Static_assert(ACMP_MAX_SINKS <= UINT8_MAX, ...)` (S1).
  - `src/acmp.c:312` changes `1u <<` to `UINT32_C(1) <<` (S2).
- No public function, callback, configuration, view, counter or field changes in round 2. The `acmp_owed.release` array type is round 1's, and the ruling accepted it ("Both reviews find the fix correct at every use of the mask").

## Findings

No MINOR, MAJOR, BLOCKER or RESIDUE at this head. Three suggestions, none of which affects the verdict:

### R812-2-S1: SUGGESTION (Tests). W4/W5 could assert the first sink's frames left before reusing the slot, as A19A does

- **Where:** `tests/test_acmp_wide.cpp:75-88` (`probe_in_the_slot_of`), used by `:170` and `:185`.
- **Observation:**
  - The helper casts both `acmp_poll` results to void and asserts nothing between the first bind and the refill.
  - Slot reuse is still proven: the ASSERT `owed_count == 7u && owed[slot].probe_of == 4u` at `:172` and `:187` holds only if the ring wrapped through the slot that the first bind filled.
  - The 16-sink test at `tests/test_acmp.cpp:1172-1173` also asserts that the old sink's response and probe left and that its change was reported.
- **Suggestion:** add the same intermediate assertion to the helper, `owed_count == 0u && !acmp_change_pending(&a, sink) && fk.count(Call::CHANGED) == 1u`. A later fixture change then cannot pass the slot ASSERT for another reason.

### R812-2-S2: SUGGESTION (Tests, Robustness). No build covers exactly 32 sinks, the one-word edge

- **Where:** `CMakeLists.txt:63-68` (`tsn_wide` at 33 sinks only) and `src/acmp.c:312`.
- **Observation:**
  - At exactly 32 sinks, the registered `acmp-wide-release-word-off-by-one` writes `release[1]` into a one-word array (R811-1 F1 noted this).
  - The 33-sink arm catches the plant, so the registered set has no gap.
  - Still, no binary builds the one-word edge with array bounds checking. `-fsanitize=shift,undefined` checks shifts, and the out-of-range index stays inside the struct, where address sanitizing does not see it.
- **Suggestion (optional):** a 32-sink build of `test_acmp_wide.cpp` with `-fsanitize=bounds`, or a `kLast`-parameterised fixture.

### R812-2-S3: SUGGESTION (Tests). Register the escape-without-killer check

- **Observation:**
  - `scripts/mutation.py` proves that each plant is caught by its needles.
  - That each plant escapes without its killer is shown only by probes (the author's `escape_matrix.py` and mine).
- **Suggestion (optional, later issue):** a campaign mode that reruns a plant with its killers filtered out. A future test that also kills the plant would then be reported, which keeps each needle meaningful.

## Prior public findings: resolution at this head

| Prior finding | Status at 97414fe6 | Evidence |
|---|---|---|
| R811-1 F1 = R812-1 F1 (MINOR, Tests/Docs): word-boundary and stale-bit behaviour unchecked | **RESOLVED** | W3 at `test_acmp_wide.cpp:140`; W4, W5 at `:170`, `:185`; A19A at `test_acmp.cpp:1159`. Five plants at `tests/mutations.json` (`acmp-wide-release-word-off-by-one`, `-owed-count-word-off-by-one`, `-release-loop-word-off-by-one`, `acmp-owed-release-not-cleared`, `acmp-wide-release-clears-one-word`). Each matches once (`receipts/probes/escape-matrix.json`) and is CAUGHT in my campaign (`receipts/gates/val/mutation.log:431-441`). My matrix shows that each ESCAPES the whole 9-binary CTest without its killers and is CAUGHT with all needles with them. VERIFICATION 448 core plus 4; TESTS.md and TRACEABILITY.md current (gates rc 0); ACMP-09 names all four tests. |
| R811-1 R1 = R812-1 F3 (RESIDUE): the size table does not name its compiler | **RESOLVED** | The PR body's Size names riscv64-elf-gcc 16.2.0 and the full flags. I reproduced the figures (`receipts/probes/rv32-identity.txt`). |
| R812-1 F2 (RESIDUE): the 33-sink command names one build directory | **RESOLVED** | `docs/VERIFICATION.md:26` now reads "`ctest --test-dir build-gcc -R acmp_wide` or `ctest --test-dir build-sanitize -R acmp_wide`", the exact fix. |
| R811-1 S1 = R812-1 S3 (SUGGESTION): bound `probe_of` | **TAKEN; the author's 255 is right and R812-1 S3's 254 was one too strict** | `probe_of` stores k + 1 in a `uint8_t` for k ≤ `ACMP_MAX_SINKS` − 1, so the largest stored value equals `ACMP_MAX_SINKS`, and 255 sinks (indices 0 to 254) is the exact bound. R812-1 S3's "cannot name a sink past 254" was about the index, and its `<= 254u` would refuse a working count. At run time at 255 sinks, the last sink's probe has `probe_of == 255`, leaves, is attributed to sink 254, and releases only that sink's change, with no sanitizer report. R811-1's every-sink probe also passes at 255 (`receipts/probes/bound-probe.log`). |
| R811-1 S2 (SUGGESTION): explicit-width one | **TAKEN** | `src/acmp.c:312`. RV32 object code unchanged. |
| R812-1 S2 (SUGGESTION): compile control for the refusal | **TAKEN** | `scripts/check_conditionals.py:141-170`. My planted refusal defects (off by one, removed, for each assertion) each make `capacity_controls()` raise, and the unplanted copy passes (`receipts/probes/bound-probe.log` §2). |
| R812-1 S1 (SUGGESTION): increment directly in `transmit` | **NOT TAKEN, as the ruling allows** | The ruling makes S1 optional ("only if"). The author states the bytes (−60 B at -Os) and gives two reasons: the loop is a registered plant's target, and the hold and the release would stop reading the same stored bits. I accept both. The head's -Os code equals round 1's. |

Comment rule: the delta's new comments are four `// REQ: ACMP-09` lines and one docstring in `check_conditionals.py`. Assertion messages use test-step labels (W3–W5, A19), as the existing tests do. No bench lane label, lane name, review round, reviewer ID or issue-comment ID appears in the delta, so there is no new RESIDUE. Commit subjects are one line with no body.

## Lens evidence

### Conformance: CLEAN

- **ACMP-09 (Milan v1.2 5.5.3.5).** A change notice waits only behind its own owed response and is released when that response leaves.
  - W3 checks sinks 31 and 32 in both release orders: 31's response leaves first and releases 31 alone, then 32's leaves and releases 32 alone while 31 waits on its unbind response.
  - W4, W5 and A19A check that a probe owed in a reused slot holds no sink: the old sink's next change is reported at once, and no sink is held after the drain.
- The traceability row for ACMP-09 lists all four tests.
- My campaign and matrix show each test catches the defect it was written for.

### RTL (target object code and firmware image): CLEAN

- The repository has no HDL. The artefact under this lens is the RV32 object code and image.
- `src/acmp.c` for RV32I at the PR's flags (riscv64-elf-gcc 16.2.0):

  | Flags | main | Round 1 | Head |
  |---|---:|---:|---:|
  | -Os | 10,825 B | 10,921 B | 10,921 B |
  | -O2 | 16,029 B | 16,141 B | 16,141 B |
  | -O3 | 19,365 B | 20,365 B | 20,365 B |

  At each level the disassembly hash and the `.text` byte hash are identical between round 1 and the head (`receipts/probes/rv32-identity.txt`). The ruling's -Os condition holds: no growth.
- In my `baremetal.py` run, the Release ELF is 51,480 B with sha256 `a7a2b614…`, equal to the author's published one, and the core object hashes and imports are equal too.
- The Debug ELF hash differs from the author's, most likely because debug info embeds the build paths. Its imports are equal.

### Robustness: CLEAN

- **S1** refuses 256 and accepts 255, and at 255 the last sink is named and released at run time.
- **S2** makes the shifted one 32 bits wide on every target.
- **The mask refusal.** The capacity control refuses the planted one-word mask at 33 and accepts it at 32, each refusal naming only its own assertion.
- **Other counts.** Wide-count probes at 33, 64, 65 and 255 sinks pass under `-fsanitize=shift,undefined` without recovery.
- **The set index** `(release - 1u) / 32u` is below `ACMP_RELEASE_WORDS` for every release ≤ `ACMP_MAX_SINKS`.

### Tests: CLEAN

- **Behaviour, and slot proof.**
  - W3 asserts per-sink `change_owed`, `acmp_change_pending`, and the count, order and index of `CHANGED` calls.
  - W4, W5 and A19A each ASSERT first that sink 3's probe (`probe_of == 4`) lies in the slot computed before the first bind, with 7 frames owed, which is possible only after the ring wrapped through the reused slot.
  - They then check behaviour: the old sink is not held, `acmp_set_started` is reported at once, and every count is zero after the drain.
- **My escape/catch matrix** (`scripts/escape_matrix.py`, `receipts/probes/escape-matrix.{log,json}`), on a whole-project GCC Debug build per plant:
  - each of the five plants passes all 9 CTest binaries with its killers excluded through `GTEST_FILTER`, "100% tests passed out of 9";
  - with only its killers, each fails exactly its registered killer tests, and every registered needle appears in the output;
  - the unplanted control passes both ways.
  - With only AcmpWide killers selected, `acmp_tests` exits 1 because it runs 0 tests, which `tests/main.cpp` refuses. That is expected and is not a catch; the catch is read from `acmp_wide`.
- **My round-1 scripts, run unchanged** (their hashes match my round-1 manifest, `receipts/reviewer-scripts/own-r1-*.txt`):
  - `run_wide_gaps.sh` passes unplanted, and its three plants fail as in round 1.
  - `plant_probe.py`: every round-1 survivor now fails `acmp_wide` or `acmp_tests` by a named test, namely `x-memset-removed` (also at 16 sinks), `x-memset-first-word-only`, `x-set-index-off-by-one`, `x-add-word-of-next-sink`, `x-sub-word-of-next-sink` and `x-unbind-releases-nothing`.
  - Two rows report "plant must match exactly once" because their anchor is the pre-S2 `1u <<` text: `acmp-wide-release-word-ignored` and `x-set-shift-unmasked`. The registered plant follows S2 and is CAUGHT in the campaign. `x-set-shift-unmasked` is the same defect as R811-1's `review-transmit-unbounded-shift`, which fails `acmp_wide` in the anchor-adjusted run below.
  - The `x-refusal-*` rows pass at run time, as they must: a compile refusal has no run-time test. The new capacity control kills them (Robustness above).
- **R811-1's published scripts, run unchanged:**
  - `survivors_full_ctest.sh`: all five former survivors now fail the full CTest ("89%" or "78% tests passed"), and the unplanted control passes, "100% … out of 9".
  - `plants.py` stops with `AssertionError: ('review-transmit-unbounded-shift', 0)`, which reproduces the author's statement.
- **The author's one-line anchor change** (`receipts/reviewer-scripts/r811-plants-anchor.diff`) changes `'= 1u << ((release - 1u) % 32u);' → '= 1u << (release - 1u);'` to `'= UINT32_C(1) << ((release - 1u) % 32u);' → '= UINT32_C(1) << (release - 1u);'`.
  - It is the **same defect**: the `% 32u` mask is dropped from a shift of a 32-bit unsigned one, and `UINT32_C(1)` is a 32-bit unsigned `1U` on both targets.
  - The copy is otherwise byte-identical to the published `plants.py`, and its `every_sink_probe.cpp` is identical too.
  - Run: the unplanted row passes all three binaries. Every `review-*` plant fails `acmp_wide` and the every-sink probe, and `review-mask-not-cleared` also fails `acmp_tests`.
- **Campaign.** 452 CAUGHT, 0 ESCAPED, 0 ERROR. All 8 `acmp-wide-*` and `acmp-owed-release-not-cleared` are CAUGHT.

### Docs: CLEAN

- `docs/VERIFICATION.md:24` counts 448 core plants and four generated configuration plants: `tests/mutations.json` has 452 entries, 4 under `examples/entities`.
- `:26`: the 33-sink row describes exactly what W1 to W5 and A19A check, and names both build directories that the table's own commands create.
- `:33`: the conditional-gate row matches the five capacity cases in the gate's log.
- `docs/PORTING.md:79` states the 255 bound and its reason.
- The CHANGELOG entry matches the code.
- `docs/TESTS.md` and `docs/TRACEABILITY.md` are current: the test-inventory gate refuses stale output and is rc 0, with "181 declarations, 452 plants", and the traceability gate is rc 0.
- The PR body's line references (`src/acmp.c:37`, `:312`, `scripts/check_conditionals.py:141`, `tests/test_acmp_wide.cpp:140/170/185`, `tests/test_acmp.cpp:1159`) all point at the stated lines.

## Executed evidence (this review, at exact head)

| Run | Result | Receipt |
|---|---|---|
| `validate.py --work <scratch> --jobs 16 --graphs` | rc 0; 28 of 28 gates rc 0; mutation `{"CAUGHT": 452, "ESCAPED": 0, "ERROR": 0}`; coverage `src/acmp.c` 815/815 lines, 426/426 branches, every file 100 % after exclusions; GCC and sanitizer CTest 9/9 including `acmp_wide`; wall 11:24, max RSS 0.45 GB | `receipts/gates/validate.{log,rc,time}`, `receipts/gates/val/*` |
| `baremetal.py --work <scratch> --jobs 8` (concurrent with the above) | rc 0; Debug and Release rc 0 with the QEMU smoke run; Release imports `__umodsi3`, `ctrl_reentry_assert`, `memcpy`, `memset` | `receipts/gates/baremetal.*`, `receipts/gates/rv32/results.json` |
| Clone status and diff before and after | empty, diff sha of the empty input both times | `receipts/gates/status-*`, `diffsha-*` |
| Escape/catch matrix, 5 plants plus control | all ESCAPE without killers and are CAUGHT with all needles | `receipts/probes/escape-matrix.*` |
| My round-1 scripts unchanged | as above | `receipts/reviewer-scripts/r812-*` |
| R811-1's published scripts unchanged, and the anchor copy | as above | `receipts/reviewer-scripts/r811-*` |
| Bound probe (wide counts, capacity-control plants) | all pass; all 4 plants kill the control | `receipts/probes/bound-probe.*` |
| RV32 identity (main, round 1, head) | head equals round 1 at -Os, -O2 and -O3 | `receipts/probes/rv32-identity.txt` |
| Author packet spot-check | 18 receipts verify against `author-r2/MANIFEST.sha256`, among them `validate.{log,rc}`, `val/mutation.log` (452/0/0), `val/coverage.log`, `val/gates.json`, `rv32/results.json`, `escape-matrix.log`, `PR-BODY.md` and the anchor diff. My figures agree with theirs. | `receipts/author-receipts-spotcheck.*` |

- **Toolchain** (`receipts/gates/tools.txt`):
  - GoogleTest and GMock 1.14.0, Clang 18.1.3 as `clang-18` for the lexing gates, clang-tidy 18.1.3 and Mermaid CLI 11.16.0;
  - from the host: GCC 16.2.1, Clang 23.1.4 (sanitizer build and capacity controls), CMake 4.4.5, Cppcheck 2.22.0, riscv64-elf-gcc 16.2.0 and QEMU 11.1.3.
- **Clone integrity after every probe** (`receipts/clone-integrity.txt`): HEAD and tree are exact, the status is empty including ignored files, `git diff HEAD` is empty, and the index hash is recorded. There are no submodule gitlinks, and `git fsck` is clean. Probes ran only on `git archive` exports under the packet scratch.

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | ACMP-09 vs W1–W5 and A19A; the TRACEABILITY ACMP-09 row; the escape/catch matrix | R812-2 (round-1 mask uses carried: unchanged by the delta except S2, checked) | 97414fe6518cda2bf7c4ea136fdd8bd25c860d83 |
| RTL | CLEAN | RV32I `acmp.c` objects at main, round 1 and head (-Os, -O2, -O3, disassembly and text hashes); `baremetal.py` Release ELF and core objects vs the author's | R812-2 | 97414fe6518cda2bf7c4ea136fdd8bd25c860d83 |
| Robustness | CLEAN | `src/acmp.c:35-37`, `:312`; capacity controls and 4 refusal plants; 33/64/65/255-sink sanitizer probes | R812-2 | 97414fe6518cda2bf7c4ea136fdd8bd25c860d83 |
| Tests | CLEAN | `tests/test_acmp_wide.cpp`, `tests/test_acmp.cpp:1159-1193`, `tests/mutations.json` (5 new entries, 1 re-anchored), `scripts/mutation.py`, `scripts/check_conditionals.py`; campaign 452/0/0; matrix; round-1 scripts of both reviewers | R812-2 | 97414fe6518cda2bf7c4ea136fdd8bd25c860d83 |
| Docs | CLEAN | `docs/VERIFICATION.md:24,26,33`, `docs/PORTING.md:76-79`, CHANGELOG, generated TESTS.md and TRACEABILITY.md (gates), PR body | R812-2 | 97414fe6518cda2bf7c4ea136fdd8bd25c860d83 |

## Real limits

- **Toolchain.** The sanitizer build and the capacity controls' `clang` used host Clang 23.1.4, not the CI image's Clang 18. GCC is host 16.2.1, not the CI's GCC 13.
- **Hosted CI.** The hosted job read is not my execution. At the time of reading:
  - run 42763951552 had `quality` and `bare-metal` both success;
  - run 42763946123 had `bare-metal` success and `quality` still in progress (started 05:45:34Z).
  - The manager owns hosted and act acceptance (`receipts/hosted/check-runs-at-review.txt`).
- **No manager source bank** ran at this head, and I claim none. The source-head execution evidence is the author's published receipts plus my own runs above.
- **Physical calibration NOT RUN.** No hardware was used. The QEMU smoke run is not hardware proof.
- **Not re-measured.** The author's R812-1 S1 variant figures (10,861 B at -Os) were not re-measured, because my round-1 variant script anchors on the pre-S2 text. The figures do not affect the verdict, since the suggestion was not taken.
- **Debug image hash.** My Debug bare-metal ELF hash differs from the author's, most likely because of embedded build paths. For Debug I compared only the core imports, which are equal, and not the loaded sections.

## Pending manager duties

- Build and validate the current-dev merge candidate (source base `ea4af6f1`, live dev `123f57a922bf07476cd69f91867f3b6f07080804`), run the builder and native banks, and link their receipts on the PR.
- Hosted and act acceptance at the final candidate, including the `quality` job that was still in progress at this head when I read it.
- Carry the three suggestions above to the author or the follow-up list as the manager sees fit. None blocks.
- Merge still needs the second independent positive review at the same head.

R812-2 FINISHED
