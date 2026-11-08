# [A750c] HANDOFF: tsn-c-stack issue #26 (ACMP owed bound), round 3: sync with main

Status: **STOP** at 13dd785ba2b9b5bec9e93afebfce3db9921d2786.

The merge itself is complete and clean. 27 of the 28 `validate.py` gates return 0 on a clean clone of the merge
head. `baremetal.py` Debug and Release both return 0. The mutation campaign is 417/417 CAUGHT, with both sides'
plants.

One gate fails: `privacy` returns rc 1 on main's own merge commit d7e6a2a1. GitHub created that commit with a
two-paragraph message, and the gate requires one-line messages on every reachable commit. main's CI is red for the
same reason (run 42467930308, `quality` job, `privacy: rc 1`). Every descendant of d7e6a2a1 fails this gate, so no
sync of this branch can pass it. A fix needs a change to `scripts/check_privacy.py` or to main's history. Both are
outside this round ("change nothing else"), so I stopped rather than report REVIEW READY.

- Repository: kebag-logic/tsn-c-stack, PR #28, branch `26-acmp-owed`.
- Round 2 head: 9002bfec5b135da4c0e11892464f509f725feb1f (pushed).
- main: d7e6a2a19a57a8277cd26042557a8c99f2ee5496 (PR #29, issue #27).
- Merge commit: 13dd785ba2b9b5bec9e93afebfce3db9921d2786.
  - Parents: 9002bfe (first) and d7e6a2a1.
  - Made with `git fetch origin` then `git merge --no-ff origin/main`. No rebase, force or amend.
  - Author and committer: hackerman-kl <hackerman-kl@kebag-logic.com>.
  - One-line subject "Merge origin/main d7e6a2a1 into 26-acmp-owed", with no body and no trailers.
- Not pushed; no PR opened or edited. PR text: `PR-BODY.md` (first line "[A750c]", "Relates to #26").
- Issue #26: "[A750c] TAKEN" posted at the start; "[A750c] STOP 13dd785ba2b9b5bec9e93afebfce3db9921d2786" posted at the end.
- No core change. `src/` and `include/acmp.h` match round 2; `include/wire.h` comes from main unchanged.

## What the merge brings in

`git diff 9002bfe 13dd785` contains exactly main's change, plus the regenerated outputs below. It touches the same
8 files, with 76 insertions and 7 deletions:

- `include/wire.h`: `wire_put_be` in two 32-bit halves.
- `scripts/mutation.py`: header-only plants build the module of their kill's arm.
- `tests/mutations.json`: two new plants, `wire-put-be-skips-an-odd-field-first-byte` and
  `wire-put-be-writes-past-an-odd-field`.
- `tests/test_acmp.cpp:2893`: `Wire.W1PutBeWritesTheLowBytesMostSignificantFirst`. Git placed it after the AcmpOwed
  tests at file scope, as on main.
- `docs/VERIFICATION.md:196`: the header-plant sentence.
- The regenerated outputs: `docs/TESTS.md`, `docs/TRACEABILITY.md` and `tests/coverage.ratchet`.

## Conflicts and resolutions

| File | Conflict | Resolution |
|---|---|---|
| `docs/VERIFICATION.md:24` (mutation row) | HEAD "All 411 core plants", main "All 386 core plants". | "All 413 core plants and four generated configuration plants": 411 on this branch plus main's two `wire-put-be-*` plants. `tests/mutations.json` merged without conflict to 417 plants: 413 core (277 `src/acmp.c`, 71 `src/maap.c`, 48 `src/adp.c`, 10 `include/acmp.h`, 5 `include/maap.h`, 2 `include/wire.h`) and 4 generated configuration. No script checks this sentence, so it is the only hand-resolved line. |
| `docs/TRACEABILITY.md:16-17` (ACMP-02 and ACMP-03 rows) | HEAD's rows have line anchors shifted by the AcmpOwed tests. main's ACMP-02 row adds `Wire.W1…#L2562`. | Generated. I took HEAD's side to clear the markers, then ran `python3 scripts/traceability.py --write`, which rewrote the file. ACMP-02 now lists `Wire.W1PutBeWritesTheLowBytesMostSignificantFirst` at `#L2893`. Summary: 46 requirements, 159 test declarations. |
| `tests/coverage.ratchet:4-5` | HEAD `wire.h 10/10`, `acmp.c 795/795, 402/402`. main `wire.h 14/14`, `acmp.c 792/792, 392/392`. | Generated in the CI environment. I took main's side as the input floor, then ran `python3 scripts/coverage.py <build> --write` in the Ubuntu 24.04 CI image. Result: `include/wire.h lines 14/14 branches 2/2` and `src/acmp.c lines 795/795 branches 402/402`; adp.c and maap.c are unchanged. See below. |
| `docs/TESTS.md:170` (no textual conflict) | Git auto-merged main's new row with a stale anchor, `#L2562`. In the merged file the test is at line 2893. | Generated: `python3 scripts/test_inventory.py --write` corrected it to `#L2893`. Summary: 159 declarations, 417 plants. Without the regeneration, the `test-inventory` gate would fail. |

Generated-file sha256 at the merge head:

- `tests/coverage.ratchet`: `aacd6f19630ed643ef7ddd45a29e27654df5511a30b5e4e858fe8c3107cdab57`. Identical to the
  file the CI image wrote.
- `docs/TESTS.md`: `bc7a4c7a1be411ae34d37505b079ba7efc55482abae10710bf47f0cf022405bc`.
- `docs/TRACEABILITY.md`: `c5b18ceab0b75d3c2f8141de3d436ec28098b19ca47068741f0d628682036454`.

Other generated files did not change on either side, and their gates pass: `scripts/assertion-defaults.json`
(assertion-templates), the REQUIREMENTS tables (traceability) and the graphs.

### Coverage ratchet in the CI environment

- Image: local `697c-r6-ci` (Ubuntu 24.04). It has GCC 13.3.0, CMake 3.28.3 and `libgtest-dev` 1.14.0-1, the same
  packages CI's `ubuntu-24.04` job installs. It ran with `--network=none` on an exact export of the merged working tree.
- Script: `cov-ci.sh`. It runs:

  ```sh
  cmake -S . -B /b -DTSN_COVERAGE=ON -DCMAKE_BUILD_TYPE=Debug
  cmake --build /b -j16
  ctest --test-dir /b --output-on-failure -j16
  python3 scripts/coverage.py /b --write
  ```

- All 8 tests passed and the result is 100% after exclusions. Log: `coverage-ci.log`.
- The `coverage` gate on the clean clone (host GCC 16.2.1) then checked the same ratchet: rc 0.

## Gate table (clean clone of 13dd785, Linux hosted and bare-metal RV32)

- Clone: a fresh `git clone` of the branch at 13dd785. `git status` was empty before and after every run.
- Toolchain:
  - GoogleTest/GMock 1.14.0 from the pinned prefix.
  - Host GCC 16.2.1 and the host Clang for the hosted builds.
  - Clang 18.1.3 from `$VALIDATION_TOOLS/clang-18/bin` and clang-tidy 18.1.3 from `$VALIDATION_TOOLS/clang-tidy-18/bin`,
    both first on PATH.
  - Mermaid CLI 11.16.0, the CI pin, installed in scratch with `npm ci`. Node 22.11.0 and Puppeteer's browser
    cache are also in scratch.
- Runs:
  - Run A: `python3 scripts/validate.py --work <scratch>/val-merge --jobs 16 --graphs`, alongside
    `python3 scripts/baremetal.py --work <scratch>/rv32-merge --jobs 8`. validate.py stops after its 17 source and
    metadata gates when any of them fails, so `privacy` rc 1 skipped the build, mutation and graph gates.
  - Run B (diagnostic): the clone's own `scripts/validate.py`, with only its `('privacy', 'check_privacy.py', [])`
    entry removed, so every other gate runs. Wrapper: `validate_minus_privacy.py`. It reads the file, asserts the
    exact text once, and execs it with the clone as ROOT. The clone was not modified.

| Gate | Run A | Run B | Scope |
|---|---|---|---|
| entity-golden, entity-controls | 0, 0 | 0, 0 | Shared |
| boundary, dependencies | 0, 0 | 0, 0 | Hosted |
| needles, assertion-templates | 0, 0 | 0, 0 | Assertion contract |
| comments | 0 | 0 | Comment contract, including the RV32 cross-compiled controls |
| conditionals | 0 | 0 | Conditional matrix |
| port-contracts | 0 | 0 | |
| acmp-cache, registration-controls, license | 0, 0, 0 | 0, 0, 0 | |
| traceability, test-inventory | 0, 0 | 0, 0 | 46 requirements, 159 declarations, 417 plants |
| coverage-controls, privacy-selftest | 0, 0 | 0, 0 | |
| **privacy** | **1** | not run | `d7e6a2a19a57…: commit message must be one line` |
| gcc configure / build / test | skipped | 0 / 0 / 0 | |
| coverage | skipped | 0 | wire.h 14/14, acmp.c 795/795 lines and 402/402 branches |
| clang-sanitizers configure / build / test | skipped | 0 / 0 / 0 | ASan, UBSan, leaks |
| static-analysis | skipped | 0 | clang-tidy 18.1.3 and cppcheck |
| mutation | skipped | 0 | 417 CAUGHT, 0 ESCAPED, 0 ERROR |
| mutation-controls | skipped | 0 | |
| graphs | skipped | 0 | 4 rendered |
| `baremetal.py` Debug | rc 0 | | RV32I ILP32 freestanding link and QEMU smoke, including `acmp_owed_smoke` |
| `baremetal.py` Release | rc 0 | | Same, -O3 |

The privacy failure is inherited:

- `scripts/check_privacy.py` on 9002bfe (round 2 head): rc 0, "18 commits, 295 historical blobs, 98 current files; pass".
- `scripts/check_privacy.py` on d7e6a2a1 (main alone): rc 1, the same message.
- main's CI run 42467930308 at d7e6a2a1: the `quality` job fails at `privacy: rc 1`.
- Cause: the message has a body line, "Pack wire_put_be as two 32-bit halves, no 64-bit shift per byte on 32-bit
  cores (#27)". Author and committer are the allowed web-flow pair; only the line count fails. The gate already has
  an exact-commit exception for one earlier owner squash (`OWNER_SQUASH`). The merge's content scan passes.
- Suggested fix, a main-side change under its own issue: extend that exact-commit exception to d7e6a2a1. Then sync
  this branch again. No branch change is needed.

Mutation campaign:

- Every plant registered on either side is caught, including:
  - Round 2's plants: `owed-ready-one-slot`, `owed-bind-one-slot`, `owed-bind-owes-one`,
    `owed-bind-answer-lost-after-decline` and `owed-get-tx-state-answer-lost-after-decline`.
  - main's plants: `wire-put-be-skips-an-odd-field-first-byte` and `wire-put-be-writes-past-an-odd-field`.
- Round 2: 415/415. Merge: 417/417.
- Tests and their kills are unchanged from round 2 (round 2 HANDOFF, "Tests and the planted mutants they kill").
  The merge adds no ACMP test. Main's Wire test kills main's two plants.

Receipts: `merge-gates.json`, `merge-privacy.log` and `merge-rv32-results.json` (Run A); `rest-gates.json` and
`rest-mutation-summary.txt` (Run B).

## Bare-metal image size, memory and cost (moved, because of main's `wire_put_be`)

### Image (`scripts/baremetal.py`, `rv32_smoke.elf`)

Round 2 9002bfe, main d7e6a2a1 and the merge 13dd785 were each exported with `git archive` and built at paths of equal
length (`xt-r2`, `xt-mn`, `xt-mg`), so the Debug sizes compare fairly. Script: `measure/imgx.sh` and `measure/imgsize.sh`.

| Build | Round 2 9002bfe | main d7e6a2a1 | Merge 13dd785 |
|---|---|---|---|
| Release ELF bytes | 48152 | 47352 | 48952 |
| Release `.text` | 36392 | 35652 | 37188 |
| Release `acmp.c` object text | 18537 | 18413 | 18897 |
| Debug ELF bytes | 145180 | 141796 | 145492 |
| Debug `.text` | 47608 | 45380 | 47528 |
| Debug `acmp.c` object text | 20917 | 20713 | 20901 |

Notes:

- `.rodata` is 1961 (Release) and 2048 (Debug); `.bss` is 8. Neither changes.
- Release, round 2 → merge: +800 ELF bytes and +796 `.text`. Of that, +360 is the `acmp.c` object: -O3 inlines the
  two-half `wire_put_be`. main grew by the same order: 46552 → 47352 Release ELF bytes from 70936b7 to d7e6a2a1.
- Debug, round 2 → merge: −80 `.text`.
- Split-firmware flags (`-march=rv32im -Os`), `acmp.c` object text: round 2 10685, main 10617, merge 10605.
- Release ELF sha256:
  - Round 2: `a908542f5ae6c8a043f09f6884e37f7ba4709a62b2b67e02170ba29507be3f41`. Byte-identical to round 2's receipt,
    so the build reproduces.
  - Merge: `71c3bde3353ee62ee322483a884f6c3070f1191d19b425cf95770e4e5414f93a`. The same from the export and from
    the clean-clone gate build.
- Debug ELF sha256 (merge, clean-clone gate build): `9fa852fbb264a05703d688a3c4a68738f8ce8a3368d81a00a0ee38495bb251ca`,
  145496 bytes. Its debug information records the clone path.
- Full table with sha256s: `measure/sizes-and-images.txt`.

### Memory (unchanged)

The owed set is 8 × 80 = 640 bytes on both targets. `sizeof(struct acmp)` is 5064 bytes on RV32 and 5072 bytes on
x86-64. It is the same at round 2 and at the merge (`measure/sizes-run.sh`, `measure/sizes.c`).

### Record path cost

The harness is round 2's `measure/measure.c` and `measure/build.sh`, byte-identical. It counts RV32 instructions
retired under QEMU `virt` with `-icount shift=0`; a CSR read pair costs 1. Configuration: 16 sinks, 16 sources and
1 interface, with stub ports.

- The round 2 rerun reproduces round 2's receipts exactly, both outputs and both ELF sha256s.
- main is built without `-DLANE` because it has no `acmp_rx_ready`.

| Step | rv32i -O3: round 2 | main d7e6a2a1 | merge | rv32im -Os: round 2 | main d7e6a2a1 | merge |
|---|---:|---:|---:|---:|---:|---:|
| **Worst `acmp_rx` step**: BIND_RX behind 6 owed | 7904 | 8039 | **8061** | 24383 | 22251 | **22260** |
| BIND_RX sent directly | 7419 | 7554 | 7576 | 23798 | 21666 | 21675 |
| BIND_RX behind 7 owed | 200 (declined) | 7783 (probe lost) | 200 (declined) | 348 | 21637 | 348 |
| GET_RX_STATE sent directly | 6274 | 6317 | 6341 | 19766 | 18817 | 18825 |
| GET_RX_STATE behind 7 owed | 6645 | 6688 | 6712 | 20392 | 19443 | 19451 |
| A command behind the full owed set | 200 | 5408 (dropped) | 200 | 348 | 16522 | 348 |
| PROBE_TX behind the full owed set | 196 | 5404 | 196 | 341 | 16518 | 341 |
| PROBE_TX sent directly | 6469 | 6512 | 6536 | 20262 | 19314 | 19321 |
| `acmp_poll`, one owed frame | 5436 | 5436 | 5436 | 16454 | 16454 | 16454 |
| `acmp_rx_ready` | 10 | n/a | 10 | 10 | n/a | 10 |

- Every send path moves by main's change only.
- rv32i -O3: +67 per sent frame, and +157 for a BIND_RX, which sends two.
- rv32im -Os: −941 per frame and −2123 for a BIND_RX, because no byte calls the 64-bit shift helper.
- The decline paths, `acmp_poll` and `acmp_rx_ready` do not move.
- Raw outputs: `measure/{r2,mn,mg}-{release,split}-result.txt`.

Measurement ELF sha256:

| Build | Round 2 | main d7e6a2a1 | Merge |
|---|---|---|---|
| rv32i -O3 | e2ff8cc874cd87c77855351fd0d1e217d4e11826456c094898ba7dd59cafa70a | c33d9906342990ad1694b830eebb4cc8440198d0bc062c30aca4edaf626e718d | 2e5cddf3fd3a5ab1b089058d17ebd339cf73a2aea6ef2c63cd9d36325c3bede8 |
| rv32im -Os | d8a12bf98c20c26f7fc7ab0579e852196fae2467322ae73e989c0a600a03993f | 37ed5d29e27cc85489e92393f2f37b15eeb347d2a5a9d54582f00cd392b86bab | bf5450416f61bcc71b6d2889a94fe4e33324713daefed34ad2056902476e1158 |

## Acceptance items (issue #26)

Unchanged from round 2: three items are met in this repository. milan-fpga's harness row is not met here; it needs
the parent firmware to adopt this change. Hence "Relates to #26".

## Environment notes

- Scratch: `$VALIDATION_STORAGE/tsn26-a750c/`. It holds the clean clone (`clone`), exports (`xt-*`), the CI-image
  coverage tree (`covtree`), Node, the Mermaid CLI and Puppeteer's cache.
- The output directory holds only text receipts and scripts, all under 200 KB.
- Memory: the unit's MemoryPeak, including page cache, was 7.3 GB, against the 12 GB cap. Run B ran alongside the
  image export builds.
- The lane's ignored `build-registration/` predates this session and was left alone. Generator builds used scratch.
