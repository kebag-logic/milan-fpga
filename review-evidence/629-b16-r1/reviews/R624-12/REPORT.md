[R624] POSITIVE - exact head ada26e56ac42ee5de311aef84cb86c8435b97cee

# R624-12: composition re-check of PR #725 (issue #629, lane B16) in the merge-train candidate

Role: independent composition reviewer, cleared context. Round R624-12.

| Item | Value |
|---|---|
| Candidate | `ada26e56ac42ee5de311aef84cb86c8435b97cee`, tree `af715ad7841e88695ce0eaa845c0d3e154cfa424` |
| Parents | `cdb49e7e` (the #726 candidate) and `f1b2489f` (PR #725's head, unchanged) |
| Scope | Composition acceptance only. Documents only: no bench, no hardware |
| Reconstructed from | AGENTS.md, CONTRIBUTING.md, docs/README.md, the PR body, the manager's ruling [6144924772](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6144924772), the review start [6145411331](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6145411331), the diff `cdb49e7e..ada26e56` and its history, and the public packet `review-evidence/629-b16-r1/` at evidence commit `5e6a3d5f` (`author-r10/`, `author-r11/`) |
| Read only after the verdict and ledger were drafted | Earlier review findings |

## Verdict in one paragraph

The merged tree is the exact three-way merge of its parents: `git merge-tree --write-tree cdb49e7e f1b2489f` gives `af715ad7`. The one file both sides change is the findings page, and the merged page is the PR's page with #726's 7-line counter-law note above the H1. Nothing else interacts. `README.md` is byte-equal to the PR head's, and no registry, workflow, record pin or gate inventory is touched.

R624-11-F1 is resolved under the manager's first option:

- The regenerated check in `author-r11` is built byte-for-byte from the published spec and build. The page is the only input that changed.
- My own independent +7 shift of the `author-r10` check is byte-identical to it.
- Its unchanged run on the candidate page exits 0: 1,960 of 1,960 rows, 0 uncovered digits, 0 MARKUP.
- `reproduce.sh` passes end to end.
- Every earlier control runner, self-probe set, parser and reader audit, and all 15 review probes reproduce the packet's receipts. Each keeps its outcome, or its +7 locator is listed.
- The packet's hashes match, and the PR body states both bindings.

Every B16, B16b and B16c statement stays true under the note. Every documentation gate passes on the candidate, and every link resolves. No BLOCKER, MAJOR or MINOR is open, and no new RESIDUE is raised. One SUGGESTION concerns the packet's own tooling.

## 1. The composition

| Check | Result | Receipt |
|---|---|---|
| Merge reproduces the candidate | `merge-tree` = `af715ad7` = `ada26e56^{tree}` | reproduced this round |
| PR's files (`c20c85bd..f1b2489f`) | `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md`, `docs/findings/README.md` | `git diff --stat` |
| Predecessor's files (`c20c85bd..cdb49e7e`, 91 files) that the PR also changes | exactly one: the findings page, by `7b491e595` (+7 lines, note at lines 4-10) | `git diff --stat`; `git log c20c85bd..cdb49e7e -- <page>` |
| Candidate vs `cdb49e7e` | two files, +2,341/-1, equal to the PR's own diff stat | `git diff --stat cdb49e7e ada26e56` |
| `README.md` | blob `20b7c077` at both `f1b2489f` and `ada26e56`; #726 did not touch it (blob `c49ebdcb` at `c20c85bd` and `cdb49e7e`) | `git rev-parse <c>:docs/findings/README.md` |
| Page blobs | source `844ff7fb` (330,109 B, SHA-256 `bb5da487…401a1f`); candidate `cdd3121f` (330,604 B, `cba50df4…0c33`) | `receipts/binding-hashes.txt` and the runs below |
| Live dev | `e81ce82f`, tree `ab5a465c`, equal to `cdb49e7e^{tree}`; PR head ref `f1b2489f`; evidence branch tip `5e6a3d5f` | `receipts/ls-remote.txt` |

## 2. The manager's questions

**(1) Both sides stated correctly.** The note (candidate lines 4-9) says the measurements below keep their original image semantics. B16, B16b and B16c ran on the `5603c353` image, before #726's counter change. The B16 counter statements on the candidate page are:

- `:2420-2423`: MEDIA_LOCKED and FRAMES_RX of the reference peer's listener, not the DUT's.
- `:2548-2552`: the peer's STREAM_INPUT 0 counters and the DUT talker's stream stops and starts.
- `:3235-3240`, `:3315-3318`: MEDIA_RESET, which the note leaves on its interval law.
- `:3242-3245`, `:3319-3320`: CLOCK_DOMAIN LOCKED and UNLOCKED, untouched by the note.
- `:3317-3318`: the DUT listeners' GET_COUNTERS "advanced with the binds". That is a direction observed on the original image, with no count or law claimed.

No B16 text in the section (`:2294-4609`), the introduction (`:25-46`) or the Contents entry (`:91`) mentions #726, per-AVTPDU counting, 32-bit wrap, or the new reset and retention rules. None contradicts them.

**(2) The figure check on the merged tree.** I ran it myself under the pinned parser: cmarkgfm 2025.10.22, html5lib 1.1, six 1.17.0, webencodings 0.6.1, cffi 2.1.1 and pycparser 3.0, as `tools/markdown/requirements.txt` pins them, in an isolated environment (`receipts/tool-identity.txt`).

| Run | rc | Rows OK / BAD | Digits by row / identifier / uncovered | MARKUP | Receipt |
|---|---|---|---|---|---|
| Candidate page, `author-r11` check, unchanged | 0 | 1,960 / 0 | 12,988 / 2,609 / 0 | 0 | `receipts/checks/cand-r11.*` |
| Candidate page, my +7 probe (`scripts/shift_rows.py`) | 0 | 1,960 / 0 | 12,988 / 2,609 / 0 | 0 | `receipts/checks/cand-probe7.*` |
| Source page, `author-r10` check (control) | 0 | 1,960 / 0 | 12,988 / 2,609 / 0 | 0 | `receipts/checks/src-r10.*` |
| Candidate page, `author-r10` check (negative control) | 1 | 53 / 1,907 | 129 / 2,689 / 12,779 | 0 | `receipts/checks/cand-r10.*` |
| Source page, `author-r11` check (reverse binding control) | 1 | 55 / 1,905 | 131 / 2,688 / 12,778 | 0 | `receipts/checks/src-r11.*` |

How the note is judged:

- The note's digits are `2026-10-12`, `726`, `6125741685` and `32`. The check's own `scope()` places them outside the covered text. It anchors on the section heading `## Dev 5603c353, 2026-10-12: lane B16`, on the introduction paragraph that opens "In lane B16, the operator tried…", and on the Contents entry's own text.
- The lowest page line any row or coverage entry names is 25 (`receipts/checks/cand-r11-*.tsv`).
- The EXCLUDE block is byte-identical between `author-r10` and `author-r11`, because the whole file outside the row block is identical. Its issue-number category is still `629|645`. So nothing was exempted for the note: its digits are excluded by the scope rule alone.

**(3) Links.**

- `scripts/link_audit.py` resolves every relative link and fragment out of the page and the index, and every link into them, from any Markdown file in the tree. Candidate: 224 links, 0 problems. Source: 223. The difference is the note's link to `../testing/726_STREAM_COUNTERS.md`, which exists. See `receipts/link-audit-*.json`.
- The repository gates also pass on the candidate: `check_doc_paths.py` (974 cited paths) and `gen_toc.py --verify-anchors` (486 cross-page fragment links).

## 3. Round 12 verifications

| Required | Result | Evidence |
|---|---|---|
| The regenerated check is built byte-identically from the published spec and build, with only the page input changed | Yes. With the candidate page, the published spec (`407817bd…`) and build (`d2075750…`) turn the `author-r10` check into a file byte-equal to the `author-r11` check (`49d3d069…`, 199,268 B). The same spec and build with the source page give the `author-r10` check (`a9f36f9d…`) | `receipts/comparisons.txt`, `receipts/checks/rebuild-*.{rc,stdout}`, `receipts/unpublished-large-files.txt` |
| What changed between the two checks | My `shift_rows.py`, written independently, moves only bare page-row locators in the row block by +7. It moves 1,934; 26 `README.md:` rows and every byte outside the block are unchanged. Its output is byte-identical to the `author-r11` check | `receipts/checks/probe-plus7-shift.json`, `receipts/comparisons.txt` |
| The unchanged run on the candidate page | rc 0, 1,960/1,960, 0 uncovered, 0 MARKUP. Its stdout, rows and coverage are byte-equal to my +7 probe's and to the packet's `receipts/cand.*` | `receipts/checks/`, `receipts/comparisons.txt` |
| Normalized equality | The candidate rows and coverage, moved back by 7, equal the source run byte for byte (my own normalization, and also the packet's `compare_figures.py`). The stdout is identical without normalization | `receipts/reproduce/normalized-comparison.json` |
| `reproduce.sh` | Run unchanged with the candidate clone, a source-head clone, `author-r10/` and the pinned interpreter: `src` rc 0, `cand` rc 0, step 2 rebuild `cmp` equal, step 3 comparison all true. Script rc 0. All nine outputs are byte-equal to the packet's `receipts/reproduce/` | `receipts/reproduce.{log,rc}`, `receipts/reproduce/` |
| Earlier controls (runners r3 to r10) | 5/5 (rc 0), 7/8, 21/22, 38/39, 48/50 (rc 1 each, the historical failures that [decision 6132293481](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6132293481) supersedes), 73/73, 97/97, 117/117 (rc 0). Every differing field differs only by page locators +7 (`semantics_equal` true for all eight). Every `controls-N.json` and `.rc` is byte-equal to the packet's | `receipts/validation/control-comparison.json`, `receipts/comparisons.txt` |
| Self-probes, parser audit, reader controls, layers | 172/172 met, and all four equal to round 10 after normalization. All are byte-equal to the packet's receipts | `receipts/validation/supplementary-comparison.json`, `validation-summary.json` |
| The 15 review probes | All outcomes equal to round 10 (`all_outcomes_equal` true). 14 rerun receipts are byte-equal to the packet's. `r624-9-autolink` differs only in `results.check`, the absolute path of the check file; its reading and exit are equal | `receipts/validation/probe-comparison.json`, `probes/` |
| Relocated copies | They differ from the originals only in the locators the PR body lists: 3008/3174/3200 to 3015/3181/3207, and anchor 3244 to 3251. On the candidate, the originals keep their stated results: both row selectors select nothing, and R624-6's escape probe refuses at its fixed anchor before running the check (its stderr matches the packet's `r624-6-original-abort.json`). The copies give receipts byte-equal to the packet's | `receipts/validation/relocated-*.json`, `r624-6-escapes-original-candidate.stderr`, `logs/probes-polls.log` |
| Packet hashes | Every `author-r11` file equals its published hash in the branch `MANIFEST.json`. The 10 files whose `MANIFEST.sha256` original hash differs are exactly the 10 flagged `path_redacted`. `bindings.json` (bytes, SHA-256, Git blob) matches my recomputation for both checks, the spec, the build and both pages. `author-r10/` has the same tree (`f093cac9`) at `5775cfa7` and at `5e6a3d5f` | `receipts/binding-hashes.txt` |
| The PR body states both bindings | Yes, under "Round 11: composition, packet only": `author-r10` to source blob `844ff7fb` at `f1b2489f`, published at `5775cfa7`; `author-r11` to merged blob `cdd3121f` at `ada26e56`. The PR head ref is still `f1b2489f` | `receipts/pr725-final.json` |

## 4. Gates on the candidate

All rc 0 (`receipts/gates/`):

- `docs_check.py`: 0 findings across 206 md files.
- `check_doc_style.py`.
- `gen_toc.py --check`: 146 pages.
- `gen_toc.py --verify-anchors`: 486 links.
- `check_em_dash.py --base cdb49e7e`: 0 findings over 2,341 added lines.
- `check_em_dash.py --base e8454e27`: 0 findings over 5,381 lines.
- `check_doc_paths.py`.
- `ci_scope.py --selftest`.
- `ci_events.py --check`: 2,016 contract items.
- `check_baremetal_only.py --check`.
- `check_feature_status.py --self-test`: 46/46.
- `git diff --check cdb49e7e ada26e56` and the worktree.

## 5. Findings

No BLOCKER, MAJOR or MINOR. No new RESIDUE.

### R624-12-S1: SUGGESTION. Lenses: Tests

- **Where:** `author-r11/tools/run_validation.py:24-39` with `r11_probe_reruns.py:193-220` (the read at `:206`).
- **Evidence:** In the group mode `probes-1`, the original `probe_r624_6_escapes.py` refuses on the candidate, as expected and as recorded. Its `out.json` is then never written, so `main()` raises `FileNotFoundError` and the group stops. `r624-6-row3200-polls` is skipped silently (group rc 1, `receipts/validation/logs/probes-1.log`). I reproduced its receipt only with the single-probe mode `probes-r624-6-row3200-polls`.
- **Impact:** A later re-runner using the group modes can miss one probe. Nothing is falsely green, because the abort is loud and the packet's receipts are complete.
- **Optional outcome:** State the individual-mode invocation in the packet's handoff, or record a refused original in its group without aborting the group.

### Carried by the ruling, not a finding

Per [6144924772](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6144924772), the page names no check hash, so it does not say which check binds it. The relevant sentences are "A row gives the document line" and "With these changes the page passes" (`:3533`, `:4263`, `:4414`, `:4585`). That binding wording is on the #495 residue list. It is true of the merged page under `author-r11`.

## 6. Earlier findings, read after the verdict and ledger above

| Finding | Status at `ada26e56` | Evidence |
|---|---|---|
| R624-11-F1, MINOR (the line-keyed check fails on the merged page) | RESOLVED | Section 3: the regenerated check passes 1,960/1,960 with 0 uncovered and 0 MARKUP, equals my +7 probe, `reproduce.sh` passes, controls and probes are retained, and the PR body states both bindings |
| R624-10-R1, RESIDUE (PR-body "Local commit: … not pushed.") | RESOLVED in the live body. The Round 10 section now reads "Commit: `f1b2489f5b1c929e81eeae79a469b2b27c47e340`, the PR head."; "not pushed" occurs 0 times | `receipts/pr725-final.json` |
| R624-10-S1, R624-10-S2, SUGGESTION | Unchanged by the composition, and optional. The note adds no list or entity to the covered text, and `README.md` is byte-equal | above |
| R624-1..9 and R625-1..9 findings, settled or resolved at the source head | RESOLVED and held. The PR's text is byte-identical in the candidate apart from the 7-line offset, and their executable controls and probes are retained (section 3) | `receipts/validation/` |

Source reviews named for the lenses this composition does not touch: [R624-10](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6137929166) and [R625-10](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6137837087). Both are POSITIVE at `f1b2489f`, with all five lenses clean.

## 7. Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN (composition touches it) | The manager's questions (1)-(3) and the round 12 list; ruling 6144924772; candidate page `:4-9` against `:2420-2423`, `:2548-2552`, `:3235-3245`, `:3315-3320`; PR body bindings (`receipts/pr725-final.json`); `receipts/checks/cand-r11.stdout` | R624-12 | `ada26e56ac42ee5de311aef84cb86c8435b97cee` |
| RTL | CLEAN. The composition does not touch it: `git diff --stat cdb49e7e ada26e56` is two Markdown files, with no HDL, firmware, tool, workflow, record or pin. The PR's own scope is covered by the source reviews | the composition diff; source reviews R624-10 and R625-10 | R624-12 (composition); R624-10, R625-10 (source) | `ada26e56…` (composition); `f1b2489f5b1c929e81eeae79a469b2b27c47e340` (source) |
| Robustness | CLEAN (composition touches it) | `check_b16_figures.py` `scope()` and EXCLUDE (identical in both checks): content-anchored, with the note outside every covered block (lowest named line 25). Both cross-binding controls fail closed (rc 1, no false pass). 0 MARKUP and 0 refused blocks on the candidate. Relocated and original probe behaviour on the shifted page | R624-12 | `ada26e56…` |
| Tests | CLEAN (composition touches it); S1 is optional | `receipts/checks/*` (5 runs, 2 rebuilds, the +7 probe); `receipts/reproduce/*`; `receipts/validation/*` (8 control runners, 172 self-probes, parser, reader, layers, 15 probes, 3 relocated copies); `receipts/comparisons.txt` (68 byte-equal comparisons, 1 path-only difference) | R624-12 | `ada26e56…` |
| Docs | CLEAN (composition touches it; ruling residue carried, not new) | Candidate page `:1-46`, `:91`, `:3533`, `:4263-4609`; `docs/findings/README.md:15` (blob equal to the source); `docs/testing/726_STREAM_COUNTERS.md`; 13 gates rc 0 (`receipts/gates/`); link audit (224 links, 0 problems); PR body | R624-12 | `ada26e56…` |

## 8. Real limits

- Composition only. The PR's content at `f1b2489f` was not re-reviewed beyond what composition reads. Its figures were verified only through the published check against the packet's receipts. Nothing was re-derived from raw bench data.
- The check, spec, controls and probes come from the public packet at `5e6a3d5f` (`author-r10` unchanged since `5775cfa7`). Their trust rests on that packet and on the source reviews. I verified their bytes and re-ran them; I did not redesign them.
- No bench, hardware, Docker or act, and no host act runner. Hosted runs were not inspected. Physical calibration was NOT RUN, and field skips are not hardware proof. No manager source bank was claimed or inferred.
- External URLs were not fetched. The link audit uses a GitHub-style slug approximation, and the repository's own anchor gate is the authority.
- Process note: two concurrent batches went over the 16-job cap. The check-and-gate batch peaked at 20 short processes, and the validation batch at 18. Both stayed well inside the memory cap and finished in under 6 minutes. Every result was compared byte for byte with the packet's receipts, so the outputs were not affected.
- Four rebuilt-check copies and four large negative-control TSVs are kept out of publication for size. Their SHA-256 and byte counts are in `receipts/unpublished-large-files.txt`.

## 9. Pending manager duties

- Validate the final current-dev merge candidate (builder and native banks) at the merge turn, and link its receipts on the PR. Live dev is still `e81ce82f` at this round.
- Own hosted and act acceptance at the exact candidate head.
- Keep the page-binding wording on the #495 residue list, as ruled.
- Merge only with explicit maintainer authorization and the full completion bar.

## Method and restoration

The scripts are in `scripts/`:

- `run_checks.sh` and `shift_rows.py`;
- `run_gates.sh`;
- `run_validation_all.sh`, which drives the packet's own `run_validation.py`;
- `link_audit.py`.

Every command ran in the foreground. Every probe ran on copies under the unpublished `scratch/`: a source-head clone, a candidate fixture clone, a validation overlay, and the extracted packet. In published receipts, host paths are replaced with `$PACKET`, `$CANDIDATE`, `$MDVENV` and `$PYLIB`.

The review clone's only change was `scripts/__pycache__` (2 files, written by the gate runs in this session at 14:24). It is ignored by git and was removed. After removal (`receipts/clone-integrity.txt`):

- HEAD is `ada26e56`, and `git write-tree` is `af715ad7`.
- There is no index or worktree diff, and no untracked or ignored file.
- The index's modes, blobs and paths hash equal to `ls-tree -r ada26e56`.
- The page blob is `cdd3121f` (mode 100644) and the README blob is `20b7c077`.
- The gitlinks are unchanged: `external` `efeb541a`, `gptp-processor` `7dda9c3b`, `protocol-processor` `2ad2f845`, `third_party/lwSRP` `08ee86e8`, `third_party/verilog-axis` `48ff7a7e`.

R624-12 FINISHED
