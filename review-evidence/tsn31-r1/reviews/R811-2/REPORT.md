[R811] POSITIVE - exact head 97414fe6518cda2bf7c4ea136fdd8bd25c860d83

# R811-2: internal independent review of kebag-logic/tsn-c-stack PR #33 (issue #31)

- **Head:** `97414fe6518cda2bf7c4ea136fdd8bd25c860d83`, tree `81556a7e3451a5c0633c93790732520ea81c941e`. The PR's `headRefOid` equals it.
- **Base:** `main` `ea4af6f1`.
- **Delta reviewed:** three commits on round 1's `c6013804`: `6a81006` (S1 and S2), `a7fb45d` (tests, plants, generated docs) and `97414fe` (compile controls).
- **Ruling judged against:** PR #33 issuecomment-6756156104, the round 2 ruling on R811-1 and R812-1. Both were NEGATIVE at `c6013804` on F1, the test gap.
- **Author packet:** milan-fpga archive `18c77dbea82413574efe9b49ed1bd019021eeb9a`, `review-evidence/tsn31-r1/author-r2`.

## Verdict

POSITIVE. Every item of the round 2 ruling is met at this head, and I checked each one against the code and my own runs, not the author's summary.

- **Item 1, tests.** W3, W4, W5 and A19A assert behaviour: whether a change is pending, whether it is reported at once, the owed counts, and the state after the drain. Each slot test first proves that the probe sits in the reused slot. That is an `ASSERT` on `probe_of == 4` in the slot where the earlier response was queued.
- **Item 1, plants.** All five former survivors are registered, and each applies to exactly one place. My own probe shows that each escapes both ACMP binaries with its killers filtered out. Run with only its killers, each fails and prints every registered needle.
- **Item 1, round 1 scripts.** At this head my round 1 `survivors_full_ctest.sh`, run unchanged, fails the full CTest for all five plants, and the unplanted control passes. My round 1 `plants.py`, run unchanged, stops at its own one-application check on the S2 line. The author's copy changes only that anchor and keeps the same defect. With it, all eight review plants fail `acmp_wide`.
- **Item 3, S1.** The 255-sink bound is exact. R812-1 S3's 254 was one too low.
- **Item 3, S2.** The explicit-width shift is in place.
- **Item 3, compile controls.** They refuse and accept on both sides of each bound, with gcc and with clang, and each refusal must name its own assertion. With either assertion removed, the gate fails.
- **Item 3, object code.** RV32 object code for `src/acmp.c` equals round 1's byte for byte at `-Os`, `-O2` and `-O3`, at 16 sinks and at 33.
- **Item 4, residue.** All of the residue the ruling listed is fixed.
- **Item 5, gates.** `validate.py` passes 28 of 28 gates. The mutation campaign gives 452 caught, 0 escaped and 0 error. Coverage is 100 % of lines and branches. `baremetal.py` passes Debug and Release, both rc 0. The clone was clean before and after.
- **STOP condition.** The delta does not touch `include/`. The only `src/` lines it changes are S1 (`src/acmp.c:37`) and S2 (`src/acmp.c:312`). No public API changes.

There is no open BLOCKER, MAJOR, MINOR or RESIDUE. Two SUGGESTIONs follow; they do not affect the verdict.

## Scope reconstructed

- **CONTRIBUTING.md.** The repository has no AGENTS.md.
  - A regression needs a failing assertion and a runnable planted defect.
  - A protocol change updates its requirement, tests and traceability.
  - The coverage ratchet is not lowered.
  - Commits use one-line subjects with no body.
  - Neutral role labels are used, and private identifiers are kept out.
- **Issue #31.** Wanted: the mask sized from `ACMP_MAX_SINKS` at every use, a build-time refusal for any count the type cannot hold, and a 33-sink unit test under UBSan.
- **Round 2 ruling.** The round is tests and docs only.
  - STOP if `src/` or `include/` needs any change beyond S1 and S2, or if any public API changes.
  - Item 1 (F1): the tests, the five plants, the counts and generated docs, and both reviewers' scripts run unchanged.
  - Item 2 (residue): the PR size table names its compiler, and the 33-sink command does not depend on one build directory.
  - Item 3 (suggestions): S1, S2, the refusal compile control, and R812-1 S1 only if `-Os` does not grow, with the bytes stated either way.
  - Done means 28 of 28 gates, a full mutation campaign with 0 escaped, and `baremetal.py` Debug and Release on a clean clone, with the size before and after stated.
- **Requirement.** ACMP-09 (Milan v1.2 5.5.3.5): a change notification waits until its response is accepted. ACMP-12 is the owed bound.

## Findings

### Prior public findings on this PR, resolved at this head

Both round 1 reports were read only after my own pass over the diff.

| Prior finding | Status at `97414fe6` | Evidence |
|---|---|---|
| R811-1 F1 = R812-1 F1 (MINOR, Tests and Docs): the multi-word mask has no catching assertion for the word boundary or stale bits | **RESOLVED** | Details in the rows below. |
| ↳ word boundary | | `tests/test_acmp_wide.cpp:140` (W3) binds sinks 31 and 32 and checks each release order: 31's response leaves first, then 32's leaves ahead of 31's unbind response. |
| ↳ slot reuse at 33 sinks | | `:170` (W4, word 0) and `:185` (W5, word 1). |
| ↳ slot reuse at 16 sinks | | `tests/test_acmp.cpp:1159` (A19A). |
| ↳ the five plants | | Registered in `tests/mutations.json` (`acmp-wide-release-word-off-by-one`, `acmp-wide-owed-count-word-off-by-one`, `acmp-wide-release-loop-word-off-by-one`, `acmp-owed-release-not-cleared`, `acmp-wide-release-clears-one-word`). Kill and escape are shown by `receipts/escape-kill.log`, and the full CTest by `receipts/r811-1-survivors-at-head.txt`. R812-1's two plants are the same defects as the one-word clear and the set-index off-by-one. |
| ↳ docs | | The `docs/VERIFICATION.md:26` claim now states only what the binary checks. |
| R811-1 R1 = R812-1 F3 (RESIDUE): the PR size table does not name its compiler | **RESOLVED** | The PR body's Size section names `riscv64-elf-gcc 16.2.0` and the full flags. |
| R812-1 F2 (RESIDUE): the 33-sink command names one build directory | **RESOLVED** | `docs/VERIFICATION.md:26` names both `build-gcc` and `build-sanitize`. |
| R811-1 S1 = R812-1 S3 (SUGGESTION): bound `probe_of` | **TAKEN** | `src/acmp.c:37` bounds by `UINT8_MAX` (255). That is exact: `receipts/bound-probes.txt`. R812-1 S3's 254 would refuse a valid build. |
| R811-1 S2 (SUGGESTION): an explicit-width one | **TAKEN** | `src/acmp.c:312` uses `UINT32_C(1) <<`. The object code is unchanged. |
| R812-1 S2 (SUGGESTION): a compile control for the refusal | **TAKEN** | `scripts/check_conditionals.py:141-170`. My ablation shows the gate fails without either assertion. |
| R812-1 S1 (SUGGESTION): increment the released sink directly | **MEASURED, NOT TAKEN** (permitted) | The ruling made it optional, conditioned on `-Os`. The PR states the bytes (10,921 to 10,861 B at `-Os`) and gives its reasons: the variant would delete a plant target, and the hold and the release would stop reading the same bits. This is acceptable, and I make no further request. |

### New findings at this head

#### S-1: SUGGESTION. Assert the drain in the 33-sink slot-reuse helper too

- **Lenses:** Tests.
- **Where:** `tests/test_acmp_wide.cpp:75-88` (`probe_in_the_slot_of`).
- **Evidence:**
  - A19A (`tests/test_acmp.cpp:1167-1172`) asserts that the earlier sink's response and probe left before the slot is reused.
  - The 33-sink helper relies on the later `owed_count == 7u`. That count does imply the drain, since exactly seven frames are owed afterwards. So the proof holds, but it is indirect.
- **Impact:** none on correctness. If the helper is ever changed, the precondition of W4 and W5 would be checked one step later than in A19A.
- **Suggested outcome:** optionally add the same `ASSERT_TRUE(a.owed_count == 0u && !acmp_change_pending(&a, sink))` after the two polls in the helper.
- **Verification:** none needed for this verdict.

#### S-2: SUGGESTION. Round 1's "Not in this PR" bullet in the PR body now describes work this PR does

- **Lenses:** Docs.
- **Where:** PR #33 body, section "Round 1 … Not in this PR", second bullet.
- **Evidence:** the bullet already adds "Round 2 refuses such a build (S1)", so it is not wrong.
- **Suggested outcome:** optionally move the bullet into the Round 2 "S1" item, or delete it.

### Comment rule (owner 2026-10-15)

- **New source comments in the delta:** four `// REQ: ACMP-09` lines (`tests/test_acmp.cpp:1158`, `tests/test_acmp_wide.cpp:139,169,184`) and the `capacity_controls` docstring in `scripts/check_conditionals.py`.
- **New assertion messages:** these use the file's existing test-step labels (W3 to W5, and A19 for the A19A group, the same label every A19A test already uses).
- **Result:** no bench lane label, lane name, review round, reviewer ID or issue-comment ID appears. There is no residue, and the comments gate passes (rc 0).
- **Commits:** the three commits have one-line subjects and empty bodies.

## Lens evidence

### Conformance: CLEAN

- **ACMP-09 and Milan v1.2 5.5.3.5:** a change waits until its response is accepted.
  - W3 shows this on both sides of the word boundary, in both release orders.
  - W4, W5 and A19A show that a release-less probe in a reused slot holds no sink, and that the earlier sink's next change is reported at once.
- **Round 1 behaviour carries forward unchanged.** S1 is a compile-time check and S2 a type spelling, and the RV32 object code equals round 1's at all six levels (`receipts/rv32-compare.txt`).
- **Hosted context (executed, not skipped):** check runs at the exact head show `quality` completed success (05:58 to 06:05Z) and two `bare-metal` runs completed success. A second `quality` context, started at 05:45Z, was still `in_progress` when queried (`receipts/hosted-check-runs.tsv`). Hosted acceptance belongs to the manager.

### RTL: CLEAN

This repository has no HDL; the lens covers the RV32 firmware target.

- **`src/acmp.c` with `riscv64-elf-gcc` 16.2.0:**
  - **Flags:** `-march=rv32i -mabi=ilp32 -ffreestanding -fno-builtin -nostdinc -std=c11 -DNDEBUG -DCTRL_REENTRY_ASSERT`.
  - **Text against `main`, round 1's script unchanged:**
    - At 16 sinks: `main` 10,825 / 16,029 / 19,365 B, head 10,921 / 16,141 / 20,365 B at `-Os` / `-O2` / `-O3`.
    - At 33 sinks: `main` 10,817 / 16,049 / 18,117 B, head 10,985 / 16,229 / 18,813 B.
    - **Round 1 against head:** `objdump -d -r` and `.text` bytes are identical at all six levels.
  - **The ruling's `-Os` condition:** met. `-Os` did not grow from round 1 to the head (0 B).
- **`baremetal.py`, run by me at the head:**
  - Debug and Release rc 0, with the QEMU smoke run.
  - The core imports are unchanged: `__umodsi3`, `ctrl_reentry_assert`, `memcpy` and `memset` in Release.
  - The Release ELF has sha256 `a7a2b614ad2ce743…` and is 51,480 B. That is identical to round 1's published receipt and to the author's.
  - The Debug ELF hash differs only as debug-info paths do, and I did not take it as evidence.

### Robustness: CLEAN

- **The S1 bound is exact.**
  - `probe_of` stores `k + 1` with `k < n_sinks <= ACMP_MAX_SINKS` (init refuses more: `src/acmp.c:1043`), so its largest value is `ACMP_MAX_SINKS`.
  - My runtime probe (`scripts/probe_of_bound.cpp`) passes at 254 and at 255 sinks: the last sink's owed probe names it, `probe_of == 255`.
  - At 256 sinks the head refuses to build, with gcc and with clang, and names "the owed probe_of names one plus the index of every sink".
  - With only that assertion removed, 256 builds and the probe stores 0, so the last sink's probe names no sink. The bound is therefore exactly 255, and R812-1 S3's 254 is one too low.
- **Index bounds.** `(release - 1u) / 32u < ACMP_RELEASE_WORDS` because `release <= n_sinks`. The loops read word `k / 32u` with `k < n_sinks`.
- **The S2 plant change.** `UINT32_C(1)` expands to an `unsigned int` constant on both hosts and on ilp32. The author's re-anchored `review-transmit-unbounded-shift` is therefore the same defect: at this head it aborts `acmp_wide` with `shift exponent 32 is too large for 32-bit type 'unsigned int'` at `src/acmp.c:312:50`.
- **The compile controls refuse and accept in the right places** (`receipts/bound-probes.txt`, `receipts/ci/val-conditionals.log`):
  - The committed storage compiles at 33 and 255 sinks and is refused at 256 by the probe_of assertion only.
  - A one-word `ACMP_RELEASE_WORDS` compiles at 32 sinks and is refused at 33 by the mask assertion only.
  - Each case runs with gcc 16.2.1 and with clang, and each refusal must name exactly its own message.
- **The compile controls fail when an assertion is missing.** My ablation runs the selftest on copies of the tree:
  - The exact copy passes (rc 0).
  - Without the probe_of assertion the gate fails (rc 1, "committed at 256u sinks with gcc: rc 0").
  - Without the mask assertion the gate fails (rc 1, "one-word at 33u sinks with gcc: rc 0").
- **Sanitizers.** The GCC `-fsanitize=shift,undefined` 33-sink binary and the Clang ASan and UBSan suite both pass in validate.

### Tests: CLEAN

- **W3** (`tests/test_acmp_wide.cpp:140-167`) checks the hold and the release through behaviour: `acmp_change_pending`, the CHANGED callback order and sink, and `change_owed` totals.
  - Both release orders are covered: 31's response leaves before 32's, then 32's response leaves before 31's unbind response.
- **W4, W5 and A19A** first `ASSERT` that sink 3's probe (`probe_of == 4`) lies in the slot where the earlier sink's response was queued, with seven frames owed.
  - They then check that only sinks 1 to 3 wait, that `acmp_set_started` on the earlier sink is reported at once, and that nothing is held after the drain.
  - A19A runs at the default 16 sinks with all 16 configured, where the stale-bit defect is live.
- **The five plants** (`receipts/escape-kill.log`, my `scripts/escape_kill.py`):
  - Each `old` text occurs exactly once in `src/acmp.c`.
  - With every registered killer filtered out, each plant passes `acmp_tests` (126 or 127 tests) and `acmp_wide` (3 or 4 tests).
  - With only its killers, each fails, and every registered needle appears in the output.
  - In the full campaign, all five are CAUGHT (`receipts/ci/val-mutation.log`).
- **Round 1 scripts at this head:**
  - `survivors_full_ctest.sh`, unchanged: all five plants give rc 8 (one of nine failed; `review-mask-not-cleared` two of nine), and the unplanted control passes nine of nine.
  - `plants.py`, unchanged: rc 1, stopped by its own `count(old) == 1` check at `review-transmit-unbounded-shift`, the line S2 rewrote.
  - The author's copy changes only that anchor; I checked it by diff and by sha256 `3dddb57c…`. At the head it gives the unplanted row passing on all three binaries, and every one of the eight `review-*` plants fails `acmp_wide` and the every-sink probe.
- **Coverage.** 100 % of lines and branches after exclusions, with `src/acmp.c` at 815/815 lines and 426/426 branches. The ratchet file is unchanged.

### Docs: CLEAN

- **`docs/VERIFICATION.md`:**
  - The mutation row (`:24`) counts 448 core plants plus four generated ones, which matches the 452-entry registry and the 452 caught.
  - The 33-sink row (`:26`) names both build directories and states only what `acmp_wide` checks.
  - The conditional row describes the capacity controls exactly as the gate runs them.
- **`docs/PORTING.md:76-79` and `:329`.** The 255-sink refusal sentence is accurate, and the `release` row matches the code.
- **CHANGELOG.** The entry is accurate.
- **Generated docs.** `docs/TESTS.md` (181 declarations, 452 plants) and `docs/TRACEABILITY.md` (ACMP-09 names the four new tests) are fresh: both generator gates compare byte for byte and pass (rc 0). The anchors `#L140`, `#L170`, `#L185` and `#L1159` point at the `TEST_F` lines.
- **PR body.** Its line references (`src/acmp.c:37`, `:312`, `tests/test_acmp_wide.cpp:140/170/185`, `tests/test_acmp.cpp:1159`, `scripts/check_conditionals.py:141`) and its size and image figures match my measurements.

## Executed evidence (this review)

| Run | Result | Receipt |
|---|---|---|
| Round 1 `run_ci_steps.sh`, unchanged, on a clean clone of the head (validate `--jobs 8 --graphs` beside baremetal `--jobs 8`) | validate rc 0, 28 of 28 gates rc 0; mutation `{"CAUGHT": 452, "ESCAPED": 0, "ERROR": 0}`; coverage 100 %; all nine CTest binaries pass in the GCC and the sanitizer builds. baremetal rc 0, Debug and Release. Status empty and diff sha unchanged before and after. | `receipts/ci/` |
| Round 1 `survivors_full_ctest.sh`, unchanged | Five plants fail the full CTest; the control passes | `receipts/r811-1-survivors-*` |
| Round 1 `plants.py`, unchanged | rc 1 at its own anchor check (expected after S2) | `receipts/r811-1-plants-unchanged.*` |
| `plants.py` with only the S2 anchor changed (author's copy, byte-verified) | rc 0; eight of eight review plants fail `acmp_wide` | `receipts/r811-1-plants-s2-anchor*` |
| Escape and kill matrix for the five registered plants | Five of five OK | `receipts/escape-kill*` |
| probe_of bound, compile controls and ablations | 255 is exact; the gate fails without either assertion | `receipts/bound-probes.txt` |
| RV32 text and disassembly, `main`, round 1 and head | Round 1 and head identical at all six levels | `receipts/rv32-compare.txt` |
| Evidence integrity | Author `MANIFEST.sha256`: 133 of 133 OK. Archive `MANIFEST.json`: 450 entries, 0 mismatches against published hashes. | `receipts/evidence-verification.txt` |
| Review clone after the probes | HEAD and tree exact; status and ignored list empty; index modes and blobs equal the HEAD tree; every tracked blob re-hashes to its index entry. The repository has no submodules (no `.gitmodules`, 0 gitlinks), so no gitlink check applies. | `receipts/clone-integrity.txt` |

**Toolchain:**

- **Pinned:** GoogleTest and GMock 1.14.0, Clang 18.1.3 and clang-tidy 18.1.3, and Mermaid CLI 11.16.0.
- **From the host:** GCC 16.2.1, Clang 23.1.4, cppcheck, CMake, riscv64-elf-gcc 16.2.0 and QEMU (`receipts/ci/toolchain.txt`).

Paths in receipts are shown as `$PACKET`, `$CLONE`, `$TOOLS` and `$HOME`.

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | ACMP-09 and Milan v1.2 5.5.3.5 against W3, W4, W5 and A19A; `src/acmp.c` delta (`:37`, `:312`); object-code identity with round 1; hosted check runs at the head | R811-2 | 97414fe6518cda2bf7c4ea136fdd8bd25c860d83 |
| RTL (RV32 firmware target; no HDL here) | CLEAN | RV32I text and disassembly at 16 and 33 sinks for `-Os`, `-O2` and `-O3`; `baremetal.py` Debug and Release rc 0; Release ELF identical to round 1; imports unchanged | R811-2 | 97414fe6518cda2bf7c4ea136fdd8bd25c860d83 |
| Robustness | CLEAN | S1 bound exact (runtime probe at 254, 255 and 256); S2 type; capacity controls with gcc and clang and their ablations; index bounds; sanitizer builds | R811-2 | 97414fe6518cda2bf7c4ea136fdd8bd25c860d83 |
| Tests | CLEAN (S-1 suggestion) | `tests/test_acmp_wide.cpp` W3 to W5; `tests/test_acmp.cpp` A19A; five plants in `tests/mutations.json` (apply once, escape without killers, caught with needles); round 1 scripts at the head; 452/0/0 campaign; coverage 100 % | R811-2 | 97414fe6518cda2bf7c4ea136fdd8bd25c860d83 |
| Docs | CLEAN (S-2 suggestion) | `docs/VERIFICATION.md`, `docs/PORTING.md`, CHANGELOG, regenerated `docs/TESTS.md` and `docs/TRACEABILITY.md` (fresh by gate), PR body figures and line references, comment rule, commit format | R811-2 | 97414fe6518cda2bf7c4ea136fdd8bd25c860d83 |

## Real limits

- **No manager source bank** ran at this exact head, and I claim none. Source-head execution evidence is the author's published gate receipts plus my own runs above.
- **No physical calibration (NOT RUN).** No hardware or field run was used, and field skips are not hardware proof.
- **Not run:** Docker or act, the parent, PP, gPTP, Yosys or builder banks, and any milan-fpga image, simulation or pin move.
- **Toolchain differs from CI.** The host GCC is 16.2.1, where CI uses Ubuntu's GCC. The RISC-V cross compiler is riscv64-elf-gcc 16.2.0, where CI uses Ubuntu's gcc-riscv64-unknown-elf. The `apt-get` and `npm` install steps were not run. I ran validate with `--jobs 8` beside baremetal with `--jobs 8`.
- **Packet integrity rests on hashes.** The author packet carries no cryptographic signature; its integrity is the manifest hashes, all of which match. The `tsn31-review-evidence` branch has moved past `18c77dbe` (now `9c634ca7…`), and I used only the pinned archive.
- **R812-1's disposable 33-sink test** I did not re-run. Its three plants are the same defects as the registered `acmp-wide-release-clears-one-word`, `acmp-owed-release-not-cleared` and `acmp-wide-release-word-off-by-one`, which my escape and kill matrix covers. The author's receipt (`author-r2/receipts/reviewers/r812-wide-gaps.log`) shows the test passing unplanted with all three plants failing.
- **The Debug bare-metal image** was not compared section by section with round 1.

## Pending manager duties

- Validate the current-dev merge candidate at the merge turn (source base `ea4af6f1`, live dev `45c0b56c1f4a8a52878815fdcb1359d18e2c5b1c`): run the builder and native banks, and own hosted and act acceptance. One hosted `quality` context at the head was still in progress when queried.
- Collect the second independent review (R812-2). I did not read it.
- Note: the ruling asked for REVIEW READY to be posted on this PR. The round 2 notice appears on issue #31 (issuecomment-6760027932), and the PR body was updated.
- Merge needs two independent positive reviews and the full completion bar.

R811-2 FINISHED
