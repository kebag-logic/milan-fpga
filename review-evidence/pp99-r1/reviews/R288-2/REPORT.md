[R288] POSITIVE - exact head 9cde1c19dbfd859257be8e012d4455856fcfce3b

# R288-2 independent internal review (delta): processor issue #99 / PR #119

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan
- Exact head: `9cde1c19dbfd859257be8e012d4455856fcfce3b`, tree `899808411b924cd161e849039806685e939e6fc4`. Both were verified in the isolated detached clone.
- Round-1 head: `663d50d65ff49c33b153107b2f79d6f3c5725799`. Source base: `008edbbf486598ae237414273d75e385cf0e1a56`. Merged main: `60152f3ff068b81333326b5081b5303253ba7fe7`.
- Delta reviewed: one commit, `9cde1c1` "Fix parameter owner anchors and document the inventory gate", by executor A302. Its single parent is `663d50d`.
- Review start: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/119#issuecomment-5827157343
- Assignment: [A10] round-2 comment 5827048744 on issue #99, covering R288-1 F1 and F2 and R289-1 F1.

## Verdict

POSITIVE. Both of my round-1 findings are resolved at this head, and nothing else changed.

- **R288-1 F1 is resolved.** The five owner links in integrator-guide §2 now use explicit anchors. Those anchors exist on GitHub's rendering of the exact head and in the repository's link gate:
  - `DESC_BASE_P`, `DESC_LINE_BYTES_P`, `DESC_IDX_ENTRIES_P` and `DESC_NAME_ENTRIES_P` → `#sec-desc-memory`.
  - `RESP_BASE_P` → the new `#sec-resp-memory`.
- **R288-1 F2 is resolved.** `09_verification.md` §7 has a `params` row. It names `scripts/check-integrator-params.py` and states what the checker asserts.
- **Scope held.** The only files changed are `07_memory_maps.md`, `09_verification.md` and `integrator.md`, adding 7 lines and removing 5. `make check`, the link gate, the params gate and `git diff --check` all return 0. Hosted docs-gates succeeded in both contexts at the exact head.

No MINOR, MAJOR or BLOCKER finding is open. Four non-blocking suggestions are carried forward from round 1.

## Reconstructed scope (public)

- There is still no `AGENTS.md` or `CONTRIBUTING.md`. The conventions come from `README.md` and `docs/README.md`:
  - §2 single-source rules: parameter values live only in F01.5 and timing values only in F08.1.
  - §6 editing workflow: `make check` must pass.
- Issue #99 is unchanged. It covers the complete top-level parameter inventory, including decision 5789750553, and changes no RTL and no default values.
- Round-2 assignment 5827048744 has three items:
  1. Point the five rows at anchors that exist on GitHub and in the link gate. Use `#sec-desc-memory` for §3.3.1, and add an explicit `<a id>` in the file's existing style for §3.3.2. Do not use double-hyphen slugs. The reviewer's anchor check must report 0 dead.
  2. Add a `params` row to 09 §7.
  3. Change nothing else. The gates are `make check`, the docs gates, the link gate and `git diff --check`.
- Author ready note 5827134004 claims 59 anchor links checked and 0 dead. My run independently gives the same count (see Conformance).
- Public state at fetch time (`receipts/pr119*.json`, `receipts/issue99*.json`):
  - The PR is open, head `9cde1c1`, base `main`.
  - It has 0 formal reviews and 0 inline review comments.
  - The issue comments are the two round-1 reports (R288-1 and R289-1) and the review-start comments.

## Findings

None open at MINOR or above.

### Resolution of prior public findings at this head

| Finding | Status at `9cde1c1` | Evidence |
|---|---|---|
| R288-1 F1 (MINOR; Conformance, Docs): five owner links point at anchors GitHub does not render | **RESOLVED** | `integrator.md:80-83` → `07_memory_maps.md#sec-desc-memory` (explicit anchor, `07:146`). `integrator.md:88` → `#sec-resp-memory`, which is new at `07:215` directly before the §3.3.2 heading, in the same style as `07:146`. GitHub's rendering at the exact head has `id="user-content-sec-resp-memory"` once, and the next element is the §3.3.2 `<h4>`, 80 characters later. The same holds for §3.3.1 (`receipts/gh-anchor-heading-adjacency.txt`). `github_anchor_check.py` over `integrator.md`, `diagrams/README.md`, 07 and 09 reports 59 OK and 0 dead, rc 0 (`receipts/github-anchors-head.txt`). The slug-gap scan no longer lists any PR link; only the 4 pre-existing main links remain (`receipts/slug-gap-scan-head.txt`, see S1). No file still links the old `#331-`/`#332-` heading slugs (grep). |
| R288-1 F2 (MINOR; Docs, Tests): 09 §7 omits the `params` target | **RESOLVED** | `09_verification.md:120` adds a `params` row naming `scripts/check-integrator-params.py`. The row says the guide §2 table and diagram 21's `integration-parameters` group each equal the overridable parameter set of `protocol_processor_top`, with no missing, extra or duplicate names, and that empty or unparseable inputs fail. Each claim matches the checker (`scripts/check-integrator-params.py:3-8,83-85,105,124-128`) and the 29 re-run probes (`receipts/checker-probes.txt`). The row sits between `modmatrix` and `stale`, matching the order of the `Makefile:13` prerequisites. |
| R289-1 F1 (MINOR; Docs) | **RESOLVED** | see "Prior findings from the other round-1 review" below; that section was written after this verdict and ledger |

### Suggestions (non-blocking, carried from round 1)

- **S1 (Tests, Docs; pre-existing; follow-up outside #99):** `scripts/check-links.py:22-26` `slug()` collapses runs of whitespace, but GitHub emits one hyphen per space. The repository's link gate therefore still accepts heading slugs that are dead on GitHub. Probe `OBS-old-332-slug-passes-local` puts the round-1 dead slug back in the `RESP_BASE_P` row, and the local gate returns rc 0 (`receipts/link-gate-probes.txt`). The 4 main links listed in round 1 are still dead on GitHub (`receipts/slug-gap-scan-head.txt`). This PR now avoids the class by using explicit ids, but the gate cannot prevent the next occurrence.
- **S2 (Robustness):** the checker counts `display="none"` text inside the diagram group, although its docstring says "only visible text" (`scripts/check-integrator-params.py:8` vs `:80-88`). This is unchanged; `OBS-diagram-hidden-text-counts` still gives rc 0 (`receipts/checker-probes.txt`). The new 09 §7 row does not claim visibility, so it is accurate as written.
- **S3 (Docs):** the `DESC_NAME_ENTRIES_P` row (`integrator.md:83`) could also link `hdl/aecp/KL_aecp_desc_store.sv`, where the 1..1024 bound is enforced by elaboration `$error`. This is unchanged.
- **S4 (Docs):** the diagram 21 paragraph in `docs/diagrams/README.md` still sits before the general checklist. This is unchanged; the file is identical to the round-1 head.
- The shorter summaries of `make check` in `docs/guides/hdl-engineer.md:218` and `docs/README.md:154` do not list `params`. They already omitted `modmatrix` on main, and the round-2 assignment said "change nothing else". Round 1 marked this optional, so it is not a finding. A later docs sweep could point those summaries at 09 §7.

## Lens evidence (delta at `9cde1c1`; round-1 evidence otherwise stands)

### Conformance

- **Assignment item 1:**
  - The four §3.3.1 rows use the pre-existing explicit anchor `#sec-desc-memory`. That anchor is unique in 07; `integrator.md:135` has its own `sec-desc-memory`, in a different file.
  - The §3.3.2 row uses the new `<a id="sec-resp-memory"></a>` (`07:215`). It follows the exact line pattern of `07:146`: a blank line, the anchor, then the heading on the next line.
  - No double-hyphen slug is used anywhere.
- **GitHub check:** the rendered HTML of 07 at the exact head, fetched read-only (`receipts/gh-rendered-07_memory_maps.html`), contains exactly one `user-content-sec-resp-memory` and one `user-content-sec-desc-memory`. Each renders as an empty paragraph immediately followed by its §3.3.x heading, so the owner link lands on the owning section (`receipts/gh-anchor-heading-adjacency.txt`).
- **Anchor check:** `github_anchor_check.py` at the exact head reports 59 fragment links, all OK and 0 dead (`receipts/github-anchors-head.txt`). This includes all 6 `sec-desc-memory` and `sec-resp-memory` links: the five §2 rows plus the existing §4.1 link.
- **Assignment item 3:** `git diff --name-status 663d50d HEAD` lists only the three assigned files (`receipts/delta-scope.txt`). The labels, owners and descriptions in the five edited rows are byte-identical except for the fragment. The inventory is still top 24, guide 24, diagram 24.
- The author's published `commit.json` sha256 values for the three files equal the exact-head bytes (`receipts/author-r2-sha-crosscheck.txt`).

### RTL

- `hdl`, `tb` and `syn` tree ids at `9cde1c1` equal those at round-1 head `663d50d` and at main `60152f3` (`d8879608…`, `a2ca8912…`, `1b062a92…`; `receipts/delta-scope.txt`).
- `scripts`, `.github`, `Makefile` and `docs/diagrams` are identical to round 1.
- No RTL, testbench, synthesis, checker, workflow or diagram byte changed. The round-1 RTL evidence carries over unchanged: the unchanged parameter header, pinned-simulator lint with 24 overrides, and override acceptance and rejection. The pinned simulator was not needed or run in this round.

### Robustness

- **Link-gate fault probes** (`scripts/probe_delta_links.sh`, `receipts/link-gate-probes.txt`): 7 probes on fresh `git archive` copies, with the unmodified `check-links.py`.
  - Baseline: rc 0.
  - Each of these returned rc 1 with a `missing anchor` diagnostic:
    - typo in the `RESP_BASE_P` fragment
    - typo in the row-80 fragment
    - `sec-resp-memory` anchor deleted
    - `sec-desc-memory` anchor deleted (all dependent links reported)
    - `sec-resp-memory` anchor renamed
  - The observational probe is S1.
  - The new anchor is therefore enforced by the repository gate, not only by the review-time GitHub check.
- **Checker fault probes** re-run at this head (`receipts/checker-probes.txt`): 29 probes and 0 unexpected results. All 28 controls still fail closed, and the observational probe is S2. No probe produced a traceback.

### Tests

- **Local gates at the exact head** (`receipts/head-gates.txt`, `receipts/make-check.txt`), all rc 0:
  - `check-integrator-params` (24/24/24)
  - `check-links` (916 links)
  - `check-matrix`
  - `git diff --check` against `663d50d`, `008edbbf` and `60152f3`
  - full `make check`: lint 41 mermaid + 18 wavedrom, wavedrom, links, matrix, modmatrix 92 rows / 0 untested, params, stale
- **Hosted at the exact head** (`receipts/hosted-check-runs.txt`, `receipts/hosted-docs-gates-log-excerpt.txt`):
  - docs-gates `success` on the push context (run 36097408423) and on the PR merge-ref context (run 36097411757). The merge ref `4960f75` is "Merge 9cde1c1… into 60152f3…". Both logs show `parameters: top 24, guide 24, diagram 24, OK` and `links: 916 checked, OK`.
  - portability `success` on both contexts.
  - suites were `in_progress` on both contexts at 05:14 UTC (see pending manager duties).
- F2's verification is met: 09 §7 now matches the `check:` prerequisites in `Makefile:13`, target for target.

### Docs

- **`integrator.md` §2:** the five edited rows keep their structure: four columns, the same labels, the same owner split. Only the fragments changed.
- **`07_memory_maps.md`:** one line added. It follows the file's existing explicit-anchor convention and does not change the §3.3.2 text or heading.
- **`09_verification.md` §7:** the new row is accurate and in the same register as its neighbours (see F2 above). It restates no parameter values, so the single-source rule holds.
- The diagram SVG and PNG and `docs/diagrams/README.md` are unchanged since round 1. The round-1 re-render and visual-inspection evidence stands.

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | round-2 assignment 5827048744; `integrator.md:80-83,88`; `07_memory_maps.md:146,215`; GitHub-rendered 07 at head; `github_anchor_check.py` over 4 files (59/0); delta file list; author tested-byte cross-check | R288-2 (delta), R288-1 (rest) | 9cde1c19dbfd859257be8e012d4455856fcfce3b |
| RTL | CLEAN | `hdl`/`tb`/`syn`/`scripts`/`.github`/`Makefile`/`docs/diagrams` ids equal to round-1 head and main | R288-2 (identity), R288-1 (substance) | 9cde1c19dbfd859257be8e012d4455856fcfce3b |
| Robustness | CLEAN (S1, S2 suggestions only) | 7 link-gate fault probes on the new anchors; 29 checker probes re-run | R288-2 | 9cde1c19dbfd859257be8e012d4455856fcfce3b |
| Tests | CLEAN | `09_verification.md` §7 against `Makefile:13` and the checker; local gates and `make check`; `git diff --check` ×3; hosted docs-gates and portability logs in both contexts | R288-2 | 9cde1c19dbfd859257be8e012d4455856fcfce3b |
| Docs | CLEAN (S1, S3, S4 suggestions only) | the three changed files in full context; row structure; anchor convention; §7 row wording; summaries in `hdl-engineer.md` and `docs/README.md` | R288-2 (delta), R288-1 (rest) | 9cde1c19dbfd859257be8e012d4455856fcfce3b |

## Prior findings from the other round-1 review

The R289-1 report (PR comment 5827043730, head `663d50d`) was read after the verdict and ledger above were written. None of its findings changes them.

| Finding | Status at `9cde1c1` | Evidence |
|---|---|---|
| R289-1 F1 (MINOR; Docs): 09 §7 omits `params` | **RESOLVED** | This is the same defect as R288-1 F2; the manager's assignment equates them. The new row at `09_verification.md:120` covers every element R289-1 required: the guide §2 table and the diagram 21 `integration-parameters` group each equal the top's overridable parameters, duplicates fail, and empty inventory fails. See R288-1 F2 above. |
| R289-1 S1 (hidden diagram text counts) | RETAINED as a suggestion | Same as S2 here. The checker is unchanged (`scripts` tree id equals round 1), and the probe still returns rc 0. |
| R289-1 S2 (no committed checker self-test) | RETAINED as a suggestion | The checker and Makefile are unchanged. The controls are still proven only by out-of-tree probes, including this review's 29-probe re-run. |
| R289-1 S3 (PNG freshness against the SVG not gated) | RETAINED as a suggestion | `docs/diagrams` tree id is unchanged since round 1, so the round-1 pixel and byte identity of the PNG with a fresh render still holds. No gate was added. |
| R289-1 S4 (diagram README paragraph placement) | RETAINED as a suggestion | Same as S4 here. The file is unchanged. |
| R289-1 S5 (default restated at `integrator.md:355-356`; outside scope) | RETAINED as a suggestion, outside #99 | The text is still present at the same lines at this head. It predates the base and sits outside §2. The round-2 assignment said "change nothing else". |
| R289-1 origin observation X2 (five missing inventory names) | RESOLVED; unchanged | The inventory is still 24/24/24 at this head (`receipts/head-gates.txt`). |

One note on authority: R289-1 cites an `AGENTS.md`. None exists in this repository at this head (checked). Its conclusion does not depend on that citation, because the `Makefile:12` comment and 09 §7 carry the same authority.

## Real limits

- Not run by this review, because they were not permitted: the full suite, PP, gPTP, Yosys and builder banks, the parent consumer gates, hosted re-runs, and act.
- The manager's statement that the full source static/builder and native banks passed at this head is taken from the assignment. At fetch time there was no bank receipt for `9cde1c1` in `kebag-logic/milan-fpga@81a6fb3…/review-evidence/pp99-r1` (that tree has `author-r2` docs-gate logs only) or in the issue or PR comments. Because `hdl`, `tb`, `syn`, `scripts`, `.github`, `Makefile` and `docs/diagrams` are identical to round 1, the round-1 bank results apply by tree identity. That is an inference, not an execution.
- The GitHub anchor results reflect GitHub's rendering at review time.
- A keyword scan for "evidence"/"bank" over the PR comments printed three lines of the other reviewer's round-1 report before this verdict was drafted: the lens-framing sentence, a parent-consumer evidence paragraph, and a section heading. It printed no finding text. Every conclusion above rests on this review's own receipts.
- **Clone state after the probes:** the ignored `.venv-wavedrom/` and `scripts/__pycache__/` byproducts of the local gates were removed. HEAD and tree are exact and detached, and the index tree equals HEAD's tree. `git status --porcelain --ignored` is empty. All 247 tracked blobs were re-hashed and their modes checked: 0 mismatches. There are 0 gitlinks and no `.gitmodules`, so there are no submodule pins in this repository (`receipts/restore-verification.txt`).

## Pending manager duties

- Hosted `suites` at the exact head (push run 36097408423, PR run 36097411757) were still `in_progress` when this review ended. Hosted and act acceptance stay with the manager.
- The final current-dev candidate at the merge turn: source base `008edbbf…`, live dev `c533b4818df8b3f581df76aa0d1c6d5f55d20449`. This is separate from source validation.
- Parent consumer adoption of the processor gitlink at `9cde1c1` on `508-pp-pin-adopt`.
- Physical calibration NOT RUN. Field skips are not hardware proof.

R288-2 FINISHED
