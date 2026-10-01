[R424] POSITIVE - exact head 86726d5e60ced4f7baad6a042890b44abf7d76ed

Round R424-6, composition review of issue #117 / PR #628 (bench lane B5, acceptance box 4, the audio continuity row). Cleared context. Candidate commit `86726d5e60ced4f7baad6a042890b44abf7d76ed`, tree `84d57ec2af76a43e18ebc5c5d93cff2d01cd1149`, parents live dev `ea3fb38877842f223afea97e3bd72a10500455c9` and PR source head `e5ad118783c2ff96e13f1d794f10bf2b63741282`.

**Verdict basis.** No BLOCKER, MAJOR or MINOR is open at this head. The composed tree introduces no defect beyond the reviewed sources. All five lenses are CLEAN; RTL is untouched by the composition and stays covered by the source reviews.

## 1. What the composition is

Receipt: `receipts/composition.txt`.

- The PR branch was cut from dev `e4b771f93ee870fb2a93f8360b8677bb0b3e2a3b` (the merge base). Live dev has since moved to `ea3fb388` by one predecessor: **PR #627** (#451 TDM8 timing on the SoC board, bench lane B4; commits `35a8b04d`..`ae98b30b`, merge `ea3fb388`). No other queued predecessor is in the candidate.
- `git merge-tree --write-tree ea3fb388 e5ad1187` gives `84d57ec2...`, the candidate's tree: a clean automatic merge with no hand resolution.
- Files the PR changes: `docs/findings/117_AUDIO_CONTINUITY.md` (added) and `docs/findings/README.md` (one row).
- Files the predecessor changes: `docs/findings/451_TDM8_TIMING_SOC_BOARD.md` (added) and `docs/findings/README.md` (one row).
- **Overlap: `docs/findings/README.md` only.** Candidate vs dev is exactly the PR's page and its one row. Candidate vs PR head is exactly #627's page and its one row.
- Blob identity: `117_AUDIO_CONTINUITY.md` is `9e2fae6c` at both the PR head and the candidate. `451_TDM8_TIMING_SOC_BOARD.md` is `dde50cd9` at both dev and the candidate. So both reviewed pages land byte for byte.
- Submodule gitlinks (`external`, `gptp-processor`, `protocol-processor`, `third_party/verilog-axis`) are identical at dev and the candidate.
- Nothing outside `docs/findings/` changes on either side: no RTL, firmware, script, workflow, registry, pin, record or generator input.

## 2. Semantic interactions checked

| Interaction | Result | Evidence |
|---|---|---|
| Index table in `docs/findings/README.md` | Both rows present, once each, in their source positions: #627's at `:12`, this PR's at `:21`. Rendered with the pinned cmark-gfm lock: 15 body rows at dev, 15 at the PR head, 16 at the candidate; 3 cells per row; every link target exists in the tree; no duplicate target | `receipts/index_render.txt` |
| Cross-page links from the 117 page (`451_TDM8_FIRST_LIGHT.md#method`, `../design/TIME_SYNC.md#talker-capture-handoff`, `../reference/REGISTER_MAP.md#0x8d4-...`, `../../scripts/baremetal_uart_smoke.py`) | None of their targets is touched by #627; anchors reproduce at the candidate (287 cross-page fragment links) | `receipts/gates_candidate/gen_toc_anchors.log`, `doc_paths.log` |
| References between the two composed pages | Neither page links the other; the only tree references to either are their own index rows | `receipts/composition.txt` (tree-wide grep) |
| Factual overlap: SoC board state between B4 and B5 | Consistent. #627 records the capture ending at the bench host's USB loss and the SoC board restored with its USB function configured and its bridge legs under new process IDs; the 117 page (`:92-94`) starts B5 with the SoC board at a root prompt "on the boot lane B4 left", both bridge legs running and its USB function configured. B5 does not use the bench host's USB Audio card, so #627's owner item on that card does not reach this page | `docs/findings/451_TDM8_TIMING_SOC_BOARD.md:262-291`, `:338-339`; `docs/findings/117_AUDIO_CONTINUITY.md:92-94` |
| Factual overlap: clock rates | No contradiction. #627 states fs against the SoC board's uncalibrated clock (-42.8 ppm). The 117 page states a 16.46 ppm rate difference between the stream and the peer's recorded output, attributed by inference only (`:302-311`). Different references; neither page claims the other's figure | same pages |
| Gate inventories, TOC, doc map, CI event contract | Unchanged by either side; their gates pass on the candidate | section 3 |

## 3. Gates run on the candidate

Script: `scripts/run_gates.sh`. Interpreter: a disposable environment with `tools/markdown/requirements.txt` installed by hash. Summary: `receipts/gates_candidate/summary.txt`. **21 of 21 rc 0**, and the review clone was clean afterwards.

- `docs_check.py`: 0 findings across 183 md files and 954 scrubbed text files.
- `check_em_dash.py --base ea3fb388` (the base the docs workflow derives for this candidate): 0 findings over 553 added lines in 2 pages, exactly the PR's 552 page lines plus its index row. Also `--base e4b771f9`, covering both PRs: 0 findings over 947 added lines in 3 pages. `--selftest` passes.
- `check_doc_style.py` and `--selftest`; `check_doc_paths.py` (861 cited paths resolve).
- `gen_toc.py --selftest`, `--verify-anchors`, `--check`.
- `docs/DOC_MAP.gen.py --check` and `--selftest`; `check_solution_docs.py`; `check_feature_status.py` and `--self-test`; `check_hygiene.py --check`; `check_archive.py`; `ci_events.py --check` and `--selftest` (1655 contract items); `docs/traceability/gen_module_matrix.py --check`; `measure_test_evidence.py --check`.

**Probes that show these gates read the composed files.** Script: `scripts/probes.sh`. Run on a disposable clone of the candidate, each probe committed locally there; the review clone was never edited. Receipts: `receipts/probes/`.

| Probe | Planted defect | Result |
|---|---|---|
| P0 | none (control) | the four gates rc 0 |
| P1 | em dash in the composed 117 index row | `check_em_dash.py --base ea3fb388` rc 1, at `README.md:21` |
| P2 | 117 index row pointing to a missing file | `docs_check.py` rc 1 (broken link); `check_doc_paths.py` and `--verify-anchors` do not own this |
| P3 | 117 page's anchor into `451_TDM8_FIRST_LIGHT.md` broken | `gen_toc.py --verify-anchors` rc 1 |
| P4 | a wrong resolution that drops #627's index row | no gate fires |
| P5 | a wrong resolution that duplicates the 117 row | no gate fires |

P4 and P5 show that index completeness and duplication are not gated. That is why the row-level check in section 2 was done directly. At this candidate both rows are present exactly once, so this is a limit, not a finding.

## 4. Prior public findings, resolved or retained at this head

These were read after the independent pass above.

- **Every MINOR from R424-1 to R424-4 and from R425-1 to R425-4 was resolved at `e5ad1187`.** R424-5 and R425-5 recorded this, both POSITIVE at that head. The candidate carries the page blob `9e2fae6c` and the index row byte for byte as reviewed, so every resolution is **retained** at this head. Composition changes only the row's line number: R425-5's `docs/findings/README.md:20` is `:21` here.
- **Open SUGGESTIONs, retained unchanged:**
  - R424-5-S1 and R425-5-S1 (archive pin).
  - R424-5-S2 and R425-5-S2 (the PR body's gate count). These are PR text, not in the tree.
  - R425-5-S3 (masked gate outputs not named).
  - The forward-pointer suggestion first raised as R424-1 S1, retained by the manager. The #75 row it names is unchanged at `README.md:15`.
- None of these affects a lens.

## 5. Findings

None at BLOCKER, MAJOR or MINOR. No new SUGGESTION.

## 6. Clean-lens results

```text
[R424] PASS Conformance - docs/findings/117_AUDIO_CONTINUITY.md blob 9e2fae6c (identical to e5ad1187), docs/findings/451_TDM8_TIMING_SOC_BOARD.md:262-291,338-339 vs 117 page :92-94,:302-311 - the composed tree carries the reviewed #117 box 4 row unchanged, and the predecessor's page contradicts none of its claims (SoC board state between B4 and B5; clock-rate references)
[R424] PASS RTL - receipts/composition.txt (name-status candidate vs both parents; gitlinks) - composition changes no HDL, firmware, constraint, script or submodule pin; not touched, covered by R424-5 and R425-5 at e5ad1187
[R424] PASS Robustness - receipts/index_render.txt, receipts/probes/probes.txt P4/P5 - the overlapping index table, rendered by the pinned renderer, holds both rows once each with live targets; the ungated resolution failures (row loss, duplication) were checked directly and are absent
[R424] PASS Tests - receipts/gates_candidate/summary.txt (21/21 rc 0), receipts/probes/probes.txt P0-P3 - every gate that reads the composed files passes on the candidate, and the em-dash, link and anchor gates are shown to fire on planted defects in exactly those files
[R424] PASS Docs - docs/findings/README.md:12,:21 at 86726d5e; receipts/composition.txt raw README diffs against both parents - the index carries each source row byte for byte, the two pages are byte-identical to their reviewed heads, and prior findings are retained as resolved (section 4)
```

## 7. Ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | 117 page blob identity; #627 page vs 117 page factual overlap (section 2); issue #117 acceptance box 4 and the B5 assignment 5925737609 | R424-6 (composition), on top of R424-5 and R425-5 for the source | `86726d5e60ced4f7baad6a042890b44abf7d76ed` |
| RTL | CLEAN (not touched by the composition) | `receipts/composition.txt`: only `docs/findings/` changes on either side; gitlinks identical | R424-5 and R425-5 (source); R424-6 confirms the composition is outside this lens's scope | `e5ad1187...` (source); `86726d5e...` (composition) |
| Robustness | CLEAN | `receipts/index_render.txt`; probes P4 and P5 | R424-6 | `86726d5e60ced4f7baad6a042890b44abf7d76ed` |
| Tests | CLEAN | `receipts/gates_candidate/` (21 gates); `receipts/probes/` P0 to P3 | R424-6 | `86726d5e60ced4f7baad6a042890b44abf7d76ed` |
| Docs | CLEAN | `docs/findings/README.md` at the candidate and both parents; both page blobs; prior findings (section 4) | R424-6 | `86726d5e60ced4f7baad6a042890b44abf7d76ed` |

## 8. Real limits

- This round did not run the full parent, protocol-processor, gPTP, Yosys or builder banks, any act or Docker replica, or the host runner's self-test (excluded by the assignment). For a docs-only composition those banks read no changed file. Their results at this head are the manager's.
- **The candidate commit is not on the remote**, so it has no hosted evidence: the check-runs query returns "No commit found" (`receipts/hosted_checks.txt`). At the PR source head `e5ad1187`:
  - `rtl-fast`, `elaborate`, `bdd-conformance`, `wire-accountability`, `docs-check-no-git`, `changes` and `full-ci-gate` completed with success.
  - `docs-check` was still in progress when read.
  - `verilator-suites`, `verilator-lint`, `yosys-portability`, `yosys-elaboration`, the shards and Physical gPTP were **skipped**, not executed.
- In the threads I read, I found no public manager comment stating the source static/builder and native bank results at `86726d5e`. The cited tree `ef3a7091:review-evidence/b5-r1` carries the round 1 author packet. I did not re-verify that packet: the source rounds own it.
- This round covers composition with dev `ea3fb388` only. If dev moves before the merge, the new candidate is not covered.
- Physical calibration was NOT RUN. Field skips are not hardware proof. This round made no hardware claim.
- Index completeness and row uniqueness in `docs/findings/README.md` are not machine-gated (probes P4 and P5). They were checked by hand at this candidate only.

## 9. Pending manager duties

- Build and gate the final current-dev candidate at the merge turn, and record both object IDs with the local gate results (CONTRIBUTING step 7).
- Own hosted and act acceptance: the exact-head `docs-check` result, and whether the skipped long gates are correctly path-filtered for a docs-only head.
- Confirm the full review bar of CONTRIBUTING and AGENTS.md section 7 before merge.
- Merge only with explicit maintainer authorization, using "Refs #117" (no closing keyword), then run post-merge containment (`check_merge_containment.py`, `check_merge_review_integrity.py`).
- Decide the retained SUGGESTIONs listed in section 4.

## 10. Integrity after probes

`receipts/integrity.txt`:

- The review clone is at `86726d5e`, tree `84d57ec2`, with 0 porcelain lines.
- The worktree and the index are identical to HEAD; the index tree is `84d57ec2`.
- The staged modes, blobs and paths hash to the same value as `ls-tree -r HEAD` (`2e1f7dea...`).
- The four submodule gitlinks are as at dev.
- All probes ran on a separate disposable clone.

R424-6 FINISHED
