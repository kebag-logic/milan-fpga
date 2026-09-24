[R273] POSITIVE - exact head 062e89ad098806ae5def8341fcb8c2815583ca00

# R273-8: external independent review of PR #535 (#408, #409), correction round 6

- Head `062e89ad098806ae5def8341fcb8c2815583ca00`, tree `ef7a41cf161ceabf86bcb093e409c689cbb5f30d`. Parent `991d59653ff82ccf73ef4df9477de1df8c8c5964`, where R272-6 is POSITIVE and R273-7 is NEGATIVE on one MINOR.
- Source base `759da623072358afdb0e9d570a7b4b6a788492c9`. Live dev `573f0052a0e4412e81f0845438fcec2086ce5d55` is the manager's merge-turn candidate and was not built here.
- This is a delta review. The only commit reviewed is `062e89ad` (A276), which answers R273-7 F1 MINOR and takes up R273-7 S1 and R272-6 S1-S3. All five lenses were applied to the delta at this exact head.

## Verdict

**POSITIVE.** No BLOCKER, MAJOR or MINOR is open at this head. All five lenses are covered CLEAN at `062e89ad`. The two findings below are SUGGESTIONs and do not affect coverage.

- **What the gate accepts or refuses is unchanged, except for the new cell.**
  - The syntax tree of `sw/builder/test_builder.py` at the head equals the parent's once the one added lexer-corpus row is removed (`receipts/delta-probe.json`, `trees_equal_without_row: true`).
  - The added row `/*/` agrees with the pinned GCC. GCC keeps `(a, z)`, which is the recorded answer.
  - 348 whole-firmware cases from rounds one to five were re-graded in both modes. None changed verdict or refusal reason.
- **Acceptance 4 holds.** It is 280/280 with the pinned SDK and 222/222 with every cross compiler hidden. The accepted edits stay at 29/29 firmware and 4/4 Makefile. The lexer spellings are 1846/1846 (79 fixed, 1767 generated) and the closure cells 6440/6440 in both modes. `GATE 1b PASS` with 0 NOT RUN and 467 compiles using the SDK; with the compilers hidden, 1 NOT RUN (the named census stand-down) and 0 compiles.
- **The scoped sentence matches the table.** The call-site comment at `sw/builder/test_builder.py:11294-11299` now makes three claims:
  - refusal outside the allowlist does not depend on position;
  - agreement is measured at the table's 23 positions;
  - everywhere else, agreement rests on the two lexer corpora.

  `_CLOSURE_POSITIONS` (`:2774`) holds 9 + 14 = 23 positions. The gate prints "in 23 positions", and the lexer claim in the gate print carries its corpus count. `grep "every byte in every position\|every position"` finds no unscoped claim (`receipts/grep-scope-and-refs.txt`).

## Reconstruction

- **Contracts read.** `AGENTS.md` and `CONTRIBUTING.md`, then `docs/README.md`.
- **Issue #408.** Acceptance 1-5 and the scope decisions:
  - 5758649507: remaining scope;
  - 5798077836: bundle assignment;
  - 5815136430: the byte-order mark and invalid UTF-8 refusals stand;
  - 5820090472: round-six assignment, "wording only; an added `/*/` spelling must be refused or agree with GCC";
  - 5820461649: A276 REVIEW READY.
- **Issue #409.** Acceptance 1-5.
- **Diffs.** `git diff 759da623..062e89ad` (three files) and `git diff 991d5965..062e89ad` (two files, +40/-32). History `759da623..062e89ad` has eleven commits.
- **Public evidence.** `review-evidence/408-r1/author-r6/` at `485f866f`:
  - `gates.json`, `sdk-summary.json` (280/280, 29/29, 4/4, 1846/1846, 6440/6440), `absent-summary.json` (222/222, 0 compiles) and `final-state.json`;
  - `scope-check.json`, which equals my own syntax-tree result.
- **Order.** Prior review findings (R273-7, R272-6 and the R272 F1s the new references cite) were read only after `receipts/verdict-before-prior-findings.txt` was written.

## Findings

### R273-8 S1 - SUGGESTION - Tests - `sw/builder/test_builder.py:2481` and the lexer corpora from `:5571`: no row pins an empty block comment `/**/`

- **Evidence.** This mutation is the mirror image of the author's `/*/` control.
  - The mutant `closer-from-i+3` changes `raw.find(... "*/", i + 2)` to `i + 3`. Both lexer corpora and the full closure table still pass, at the parent and at the head (`receipts/delta-probe.log`).
  - On `int a;\n/**/\n#define FOO\n/* */\n#ifdef FOO\nint b;\n#endif\nint z;\n`, the pinned GCC keeps `(a, b, z)` and the intact head readers agree. The mutant's readers keep `(a, z)` (`receipts/empty-comment-check.log`).
- **Impact.** None at this head, because the readers are correct. A regression that skips a `*/` placed right after the opener would get past the corpora and the table. The page bounds agreement to the corpora outside the 23 positions, so this is a gap in evidence strength, not an overclaim. It predates this round.
- **Optional outcome.** A fixed-corpus row holding `/**/` with a directive after it, recorded on the pinned GCC.
- **Verification.** The mutant `closer-from-i+3` stops `assert_lexer_matches_compiler()` in both modes.

### R273-8 S2 - SUGGESTION - Docs - `docs/integration/BAREMETAL_FIRMWARE.md:337` and `:1622`, and `sw/builder/test_builder.py:5566`: "comment, literal and directive-line boundaries" names thirteen of the fourteen

- **Evidence.** One of the fourteen positions, "at the end of the file, in code" (`test_builder.py:2831`), is not a comment, literal or directive-line boundary.
  - The code comment at `:2761-2763` names it correctly: "comment and literal boundaries, directive-line continuation and file ends".
  - The page's own breakdown also names it correctly (`BAREMETAL_FIRMWARE.md:345-349`): eleven comment or literal positions, one directive-line position, two file-end positions. That split matches `_CLOSURE_POSITIONS` exactly.
- **Impact.** Wording only. Every cell is listed and measured.
- **Optional outcome.** Add "and file ends" to the three labels.

## Prior public findings at this head

| Finding | Status at 062e89ad | Evidence |
|---|---|---|
| R273-7 F1 MINOR, Docs (unscoped closure claim at the call site) | **Resolved.** `:11294-11299` states position-independent allowlist refusal, agreement at the table's 23 positions, and the two corpora as the bound elsewhere, which is the scope R273-7 required. The spelling-level claim is bounded by the corpora. | `receipts/grep-scope-and-refs.txt`: no "every position" claim remains in either file (the one hit, `:13830`, is about macro parameters). The gate print carries "(1846/1846 directive spellings ...)" and "in 23 positions" (`receipts/gate1b/head-*.log`). |
| R273-7 S1 SUGGESTION (null directive cost) | **Addressed.** Page `:356` and cost row `:1368` now name the null directive. I tested the new claim "refused, wherever it sits". Five more placements are refused at the head and at dev, in both modes: in the `#error` guard group, in the verifier's `#else` arm, `# /* c */`, `#\t// c`, and a spliced `#\`. A `#` inside a block comment stays accepted, which is the control. In the guard group the full gate reports the #error pin first. Called directly, the directive-set closure refuses all five. | `receipts/probes/nd6-*.json`, `receipts/closure-on-null-directives.log`, and round five's N2-N5, unchanged (`receipts/probes/nulldir-*.json`). |
| R272-6 S1 SUGGESTION, Tests (no `/*/` row) | **Resolved.** The row is at `:5614-5616`. The pinned GCC agrees with it. `closer-from-i+1` passes at the parent and fails `assert_lexer_matches_compiler()` at the head, keeping `('a', 'b', 'z')`. | `receipts/delta-probe.log` / `.json` |
| R272-6 S2 SUGGESTION, Docs (the directive-line position) | **Resolved.** The page `:345-349` and the comment `:2761-2773` separate out the `#define` splice position. The residual label wording is R273-8 S2. | `_CLOSURE_POSITIONS` `:2774-2839` |
| R272-6 S3 SUGGESTION, Docs (finding tags without a head) | **Resolved.** `:309` and `:1369` read "at `8e12d31f`", which matches R272-3-F1, the `$` finding, at that head (comment 5811500607). `:1485` reads "at `a13b6e2e`", which matches R272-1 F1, the form-feed finding (comment 5802602464). `:339` and `:1371` already name a head. | `receipts/grep-scope-and-refs.txt` |
| Earlier findings (R272-1 to R272-5, R273-1 to R273-6), as tabled resolved by R272-6 and R273-7 at `991d5965` | **Remain resolved.** The executable delta is one corpus row, and every case probe of those rounds re-grades identically. | `receipts/probes-vs-round5.txt`: 348 cases, 0 verdict changes, 0 pin changes |

## Lens ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Assignment 5820090472: no change to what the gate accepts or refuses except the new cell, which agrees with GCC (`receipts/delta-probe.json`). #408/#409 acceptance 4: 280/280 SDK and 222/222 absent, 29/29 + 4/4 (`receipts/gate1b/head-*.log`). Acceptance 1 stand-down names the arm (absent log, NOT RUN line). Decision 5815136430 (BOM and invalid UTF-8 refusals) unchanged: bom and md cases identical. | R273-8 | 062e89ad098806ae5def8341fcb8c2815583ca00 |
| RTL | CLEAN | No HDL in the PR (`git diff --stat 759da623..062e89ad`: two docs and `sw/builder/test_builder.py`). Submodule gitlinks are identical to the parent. The executable delta is a lexer-corpus data row. The reader logic it exercises, `test_builder.py:2481` (the block-comment closer), is byte-unchanged (syntax-tree equality). | R273-8 | 062e89ad098806ae5def8341fcb8c2815583ca00 |
| Robustness | CLEAN | Hostile and boundary inputs re-run unchanged: round-one to round-five cases, both modes (348), the subset and boundary probes, 14882 out-of-table closure cells (`receipts/closure-extend-summary.txt`: 0 changed, identical to round five), the round-two gate probe and the allowlist disconnect (both modes). Plus seven new null-directive placements (`cases/round6/null-directive-more.json`). | R273-8 | 062e89ad098806ae5def8341fcb8c2815583ca00 |
| Tests | CLEAN (S1 is a SUGGESTION) | The new row fails for its defect: `closer-from-i+1` is caught at the head and not at the parent. Round-five mutation power reproduces exactly (`receipts/new-cells-probe.log`: the same five mutants caught, by the same checks). Lexer oracle: 79 fixed + 1767 generated, 0 record-vs-GCC and 0 gate-vs-record mismatches (`receipts/lexer-oracle.jsonl`). Mutation-table count not reduced (280/222). | R273-8 | 062e89ad098806ae5def8341fcb8c2815583ca00 |
| Docs | CLEAN (S2 is a SUGGESTION) | `BAREMETAL_FIRMWARE.md:309`, `:322-362`, `:1368-1369`, `:1485`, `:1620-1624`, `:1673-1676` (1846 / 79 fixed, matching the gate print). Site comments `test_builder.py:2761-2773`, `:5566-5569`, `:11294-11299`. Finding references checked against the public R272 rounds. Static checks all exit 0 (`receipts/static-checks.log`): `docs_check.py`, `check_baremetal_only.py --check`, `check_em_dash.py --base 759da623`, `check_doc_style.py`, `gen_toc.py --check`, `check_doc_paths.py`, `check_py_idiom.py`, and `git diff --check` for both ranges. | R273-8 | 062e89ad098806ae5def8341fcb8c2815583ca00 |

## Executed evidence (all at 062e89ad, in the foreground)

- **Tools.** Pinned Verilator 5.050 at `<pinned-tool-bin>/verilator`, sha256 `905795b99e0a8803383b198b118bafcbd87d20b877e3f09c39c31ea81979e92f` (the same identity as round five). The pinned SDK was freshly installed from the archive with digest `d42680e926542595c4c87629d33f5f90aac1e9a964c8955089e0514caa01b78f`: `SDK fresh installation: verified`, GCC 14.3.0 (`receipts/sdk-verify.log`).
- **Gate 1b.** `sw/builder/test_firmware_compiler.py` was run with `--sdk-destination --require-rv32` and again with `--absent`. Both exit 0, in 405 s run concurrently (`receipts/gate1b/`).
- **Round-five probes.** All were re-run unchanged. Scripts and cases are byte-identical to round five, 61 files (`receipts/probes-unchanged-vs-r273-7.txt`). The command record is `probes/round6/RUN.sh`.
- **Differences from round five.** There are only two:
  - the lexer count moves 1845 → 1846 and 78 → 79 fixed;
  - `regex-audit.txt` shifts by +4 lines and is otherwise identical.

  `closure-extend.jsonl` is byte-identical (`receipts/closure-extend-jsonl.sha256`).
- **New this round.**
  - `probes/round6/delta_probe.py`: syntax-tree scope, the GCC answer for the new row, and detection with two mutants at the parent and the head;
  - `empty_comment_check.py`;
  - `closure_on_guard.py`;
  - `cases/round6/null-directive-more.json`.
- **Clean state.** The clone is byte-exact before and after (`receipts/clone-state-before.txt` = `-after.txt`): HEAD, tree, index digest, 830/42/4 modes and the four gitlinks. A `scripts/__pycache__/` that one tool run created was removed, and `git status --porcelain --ignored` is empty.

## Real limits

- Physical calibration was NOT RUN. Field and hardware skips are not hardware proof.
- The full parent, PP, gPTP, Yosys and builder banks, Docker, act and the candidate merge were not run here. Gate 1b was run on its own, in both modes.
- Hosted checks at this head, as read at review time (`receipts/hosted-checks-at-review.txt`):
  - 18 completed jobs succeeded;
  - `Verilator shard 4/5` was still in progress;
  - `Physical gPTP (nightly and manual)` was skipped, and is not evidence.
- The closure table and the lexer corpora bound agreement to what they hold, as the page states. The out-of-table disagreements measured in round five all fail safe (Part B/C, unchanged).

## Pending manager duties

- Hosted/act acceptance at the exact head, including the in-progress Verilator shard.
- The candidate merge build against live dev `573f0052` and post-merge containment.
- The merge itself, only with maintainer authorization.
- Publication of this report and the manifest-listed receipts.
- Optional routing of S1 and S2.

R273-8 FINISHED
