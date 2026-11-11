# [A683zf] kebag-logic/tsn-c-stack#32: the merge of `main` into the changed-sink walk (DONOR HANDOFF, round 26)

**Status: committed, not pushed. Head `9043b926532dc4ffb57218ee0eebca7564262289`** on branch `32-acmp-dirty-walk` in the donor clone (`<lanes>/tsn-c-stack-32-walk`): `fa31d4c8` (round 25's draft), the merge commit `dd8b026f` of `origin/main` `9deb0dd` (`Merge pull request #33`, the #31 mask work), and `9043b926` on it. No rebase. The PR body is `DONOR-PR-BODY.md` ("Closes #32", the stack's own issue). The manager pushes the branch and opens the PR.

- Authority: the round 26 ruling on milan-fpga #665 (issuecomment-6779973927), item 1.
- Receipts: `receipts/donor/` (`gates/` the clean-clone CI run at `9043b926`, `gates-dd8b026/` the first run at the merge commit, `bench/` the host benchmark, `scripts/` the runners and the plant table's merge script). `<scratch>`, `<lanes>`, `<tools>` and `<home>` stand for the host paths they replaced.

## 1. The merge (`dd8b026f`, then `9043b926`)

`git merge --no-ff origin/main` left ten files in conflict. Each resolution:

| File | Conflict | Resolution |
|---|---|---|
| `src/acmp.c` | `acmp_poll`'s release loop: #31 reads each sink's bit from its word (`o->release[k / 32u] >> (k % 32u)`); the walk decrements and marks only the released sinks | both: `if (((o->release[k / 32u] >> (k % 32u)) & 1u) != 0u) { mark(a, k); a->sinks[k].change_owed--; }`. Every other hunk merged by git; the walk's diff against `main` is the drafted one but for that line (compared line by line) |
| `include/acmp.h` | `ACMP_RELEASE_WORDS` (#31) and `ACMP_DIRTY_WORDS` (#32) on one line | both |
| `CMakeLists.txt` | both added a 33-sink library with the same definition and sanitizers (`tsn_wide`, `tsn_walk`) | one, `tsn_wide`, linked by both `acmp_wide` and `acmp_walk` |
| `scripts/mutation.py` | both added a 33-sink arm and its flags (`WIDE`, `WALK`) | one list, `WIDE`, for both arms |
| `tests/mutations.json` | both appended plants; two plants changed on both sides | merged by plant name (`scripts/merge_mutations.py`): `acmp-unbind-srp-after-response` (the walk's `mark` with #31's `k + 1u` release argument) and `acmp-first-owed-releases-every-change` (the walk's loop with #31's word read) by hand; #31's `acmp-wide-release-loop-word-ignored` and `acmp-wide-release-loop-word-off-by-one` re-anchored on the merged loop line, the same defects. 470 plants, each anchored once |
| `CHANGELOG.md`, `docs/VERIFICATION.md` | both entries | both; 466 core plants |
| `docs/TESTS.md`, `docs/TRACEABILITY.md` | generated | regenerated (`test_inventory.py --write`, `traceability.py --write`) |

The first clean-clone CI run, at `dd8b026f`, failed `entity-controls` (`gates-dd8b026/entity-controls.log`): `entity_selftest.py` reads the plant table's last three plants as the entity plants, and the merge had appended the walk's plants after them. `9043b926` puts the walk's plants after #31's and before the wire and entity plants; both parents' plant orders are kept (checked plant by plant).

## 2. Gates (clean clone of `9043b926`)

`git clone --no-local` of the donor clone, detached at the head; status empty before and after (`gates/before.txt`, `after.txt`). `scripts/tsn_ci.sh` runs the CI's two testing steps, `--jobs 12`:

| `run:` step | rc | Result |
|---|---:|---|
| Install host dependencies | not run | the host is not the CI image: the pinned GoogleTest/GMock 1.14.0, Clang 18.1.3 and clang-tidy 18.1.3 stand in |
| `python3 scripts/validate.py --work build-validation --jobs 16 --graphs` (run with `--jobs 12`) | 0 | 28 of 28 gates rc 0 (`gates/gates.json`): mutation `{"CAUGHT": 470, "ESCAPED": 0, "ERROR": 0}` (the full results by SHA-256 in `gates/not-copied.txt`); coverage 100 % lines and branches after exclusions, `src/acmp.c` 847/847 and 436/436; GCC and Clang-sanitizer CTest 10 of 10 each, `acmp_walk` 4 of 4 (1, 8, 32 and 33 sinks); static analysis, boundary, conditionals, comments, needles, traceability, test inventory, privacy and graphs rc 0. 224 s |
| Install RV32 dependencies | not run | the host's RISC-V GCC and QEMU |
| `python3 scripts/baremetal.py --work build-rv32 --jobs 16` (run with `--jobs 12`) | 0 | Debug and Release rc 0 (`gates/rv32-results.json`); the core imports equal `main`'s at `9deb0dd` (`gates/rv32-results-main.json`): Debug `__mulsi3`, `__umodsi3`, `ctrl_reentry_assert`, `memcpy`, `memset`, `port_assert_failed`; Release `__umodsi3`, `ctrl_reentry_assert`, `memcpy`, `memset` |

The differential test (`AcmpWalk.OneSinkMatchesTheFullWalk`, `EightSinksMatchTheFullWalk`, `ThirtyTwoSinksMatchTheFullWalk`, `ThirtyThreeSinksMatchTheFullWalk`) passes in both CTest builds; the campaign holds its 18 plants among the 470.

Host benchmark (`bench/bench_finish.c`, `bench/bench.txt`): x86 TSC cycles, median of 200,000 `acmp_set_started` entries on one of `n` bound sinks, a core at `ACMP_MAX_SINKS=32u`, pinned to one CPU, `main` `9deb0dd` against the head:

| Sinks | `main` -O2 | head -O2 | `main` -Os | head -Os |
|---:|---:|---:|---:|---:|
| 8 | 558 | 124 | 961 | 217 |
| 32 | 2,294 | 279 | 3,844 | 465 |

## 3. At milan-fpga's pin (scratch only; the pin does not move)

The merged head's `src/acmp.c` and `include/acmp.h` diff against `main` (`git diff origin/main 9043b92`, 228 lines) applied to milan-fpga's pin `70936b77` by `git apply --3way` conflicts only where #31 is not at the pin: the release loop's word read and `ACMP_RELEASE_WORDS`. Resolved in #32's terms at the pin (the pin's one-word mask), the two files are byte-identical to round 25's port of `fa31d4c8` (SHA-256 `60952eea...` and `6c710bdf...`, `cmp` equal to round 25's measurement clones' stacks). So the "with tsn-c-stack#32" column round 25 measured is the merged head's; round 26 measures it again only for the costs its own firmware changes move (milan-fpga HANDOFF, section 4).

## 4. Run history

- 2026-11-10 22:5x CET: `git fetch origin`; `main` at `9deb0dd`, five commits past `ea4af6f`; `git merge --no-ff --no-commit origin/main`: ten files in conflict, resolved (section 1); the stack's ten CTest binaries pass on the working tree; committed `dd8b026f`.
- 22:5x: the clean-clone CI run at `dd8b026f`: `entity-controls` rc 1 (the plant order); `9043b926` commits the order; the clean-clone CI run at `9043b926`: both steps rc 0.
- 23:0x: the host benchmark at `main` and the head; the port to the pin compared.
