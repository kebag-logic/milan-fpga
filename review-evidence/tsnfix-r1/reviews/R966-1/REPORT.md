[R966] POSITIVE - exact head a8551cdd3cf715c52cca164a57d6d7f022e62c00

# R966-1: external independent review of kebag-logic/tsn-c-stack PR #44 (kebag-logic/milan-fpga#977)

- Head `a8551cdd3cf715c52cca164a57d6d7f022e62c00`, tree `63a8690a17af206ffe6e3e56614ed98bf838dcf0`, branch `main-gate-fixes`.
- Base `main` `5a07d9b7d87298f04b15aa28f0304ec88b0aef81`. Two commits, five files, +18 −12.
- Verdict: **POSITIVE**. No BLOCKER, MAJOR or MINOR finding. One RESIDUE and one SUGGESTION are recorded below.
- All five lenses are CLEAN at this head (ledger below).

Both claims of the PR hold when re-derived independently:

1. **Privacy gate.** `main` fails its own privacy gate on the merge of #41 and on nothing else. With the change the gate passes over main's whole history, and a two-paragraph message on any other commit is still refused, by the self-test and by the real gate.
2. **Coverage ratchet.** The committed file is byte-identical to what `scripts/coverage.py --write` generates. The two-arc drop in `src/adp.c` is two covered guards removed and one covered ternary added by #40. `src/acmp.c` only rose.

## Findings

### R966-1-R1 (RESIDUE): the PR body's toolchain sentence does not say which arms Clang 18.1.3 covered

- **Lenses:** Docs.
- **Artifact:** PR #44 body, section "Validation": "with Clang 18.1.3, clang-tidy 18.1.3 and GoogleTest 1.14.0: all 28 gates rc 0".
- **Evidence:**
  - `scripts/validate.py:46-47` builds the GCC arm with `gcc`/`g++` and the sanitizer arm with `clang`/`clang++`.
  - The author's published `receipts/tools/env.sh.txt` prepends directories that supply `clang-18` and `clang-tidy`; the published `validate.out` prints `clang-18 --version`. The packet holds no configure log, so the compiler of the GCC arm and of the sanitizer arm is not evidenced.
  - In this review's run with the same pinned directories, the sanitizer arm identified Clang 23.1.5 and the GCC arm GNU 16.2.1 (`receipts/validate/summary.txt`). Clang 18.1.3 served the token gates only.
- **Impact:** wording only. No figure, gate result or verdict changes: the hosted run at this exact head executed the same command with GNU 13.3.0 and Clang 18.1.3, 28 gates rc 0, and its `coverage.log` is byte-identical to the author's and to this review's (`receipts/hosted/summary.txt`).
- **Exact fix:** in the PR body, replace the toolchain clause with: "with GoogleTest 1.14.0, clang-tidy 18.1.3 and Clang 18.1.3 for the token gates, and the host's `gcc` and `clang` for the GCC and sanitizer arms; the hosted run 46132722374 at this head ran the same command with GNU 13.3.0 and Clang 18.1.3, 28 gates rc 0".
- **Verification:** read the PR body; compare with the hosted `gcc-configure.log` and `clang-sanitizers-configure.log`.

### R966-1-S1 (SUGGESTION): the ratchet gate does not notice a stale row

- **Lenses:** Tests, Robustness.
- **Artifact:** `scripts/coverage.py:305-319` (`compare`), `tests/coverage.ratchet:1` ("Exact per-file line and branch ratchet"). Not part of the reviewed delta.
- **Evidence:** `compare` tests covered/total fractions. On the head build the gate returns rc 0 with the `src/adp.c` row set to the old `205/205 97/97`, and also with `216/216 96/96` (`receipts/coverage/ratchet-exactness-probe.txt`). The `acmp.c` row was stale from #33 and the `adp.c` row from #40 with every gate green (`receipts/coverage/chain.txt`).
- **Impact:** none on this PR; the record can drift again unnoticed. The author raised the same question for the owner in the public handoff.
- **Outcome proposed:** a separate issue deciding whether `compare` refuses any difference in totals, so each source change regenerates the file in its own PR.
- **Verification:** a ratchet row with a wrong total fails `scripts/coverage.py`, with a control in `scripts/coverage_selftest.py`.

No other finding. Prior public review findings on this PR: none exist (see the last section).

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `CONTRIBUTING.md` (issue scope, one-line subjects, identities, ratchet rule); `docs/VERIFICATION.md:23,41-43,155-157,211`; `docs/COVERAGE.md`; issue #977 body and the manager and owner decisions on it; commit metadata of `a905c32d`, `a8551cdd`, `5a07d9b7`, `d7e6a2a1`; `git diff 5a07d9b7..a8551cdd` | R966-1 | `a8551cdd3cf715c52cca164a57d6d7f022e62c00` |
| RTL | CLEAN | No RTL in the repository or the delta. Implementation artifacts: `src/`, `include/`, `examples/`, `cmake/`, `CMakeLists.txt`, `.github/` and every test source are byte-unchanged from base; hosted RV32 ELF, core-object and generated-object hashes equal between base and head; gate logic `scripts/check_privacy.py:15-37,40-68,83-86` read line by line | R966-1 | `a8551cdd3cf715c52cca164a57d6d7f022e62c00` |
| Robustness | CLEAN | `scripts/check_privacy.py` under six new-commit cases through the real gate and eight planted defects; near-miss ids; sorted iteration of the exemption set; fail-fast order in `scripts/validate.py:53-72`; ratchet regeneration from base and head builds | R966-1 | `a8551cdd3cf715c52cca164a57d6d7f022e62c00` |
| Tests | CLEAN | `check_privacy.py --selftest` (17 controls); all 28 gates of `scripts/validate.py --graphs`; mutation 522/522 including the plant on the new ternary; `scripts/baremetal.py`; coverage measured at seven commits; per-line arc dumps of `src/adp.c`; hosted runs at head and base | R966-1 | `a8551cdd3cf715c52cca164a57d6d7f022e62c00` |
| Docs | CLEAN | `CHANGELOG.md:5-6`; `docs/IMPORT.md:135-138`; `docs/VERIFICATION.md:43`; source comment `scripts/check_privacy.py:17`; PR #44 body; public author packet `review-evidence/tsnfix-r1/author` at milan-fpga `6307be01`; comment-rule scan of the 18 added lines. R1 is RESIDUE and leaves the lens clean | R966-1 | `a8551cdd3cf715c52cca164a57d6d7f022e62c00` |

## What was checked, by lens

### Conformance

- **Scope.** Issue #977's acceptance concerns SRP registration cost. The ruling of 2026-11-26 (item 4) has #977 pin a merge commit of stack `main`, never a branch. A `main` whose own privacy gate fails cannot give a green pin, so repairing main's gates is inside that decision. The PR changes no protocol behaviour, no requirement and no traceability row; the `traceability` and `test-inventory` gates pass.
- **Commit rules.** Both commits carry the holder identity as author and committer, a one-line subject, no body and no trailer (`receipts/comment-rule-scan.txt`). The gate accepts them (`receipts/privacy/probes.txt`, A2).
- **Ratchet rule.** `CONTRIBUTING.md` forbids lowering the ratchet to accommodate an untested path. The `adp.c` branch total falls from 97 to 95 with 95 of 95 covered; no arc became uncovered and no exclusion row changed (below, Tests). The rule is met.
- **Exemption terms.** `docs/IMPORT.md` states that main's published history is not rewritten. The exemption is by full 40-digit id, for the one-line rule only. Identity and content checks still apply to `5a07d9b7` and pass: its author and committer are the GitHub pair, and its message holds no restricted term.

### RTL (implementation artifacts)

- The repository holds portable C cores and their gates; there is no RTL, and no simulator was needed or used.
- `git diff --stat 5a07d9b7 a8551cdd -- src include examples cmake CMakeLists.txt .github tests/mutations.json tests/*.cpp tests/*.hpp` is empty. The five changed files are `CHANGELOG.md`, `docs/IMPORT.md`, `docs/VERIFICATION.md`, `scripts/check_privacy.py` and `tests/coverage.ratchet`.
- Hosted RV32 results: the Debug and Release ELF hashes, the three core-object hashes and the generated-object hashes are equal between the base run and the head run (`receipts/hosted/summary.txt`).
- `scripts/check_privacy.py`: `commit_errors` is unchanged. The only behavioural change to the gate is one more id in `TWO_LINE_MERGES` and the text of one log line. The self-test now builds three controls for each exempt id in sorted order; the earlier form took `next(iter(...))` of a set, which with two entries would test one id chosen by string-hash order.

### Robustness

All from `receipts/privacy/probes.txt`, each case on a disposable clone:

| Probe | Result |
|---|---|
| B2: the base's gate at the base | rc 1, the single line `5a07d9b7…: commit message must be one line` |
| C1: the head's gate over main's history (65 commits) | rc 0, pass |
| A2: the head's gate over the head's history (67 commits, 522 blobs, 100 files) | rc 0, pass |
| D2: new commit, holder pair, two paragraphs | refused: one line |
| D3: new commit, GitHub pair, two paragraphs (recorded as #41 was) | refused: one line |
| D6: new commit, holder pair, subject and a trailer | refused: one line |
| D5: new commit, foreign identity | refused: identity |
| D1, D4: one-line commits under each permitted pair | pass |

Planted defects in a copy of the gate:

| Plant | Refused by |
|---|---|
| E1: one-line rule removed | `web-flow-two-lines`, `holder-two-lines`, both near-miss controls |
| E2: every commit under the GitHub pair exempt | `web-flow-two-lines`, both near-miss controls |
| E3: every message starting with "Merge" exempt | both near-miss controls |
| E4: exemption matched on a 39-digit prefix | both near-miss controls |
| E5: exempt merges also skip the identity check | both foreign-identity controls |
| E7: two non-blank lines allowed on every commit | `web-flow-two-lines`, `holder-two-lines`, both near-miss controls |
| E6: the #41 id dropped from the set | the self-test passes with 14 controls; the gate over history fails on `5a07d9b7` |

Notes that are not findings:

- The self-test derives its exemption controls from the set it guards, so an id added to the set is not refused by the self-test. That is the design inherited from #29; the control is review of the diff. Probe E8 shows the same for a loop cut to the first id.
- Neither near-miss id equals the other exempt id or the owner squash id.
- The gate's log line names both merges whenever either is in the history. With `fetch-depth: 0` both are always present below `main`.

### Tests

**Every gate `validate.py` runs.** `python3 scripts/validate.py --work <work> --jobs 4 --graphs` at the exact head: rc 0, 28 of 28 gates rc 0 (`receipts/validate/`).

| Gate | Result |
|---|---|
| privacy-selftest | `17 commit controls pass` |
| privacy | `67 commits, 522 historical blobs, 100 current files; pass` |
| gcc-test, clang-sanitizers-test | 10 of 10 tests pass in each |
| coverage | 100 % lines and branches after exclusions in the four files |
| coverage-controls | branch drop, missing or extra file, moved arc and stale exclusion refused |
| mutation | 522 caught, 0 escaped, 0 errors |
| static-analysis, graphs, and every other gate of the 28 | rc 0 |

`python3 scripts/baremetal.py` (the workflow's second job): rc 0, Debug and Release (`receipts/rv32/`).

**Hosted, exact head** (`receipts/hosted/summary.txt`). Runs 46132722374 (pull_request) and 46132708242 (push): jobs `quality` and `bare-metal` both executed and succeeded; every step ran, none was skipped. The hosted `gates.json`, `coverage.log`, `privacy.log` and `privacy-selftest.log` are byte-identical to this review's local ones. The hosted run on the base (45963640932) failed in `quality` at `privacy` rc 1 after 17 gates, with the same single line as probe B2; no build, coverage or mutation gate ran there.

**The ratchet, re-derived** (`receipts/coverage/chain.txt`, `measure-*.txt`):

| Commit | `src/acmp.c` | `src/adp.c` raw | `src/adp.c` after exclusions |
|---|---|---|---|
| `ea4af6f1` merge of #28 | 813/813, 424/424 | 205/207, 97/104 | 205/205, 97/97 |
| `9deb0ddb` merge of #33 | 815/815, 426/426 | 205/207, 97/104 | 205/205, 97/97 |
| `715589c1` merge of #34 | 847/847, 436/436 | 205/207, 97/104 | 205/205, 97/97 |
| `a795471c` merge of #38 | 847/847, 436/436 | 205/207, 97/104 | 205/205, 97/97 |
| `c3bff8f3` merge of #40 | 847/847, 436/436 | 215/217, 95/102 | 215/215, 95/95 |
| `5a07d9b7` merge of #41, base | 877/877, 468/468 | 215/217, 95/102 | 215/215, 95/95 |
| `a8551cdd` head | 877/877, 468/468 | 215/217, 95/102 | 215/215, 95/95 |

- `ea4af6f1` reproduces the old ratchet exactly, so the method measures what the old record measured.
- Regeneration: `scripts/coverage.py --write` in an export of the head, and separately in an export of the base, each writes a file whose sha256 equals the committed blob, `6d1cde8a82fe38fb…` (`receipts/coverage/regenerate.txt`). No row was edited by hand.

**The two-arc drop in `src/adp.c`** (`receipts/coverage/arcdiff-adp-a795471c-c3bff8f3.txt`, from per-line gcov arc dumps either side of the #40 merge):

| Change | Statement | Arcs | Covered |
|---|---|---|---|
| removed | `if (a->rng == 0u) {` in `adp_init` | 2 | both |
| removed | `if (a->rng == 0u) {` in `adp_set_enable` | 2 | both |
| added | `a->rng = x != 0u ? x : 1u;` in `leave_down` | 2 | both |

- Raw arcs 104 to 102. Uncovered arcs 7 before and 7 after; unexecuted lines 2 before and 2 after. These are the seven arcs and two statements of the five rows in `docs/COVERAGE.md`, which the reader matches exactly on both sides. Hence 97 to 95 after exclusions, all covered.
- Measured lines: 10 rows only before, 20 only after, net +10 (205 to 215).
- `src/adp.c` is unchanged from `c3bff8f3` to the head; its arc dump is the same at `c3bff8f3`, `5a07d9b7` and `a8551cdd`.
- The new ternary's `1u` arm is held by the planted defect `seed-left-at-zero` (`a->rng = x;`), killed by `AdpCore.A22GeneratorNeverStuckAtZero`: CAUGHT locally and hosted.

**`src/acmp.c`:** 813/424, then 815/426 after #33, 847/436 after #34, 877/468 after #41. Upward at each step, 100 % at each.

### Docs

Each changed statement was checked against the evidence above.

| Statement | Check |
|---|---|
| `CHANGELOG.md:5`: #41's merge exempt by its exact commit, as #29's; identity and content still checked; the self-test checks each exempt merge, its two controls, and a two-line message on any other commit | `check_privacy.py:18,33-36,51-52,56-62`; probes A1, E1-E7 |
| `CHANGELOG.md:6`: `adp.c` 215/215 and 95/95 from 205/205 and 97/97; two guards removed, one ternary added, both arcs of each covered; none uncovered; exclusion rows unchanged; `acmp.c` 877/877 and 468/468 from 813/813 and 424/424 by #33, #34 and #41 | chain and arc diff above |
| `docs/IMPORT.md:137`: the merge of #41 was recorded with a second message paragraph and is exempt on the same terms | the message of `5a07d9b7` has a subject and one further paragraph; link target is the full id |
| `docs/VERIFICATION.md:43`: the merges of #29 and #41 each pass with a two-paragraph message under the GitHub pair; the same message fails under a foreign identity and under an id one digit away from either | the six generated controls; plants E4, E5 |
| `scripts/check_privacy.py:17`, the one new source comment | states the behaviour and its reason with the PR number and commit id |
| PR body: 17 controls up from 14; five plants; `main` passes the coverage gate at 100 % because the gate compares fractions; 104 to 102 raw arcs; `acmp.c` 847/436 after #33 and #34 | all reproduced; the packet's `PR-BODY.md` differs from the live body only by the leading label line |

- **Comment rule (owner, 2026-10-15).** The 18 added lines hold no bench lane label, lane name, review round, reviewer ID or issue-comment ID (`receipts/comment-rule-scan.txt`). No RESIDUE under that rule.
- **Author packet.** All 27 files match the `published_sha256` values of its `MANIFEST.json`. Its receipts agree with this review's independent results figure for figure.

## Limits

- **Local toolchain differs from the hosted one.** Local: GNU 16.2.1 for the GCC arm, Clang 23.1.5 for the sanitizer arm (the pinned Clang 18.1.3 on the host has no sanitizer runtime), Clang 18.1.3 for the token gates, clang-tidy 18.1.3, GoogleTest 1.14.0, Cppcheck 2.22.0, CMake 4.5.0, mmdc 11.16.0; RV32 with GCC 16.2.0 and QEMU 11.1.3. The hosted run used GNU 13.3.0 and Clang 18.1.3. The coverage log is byte-identical under both GCC versions at the head.
- **The per-arc derivation** at `a795471c` and `c3bff8f3` was made under GNU 16.2.1 only. Under GNU 13.3.0 the totals are confirmed at the head only.
- **Parallelism.** `validate.py` ran with `--jobs 4`, where the workflow passes 16, to stay inside the review's parallel-job limit. The gate set and results are the same as hosted.
- **No manager source bank** ran at this head, and none is claimed. Execution evidence at the source head is the author's published gate receipts, the hosted runs, and this review's local runs.
- **No hardware.** Physical calibration was not run; nothing here is hardware proof. No Docker, no local workflow runner, no simulator.
- **Order of reading.** The diff was first opened while orienting, before the issue thread. The author packet and the hosted artifacts were read only after the independent measurements and probes were complete.
- **Published scripts.** `scripts/env.sh` takes the toolchain directory from `TOOLS`; the runs used the host's pinned toolchain directory.
- **Clone state.** After the probes the clone is at the exact head with worktree and index equal to it, no ignored or untracked file, and no gitlink at this head (`receipts/restore.txt`).

## Pending manager duties

1. **The merge of this PR must itself pass the rule.** Record it with a one-line message under the GitHub pair or the holder pair. A second message paragraph makes main's privacy gate fail again, exactly as for #29 and #41 (probe D3).
2. Build and validate the current-dev merge candidate (builder and native banks) at the merge turn, from source base `5a07d9b7` and live dev `e275d795`, and link the receipts on the PR. This review covers the source head only.
3. Own hosted and local-runner acceptance for the merge candidate; confirm the first hosted `quality` run on `main` after the merge reaches and passes the build, coverage and mutation gates, which the base run never reached.
4. Carry R966-1-R1 to the residue checklist.
5. Decide where R966-1-S1 goes (owner question on an exact ratchet).
6. Obtain the second independent positive review at this head before merging.
7. Repin milan-fpga #977 to the resulting merge commit of stack `main`, never to the branch.

## Prior public findings

Checked after the verdict and ledger above were written, at 2026-11-28T10:10:47Z: PR #44 carries two comments, both review-start notices (7237574301 and 7237579129), no review and no review comment. There is no prior public finding on this PR to resolve or retain. The PR head was still `a8551cdd3cf715c52cca164a57d6d7f022e62c00`, open and unmerged. No other reviewer's report was read.

R966-1 FINISHED
