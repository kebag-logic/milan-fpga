# [A759] kebag-logic/tsn-c-stack#31 round 2 (PR #33, branch `31-acmp-mask-width`)

**Status: committed, not pushed. Head `97414fe6518cda2bf7c4ea136fdd8bd25c860d83`**, three new commits on round 1's `c6013804` (no rebase, no amend, no force). Every gate passes on a clean clone of the head (section 4). The PR body is `PR-BODY.md` ("Closes #31"). The manager pushes the branch and opens or updates the PR.

- Authority: the round 2 ruling on PR #33 (issuecomment-6756156104), items 1 to 3, on R811-1 and R812-1 (both NEGATIVE at `c6013804`).
- TAKEN: issue #31 issuecomment-6759629155 (06:14 CET). REVIEW READY: issue #31 issuecomment-6760027932 (06:42 CET), as the lane brief says. The ruling's last line asks for it on the PR; the manager may relay it there.
- STOP condition (a change to `src/` or `include/` beyond S1 and S2, or a public API change): not met. The only core lines changed are S1 (`src/acmp.c:37`) and S2 (`src/acmp.c:312`). No function, callback, configuration, view, counter or field changes. RV32 object code is byte-identical to round 1 (section 5).
- Receipts: `receipts/` (`gates/` the clean-clone CI run, `reviewers/` both reviewers' scripts at the new head, `probes/` the escape matrix, the variant probe, sizes and the refusal controls, `steps/` the per-commit checks, `scripts/` every runner). `$SCRATCH`, `$TOOLS`, `$LANES`, `$HOME` and `$NODE_BIN` stand for the host paths they replaced. One file over 200 KB is listed by SHA-256 in `receipts/not-copied.txt`.

Commits (one-line subjects, no body, configured identity):

| Commit | Subject |
|---|---|
| `6a81006` | Refuse an ACMP build of more than 255 sinks, which the owed probe_of cannot name, and shift an explicit-width one into the owed release mask (#31) |
| `a7fb45d` | Assert that sinks 31 and 32 at 33 sinks wait only behind their own owed responses and that a probe owed in a reused slot holds no sink at 33 and 16 sinks, and plant the five mask defects that escaped (#31) |
| `97414fe` | Compile the owed storage refusals in the conditional gate: one release word refused at 33 sinks and accepted at 32, and probe_of refused at 256 sinks and accepted at 255 (#31) |

## 1. Changes (file:line at `97414fe`)

| File:line | Change | Ruling item |
|---|---|---|
| `src/acmp.c:37` | `_Static_assert(ACMP_MAX_SINKS <= UINT8_MAX, "the owed probe_of names one plus the index of every sink");` | 3, S1. `probe_of` stores `k + 1u` in a `uint8_t` (`:309`), so 255 sinks is the exact bound: sink 254 is named 255. R812-1 S3 proposed `<= 254u`, which would also refuse 255 sinks that the field can name. `probe_of` is the only store that narrows a sink index (every `(uint8_t)` cast in `src/acmp.c` checked) |
| `src/acmp.c:312` | `o->release[...] = UINT32_C(1) << ((release - 1u) % 32u);` | 3, S2. The disassembly is unchanged at `-Os`, `-O2` and `-O3` |
| `tests/test_acmp_wide.cpp:21` | `kWordEnd`, sink 31, the last bit of word 0 | 1 |
| `tests/test_acmp_wide.cpp:46-96` | fixture helpers: `command` (any listener command; `bind` now calls it), `owed_changes` (the sum of every sink's `change_owed`), `probe_in_the_slot_of` (owe a sink's response and probe, send both, then owe a GET_RX_STATE response and three bindings, so that sink 3's probe falls in the slot the response used), `drain` | 1 |
| `tests/test_acmp_wide.cpp:140` | `AcmpWide.SinksThirtyOneAndThirtyTwoWaitOnlyForTheirOwnResponses` (W3) | 1, word boundary |
| `tests/test_acmp_wide.cpp:170` | `AcmpWide.ProbeInTheSlotOfSinkThirtyOnesResponseHoldsNoSink` (W4, word 0) | 1, slot reuse at 33 |
| `tests/test_acmp_wide.cpp:185` | `AcmpWide.ProbeInTheSlotOfSinkThirtyTwosResponseHoldsNoSink` (W5, word 1) | 1, slot reuse at 33 |
| `tests/test_acmp.cpp:145` | `AcmpCore::owed_changes` | 1 |
| `tests/test_acmp.cpp:1159` | `AcmpCore.A19AProbeInTheSlotOfAnEarlierResponseHoldsNoSink`: the entity re-initialised with all 16 sinks; the last sink's slot reused by sink 3's probe | 1, slot reuse at 16 |
| `tests/mutations.json:6962-7080` | five new plants (section 2), placed after the round 1 `acmp-wide-*` plants and before the wire and entity plants | 1 |
| `tests/mutations.json:6904-6905` | `acmp-wide-release-word-ignored` follows S2's text, with the same defect (word 0) | 3 (S2 moved its anchor) |
| `scripts/check_conditionals.py:138-172` | `capacity_controls`, run by `--selftest` (the `conditionals` gate): with gcc and with clang, the committed core compiles at 33 and 255 sinks and is refused at 256 by the `probe_of` assertion; with `ACMP_RELEASE_WORDS` planted to `1u`, it compiles at 32 and is refused at 33 by the mask assertion. Each refusal must name its own assertion and not the other | 3, the refusal's compile control. In an existing gate, so validate stays at 28 gates |
| `docs/VERIFICATION.md:24` | 448 core plants (443 + 5) | 1 |
| `docs/VERIFICATION.md:26` | the 33-sink row: `ctest --test-dir build-gcc -R acmp_wide` or `ctest --test-dir build-sanitize -R acmp_wide` (R812-1 F2's exact fix), and what the tests now check | 1, 2 |
| `docs/VERIFICATION.md:33` | the conditional row names the capacity controls | 3 |
| `docs/PORTING.md:79` | "So is a build of more than 255 sinks, because `probe_of` holds one plus a sink index in 8 bits." | 3, S1 |
| `docs/TESTS.md`, `docs/TRACEABILITY.md` | regenerated (`test_inventory.py --write`, `traceability.py --write`): 181 declarations, 452 plants; ACMP-09 names the four new tests | 1 |
| `CHANGELOG.md:5` | the #31 entry names the `probe_of` refusal and the new checks | |

## 2. Tests, the plants they kill, and each plant's escape without its killer

Each new plant applies to exactly one place in `src/acmp.c`. `receipts/probes/escape-matrix.log` (`scripts/escape_matrix.py`, mutation.py's flags) builds the 16-sink `acmp_tests` and the 33-sink `acmp_wide` with each plant. Each binary then runs twice: once with every registered killer filtered out, where all other tests pass (the plant escapes), and once with only the killers, which give rc 1 with every registered needle in the output. The unplanted row passes 127 and 5 tests. The full campaign catches all five (section 4).

| Plant (R811-1 name) | Change | Killer: needle | Without its killer |
|---|---|---|---|
| `acmp-wide-release-word-off-by-one` (transmit word off-by-one) | `o->release[release / 32u]` | W3: "sink 31's change waits behind its own owed response" | 127 of 127 and 4 of 4 pass |
| `acmp-wide-owed-count-word-off-by-one` (change-owed loop off-by-one) | `o->release[(k + 1u) / 32u]` in `transmit` | W3: the same, and "sink 31's response left: one change is reported"; W4: "once every owed frame left, no sink is held" (sink 31's count wraps to 255) | 127 of 127 and 3 of 3 pass |
| `acmp-wide-release-loop-word-off-by-one` (release loop off-by-one) | the same in `acmp_poll` | W3: "sink 31's response left: one change is reported"; W4: "once every owed frame left, no sink is held" | 127 of 127 and 3 of 3 pass |
| `acmp-owed-release-not-cleared` (deleted clear) | `memset(o->release, ...)` deleted | A19 (16 sinks): "the probe in that slot holds no sink: the last is free" and "a change of the last sink is reported at once"; W4: "... sink 31 is free"; W5: "... sink 32 is free" | 126 of 126 and 3 of 3 pass |
| `acmp-wide-release-clears-one-word` (one-word clear) | `sizeof o->release[0]` | W5: "the probe in that slot holds no sink: sink 32 is free" and "a change of sink 32 is reported at once" | 127 of 127 and 4 of 4 pass |

Without the five new tests, all five plants escape. The 16-sink suite runs every round 1 test there, so this matches R811-1's survivor receipts at `c6013804`. At 16 sinks the three off-by-ones and the one-word clear are equivalent mutants (`ACMP_RELEASE_WORDS` is 1); the deleted clear is live there, and A19 catches it.

Boundary evidence:
- W3 binds sink 31, then 32, with no room. Each waits behind one response, its own, and `owed_changes()` counts exactly those. Sink 31's response leaving releases sink 31 alone. Then sink 31's UNBIND_RX response is owed behind sink 32's frames. Sink 32's response leaving releases sink 32 alone while sink 31 still waits, and sink 31's unbind response then releases it. So each sink on both sides of the word boundary is held only by its own response and released only when that response leaves, in both orders.
- W4, W5 and A19 first assert that the reused slot holds sink 3's probe: `owed_count == 7`, `owed[slot].probe_of == 4`. With the slot asserted, they check three things. The probe holds no sink: only sinks 1 to 3 wait. The old sink's next change (`acmp_set_started`) is reported at once. After the drain no sink is held.
- The refusal controls in `receipts/gates/val/conditionals.log`: committed 33 and 255 compile; 256 refused, "the owed probe_of names one plus the index of every sink"; one word at 32 compiles; at 33 refused, "the owed release mask holds a bit for every sink", with gcc and clang. Negative controls (`receipts/probes/ctl-mask.log`, `ctl-probe.log`): with `src/acmp.c:35` removed, the gate fails "capacity control one-word at 33u sinks with gcc: rc 0"; with `:37` removed it fails "committed at 256u sinks with gcc: rc 0".

## 3. Reviewers' scripts at the new head

Run from the reviewers' packets, unchanged. The SHA-256 of `plants.py`, `survivors_full_ctest.sh`, `every_sink_probe.cpp`, R811-1's `env.sh`, `run_wide_gaps.sh`, `test_wide_gaps.cpp` and R812-1's `env.sh` all equal those packets' `MANIFEST.sha256`. They ran on a second clean clone at `97414fe` (`receipts/reviewers/`).

| Script | rc | Output at `97414fe` |
|---|---:|---|
| R811-1 `survivors_full_ctest.sh` | 0 | all five survivors now fail the full 9-binary CTest (rc 8): the three off-by-ones and the one-word clear fail `acmp_wide`; the deleted clear fails `acmp_tests` and `acmp_wide`. The unplanted control passes 9 of 9 (`r811-survivors.log`, per-plant `ctest.log`). At `c6013804` all five passed (R811-1's receipt) |
| R812-1 `run_wide_gaps.sh` (its disposable 33-sink test) | 0 | `none` rc 0; `memset-first-word-only` and `memset-removed` rc 1 (GAP1); `set-index-off-by-one` rc 1 (GAP2), the same as at `c6013804` (`r812-wide-gaps.log`) |
| R811-1 `plants.py`, unchanged | 1 | stops at its own check `assert text.count(old) == 1`: `AssertionError: ('review-transmit-unbounded-shift', 0)` (`r811-plants.log`). That plant's `old`, `= 1u << ((release - 1u) % 32u);`, is the line S2 (ruling item 3) rewrites to `UINT32_C(1) <<`, so no explicit-width one can keep it. The other 18 plants and the control had run. `r811-plants.collected.txt` (`scripts/collect_plants.py`) lists each one's `acmp_tests`, `acmp_wide` and every-sink outcome from the files `plants.py` left |
| the same, with that one plant's anchor following S2 | 0 | the diff is one line (`r811-plants-s2-anchor.diff`): `old` and `new` read `UINT32_C(1) <<`, the same defect. Full matrix (`r811-plants-s2-anchor.log`, `results.json`): unplanted pass, pass, pass; each of the eight `review-*` plants fails `acmp_wide` and the every-sink probe; `review-mask-not-cleared` fails `acmp_tests` too. At `c6013804` all five of R811-1's survivors passed both `acmp_tests` and `acmp_wide` (R811-1 `matrix-results.json`) |

An earlier `plants.py` start (`r811-plants.runner-fault.log`) passed `$TOOLS` as the tree. My runner kept the tree in `T`, which R811-1's `env.sh` also sets. The runner now uses `TREE_AT` (`scripts/run_reviewer_scripts.sh`). That run was not evidence.

## 4. Gates (clean clone of `97414fe`)

`git clone --no-local` of the lane, checked out detached at the head. Status and diff were empty before and after (`receipts/gates/status-*`, `diffsha-*`). `scripts/run_gates.sh` runs the CI's two testing steps concurrently, `--jobs 16`, and the full mutation campaign runs inside `validate.py`.

| Target | `run:` step | rc | Result | Wall, peak RSS |
|---|---|---:|---|---|
| Linux (hosted) | `python3 scripts/validate.py --work build-validation --jobs 16 --graphs` | 0 | 28 of 28 gates rc 0 (`gates/val/gates.json`). GCC build and CTest 9 of 9 (`acmp_wide` passed); Clang with address and undefined-behaviour sanitizers, CTest 9 of 9; coverage 100 % of lines and branches after exclusions, `src/acmp.c` 815/815 and 426/426; mutation `{"CAUGHT": 452, "ESCAPED": 0, "ERROR": 0}`; static analysis, boundary, conditionals (with the capacity controls), comments, needles, assertion templates, traceability, test inventory (181 declarations, 452 plants), port contracts, privacy, graphs rc 0 | 5 min 23 s, 454,488 kB |
| Bare metal (RV32, minimal port) | `python3 scripts/baremetal.py --work build-rv32 --jobs 16` | 0 | Debug and Release rc 0, no unresolved final symbols, the QEMU smoke run passes; core imports equal to round 1's and `main`'s (Release `__umodsi3`, `ctrl_reentry_assert`, `memcpy`, `memset`) (`gates/rv32/results.json`) | 1.5 s, 145,976 kB |

The install steps (`apt-get`, `npm`) were not run. The pinned toolchain stood in for them: GoogleTest and GMock 1.14.0, Clang 18.1.3 (`clang-18`, the lexer), clang-tidy 18.1.3 and Mermaid CLI 11.16.0, copied into scratch. GCC 16.2.1, Clang 23.1.4 (the sanitizer build's `clang`), cppcheck, CMake, riscv64-elf-gcc 16.2.0 and QEMU are the host's.

Per-commit checks (`receipts/steps/`). `6a81006`: CTest 9 of 9; `acmp-wide-release-word-ignored` caught at S2's text; test inventory and port contracts rc 0. `a7fb45d`: CTest 9 of 9; test inventory, traceability and needles rc 0. Its plants were caught in the selected runs during development. `97414fe`: the conditional gate with the capacity controls rc 0 (`probes/cond-dev.log`). The full gates ran once, on the final head.

## 5. Size

RV32I text of `src/acmp.c` at the default 16 sinks, riscv64-elf-gcc 16.2.0, `-march=rv32i -mabi=ilp32 -ffreestanding -fno-builtin -nostdinc -std=c11 -DNDEBUG -DCTRL_REENTRY_ASSERT` (`receipts/probes/rv32-text.log`, `scripts/rv32_text.sh`):

| Flags | `main` `ea4af6f` | round 1 `c6013804` | this head | R812-1 S1 variant on this head |
|---|---:|---:|---:|---:|
| `-Os` | 10,825 B | 10,921 B | 10,921 B | 10,861 B (−60) |
| `-O2` | 16,029 B | 16,141 B | 16,141 B | 16,081 B (−60) |
| `-O3` | 19,365 B | 20,365 B | 20,365 B | 19,133 B (−1,232) |

The head's disassembly equals round 1's at all three levels. S1 is a build-time assertion, and `UINT32_C(1)` is the same constant.

Bare-metal image (`scripts/baremetal.py`, `rv32_smoke.elf`; `receipts/probes/image-sizes.txt`):

| Image | `main` | round 1 (before) | this head (after) |
|---|---|---|---|
| Release, text + data + bss | 40,669 + 0 + 65,552 | 41,645 + 0 + 65,552 | 41,645 + 0 + 65,552 |
| Release ELF | 50,504 B | 51,480 B, SHA-256 `a7a2b614…` | 51,480 B, SHA-256 `a7a2b614…` (byte-identical) |
| Debug, text + data + bss | 51,860 + 0 + 65,552 | 51,964 + 0 + 65,552 | 51,964 + 0 + 65,552 (`.text` identical) |

The Debug ELF file size differs by run directory (150,684 B before, 150,616 B after) because its debug information holds the build path; the loaded sections are equal.

**R812-1 S1 (increment the released sink directly in `transmit`): measured, not taken.** At `-Os` it does not grow: 10,921 to 10,861 B (−60), with −60 B at `-O2` and −1,232 B at `-O3`. The ruling allows it "only if" `-Os` does not grow, and I did not take it, for two reasons:
- It deletes the change-owed loop. Ruling item 1 requires that loop's off-by-one as a registered plant (`acmp-wide-owed-count-word-off-by-one`), and R811-1's `plants.py` and `survivors_full_ctest.sh` plant into it. With the loop gone, that plant could not exist, and two more of the scripts' plants could not apply.
- The hold and the release would no longer read the same stored bits. `receipts/probes/variant-wrap.log` (`scripts/variant_wrap_probe.sh`) runs the three slot-reuse tests against four cores. With the clear deleted, the head holds the stale sink only while the probe in its old slot is owed: the hold and release stay paired, and the tests catch it at once. The variant with the same deleted clear never holds that sink, but when the probe leaves it decrements the sink's count from 0, which wraps to 255 ("once every owed frame left, no sink is held: 255" in A19, W4 and W5). Every later change of that sink would then be held. Both cores pass all three tests without the plant.

## 6. Residue (ruling item 2)

- The PR body's size table names its compiler and flags (`PR-BODY.md`, round 2 and round 1 Size sections).
- The 33-sink command names both build directories (`docs/VERIFICATION.md:26`).

## 7. Real limits

- The CTest builds used the host's GCC 16.2.1 and Clang 23.1.4, not the CI image's GCC 13 and Clang 18. Clang 18.1.3 ran the comment and assertion lexing. The hosted jobs at this head are the manager's after the push.
- The size figures are riscv64-elf-gcc 16.2.0's. The CI's Ubuntu cross compiler may differ.
- No hardware, bench, act replay or milan-fpga build was run. The 33-sink path is host-tested only.

## 8. Run history (CET, 2026-11-10)

- 06:10 start; branch confirmed at `c6013804`. 06:14 TAKEN.
- 06:15 to 06:22 read the ruling, both reviews and their scripts; baseline sizes reproduce round 1's.
- 06:22 S1 and S2; refusal checks at 16, 33, 255 and 256 with gcc and clang; the R812-1 S1 variant measured.
- 06:24 to 06:29 the four tests and five plants. The selected campaign caught all eight `acmp-wide`/`acmp-owed` plants. The first escape matrix found W4 also catching the two loop off-by-ones, so W4 was registered as a second killer of each; matrix rc 0. Capacity controls and their negative controls. Variant wrap probe.
- 06:30 to 06:32 commits `6a81006`, `a7fb45d` and `97414fe`, each after its checks.
- 06:32 to 06:38 clean-clone gates: validate rc 0 (28 of 28, mutation 452/0/0) and baremetal rc 0, concurrently with both reviewers' scripts, the escape matrix and the probes at the head.
- 06:38 to 06:42 receipts, HANDOFF, PR body; 06:42 REVIEW READY posted with the head.
