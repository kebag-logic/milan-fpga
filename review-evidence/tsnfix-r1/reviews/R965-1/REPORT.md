[R965] POSITIVE - exact head a8551cdd3cf715c52cca164a57d6d7f022e62c00

# R965-1: independent internal review of kebag-logic/tsn-c-stack PR #44 (kebag-logic/milan-fpga#977)

- Head `a8551cdd3cf715c52cca164a57d6d7f022e62c00`, tree `63a8690a17af206ffe6e3e56614ed98bf838dcf0`, branch `main-gate-fixes`, base `main` `5a07d9b7d87298f04b15aa28f0304ec88b0aef81`.
- Review start: https://github.com/kebag-logic/tsn-c-stack/pull/44#issuecomment-7237574301
- Delta: 2 commits, 5 files (`scripts/check_privacy.py`, `tests/coverage.ratchet`, `CHANGELOG.md`, `docs/IMPORT.md`, `docs/VERIFICATION.md`), +18/-12. Nothing under `src/`, `include/` or `examples/` changed: 0 diff lines `5a07d9b..a8551cd`.
- Verdict: POSITIVE. No open BLOCKER, MAJOR or MINOR finding. There are two RESIDUE wording items (F1, F2) and four SUGGESTIONs (S1 to S4). S2 and S3 concern behaviour that predates this delta.

## Reconstruction

1. **Rules.** `CONTRIBUTING.md` requires:
   - one-line commit subjects with no body or trailers;
   - one of the two accepted identity pairs;
   - neutral role labels, and no host locations or product names;
   - a protocol change updates its requirement, tests and traceability;
   - the coverage ratchet is never lowered to accommodate an untested path.

   The repository has no `AGENTS.md` and no submodules (no `.gitmodules`, 0 gitlinks). `README.md`, `docs/VERIFICATION.md`, `docs/COVERAGE.md`, `docs/IMPORT.md` and `scripts/validate.py` (the quality job's 28 gates) were read.
2. **Scope.** The issue body and comments of kebag-logic/milan-fpga#977 frame the SRP registration budget. They contain no ruling specific to PR #44. The frozen scope is the manager's brief:
   - (1) exempt merge `5a07d9b7` (PR #41) by its exact SHA, as the merge of #29 was exempted by PR #30 (`62d24a3`);
   - (2) regenerate `tests/coverage.ratchet`.

   There is no protocol, requirement or traceability change, so REQUIREMENTS/TRACEABILITY are correctly untouched.
3. **Diff and history.** Both commits use the holder identity pair (author = committer = `hackerman-kl <hackerman-kl@kebag-logic.com>`), with one-line subjects and no body.
4. **Evidence.**
   - The author's public packet (`review-evidence/tsnfix-r1` at milan-fpga `6307be01`) was read and its scripts were not executed.
   - The hosted runs at the exact head and at base main were read through the API.
5. **Prior public findings on this PR.** There are none: no reviews, no review comments, and only the two review-start comments. Nothing is carried in for resolution.

## What was executed (independently, at the exact head)

| Campaign | Result | Receipt |
|---|---|---|
| `scripts/validate.py --work … --jobs 16 --graphs` in this clone | **28 of 28 gates rc 0**: privacy (67 commits, 522 historical blobs, 100 current files; pass); privacy-selftest (17 controls); coverage; coverage-controls; static-analysis; both test suites 10/10; mutation 522 caught, 0 escaped, 0 error; mutation-controls; graphs | `receipts/validate/` |
| Privacy probes (`scripts/privacy_probes.py`, disposable `--no-local` clone) | See section 1 | `receipts/privacy-probes.txt` |
| Coverage at 8 commits (`scripts/measure.sh`: GCC coverage build, ctest, the commit's own `coverage.py`, `scripts/arcs.py`) | See section 2 | `receipts/coverage/` |
| Ratchet regeneration and ratchet probes (`scripts/ratchet_probes.sh`) | `coverage.py --write` output is byte-identical to the committed ratchet | `receipts/ratchet-probes.txt` |
| Sanitizer-runtime probe of the pinned Clang 18.1.3 | Cannot link `-fsanitize=address,undefined` (no `libclang_rt`) | `receipts/sanitizer-runtime-probe.txt` |
| Hosted evidence (read only) | Exact head: `quality` and `bare-metal` succeeded in both the push and pull_request runs. Base main: `quality` failed at privacy | `receipts/hosted-summary.txt` |
| Clone restore | HEAD and tree exact; index modes and blob ids equal the HEAD tree (100 files); 0 byte or mode differences; 0 untracked or ignored files; 0 gitlinks required | `receipts/restore-check.txt` |

Toolchain for the local runs:
- GCC 16.2.1;
- host Clang 23.1.5 for the sanitizer build;
- pinned Clang 18.1.3 as `clang-18` for the token gates;
- pinned clang-tidy 18.1.3;
- pinned GoogleTest/GMock 1.14.0 (`find_package(... 1.14.0 EXACT)`);
- cppcheck 2.22.0, CMake 4.5.0, Mermaid CLI 11.16.0.

The hosted exact-head pull_request run covers the CI toolchain: GCC 13.3.0 and Clang 18.1.3, 28 of 28 gates rc 0.

An earlier local attempt is not cited as evidence. It failed in the token gates only because `clang-18` was missing from my PATH. After the pinned wrapper was added, the run above is the one reported.

### 1. Privacy gate (`scripts/check_privacy.py`)

**The defect is real on main.**
- Base gate on base history: rc 1, `5a07d9b7…: commit message must be one line`.
- The hosted push run of main `5a07d9b7` failed `quality` at the same gate.

**The fix alone repairs main, with nothing else needed:**
- head gate on base history: rc 0 (65 commits);
- head gate on head history: rc 0 (67 commits);
- head self-test: 17 controls pass.

**The self-test is independent of set order.** It ran with 17 controls passing under PYTHONHASHSEED 0, 1, 2, 3, 12345 and random. The old `next(iter(TWO_LINE_MERGES))` pick would have varied with the seed once the set had two members. The per-merge loop over `sorted(...)` (`scripts/check_privacy.py:56-62`) removes that.

**Real commits on top of head, in a disposable clone:**
- a one-line holder commit passes;
- a **two-paragraph non-exempt holder commit is refused** (`commit message must be one line`);
- a one-line foreign-identity commit is refused (`unexpected identity`).

**Planted defects in copies of the head gate:**
- Refused by the history run: the #41 exemption dropped, the #29 exemption dropped, the #41 SHA typed one digit off.
- Refused by `--selftest`:
  - the one-line rule removed;
  - the exemption matched on a 7-digit prefix;
  - the exemption also skipping the identity check;
  - an all-zero commit added to the exemptions (refused by `web-flow-two-lines` and `holder-two-lines`);
  - any `Merge` subject exempted;
  - the near-miss built from the exact merge.
- Not refused by `--selftest`, only visible in the printed count:
  - dropping the per-merge loop (11 controls);
  - checking only the first merge (14 controls).

  See S1.
- One plant on a line outside the delta, counting blank lines in the one-line rule, passes the self-test but is refused by the history run. It is recorded as information only.

**Re-reading the code:**
- Identity and the content scan still apply to the exempt commits (`commit_errors` lines 33-36; `scan` at line 82 for every commit).
- Every non-exempt control keeps its old commit id: `"0" * 40`, or `OWNER_SQUASH` for `owner-squash` (line 55).
- Near-miss: `...f81` gives `...f80`, and `...496` gives `...490`.
- The new comment at line 17 states behaviour and reason with the PR number. It shows no lane label, review round, reviewer ID or comment ID, so the comment rule is met. The delta's added lines contain no such token.

### 2. Coverage ratchet (`tests/coverage.ratchet`)

The ratchet was last written at `8a1cb08` (#28). Measured with each commit's own `coverage.py` (adp and acmp are post-exclusion; adp's raw totals are given in parentheses):

| Commit | What it is | adp.c lines | adp.c branches | acmp.c lines / branches |
|---|---|---|---|---|
| `8a1cb08` | last ratchet write | 205 (205/207 raw) | 97 (97/104 raw) | 813 / 424 (**reproduces the old ratchet**) |
| `9deb0dd` | #33 merge | 205 | 97 | 815 / 426 |
| `715589c` | #34 merge | 205 | 97 | 847 / 436 |
| `69bac7c` | #36 merge | 205 | 97 | 847 / 436 |
| `a795471` | #38 merge | 205 | 97 | 847 / 436 |
| `c3bff8f` | #40 merge | **215 (215/217 raw)** | **95 (95/102 raw)** | 847 / 436 |
| `5a07d9b` | main, #41 merge | 215 | 95 | **877 / 468** |
| `a8551cd` | head | 215 | 95 | 877 / 468 |

**Re-derivation of adp.c's two-arc drop** (`receipts/coverage/adp-arc-delta.txt`), comparing per-line arcs by function, arc count and statement across #40:
- removed: `if (a->rng == 0u) {` in `adp_init` (line 180), 2 arcs, hits [1, 40316];
- removed: the same guard in `adp_set_enable` (line 234), 2 arcs, hits [1, 132615];
- added: `a->rng = x != 0u ? x : 1u;` in `leave_down` (line 108), 2 arcs, hits [174255, 1].

That is a net change of -2 raw arcs (104 to 102).

**Excluded arcs and lines.** `docs/COVERAGE.md` and `scripts/coverage.py` are unchanged `8a1cb08..a8551cd`. The ADP rows hold 7 arcs and 2 lines, so the post-exclusion totals are 104-7 = 97 and 102-7 = 95, and 207-2 = 205 and 217-2 = 215. No arc is uncovered.

**Other commits.**
- #38's adp.c edit (`!=` to `<`) is count-neutral. It was measured on both sides.
- adp.c is unchanged `c3bff8f..a8551cd`.

**Match with the author's packet.** The author's published per-line receipts show the same lines and hit counts. The PR body's increments for #33/#34/#41 (847/436 after #34, 877/468 after #41) match.

**The record is toolchain-stable.** The hosted exact-head run (GCC 13.3.0) prints the same raw totals (adp 215/217, 95/102; acmp 877/877, 468/468) as GCC 16.2.1 here.

**The change only updates the record.** `compare()` checks covered/total fractions, so the base ratchet (205/97, 813/424) also passes at head's measurement (rc 0). The probes show the gate refuses:
- a removed row;
- a higher fractional floor (95/94);
- an extra file row.

It accepts a non-matching 100 % row (216/216, 96/96), which is S2. The PR body states this, and no ratchet fraction is lowered.

### RV32 and image bytes

The base main and exact-head hosted `bare-metal` jobs both succeeded. Their `results.json` show **identical Debug and Release ELF sha256, core object and generated object hashes**, so no image byte moves. The RV32 gate was not run locally, because the host has no `riscv64-unknown-elf-gcc`.

## Findings

| ID | Severity | Lenses | Location | Authority / evidence | Impact | Required outcome | Verification |
|---|---|---|---|---|---|---|---|
| R965-1-F1 | RESIDUE | Docs | `docs/IMPORT.md:138` | The delta adds a second exemption at line 137. The next sentence still reads "Main's published history is not rewritten, so the exemption stands in place of a corrected message." | Prose only: the singular now under-describes two exemptions. It changes no gate, figure or claim. | Replace it with "Main's published history is not rewritten, so the exemptions stand in place of corrected messages." | Read the line. |
| R965-1-F2 | RESIDUE | Docs | PR #44 body, section "Validation": "with Clang 18.1.3, clang-tidy 18.1.3 and GoogleTest 1.14.0" | `validate.py` builds the sanitizer arm with `clang`/`clang++`. The author's published `env.sh` puts only `clang-18` ahead of the host PATH (no other `clang` on the evidence host's PATH). The pinned Clang 18.1.3 cannot link `-fsanitize=address,undefined` (`receipts/sanitizer-runtime-probe.txt`). So the local sanitizer arm cannot have run on Clang 18.1.3. The receipt header `clang: Ubuntu clang version 18.1.3` prints `clang-18 --version`. | Wording of the toolchain line only. It changes no verdict: the hosted exact-head `quality` job ran that arm on Clang 18.1.3 (GCC 13.3.0) with 28/28 rc 0, and this review ran it on Clang 23.1.5 with 28/28 rc 0. | Name the sanitizer arm's compiler as run, for example: "Clang 18.1.3 for the token gates and the host Clang for the local sanitizer build; the hosted quality job at this head ran the sanitizer build on Clang 18.1.3". | Read the PR body. |
| R965-1-S1 | SUGGESTION | Tests, Robustness | `scripts/check_privacy.py:56-68` | Planted: dropping the per-merge loop gives 11 controls, and checking only the first merge gives 14. Both pass `--selftest`; only the printed count changes. | The self-test cannot detect its own shrinkage. This was equally true before the delta. | Optionally assert `len(cases) == 11 + 3 * len(TWO_LINE_MERGES)` and derive the log line at line 86 from the set, so a third exemption cannot leave the "#29 and #41" text stale. | Re-run the two plants in `scripts/privacy_probes.py`. |
| R965-1-S2 | SUGGESTION (predates the delta) | Tests | `scripts/coverage.py:305-319`, `tests/coverage.ratchet:1` | The header says "Exact", but `compare()` is fractional. A 216/216, 96/96 row passes at 100 % (`receipts/ratchet-probes.txt`). This is how the adp and acmp rows went stale without a red gate. | A stale record goes unnoticed. The author already raised this as an owner question. | Owner decision: either refuse any row that differs from the measurement, or reword the header. | `scripts/ratchet_probes.sh`. |
| R965-1-S3 | SUGGESTION (predates the delta) | Docs | `docs/IMPORT.md:139` | "Later pull requests are squash-merged on GitHub", but #28, #29, #33, #34 and #41 landed as merge commits under the GitHub pair. Two of them (#29, #41) carried message bodies and broke main's gate. | A misleading process statement, and its cause recurs. | Correct the sentence in a later docs change, and keep merge messages to one line (see the manager duties). | Read `git log --first-parent main`. |
| R965-1-S4 | SUGGESTION | Docs | PR body, section 1 | The PR describes the defect as "Two gate defects on `main`", and later says section 2 "does not repair a failing gate". | Mild internal tension. The body already resolves it explicitly. | None is needed. Optionally say "one failing gate and one stale record". | Read the PR body. |

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Rules:<br>- `CONTRIBUTING.md` (identity, one-line subjects, no trailers, no host locations or product names, ratchet not lowered);<br>- PR #30's precedent (`62d24a3`);<br>- the comment rule on the added lines.<br>Both delta commits' raw metadata. No protocol, requirement or traceability change (0 diff lines in `src/`, `include/`, `examples/`). Privacy gate rc 0 on head history and base history with the head gate. | R965-1 | a8551cdd3cf715c52cca164a57d6d7f022e62c00 |
| RTL | CLEAN | No HDL or firmware source in the delta. Hosted RV32 `results.json` for base main vs exact head: Debug and Release ELF, core and generated object sha256 identical. Hosted `bare-metal` succeeded at the exact head (push and pull_request). | R965-1 | a8551cdd3cf715c52cca164a57d6d7f022e62c00 |
| Robustness | CLEAN | `check_privacy.py`:<br>- exact-SHA match (one-digit near-miss refused, prefix plant refused);<br>- identity and content checks kept for exempt commits;<br>- set-order independence under 6 hash seeds;<br>- real two-paragraph and foreign-identity commits refused.<br>Ratchet probes (missing row, higher floor, extra row refused). | R965-1 | a8551cdd3cf715c52cca164a57d6d7f022e62c00 |
| Tests | CLEAN | `validate.py` 28/28 rc 0 locally and hosted. Privacy self-test 17 controls. 12 planted defects: 9 refused by the self-test or history run as designed, 2 visible only by count (S1), 1 information-only plant on a line outside the delta. Coverage re-derived at 8 commits, the per-line arc delta across #40, `--write` byte-identical, GCC 13 (hosted) equals GCC 16 (local). Mutation 522/0/0. | R965-1 | a8551cdd3cf715c52cca164a57d6d7f022e62c00 |
| Docs | CLEAN (RESIDUE F1, F2 only) | `CHANGELOG.md:5-6` (figures and attribution verified against measurement), `docs/VERIFICATION.md:43` (matches the 17 controls), `docs/IMPORT.md:137-139`, the `check_privacy.py:17` comment and log line, the PR body and the author's packet. | R965-1 | a8551cdd3cf715c52cca164a57d6d7f022e62c00 |

## Real limits

**Toolchain.**
- The local toolchain is not CI's: GCC 16.2.1 and host Clang 23.1.5 for the sanitizer arm, because the pinned Clang 18.1.3 has no sanitizer runtime.
- The CI toolchain (GCC 13.3.0, Clang 18.1.3) result comes only from the hosted exact-head run, read without re-execution.

**Not run.**
- The RV32 bare-metal gate was not run locally (no cross compiler on the host). Its evidence is the hosted job and the object-hash equality.
- No manager source bank ran at this head, and none is claimed or inferred. The author's published gate receipts are the source-head execution evidence, and this review's runs are independent of them.
- This review did not build the final current-dev merge candidate (source base `5a07d9b7`, live dev `e275d7950ef3385753e6a15d2e191ba855b171ed`).
- Physical calibration was NOT RUN, and no hardware was touched. Field skips are not hardware proof.

**Inference.** F2 is inferred from the author's published `env.sh`, the pinned install on this host and the absence of any other `clang` on that PATH. The author's private environment was not inspected.

**Run conditions.** `validate.py` ran with `--jobs 16`, as the gate driver runs it: four arms concurrently.

## Pending manager duties

1. **Merge #44 with a one-line merge message** (or a squash with a one-line subject) under an accepted identity pair. A two-paragraph merge message would make main's privacy gate fail again, as `5a07d9b7` and `d7e6a2a1` did.
2. Validate the current-dev merge candidate (builder and native banks) at the merge turn and link its receipts on the PR. Hosted and act acceptance stay with the manager.
3. Carry R965-1-F1 and R965-1-F2 to the residue checklist with their exact fixes.
4. Route S2 (exact versus fractional ratchet) to the owner, as the author proposed.
5. Merge still requires the second independent positive review and the full completion bar.

## Packet

- Scripts: `scripts/env.sh`, `scripts/validate.sh`, `scripts/measure.sh`, `scripts/arcs.py`, `scripts/privacy_probes.py`, `scripts/ratchet_probes.sh`. They are portable and take their paths as arguments. `env.sh` requires `TSN_TOOLS`.
- Receipts: listed in `MANIFEST.sha256`. Paths in the receipts are neutralised as `$PACKET`, `$CLONE`, `$TOOLS` and `$HOME`.

R965-1 FINISHED
