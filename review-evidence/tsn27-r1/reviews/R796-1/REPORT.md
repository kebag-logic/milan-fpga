[R796] NEGATIVE - exact head c687810b74b53b69c1fbdff7bfd0ec9da94eaa78

External independent review R796-1 of kebag-logic/tsn-c-stack PR #29 (issue #27). Tree 20c8786758807efef217f6db8dc97158a5fa8a95, one commit on base 70936b77dc41981e192438388cd0aced69954f18. Review start: https://github.com/kebag-logic/tsn-c-stack/pull/29#issuecomment-6719702437.

**Summary.** The source change is correct and complete at this head. `wire_put_be` is bit-exact with the byte form, no `__lshrdi3` reference remains at `-Os`, and W1 is a strong test. Both new plants are caught only by W1. The `scripts/mutation.py` change works, and so does its new ERROR path. The ratchet matches the CI measurement, and both hosted targets pass at this exact head.

One MINOR finding keeps the verdict NEGATIVE (F1). The PR body's figures for this repository's own RV32 smoke images come from a host toolchain it does not name. The pinned CI toolchain at this head gives a different Release growth: +928 B instead of the +796 B quoted. The fix is a PR-body edit only. No source change or new head is needed.

## Reconstruction (order followed)

1. `CONTRIBUTING.md` (there is no `AGENTS.md`), `docs/VERIFICATION.md`, `docs/PORTING.md` (wire preconditions at `:388-391`), `docs/TESTS.md`, `docs/TRACEABILITY.md`, `docs/REQUIREMENTS.md` (ACMP-02).
2. Issue #27: body (Change and Acceptance lists) and its two comments (TAKEN, REVIEW READY). There are no other maintainer scope decisions on the issue.
3. `git diff 70936b77..c687810b` (8 files, +76/-7) and history. The commit has a one-line subject, no body and no trailers. Author and committer are identical.
4. Public evidence: milan-fpga `d40afd2b…/review-evidence/tsn27-r1` (51 blobs, each blob id rechecked with `git hash-object`; `receipts/evidence-blobs-verified.txt`). Hosted CI artifacts were downloaded read-only for both exact-head runs and for the base run.
5. Prior public review findings on PR #29: read only after my own pass. There are none. PR #29 has no reviews and no inline comments. Its two issue comments are review-start notices (R795-1, R796-1). Nothing needs to be resolved or retained.

## Acceptance items of #27, checked one by one

| # | Item | Result | Evidence |
|---|---|---|---|
| 1 | Bit-exact for widths 1 to 8. W1 uses values whose halves differ in every crossing byte and checks the bytes before and after the field | **Met.** `include/wire.h:38-47` uses only 32-bit shifts. 37,748,826 comparisons per build (widths 0 to 8, 10 edge values and 2^22 pseudo-random values, guard bytes on both sides) gave 0 mismatches under host gcc, host clang and the pinned Clang 18, each at -O0/-O2/-Os/-O3 (gcc and host clang with UBSan). W1 (`tests/test_acmp.cpp:2561-2580`) has five values, a fatal oracle check that byte k of the high half differs from byte k of the low half (k=0..3), every width 1..8, and a 10-byte 0x5A-guarded buffer with the field at offset 1, so both sides are checked. W1 also passes against base `wire.h`. | `receipts/equivalence.txt`, `receipts/variants/base-wire-with-w1.json` |
| 2 | Two plants that break only odd widths, killed by W1 alone; they replace the draft's plants; placed before the generated-entity plants | **Met.** Every call site in `src/`, `examples/` and `tests/` uses widths 2, 4, 6 or 8. With W1 removed, each plant passes all 8 hosted binaries (ctest rc 0). With W1 present, only `acmp_tests` fails, and only on W1. The focused campaign (`--select wire-put-be`) gives CAUGHT 2, ESCAPED 0, ERROR 0. The draft's plants (`high << 16`; `high >>= 8` removed), with W1 removed, are still caught by adp, acmp, maap and entity, so replacing them was justified. The plants are at `tests/mutations.json:5832` and `:5848`, before `entity-wrong-count` (`:5864`). That order is required because `scripts/entity_selftest.py:50` reads the last three entries. | `receipts/variants/*.json`, `receipts/mutation-select-wire*.{txt,json}` |
| 3 | `scripts/mutation.py` header-without-source rule and its new error path | **Met.** `arm_module()` (`:36-37`) is shared with `prepare()` (`:141`). A header with no `src/<stem>.c` builds the kill arm's module (`:221-224`). An arm outside `SOURCES` raises "unknown mutation arm" (`:219-220`), which is recorded as ERROR. Probe, head driver: a header-with-source plant with an unknown arm, a `wire.h` plant with an unknown arm and a `wire.h` plant with no arm each gave ERROR; genuine `wire.h` and `maap.h` plants gave CAUGHT; the campaign completed, wrote `results.json` and returned rc 1. Same table, base driver: `KeyError: 'bogus'` stopped the campaign and no `results.json` was written. | `receipts/errpath.json`, `receipts/errpath/*` |
| 4 | `tests/coverage.ratchet` regenerated in the pinned CI environment | **Met.** The exact-head hosted quality job (the CI environment) measured `include/wire.h 14/14, 2/2`, identical to `tests/coverage.ratchet:4`. All other rows were unchanged and the coverage gate returned rc 0. A disposable regeneration (`coverage.py --write`, host gcc) was byte-identical to the committed file. | `receipts/hosted-ci/summary.txt`, `receipts/ratchet.txt` |
| 5 | Parent split image `nm` at 1x1/1if and 8x8/2if shows no `__lshrdi3`; text sizes recorded | **Met on the author's receipts** (not rebuilt here, by scope). Before: one `__lshrdi3` per point. After: none. The before/after symbol diff at both points is `__lshrdi3` removed plus one more out-of-line `wire_put_be` copy (3 to 4), and nothing else. After the change no compiler runtime helper remains in either image. Text: 1x1 107278 to 106854 B (-424); 8x8 122106 to 121686 B (-420). Corroboration with a different compiler on the three core objects at -Os rv32i and rv32im: 3 `__lshrdi3` objects become 0. | author `receipts/image/*`, `receipts/rv32-symbols.txt` |

Both targets pass at this exact head. Hosted run 42465293588 (pull_request; it checks out the head sha) and run 42465283076 (push) both pass `quality` and `bare-metal`: 28/28 gates rc 0, 390 plants all CAUGHT (both wire plants CAUGHT on W1), and RV32 Debug and Release rc 0 with no unresolved symbols and core imports unchanged from base. The local reviewer `scripts/baremetal.py` at the head also returned rc 0.

**Trade-off weighed.** The halves form costs size in this repository's own -O3 Release smoke image and saves size wherever the helper used to be called:

- **The issue's target (the parent's -Os build):** it saves about 420 B and removes the only runtime helper from the split image.
- **This repository's Release (-O3) smoke image:** it costs 796 B with the host toolchain and 928 B with the CI toolchain.
- **Other options, measured locally on the three core objects:** it is also smaller at -O2 (-440 B) and at -O0.

The issue prescribes the halves form and targets the parent's -Os split image. The smoke image is a test artifact with no size gate in `scripts/baremetal.py`. I accept the trade-off at either figure. F1 only concerns how the figure is reported.

## Findings

### F1 - MINOR - Docs
- **Where:** PR #29 body, section "Effect on the parent's split image", paragraph starting "This repository's own RV32 smoke images never called the helper". The same figures appear in the author's `HANDOFF.md` table "The stack's own RV32 smoke images".
- **Authority/evidence:** The body gives "47508 to 47428 B (Debug) and from 36857 to 37653 B (Release, -O3)" without naming the toolchain. I reproduced all four numbers exactly with the host's riscv64-elf-gcc 16.2.0 (`receipts/baremetal-local-sizes*.txt`), and the author's `scripts/variants.sh` names that same compiler for the stack sets. The workflow's pinned toolchain (Ubuntu 24.04 `gcc-riscv64-unknown-elf`) gives different figures in the exact-head and base hosted maps (`receipts/hosted-ci/summary.txt`):
  - Debug `.text`+`.rodata`: 47072 to 46992 B (-80).
  - Release `.text`+`.rodata`: 36649 to 37577 B (+928; `.text` 34688 to 35616, `.rodata` unchanged).
- **Impact:** The PR records this trade-off for the owner to weigh against the parent's -Os gain. As written, the cost is from an unstated environment and understates the CI-environment cost by 132 B (+796 B against +928 B). A reader following "How to validate" on the CI image cannot reproduce it. The decision does not change, but a figure is involved, so this is not wording-only RESIDUE.
- **Required outcome:** Edit the PR body only; no source change and no new head. Name the toolchain behind the 47508/47428/36857/37653 figures, and add the pinned CI toolchain figures (Debug 47072 to 46992 B, -80; Release 36649 to 37577 B, +928, from the hosted maps) or replace the figures with them. Optionally also note the toolchain for the variant table's "stack -O0/-O3" columns.
- **Verification:** Compare the edited body with the `rv32-evidence` `rv32_smoke.map` output sections of runs 38295188787 (base) and 42465293588 (head), and with `receipts/baremetal-local-sizes*.txt`.

### S1 - SUGGESTION - Tests, Robustness
`scripts/mutation_selftest.py` has controls for the other ERROR paths (unknown test, mixed selection) but none for the new unknown-arm ERROR (`scripts/mutation.py:219-220`) or for the header-without-source build rule (`:221-224`). Only the two wire plants exercise the rule, and no gate exercises the unknown-arm path. A control like `receipts/errpath.json` (an unknown arm on a header-with-source plant gives ERROR, the campaign completes and `results.json` is written) would protect against regression. This does not block.

### S2 - SUGGESTION - Tests
W1's message says "and nothing past them" (`tests/test_acmp.cpp:2577`), but the assertion also checks the byte before the field. "And nothing outside them" would describe it exactly. The needle at `tests/mutations.json` is a prefix of the message and would stay valid. This does not block.

No RESIDUE. The comment-rule scan of every added line found no bench lane labels, lane names, review rounds, reviewer IDs or issue-comment IDs in source, tests, scripts or docs. The added comments are `// REQ: ACMP-02` and one behaviour comment at `scripts/mutation.py:221`. Host paths and private identifiers: none in the delta.

## Lens notes (artifact-specific)

- **Conformance:** ACMP-02 (build the ACMP format, IEEE 1722.1-2021 8.2.1) depends on big-endian field serialisation. Bit-exactness with the old form is shown, so there is no protocol behaviour change. The `docs/PORTING.md:388-391` precondition ("one at a time", 1..8 bytes) is unchanged and still true. Tracing W1 to ACMP-02 follows the issue's stated path.
- **RTL (target code generation; there is no HDL in this repository):** On RV32 at -Os the base's 3 objects with `__lshrdi3` drop to 0. At -O0, -O2 and -O3 neither form references the helper. The CI core-import sets are unchanged from base. Smoke Debug and Release pass under QEMU on hosted CI and locally. The parent image receipts show the helper removed at both points. The parent hot-list edit (`ctrl_split.ld`, `ctrl_split_hot.txt`) is a parent-side follow-up: without it the parent refuses the image, as recorded in the author's refusal receipt.
- **Robustness:** Every shift is a 32-bit shift by a constant (8 or 24), with no undefined behaviour (UBSan clean across 37.7M checks). `bytes == 0` writes nothing, as before. Outside the documented precondition (`bytes > 8`) the new form writes leading zero bytes, where the old form had an undefined shift of 64 or more, so it is no worse. `mutation.py`: the fallback applies only when `src/<stem>.c` is absent. An unknown arm becomes a per-plant ERROR, where it used to crash the campaign.
- **Tests:** Run on the W1 test alone (pinned GoogleTest 1.14.0), W1 fails on all 13 planted `wire.h` defects: both plants, crossing shift 16, high never shifted, no crossing, top byte never written, starts one short, off-by-one store, high taken from bit 31, low taken from high, width capped at 7, odd width rounded down, and byte stored from high. It passes on the head and on the base (`receipts/w1-strength.json`). The full hosted suite at the head passes 8/8.
- **Docs:**
  - `docs/VERIFICATION.md:24`: 386 core plants plus 4 generated is 390, matching `tests/mutations.json` (369 `src`, 17 `include`, 4 `examples`).
  - `docs/VERIFICATION.md:195`: the header-plant rule is accurate.
  - `docs/TESTS.md:162` and `docs/TRACEABILITY.md:16`: anchors `#L2562` are correct, and the hosted traceability and test-inventory gates return rc 0.
  - PR body and handoff claims match my probes, except the smoke-image figures (F1). The CHANGELOG was not updated, which matches the recent fix PRs and is not required by `CONTRIBUTING.md`.

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `include/wire.h:38-47`; `docs/PORTING.md:388-391`; ACMP-02 record; `receipts/equivalence.txt` | R796-1 | c687810b74b53b69c1fbdff7bfd0ec9da94eaa78 |
| RTL (RV32 target code generation) | CLEAN | `receipts/rv32-symbols.txt`; `receipts/baremetal*.txt`; hosted `rv32-evidence` (head and base); author `receipts/image/*` | R796-1 | c687810b74b53b69c1fbdff7bfd0ec9da94eaa78 |
| Robustness | CLEAN | `include/wire.h`; `scripts/mutation.py:36-37,141,219-225`; `receipts/errpath*`; UBSan equivalence | R796-1 | c687810b74b53b69c1fbdff7bfd0ec9da94eaa78 |
| Tests | CLEAN | `tests/test_acmp.cpp:2561-2580`; `tests/mutations.json:5831-5862`; `tests/coverage.ratchet:4`; `receipts/variants/*`, `w1-strength.json`, `mutation-select-wire*`, `ratchet.txt`; hosted mutation `results.json` | R796-1 | c687810b74b53b69c1fbdff7bfd0ec9da94eaa78 |
| Docs | UNCLEAN (F1) | `docs/VERIFICATION.md:24,195`; `docs/TESTS.md:162`; `docs/TRACEABILITY.md:16`; PR #29 body; author `HANDOFF.md` | R796-1 | c687810b74b53b69c1fbdff7bfd0ec9da94eaa78 |

Clone restored and verified after the probes (`receipts/clone-integrity.txt`):
- HEAD and tree are exact.
- The worktree is clean, including ignored files.
- The index is identical to HEAD, and all 98 tracked blobs match their ids, with modes 100644.
- The repository has no gitlinks (no submodules), so no submodule gitlink applies.
- Every probe ran on `git archive` copies or wrote only under the packet scratch directory.

## Real limits

- I did not rebuild the parent split image (out of scope). Item 5 rests on the author's published `nm`/`size` receipts, which I checked for internal consistency and corroborated only on core objects with a different compiler. The "7 call sites" figure was not reproduced.
- Local hosted builds used host gcc 16.2.1 with the pinned GoogleTest 1.14.0. The pinned Clang 18 tree has no sanitizer runtime, so Clang 18 equivalence ran without UBSan. The CI-environment authority for gates, coverage and RV32 sizes is the exact-head hosted artifacts, which I inspected but did not produce.
- I did not run the full `scripts/validate.py` locally. Static analysis, privacy, comments, graphs and the other gates rest on the hosted exact-head run (28/28 rc 0).
- The pinned Verilator was not used, because there is no HDL in scope.
- No manager source bank was run at this head, and none is claimed. Physical calibration was NOT RUN. Skipped field contexts are not hardware proof.

## Pending manager duties

- Validate the current-dev merge candidate (builder and native banks) at the merge turn. Source base 70936b77; live dev 0a75aa774b89ac89351700f63dd8cbb89694af6c. Link those receipts. Hosted/act acceptance is the manager's.
- Merge order with PR #28 (issue #26, head 3d57262c). Both PRs edit the same lines in `docs/VERIFICATION.md:24` (384 becomes 386 here and 406 there; combined it is 408 core plants), `tests/mutations.json` (both insert before the entity plants), `tests/coverage.ratchet`, `docs/TESTS.md`/`docs/TRACEABILITY.md` (anchors shift because both edit `tests/test_acmp.cpp`). PR #28 adds only width-2 and width-8 `wire_put_be` calls, so W1 should remain the only killer of both plants. Recheck the combined candidate's plant count, the escape property and the regenerated ratchet and docs.
- Parent follow-up: move `third_party/tsn-c-stack` to the merged commit and drop the `__lshrdi3` hot-list entries in the same commit.
- Carry F1 to the author as a PR-body edit. S1 and S2 are optional.

R796-1 FINISHED
